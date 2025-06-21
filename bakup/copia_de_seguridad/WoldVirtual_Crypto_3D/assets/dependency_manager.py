import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Set
from dataclasses import dataclass

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/dependency_manager.log'
)

@dataclass
class DependencyMetadata:
    """Metadatos específicos para dependencias."""
    name: str
    type: str
    version: str
    dependencies: List[str]
    dependents: List[str]
    is_required: bool
    is_optional: bool
    is_circular: bool

class DependencyManager:
    """Gestor de dependencias."""
    
    def __init__(self, base_path: str = "assets/dependencies"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.logger = logging.getLogger("DependencyManager")
        
        # Crear directorios necesarios
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, DependencyMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, DependencyMetadata]:
        """Carga los metadatos de dependencias desde el archivo JSON."""
        metadata_file = self.metadata_path / "dependencies_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: DependencyMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de dependencias en el archivo JSON."""
        metadata_file = self.metadata_path / "dependencies_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _check_circular_dependency(self,
                                 name: str,
                                 dependencies: List[str],
                                 visited: Set[str] = None) -> bool:
        """Verifica si hay dependencias circulares."""
        if visited is None:
            visited = set()
            
        if name in visited:
            return True
            
        visited.add(name)
        
        for dep in dependencies:
            if dep in self.metadata:
                if self._check_circular_dependency(
                    dep,
                    self.metadata[dep].dependencies,
                    visited.copy()
                ):
                    return True
                    
        return False
        
    def register_dependency(self,
                          name: str,
                          dep_type: str,
                          version: str,
                          dependencies: List[str],
                          is_required: bool = True) -> Optional[DependencyMetadata]:
        """Registra una nueva dependencia."""
        try:
            # Verificar dependencias circulares
            if self._check_circular_dependency(name, dependencies):
                self.logger.warning(f"Dependencia circular detectada para {name}")
                is_circular = True
            else:
                is_circular = False
                
            # Crear metadatos
            metadata = DependencyMetadata(
                name=name,
                type=dep_type,
                version=version,
                dependencies=dependencies,
                dependents=[],
                is_required=is_required,
                is_optional=not is_required,
                is_circular=is_circular
            )
            
            # Actualizar dependientes
            for dep in dependencies:
                if dep in self.metadata:
                    if name not in self.metadata[dep].dependents:
                        self.metadata[dep].dependents.append(name)
                        
            # Guardar metadatos
            self.metadata[name] = metadata
            self._save_metadata()
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al registrar dependencia {name}: {e}")
            return None
            
    def add_dependency(self,
                      name: str,
                      dependency: str) -> bool:
        """Añade una dependencia a un elemento existente."""
        try:
            if name not in self.metadata:
                return False
                
            # Verificar dependencia circular
            if self._check_circular_dependency(name, [dependency]):
                self.logger.warning(f"Dependencia circular detectada al añadir {dependency} a {name}")
                return False
                
            # Añadir dependencia
            if dependency not in self.metadata[name].dependencies:
                self.metadata[name].dependencies.append(dependency)
                
            # Actualizar dependientes
            if dependency in self.metadata:
                if name not in self.metadata[dependency].dependents:
                    self.metadata[dependency].dependents.append(name)
                    
            self._save_metadata()
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir dependencia {dependency} a {name}: {e}")
            return False
            
    def remove_dependency(self,
                         name: str,
                         dependency: str) -> bool:
        """Elimina una dependencia de un elemento existente."""
        try:
            if name not in self.metadata:
                return False
                
            # Eliminar dependencia
            if dependency in self.metadata[name].dependencies:
                self.metadata[name].dependencies.remove(dependency)
                
            # Actualizar dependientes
            if dependency in self.metadata:
                if name in self.metadata[dependency].dependents:
                    self.metadata[dependency].dependents.remove(name)
                    
            self._save_metadata()
            return True
            
        except Exception as e:
            self.logger.error(f"Error al eliminar dependencia {dependency} de {name}: {e}")
            return False
            
    def get_dependencies(self,
                        name: str,
                        recursive: bool = False) -> List[str]:
        """Obtiene las dependencias de un elemento."""
        try:
            if name not in self.metadata:
                return []
                
            if not recursive:
                return self.metadata[name].dependencies
                
            # Obtener dependencias recursivamente
            dependencies = set(self.metadata[name].dependencies)
            for dep in self.metadata[name].dependencies:
                if dep in self.metadata:
                    dependencies.update(self.get_dependencies(dep, True))
                    
            return list(dependencies)
            
        except Exception as e:
            self.logger.error(f"Error al obtener dependencias de {name}: {e}")
            return []
            
    def get_dependents(self,
                      name: str,
                      recursive: bool = False) -> List[str]:
        """Obtiene los elementos que dependen de uno dado."""
        try:
            if name not in self.metadata:
                return []
                
            if not recursive:
                return self.metadata[name].dependents
                
            # Obtener dependientes recursivamente
            dependents = set(self.metadata[name].dependents)
            for dep in self.metadata[name].dependents:
                if dep in self.metadata:
                    dependents.update(self.get_dependents(dep, True))
                    
            return list(dependents)
            
        except Exception as e:
            self.logger.error(f"Error al obtener dependientes de {name}: {e}")
            return []
            
    def validate_dependencies(self,
                            name: str) -> Dict[str, bool]:
        """Valida las dependencias de un elemento."""
        try:
            if name not in self.metadata:
                return {'exists': False}
                
            metadata = self.metadata[name]
            
            # Verificar dependencias
            missing_deps = []
            for dep in metadata.dependencies:
                if dep not in self.metadata:
                    missing_deps.append(dep)
                    
            return {
                'exists': True,
                'has_circular': metadata.is_circular,
                'missing_dependencies': missing_deps,
                'is_valid': not metadata.is_circular and not missing_deps
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar dependencias de {name}: {e}")
            return {'exists': False}
            
    def get_dependency_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de las dependencias."""
        stats = {
            'total_dependencies': len(self.metadata),
            'required_dependencies': 0,
            'optional_dependencies': 0,
            'circular_dependencies': 0,
            'types': {},
            'dependency_counts': {
                '0': 0,
                '1-5': 0,
                '6-10': 0,
                '10+': 0
            }
        }
        
        for metadata in self.metadata.values():
            if metadata.is_required:
                stats['required_dependencies'] += 1
            if metadata.is_optional:
                stats['optional_dependencies'] += 1
            if metadata.is_circular:
                stats['circular_dependencies'] += 1
                
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
                
        return stats 