import os
import json
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/resource_manager.log'
)

@dataclass
class ResourceMetadata:
    """Metadatos específicos para recursos."""
    name: str
    type: str
    path: str
    size: int
    hash: str
    created: str
    last_modified: str
    version: str
    is_loaded: bool
    is_cached: bool
    is_shared: bool
    dependencies: List[str]
    parameters: Dict[str, Any]

class ResourceManager:
    """Gestor de recursos."""
    
    def __init__(self, base_path: str = "assets/resources"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.cache_path = self.base_path / "cache"
        self.logger = logging.getLogger("ResourceManager")
        
        # Crear directorios necesarios
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, ResourceMetadata] = self._load_metadata()
        
        # Recursos cargados
        self.loaded_resources: Dict[str, Any] = {}
        
    def _load_metadata(self) -> Dict[str, ResourceMetadata]:
        """Carga los metadatos de recursos desde el archivo JSON."""
        metadata_file = self.metadata_path / "resources_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: ResourceMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de recursos en el archivo JSON."""
        metadata_file = self.metadata_path / "resources_metadata.json"
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
            
    def _get_resource_info(self, file_path: Path) -> Optional[ResourceMetadata]:
        """Obtiene información detallada de un recurso."""
        try:
            if not file_path.exists():
                return None
                
            # Obtener información básica
            name = file_path.stem
            resource_type = file_path.suffix[1:]  # Eliminar el punto
            size = file_path.stat().st_size
            file_hash = self._calculate_hash(file_path)
            
            # Obtener timestamps
            created = datetime.fromtimestamp(file_path.stat().st_ctime).isoformat()
            last_modified = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            
            return ResourceMetadata(
                name=name,
                type=resource_type,
                path=str(file_path),
                size=size,
                hash=file_hash,
                created=created,
                last_modified=last_modified,
                version='1.0',
                is_loaded=False,
                is_cached=False,
                is_shared=False,
                dependencies=[],
                parameters={}
            )
            
        except Exception as e:
            self.logger.error(f"Error al obtener información de recurso {file_path}: {e}")
            return None
            
    def register_resource(self,
                         file_path: Union[str, Path],
                         is_shared: bool = False,
                         dependencies: Optional[List[str]] = None,
                         parameters: Optional[Dict[str, Any]] = None) -> Optional[ResourceMetadata]:
        """Registra un nuevo recurso."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
                
            # Obtener información del recurso
            metadata = self._get_resource_info(file_path)
            if not metadata:
                return None
                
            # Actualizar metadatos
            metadata.is_shared = is_shared
            metadata.dependencies = dependencies or []
            metadata.parameters = parameters or {}
            
            # Guardar metadatos
            self.metadata[metadata.name] = metadata
            self._save_metadata()
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al registrar recurso {file_path}: {e}")
            return None
            
    def load_resource(self,
                     name: str,
                     force_reload: bool = False) -> Optional[Any]:
        """Carga un recurso."""
        try:
            if name not in self.metadata:
                return None
                
            metadata = self.metadata[name]
            
            # Verificar si ya está cargado
            if not force_reload and metadata.is_loaded and name in self.loaded_resources:
                return self.loaded_resources[name]
                
            # Cargar recurso según su tipo
            resource = None
            if metadata.type == 'json':
                with open(metadata.path, 'r') as f:
                    resource = json.load(f)
            elif metadata.type == 'txt':
                with open(metadata.path, 'r') as f:
                    resource = f.read()
            elif metadata.type == 'png':
                from PIL import Image
                resource = Image.open(metadata.path)
            elif metadata.type == 'mp3':
                import pygame
                pygame.mixer.init()
                resource = pygame.mixer.Sound(metadata.path)
            # Añadir más tipos según sea necesario
            
            if resource is not None:
                # Actualizar metadatos
                metadata.is_loaded = True
                metadata.last_modified = datetime.now().isoformat()
                self._save_metadata()
                
                # Guardar en caché
                self.loaded_resources[name] = resource
                
            return resource
            
        except Exception as e:
            self.logger.error(f"Error al cargar recurso {name}: {e}")
            return None
            
    def unload_resource(self, name: str) -> bool:
        """Descarga un recurso."""
        try:
            if name not in self.metadata:
                return False
                
            # Eliminar de caché
            if name in self.loaded_resources:
                del self.loaded_resources[name]
                
            # Actualizar metadatos
            metadata = self.metadata[name]
            metadata.is_loaded = False
            self._save_metadata()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error al descargar recurso {name}: {e}")
            return False
            
    def get_resource(self,
                    name: str,
                    default: Optional[Any] = None) -> Optional[Any]:
        """Obtiene un recurso."""
        try:
            if name not in self.metadata:
                return default
                
            # Intentar cargar si no está en caché
            if name not in self.loaded_resources:
                return self.load_resource(name)
                
            return self.loaded_resources[name]
            
        except Exception as e:
            self.logger.error(f"Error al obtener recurso {name}: {e}")
            return default
            
    def get_resources_by_type(self, resource_type: str) -> List[ResourceMetadata]:
        """Obtiene todos los recursos de un tipo específico."""
        try:
            return [
                metadata for metadata in self.metadata.values()
                if metadata.type == resource_type
            ]
            
        except Exception as e:
            self.logger.error(f"Error al obtener recursos de tipo {resource_type}: {e}")
            return []
            
    def get_loaded_resources(self) -> List[ResourceMetadata]:
        """Obtiene todos los recursos cargados."""
        try:
            return [
                metadata for metadata in self.metadata.values()
                if metadata.is_loaded
            ]
            
        except Exception as e:
            self.logger.error(f"Error al obtener recursos cargados: {e}")
            return []
            
    def get_shared_resources(self) -> List[ResourceMetadata]:
        """Obtiene todos los recursos compartidos."""
        try:
            return [
                metadata for metadata in self.metadata.values()
                if metadata.is_shared
            ]
            
        except Exception as e:
            self.logger.error(f"Error al obtener recursos compartidos: {e}")
            return []
            
    def validate_resource(self, name: str) -> Dict[str, bool]:
        """Valida un recurso."""
        try:
            if name not in self.metadata:
                return {'exists': False}
                
            metadata = self.metadata[name]
            
            # Verificar archivo
            file_path = Path(metadata.path)
            has_file = file_path.exists()
            
            # Verificar hash
            has_valid_hash = False
            if has_file:
                current_hash = self._calculate_hash(file_path)
                has_valid_hash = current_hash == metadata.hash
                
            return {
                'exists': True,
                'has_file': has_file,
                'has_valid_hash': has_valid_hash,
                'is_loaded': metadata.is_loaded,
                'is_cached': metadata.is_cached,
                'is_shared': metadata.is_shared,
                'has_dependencies': bool(metadata.dependencies),
                'has_parameters': bool(metadata.parameters)
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar recurso {name}: {e}")
            return {'exists': False}
            
    def get_resource_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de los recursos."""
        stats = {
            'total_resources': len(self.metadata),
            'loaded_resources': 0,
            'cached_resources': 0,
            'shared_resources': 0,
            'types': {},
            'dependency_counts': {
                '0': 0,
                '1-5': 0,
                '6-10': 0,
                '10+': 0
            },
            'parameter_counts': {
                '0': 0,
                '1-5': 0,
                '6-10': 0,
                '10+': 0
            }
        }
        
        for metadata in self.metadata.values():
            if metadata.is_loaded:
                stats['loaded_resources'] += 1
            if metadata.is_cached:
                stats['cached_resources'] += 1
            if metadata.is_shared:
                stats['shared_resources'] += 1
                
            stats['types'][metadata.type] = stats['types'].get(metadata.type, 0) + 1
            
            # Clasificar por número de dependencias
            dep_count = len(metadata.dependencies)
            if dep_count == 0:
                stats['dependency_counts']['0'] += 1
            elif dep_count <= 5:
                stats['dependency_counts']['1-5'] += 1
            elif dep_count <= 10:
                stats['dependency_counts']['6-10'] += 1
            else:
                stats['dependency_counts']['10+'] += 1
                
            # Clasificar por número de parámetros
            param_count = len(metadata.parameters)
            if param_count == 0:
                stats['parameter_counts']['0'] += 1
            elif param_count <= 5:
                stats['parameter_counts']['1-5'] += 1
            elif param_count <= 10:
                stats['parameter_counts']['6-10'] += 1
            else:
                stats['parameter_counts']['10+'] += 1
                
        return stats 