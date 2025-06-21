import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/effect_manager.log'
)

@dataclass
class EffectMetadata:
    """Metadatos específicos para efectos visuales."""
    name: str
    type: str
    duration: float
    is_looping: bool
    has_particles: bool
    has_lighting: bool
    has_post_processing: bool
    shaders: List[str]
    textures: List[str]
    parameters: Dict[str, Union[float, int, bool, str]]

class EffectManager:
    """Gestor de efectos visuales."""
    
    def __init__(self, base_path: str = "assets/effects"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.cache_path = self.base_path / "cache"
        self.logger = logging.getLogger("EffectManager")
        
        # Crear directorios necesarios
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, EffectMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, EffectMetadata]:
        """Carga los metadatos de efectos desde el archivo JSON."""
        metadata_file = self.metadata_path / "effects_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: EffectMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de efectos en el archivo JSON."""
        metadata_file = self.metadata_path / "effects_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _get_effect_info(self, file_path: Path) -> Optional[EffectMetadata]:
        """Obtiene información detallada de un efecto."""
        try:
            # Leer archivo de efecto
            with open(file_path, 'r') as f:
                content = json.load(f)
                
            # Extraer información
            name = content.get('name', file_path.stem)
            effect_type = content.get('type', 'unknown')
            duration = content.get('duration', 0.0)
            is_looping = content.get('isLooping', False)
            
            # Verificar características
            has_particles = 'particles' in content
            has_lighting = 'lighting' in content
            has_post_processing = 'postProcessing' in content
            
            # Obtener shaders y texturas
            shaders = content.get('shaders', [])
            textures = content.get('textures', [])
            
            # Obtener parámetros
            parameters = content.get('parameters', {})
            
            return EffectMetadata(
                name=name,
                type=effect_type,
                duration=duration,
                is_looping=is_looping,
                has_particles=has_particles,
                has_lighting=has_lighting,
                has_post_processing=has_post_processing,
                shaders=shaders,
                textures=textures,
                parameters=parameters
            )
            
        except Exception as e:
            self.logger.error(f"Error al obtener información del efecto {file_path}: {e}")
            return None
            
    def register_effect(self, file_path: Union[str, Path]) -> Optional[EffectMetadata]:
        """Registra un nuevo efecto en el sistema."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.error(f"Efecto no encontrado: {file_path}")
                return None
                
            # Obtener información del efecto
            metadata = self._get_effect_info(file_path)
            if not metadata:
                return None
                
            # Guardar metadatos
            self.metadata[file_path.stem] = metadata
            self._save_metadata()
            
            self.logger.info(f"Efecto registrado: {file_path}")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al registrar efecto {file_path}: {e}")
            return None
            
    def create_effect(self,
                     name: str,
                     effect_type: str,
                     duration: float = 0.0,
                     is_looping: bool = False,
                     parameters: Optional[Dict] = None) -> Optional[Path]:
        """Crea un nuevo efecto."""
        try:
            # Crear estructura del efecto
            effect_data = {
                'name': name,
                'type': effect_type,
                'duration': duration,
                'isLooping': is_looping,
                'parameters': parameters or {},
                'shaders': [],
                'textures': [],
                'particles': {},
                'lighting': {},
                'postProcessing': {}
            }
            
            # Guardar efecto
            output_path = self.cache_path / f"{name}.json"
            with open(output_path, 'w') as f:
                json.dump(effect_data, f, indent=2)
                
            # Registrar efecto
            self.register_effect(output_path)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al crear efecto {name}: {e}")
            return None
            
    def add_shader(self,
                  effect_path: Union[str, Path],
                  shader_path: Union[str, Path],
                  shader_type: str) -> bool:
        """Añade un shader a un efecto."""
        try:
            effect_path = Path(effect_path)
            shader_path = Path(shader_path)
            
            if not effect_path.exists() or not shader_path.exists():
                return False
                
            # Leer efecto
            with open(effect_path, 'r') as f:
                effect_data = json.load(f)
                
            # Añadir shader
            shader_info = {
                'path': str(shader_path),
                'type': shader_type
            }
            effect_data['shaders'].append(shader_info)
            
            # Guardar efecto
            with open(effect_path, 'w') as f:
                json.dump(effect_data, f, indent=2)
                
            # Actualizar metadatos
            if effect_path.stem in self.metadata:
                self.metadata[effect_path.stem].shaders.append(str(shader_path))
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir shader a efecto {effect_path}: {e}")
            return False
            
    def add_texture(self,
                   effect_path: Union[str, Path],
                   texture_path: Union[str, Path],
                   texture_type: str) -> bool:
        """Añade una textura a un efecto."""
        try:
            effect_path = Path(effect_path)
            texture_path = Path(texture_path)
            
            if not effect_path.exists() or not texture_path.exists():
                return False
                
            # Leer efecto
            with open(effect_path, 'r') as f:
                effect_data = json.load(f)
                
            # Añadir textura
            texture_info = {
                'path': str(texture_path),
                'type': texture_type
            }
            effect_data['textures'].append(texture_info)
            
            # Guardar efecto
            with open(effect_path, 'w') as f:
                json.dump(effect_data, f, indent=2)
                
            # Actualizar metadatos
            if effect_path.stem in self.metadata:
                self.metadata[effect_path.stem].textures.append(str(texture_path))
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir textura a efecto {effect_path}: {e}")
            return False
            
    def set_parameter(self,
                     effect_path: Union[str, Path],
                     name: str,
                     value: Union[float, int, bool, str]) -> bool:
        """Establece un parámetro en un efecto."""
        try:
            effect_path = Path(effect_path)
            if not effect_path.exists():
                return False
                
            # Leer efecto
            with open(effect_path, 'r') as f:
                effect_data = json.load(f)
                
            # Establecer parámetro
            effect_data['parameters'][name] = value
            
            # Guardar efecto
            with open(effect_path, 'w') as f:
                json.dump(effect_data, f, indent=2)
                
            # Actualizar metadatos
            if effect_path.stem in self.metadata:
                self.metadata[effect_path.stem].parameters[name] = value
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al establecer parámetro en efecto {effect_path}: {e}")
            return False
            
    def validate_effect(self, file_path: Union[str, Path]) -> Dict[str, bool]:
        """Valida la integridad de un efecto."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {'exists': False}
                
            # Leer efecto
            with open(file_path, 'r') as f:
                effect_data = json.load(f)
                
            # Verificar características
            has_name = 'name' in effect_data
            has_type = 'type' in effect_data
            has_parameters = 'parameters' in effect_data
            has_shaders = 'shaders' in effect_data
            has_textures = 'textures' in effect_data
            
            return {
                'exists': True,
                'has_name': has_name,
                'has_type': has_type,
                'has_parameters': has_parameters,
                'has_shaders': has_shaders,
                'has_textures': has_textures,
                'is_valid': all([has_name, has_type, has_parameters])
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar efecto {file_path}: {e}")
            return {'exists': False}
            
    def get_effect_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de todos los efectos registrados."""
        stats = {
            'total_effects': len(self.metadata),
            'particle_effects': 0,
            'lighting_effects': 0,
            'post_processing_effects': 0,
            'looping_effects': 0,
            'with_shaders': 0,
            'with_textures': 0,
            'types': {}
        }
        
        for metadata in self.metadata.values():
            if metadata.has_particles:
                stats['particle_effects'] += 1
            if metadata.has_lighting:
                stats['lighting_effects'] += 1
            if metadata.has_post_processing:
                stats['post_processing_effects'] += 1
            if metadata.is_looping:
                stats['looping_effects'] += 1
            if metadata.shaders:
                stats['with_shaders'] += 1
            if metadata.textures:
                stats['with_textures'] += 1
            stats['types'][metadata.type] = stats['types'].get(metadata.type, 0) + 1
                
        return stats 