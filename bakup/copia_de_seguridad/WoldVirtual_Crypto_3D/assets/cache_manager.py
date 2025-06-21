import os
import json
import logging
import hashlib
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/cache_manager.log'
)

@dataclass
class CacheMetadata:
    """Metadatos específicos para caché."""
    name: str
    type: str
    size: int
    hash: str
    created: str
    last_accessed: str
    access_count: int
    is_valid: bool
    dependencies: List[str]

class CacheManager:
    """Gestor de caché."""
    
    def __init__(self, base_path: str = "assets/cache"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.cache_path = self.base_path / "data"
        self.logger = logging.getLogger("CacheManager")
        
        # Crear directorios necesarios
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, CacheMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, CacheMetadata]:
        """Carga los metadatos de caché desde el archivo JSON."""
        metadata_file = self.metadata_path / "cache_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: CacheMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de caché en el archivo JSON."""
        metadata_file = self.metadata_path / "cache_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _calculate_hash(self, file_path: Path) -> str:
        """Calcula el hash de un archivo."""
        try:
            hasher = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            self.logger.error(f"Error al calcular hash de {file_path}: {e}")
            return ''
            
    def _get_cache_info(self, file_path: Path) -> Optional[CacheMetadata]:
        """Obtiene información detallada de un archivo en caché."""
        try:
            if not file_path.exists():
                return None
                
            # Obtener información básica
            name = file_path.stem
            cache_type = file_path.suffix[1:]  # Eliminar el punto
            size = file_path.stat().st_size
            file_hash = self._calculate_hash(file_path)
            
            # Obtener timestamps
            created = datetime.fromtimestamp(file_path.stat().st_ctime).isoformat()
            last_accessed = datetime.fromtimestamp(file_path.stat().st_atime).isoformat()
            
            # Verificar dependencias
            dependencies = []
            if cache_type in ['gltf', 'glb', 'fbx']:
                # Buscar texturas relacionadas
                for texture in self.cache_path.glob(f"{name}_*.png"):
                    dependencies.append(texture.name)
                    
            return CacheMetadata(
                name=name,
                type=cache_type,
                size=size,
                hash=file_hash,
                created=created,
                last_accessed=last_accessed,
                access_count=0,
                is_valid=True,
                dependencies=dependencies
            )
            
        except Exception as e:
            self.logger.error(f"Error al obtener información de caché {file_path}: {e}")
            return None
            
    def add_to_cache(self,
                    file_path: Union[str, Path],
                    cache_type: Optional[str] = None) -> Optional[Path]:
        """Añade un archivo a la caché."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
                
            # Determinar tipo de caché
            if cache_type is None:
                cache_type = file_path.suffix[1:]
                
            # Crear nombre de archivo en caché
            cache_name = f"{file_path.stem}_{self._calculate_hash(file_path)}.{cache_type}"
            cache_path = self.cache_path / cache_name
            
            # Copiar archivo a caché
            shutil.copy2(file_path, cache_path)
            
            # Obtener información de caché
            metadata = self._get_cache_info(cache_path)
            if metadata:
                self.metadata[cache_name] = metadata
                self._save_metadata()
                
            return cache_path
            
        except Exception as e:
            self.logger.error(f"Error al añadir a caché {file_path}: {e}")
            return None
            
    def get_from_cache(self,
                      name: str,
                      cache_type: str) -> Optional[Path]:
        """Obtiene un archivo de la caché."""
        try:
            # Buscar en metadatos
            for cache_name, metadata in self.metadata.items():
                if metadata.name == name and metadata.type == cache_type:
                    cache_path = self.cache_path / cache_name
                    if cache_path.exists():
                        # Actualizar metadatos
                        metadata.last_accessed = datetime.now().isoformat()
                        metadata.access_count += 1
                        self._save_metadata()
                        return cache_path
            return None
            
        except Exception as e:
            self.logger.error(f"Error al obtener de caché {name}.{cache_type}: {e}")
            return None
            
    def remove_from_cache(self,
                         name: str,
                         cache_type: str) -> bool:
        """Elimina un archivo de la caché."""
        try:
            # Buscar en metadatos
            for cache_name, metadata in self.metadata.items():
                if metadata.name == name and metadata.type == cache_type:
                    cache_path = self.cache_path / cache_name
                    if cache_path.exists():
                        # Eliminar archivo
                        cache_path.unlink()
                        # Eliminar metadatos
                        del self.metadata[cache_name]
                        self._save_metadata()
                        return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error al eliminar de caché {name}.{cache_type}: {e}")
            return False
            
    def clear_cache(self, cache_type: Optional[str] = None) -> int:
        """Limpia la caché."""
        try:
            count = 0
            # Eliminar archivos
            for cache_name, metadata in list(self.metadata.items()):
                if cache_type is None or metadata.type == cache_type:
                    cache_path = self.cache_path / cache_name
                    if cache_path.exists():
                        cache_path.unlink()
                        del self.metadata[cache_name]
                        count += 1
            self._save_metadata()
            return count
            
        except Exception as e:
            self.logger.error(f"Error al limpiar caché: {e}")
            return 0
            
    def validate_cache(self) -> Dict[str, bool]:
        """Valida la integridad de la caché."""
        try:
            results = {
                'total_files': len(self.metadata),
                'valid_files': 0,
                'invalid_files': 0,
                'missing_files': 0
            }
            
            for cache_name, metadata in list(self.metadata.items()):
                cache_path = self.cache_path / cache_name
                if not cache_path.exists():
                    results['missing_files'] += 1
                    del self.metadata[cache_name]
                    continue
                    
                # Verificar hash
                current_hash = self._calculate_hash(cache_path)
                if current_hash == metadata.hash:
                    results['valid_files'] += 1
                    metadata.is_valid = True
                else:
                    results['invalid_files'] += 1
                    metadata.is_valid = False
                    
            self._save_metadata()
            return results
            
        except Exception as e:
            self.logger.error(f"Error al validar caché: {e}")
            return {'error': True}
            
    def get_cache_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de la caché."""
        stats = {
            'total_files': len(self.metadata),
            'total_size': 0,
            'types': {},
            'access_counts': {
                '0-10': 0,
                '11-50': 0,
                '51-100': 0,
                '100+': 0
            }
        }
        
        for metadata in self.metadata.values():
            stats['total_size'] += metadata.size
            stats['types'][metadata.type] = stats['types'].get(metadata.type, 0) + 1
            
            # Clasificar por número de accesos
            if metadata.access_count <= 10:
                stats['access_counts']['0-10'] += 1
            elif metadata.access_count <= 50:
                stats['access_counts']['11-50'] += 1
            elif metadata.access_count <= 100:
                stats['access_counts']['51-100'] += 1
            else:
                stats['access_counts']['100+'] += 1
                
        return stats 