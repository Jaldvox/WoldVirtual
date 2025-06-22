import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union
import hashlib
from PIL import Image
import numpy as np
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/asset_manager.log'
)

@dataclass
class AssetMetadata:
    """Metadatos de un asset."""
    name: str
    type: str
    path: str
    size: int
    hash: str
    format: str
    dimensions: Optional[tuple] = None
    duration: Optional[float] = None
    lod_level: Optional[int] = None
    tags: List[str] = None

class AssetManager:
    """Gestor principal de assets."""
    
    def __init__(self, base_path: str = "assets"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.cache_path = self.base_path / "cache"
        self.logger = logging.getLogger("AssetManager")
        
        # Crear directorios necesarios
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, AssetMetadata] = self._load_metadata()
        
        # Pool de hilos para operaciones asíncronas
        self.executor = ThreadPoolExecutor(max_workers=4)
        
    def _load_metadata(self) -> Dict[str, AssetMetadata]:
        """Carga los metadatos desde el archivo JSON."""
        metadata_file = self.metadata_path / "assets_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: AssetMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos en el archivo JSON."""
        metadata_file = self.metadata_path / "assets_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _calculate_hash(self, file_path: Path) -> str:
        """Calcula el hash SHA-256 de un archivo."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
        
    def _get_asset_type(self, file_path: Path) -> str:
        """Determina el tipo de asset basado en la extensión."""
        ext = file_path.suffix.lower()
        if ext in ['.glb', '.gltf', '.fbx', '.obj', '.stl']:
            return 'model'
        elif ext in ['.png', '.jpg', '.jpeg', '.hdr', '.exr']:
            return 'texture'
        elif ext in ['.mp3', '.wav', '.ogg']:
            return 'sound'
        elif ext in ['.svg', '.ico']:
            return 'image'
        return 'unknown'
        
    def _get_image_dimensions(self, file_path: Path) -> Optional[tuple]:
        """Obtiene las dimensiones de una imagen."""
        try:
            with Image.open(file_path) as img:
                return img.size
        except Exception as e:
            self.logger.error(f"Error al obtener dimensiones de imagen {file_path}: {e}")
            return None
            
    def _get_audio_duration(self, file_path: Path) -> Optional[float]:
        """Obtiene la duración de un archivo de audio."""
        try:
            import wave
            with wave.open(file_path, 'rb') as wav:
                frames = wav.getnframes()
                rate = wav.getframerate()
                return frames / float(rate)
        except Exception as e:
            self.logger.error(f"Error al obtener duración de audio {file_path}: {e}")
            return None
            
    def _get_lod_level(self, file_path: Path) -> Optional[int]:
        """Determina el nivel de LOD de un modelo."""
        try:
            return int(file_path.stem.split('_')[-1].replace('lod', ''))
        except:
            return None
            
    def _extract_tags(self, file_path: Path) -> List[str]:
        """Extrae tags del nombre del archivo."""
        tags = []
        name_parts = file_path.stem.split('_')
        
        # Extraer tags comunes
        if 'lod' in name_parts:
            tags.append('lod')
        if any(ext in name_parts for ext in ['tex', 'texture']):
            tags.append('texture')
        if any(ext in name_parts for ext in ['mod', 'model']):
            tags.append('model')
        if any(ext in name_parts for ext in ['snd', 'sound']):
            tags.append('sound')
            
        return tags
        
    def register_asset(self, file_path: Union[str, Path]) -> Optional[AssetMetadata]:
        """Registra un nuevo asset en el sistema."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.error(f"Archivo no encontrado: {file_path}")
                return None
                
            # Calcular metadatos
            asset_type = self._get_asset_type(file_path)
            file_size = file_path.stat().st_size
            file_hash = self._calculate_hash(file_path)
            
            # Crear objeto de metadatos
            metadata = AssetMetadata(
                name=file_path.stem,
                type=asset_type,
                path=str(file_path.relative_to(self.base_path)),
                size=file_size,
                hash=file_hash,
                format=file_path.suffix[1:],
                tags=self._extract_tags(file_path)
            )
            
            # Agregar metadatos específicos según el tipo
            if asset_type == 'texture':
                metadata.dimensions = self._get_image_dimensions(file_path)
            elif asset_type == 'sound':
                metadata.duration = self._get_audio_duration(file_path)
            elif asset_type == 'model':
                metadata.lod_level = self._get_lod_level(file_path)
                
            # Guardar metadatos
            self.metadata[file_hash] = metadata
            self._save_metadata()
            
            self.logger.info(f"Asset registrado: {file_path}")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al registrar asset {file_path}: {e}")
            return None
            
    def get_asset(self, asset_hash: str) -> Optional[AssetMetadata]:
        """Obtiene los metadatos de un asset por su hash."""
        return self.metadata.get(asset_hash)
        
    def find_assets(self, 
                   asset_type: Optional[str] = None,
                   tags: Optional[List[str]] = None,
                   min_size: Optional[int] = None,
                   max_size: Optional[int] = None) -> List[AssetMetadata]:
        """Busca assets que coincidan con los criterios especificados."""
        results = []
        
        for metadata in self.metadata.values():
            if asset_type and metadata.type != asset_type:
                continue
            if tags and not all(tag in metadata.tags for tag in tags):
                continue
            if min_size and metadata.size < min_size:
                continue
            if max_size and metadata.size > max_size:
                continue
            results.append(metadata)
            
        return results
        
    def optimize_asset(self, asset_hash: str) -> bool:
        """Optimiza un asset específico."""
        try:
            metadata = self.get_asset(asset_hash)
            if not metadata:
                return False
                
            file_path = self.base_path / metadata.path
            
            if metadata.type == 'texture':
                self._optimize_texture(file_path)
            elif metadata.type == 'model':
                self._optimize_model(file_path)
            elif metadata.type == 'sound':
                self._optimize_sound(file_path)
                
            # Actualizar metadatos después de la optimización
            self.register_asset(file_path)
            return True
            
        except Exception as e:
            self.logger.error(f"Error al optimizar asset {asset_hash}: {e}")
            return False
            
    def _optimize_texture(self, file_path: Path):
        """Optimiza una textura."""
        try:
            with Image.open(file_path) as img:
                # Convertir a RGB si es necesario
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                    
                # Redimensionar si es muy grande
                max_size = 2048
                if max(img.size) > max_size:
                    ratio = max_size / max(img.size)
                    new_size = tuple(int(dim * ratio) for dim in img.size)
                    img = img.resize(new_size, Image.LANCZOS)
                    
                # Guardar optimizado
                img.save(file_path, optimize=True, quality=85)
                
        except Exception as e:
            self.logger.error(f"Error al optimizar textura {file_path}: {e}")
            
    def _optimize_model(self, file_path: Path):
        """Optimiza un modelo 3D."""
        # Implementar optimización de modelos según el formato
        pass
        
    def _optimize_sound(self, file_path: Path):
        """Optimiza un archivo de sonido."""
        # Implementar optimización de audio según el formato
        pass
        
    def cleanup_cache(self, max_age_days: int = 7):
        """Limpia la caché de assets antiguos."""
        try:
            import time
            current_time = time.time()
            max_age_seconds = max_age_days * 24 * 60 * 60
            
            for cache_file in self.cache_path.glob('*'):
                if current_time - cache_file.stat().st_mtime > max_age_seconds:
                    cache_file.unlink()
                    self.logger.info(f"Archivo de caché eliminado: {cache_file}")
                    
        except Exception as e:
            self.logger.error(f"Error al limpiar caché: {e}")
            
    def validate_assets(self) -> Dict[str, List[str]]:
        """Valida la integridad de todos los assets."""
        results = {
            'valid': [],
            'invalid': [],
            'missing': []
        }
        
        for metadata in self.metadata.values():
            file_path = self.base_path / metadata.path
            
            if not file_path.exists():
                results['missing'].append(metadata.path)
                continue
                
            current_hash = self._calculate_hash(file_path)
            if current_hash == metadata.hash:
                results['valid'].append(metadata.path)
            else:
                results['invalid'].append(metadata.path)
                
        return results
        
    def __del__(self):
        """Limpieza al destruir el objeto."""
        self.executor.shutdown(wait=True) 