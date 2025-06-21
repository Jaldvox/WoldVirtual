import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/version_manager.log'
)

@dataclass
class VersionMetadata:
    """Metadatos específicos para versiones."""
    name: str
    version: str
    created: str
    modified: str
    author: str
    description: str
    changes: List[str]
    is_stable: bool
    is_beta: bool
    is_alpha: bool
    dependencies: Dict[str, str]

class VersionManager:
    """Gestor de versiones."""
    
    def __init__(self, base_path: str = "assets/versions"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.logger = logging.getLogger("VersionManager")
        
        # Crear directorios necesarios
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, VersionMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, VersionMetadata]:
        """Carga los metadatos de versiones desde el archivo JSON."""
        metadata_file = self.metadata_path / "versions_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: VersionMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de versiones en el archivo JSON."""
        metadata_file = self.metadata_path / "versions_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _parse_version(self, version: str) -> Tuple[int, int, int]:
        """Parsea una versión en formato semántico."""
        try:
            major, minor, patch = version.split('.')
            return int(major), int(minor), int(patch)
        except:
            return 0, 0, 0
            
    def _compare_versions(self, v1: str, v2: str) -> int:
        """Compara dos versiones."""
        major1, minor1, patch1 = self._parse_version(v1)
        major2, minor2, patch2 = self._parse_version(v2)
        
        if major1 != major2:
            return major1 - major2
        if minor1 != minor2:
            return minor1 - minor2
        return patch1 - patch2
        
    def create_version(self,
                      name: str,
                      version: str,
                      author: str,
                      description: str,
                      changes: List[str],
                      dependencies: Optional[Dict[str, str]] = None,
                      is_stable: bool = False,
                      is_beta: bool = False,
                      is_alpha: bool = False) -> Optional[VersionMetadata]:
        """Crea una nueva versión."""
        try:
            # Verificar versión única
            version_key = f"{name}_{version}"
            if version_key in self.metadata:
                self.logger.error(f"La versión {version} ya existe para {name}")
                return None
                
            # Crear metadatos
            now = datetime.now().isoformat()
            metadata = VersionMetadata(
                name=name,
                version=version,
                created=now,
                modified=now,
                author=author,
                description=description,
                changes=changes,
                is_stable=is_stable,
                is_beta=is_beta,
                is_alpha=is_alpha,
                dependencies=dependencies or {}
            )
            
            # Guardar metadatos
            self.metadata[version_key] = metadata
            self._save_metadata()
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al crear versión {version} para {name}: {e}")
            return None
            
    def update_version(self,
                      name: str,
                      version: str,
                      changes: List[str],
                      dependencies: Optional[Dict[str, str]] = None) -> bool:
        """Actualiza una versión existente."""
        try:
            version_key = f"{name}_{version}"
            if version_key not in self.metadata:
                return False
                
            # Actualizar metadatos
            metadata = self.metadata[version_key]
            metadata.modified = datetime.now().isoformat()
            metadata.changes.extend(changes)
            if dependencies:
                metadata.dependencies.update(dependencies)
                
            self._save_metadata()
            return True
            
        except Exception as e:
            self.logger.error(f"Error al actualizar versión {version} de {name}: {e}")
            return False
            
    def get_version(self,
                   name: str,
                   version: str) -> Optional[VersionMetadata]:
        """Obtiene una versión específica."""
        try:
            version_key = f"{name}_{version}"
            return self.metadata.get(version_key)
            
        except Exception as e:
            self.logger.error(f"Error al obtener versión {version} de {name}: {e}")
            return None
            
    def get_latest_version(self,
                          name: str,
                          include_beta: bool = False,
                          include_alpha: bool = False) -> Optional[VersionMetadata]:
        """Obtiene la última versión disponible."""
        try:
            versions = []
            for key, metadata in self.metadata.items():
                if metadata.name == name:
                    if not include_beta and metadata.is_beta:
                        continue
                    if not include_alpha and metadata.is_alpha:
                        continue
                    versions.append(metadata)
                    
            if not versions:
                return None
                
            # Ordenar por versión
            versions.sort(key=lambda x: self._parse_version(x.version), reverse=True)
            return versions[0]
            
        except Exception as e:
            self.logger.error(f"Error al obtener última versión de {name}: {e}")
            return None
            
    def get_version_history(self,
                           name: str,
                           include_beta: bool = False,
                           include_alpha: bool = False) -> List[VersionMetadata]:
        """Obtiene el historial de versiones."""
        try:
            versions = []
            for key, metadata in self.metadata.items():
                if metadata.name == name:
                    if not include_beta and metadata.is_beta:
                        continue
                    if not include_alpha and metadata.is_alpha:
                        continue
                    versions.append(metadata)
                    
            # Ordenar por versión
            versions.sort(key=lambda x: self._parse_version(x.version), reverse=True)
            return versions
            
        except Exception as e:
            self.logger.error(f"Error al obtener historial de versiones de {name}: {e}")
            return []
            
    def compare_versions(self,
                        name: str,
                        version1: str,
                        version2: str) -> int:
        """Compara dos versiones de un elemento."""
        try:
            v1 = self.get_version(name, version1)
            v2 = self.get_version(name, version2)
            
            if not v1 or not v2:
                return 0
                
            return self._compare_versions(v1.version, v2.version)
            
        except Exception as e:
            self.logger.error(f"Error al comparar versiones {version1} y {version2} de {name}: {e}")
            return 0
            
    def validate_version(self,
                        name: str,
                        version: str) -> Dict[str, bool]:
        """Valida una versión."""
        try:
            version_key = f"{name}_{version}"
            if version_key not in self.metadata:
                return {'exists': False}
                
            metadata = self.metadata[version_key]
            
            # Verificar dependencias
            missing_deps = []
            for dep_name, dep_version in metadata.dependencies.items():
                dep_key = f"{dep_name}_{dep_version}"
                if dep_key not in self.metadata:
                    missing_deps.append(f"{dep_name}@{dep_version}")
                    
            return {
                'exists': True,
                'has_description': bool(metadata.description),
                'has_changes': bool(metadata.changes),
                'missing_dependencies': missing_deps,
                'is_valid': bool(metadata.description) and bool(metadata.changes) and not missing_deps
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar versión {version} de {name}: {e}")
            return {'exists': False}
            
    def get_version_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de las versiones."""
        stats = {
            'total_versions': len(self.metadata),
            'stable_versions': 0,
            'beta_versions': 0,
            'alpha_versions': 0,
            'elements': {},
            'version_counts': {
                '0.x': 0,
                '1.x': 0,
                '2.x': 0,
                '3.x': 0,
                '4.x+': 0
            }
        }
        
        for metadata in self.metadata.values():
            if metadata.is_stable:
                stats['stable_versions'] += 1
            if metadata.is_beta:
                stats['beta_versions'] += 1
            if metadata.is_alpha:
                stats['alpha_versions'] += 1
                
            stats['elements'][metadata.name] = stats['elements'].get(metadata.name, 0) + 1
            
            # Clasificar por versión mayor
            major = self._parse_version(metadata.version)[0]
            if major == 0:
                stats['version_counts']['0.x'] += 1
            elif major == 1:
                stats['version_counts']['1.x'] += 1
            elif major == 2:
                stats['version_counts']['2.x'] += 1
            elif major == 3:
                stats['version_counts']['3.x'] += 1
            else:
                stats['version_counts']['4.x+'] += 1
                
        return stats 