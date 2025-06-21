import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
import numpy as np
from dataclasses import dataclass
import trimesh
from trimesh.exchange.gltf import load_gltf, export_gltf
import pygltflib

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/animation_manager.log'
)

@dataclass
class AnimationMetadata:
    """Metadatos específicos para animaciones."""
    duration: float
    frames: int
    fps: float
    channels: int
    format: str
    is_looping: bool
    has_weights: bool
    has_morphs: bool

class AnimationManager:
    """Gestor de animaciones."""
    
    def __init__(self, base_path: str = "assets/animations"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.cache_path = self.base_path / "cache"
        self.logger = logging.getLogger("AnimationManager")
        
        # Crear directorios necesarios
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, AnimationMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, AnimationMetadata]:
        """Carga los metadatos de animaciones desde el archivo JSON."""
        metadata_file = self.metadata_path / "animations_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: AnimationMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de animaciones en el archivo JSON."""
        metadata_file = self.metadata_path / "animations_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _get_animation_info(self, file_path: Path) -> Optional[AnimationMetadata]:
        """Obtiene información detallada de una animación."""
        try:
            # Cargar animación según el formato
            if file_path.suffix.lower() in ['.glb', '.gltf']:
                model = pygltflib.GLTF2().load(str(file_path))
                
                # Obtener información de animaciones
                if not model.animations:
                    return None
                    
                animation = model.animations[0]
                duration = max(channel.sampler.input.max for channel in animation.channels)
                frames = len(model.accessors[animation.channels[0].sampler.input].count)
                fps = frames / duration
                channels = len(animation.channels)
                
                # Verificar características
                has_weights = any(ch.target.path == 'weights' for ch in animation.channels)
                has_morphs = any(ch.target.path == 'morphTargetWeights' for ch in animation.channels)
                
            else:
                # Usar trimesh para otros formatos
                scene = trimesh.load(file_path)
                if not hasattr(scene, 'animation'):
                    return None
                    
                duration = scene.animation.duration
                frames = len(scene.animation.frames)
                fps = scene.animation.frame_rate
                channels = len(scene.animation.channels)
                
                # Verificar características
                has_weights = hasattr(scene.animation, 'weights')
                has_morphs = hasattr(scene.animation, 'morphs')
                
            return AnimationMetadata(
                duration=duration,
                frames=frames,
                fps=fps,
                channels=channels,
                format=file_path.suffix[1:],
                is_looping=False,  # Se determinará después si es necesario
                has_weights=has_weights,
                has_morphs=has_morphs
            )
            
        except Exception as e:
            self.logger.error(f"Error al obtener información de la animación {file_path}: {e}")
            return None
            
    def register_animation(self, file_path: Union[str, Path]) -> Optional[AnimationMetadata]:
        """Registra una nueva animación en el sistema."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.error(f"Animación no encontrada: {file_path}")
                return None
                
            # Obtener información de la animación
            metadata = self._get_animation_info(file_path)
            if not metadata:
                return None
                
            # Guardar metadatos
            self.metadata[file_path.stem] = metadata
            self._save_metadata()
            
            self.logger.info(f"Animación registrada: {file_path}")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al registrar animación {file_path}: {e}")
            return None
            
    def optimize_animation(self, 
                          file_path: Union[str, Path],
                          target_fps: float = 30) -> Optional[Path]:
        """Optimiza una animación reduciendo su framerate."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
                
            # Cargar animación
            if file_path.suffix.lower() in ['.glb', '.gltf']:
                model = pygltflib.GLTF2().load(str(file_path))
                animation = model.animations[0]
                
                # Reducir framerate
                for channel in animation.channels:
                    input_accessor = model.accessors[channel.sampler.input]
                    output_accessor = model.accessors[channel.sampler.output]
                    
                    # Reducir frames
                    new_frames = int(len(input_accessor.count) * target_fps / animation.fps)
                    input_accessor.count = new_frames
                    output_accessor.count = new_frames
                    
                # Guardar animación optimizada
                output_path = self.cache_path / f"{file_path.stem}_optimized{file_path.suffix}"
                model.save(output_path)
                
            else:
                scene = trimesh.load(file_path)
                if not hasattr(scene, 'animation'):
                    return None
                    
                # Reducir framerate
                scene.animation.frame_rate = target_fps
                
                # Guardar animación optimizada
                output_path = self.cache_path / f"{file_path.stem}_optimized{file_path.suffix}"
                scene.export(output_path)
                
            # Actualizar metadatos
            if file_path.stem in self.metadata:
                self.metadata[file_path.stem].fps = target_fps
                self.metadata[file_path.stem].frames = int(self.metadata[file_path.stem].duration * target_fps)
                self._save_metadata()
                
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al optimizar animación {file_path}: {e}")
            return None
            
    def convert_format(self, 
                      file_path: Union[str, Path],
                      target_format: str) -> Optional[Path]:
        """Convierte una animación a otro formato."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
                
            # Cargar animación
            scene = trimesh.load(file_path)
            if not hasattr(scene, 'animation'):
                return None
                
            # Guardar en nuevo formato
            output_path = self.cache_path / f"{file_path.stem}.{target_format}"
            scene.export(output_path)
            
            # Actualizar metadatos
            if file_path.stem in self.metadata:
                self.metadata[file_path.stem].format = target_format
                self._save_metadata()
                
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al convertir animación {file_path}: {e}")
            return None
            
    def extract_keyframes(self, 
                         file_path: Union[str, Path],
                         threshold: float = 0.1) -> Optional[Path]:
        """Extrae keyframes de una animación."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
                
            # Cargar animación
            scene = trimesh.load(file_path)
            if not hasattr(scene, 'animation'):
                return None
                
            # Extraer keyframes
            keyframes = []
            prev_frame = None
            
            for i, frame in enumerate(scene.animation.frames):
                if prev_frame is None or np.max(np.abs(frame - prev_frame)) > threshold:
                    keyframes.append(i)
                    prev_frame = frame
                    
            # Crear nueva animación con keyframes
            scene.animation.frames = scene.animation.frames[keyframes]
            
            # Guardar animación con keyframes
            output_path = self.cache_path / f"{file_path.stem}_keyframes{file_path.suffix}"
            scene.export(output_path)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al extraer keyframes de {file_path}: {e}")
            return None
            
    def validate_animation(self, file_path: Union[str, Path]) -> Dict[str, bool]:
        """Valida la integridad de una animación."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {'exists': False}
                
            # Cargar animación
            if file_path.suffix.lower() in ['.glb', '.gltf']:
                model = pygltflib.GLTF2().load(str(file_path))
                has_animation = bool(model.animations)
                is_valid = all(
                    channel.sampler.input is not None and
                    channel.sampler.output is not None
                    for animation in model.animations
                    for channel in animation.channels
                )
                
            else:
                scene = trimesh.load(file_path)
                has_animation = hasattr(scene, 'animation')
                is_valid = has_animation and len(scene.animation.frames) > 0
                
            return {
                'exists': True,
                'has_animation': has_animation,
                'is_valid': is_valid
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar animación {file_path}: {e}")
            return {'exists': False}
            
    def get_animation_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de todas las animaciones registradas."""
        stats = {
            'total_animations': len(self.metadata),
            'total_frames': 0,
            'total_duration': 0,
            'formats': {},
            'fps_ranges': {},
            'with_weights': 0,
            'with_morphs': 0
        }
        
        for metadata in self.metadata.values():
            stats['total_frames'] += metadata.frames
            stats['total_duration'] += metadata.duration
            stats['formats'][metadata.format] = stats['formats'].get(metadata.format, 0) + 1
            fps_range = f"{int(metadata.fps)}-{int(metadata.fps + 5)}"
            stats['fps_ranges'][fps_range] = stats['fps_ranges'].get(fps_range, 0) + 1
            if metadata.has_weights:
                stats['with_weights'] += 1
            if metadata.has_morphs:
                stats['with_morphs'] += 1
                
        return stats 