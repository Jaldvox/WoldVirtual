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
    filename='assets/logs/prefab_manager.log'
)

@dataclass
class PrefabMetadata:
    """Metadatos específicos para prefabs."""
    name: str
    type: str
    version: str
    has_mesh: bool
    has_materials: bool
    has_animations: bool
    has_physics: bool
    has_scripts: bool
    dependencies: List[str]
    parameters: Dict[str, Union[float, int, bool, str]]

class PrefabManager:
    """Gestor de prefabs."""
    
    def __init__(self, base_path: str = "assets/prefabs"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.cache_path = self.base_path / "cache"
        self.logger = logging.getLogger("PrefabManager")
        
        # Crear directorios necesarios
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, PrefabMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, PrefabMetadata]:
        """Carga los metadatos de prefabs desde el archivo JSON."""
        metadata_file = self.metadata_path / "prefabs_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: PrefabMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de prefabs en el archivo JSON."""
        metadata_file = self.metadata_path / "prefabs_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _get_prefab_info(self, file_path: Path) -> Optional[PrefabMetadata]:
        """Obtiene información detallada de un prefab."""
        try:
            # Leer archivo de prefab
            with open(file_path, 'r') as f:
                content = json.load(f)
                
            # Extraer información
            name = content.get('name', file_path.stem)
            prefab_type = content.get('type', 'unknown')
            version = content.get('version', '1.0')
            
            # Verificar características
            has_mesh = 'mesh' in content
            has_materials = 'materials' in content
            has_animations = 'animations' in content
            has_physics = 'physics' in content
            has_scripts = 'scripts' in content
            
            # Obtener dependencias
            dependencies = content.get('dependencies', [])
            
            # Obtener parámetros
            parameters = content.get('parameters', {})
            
            return PrefabMetadata(
                name=name,
                type=prefab_type,
                version=version,
                has_mesh=has_mesh,
                has_materials=has_materials,
                has_animations=has_animations,
                has_physics=has_physics,
                has_scripts=has_scripts,
                dependencies=dependencies,
                parameters=parameters
            )
            
        except Exception as e:
            self.logger.error(f"Error al obtener información del prefab {file_path}: {e}")
            return None
            
    def register_prefab(self, file_path: Union[str, Path]) -> Optional[PrefabMetadata]:
        """Registra un nuevo prefab en el sistema."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.error(f"Prefab no encontrado: {file_path}")
                return None
                
            # Obtener información del prefab
            metadata = self._get_prefab_info(file_path)
            if not metadata:
                return None
                
            # Guardar metadatos
            self.metadata[file_path.stem] = metadata
            self._save_metadata()
            
            self.logger.info(f"Prefab registrado: {file_path}")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al registrar prefab {file_path}: {e}")
            return None
            
    def create_prefab(self,
                     name: str,
                     prefab_type: str,
                     version: str = '1.0',
                     parameters: Optional[Dict] = None) -> Optional[Path]:
        """Crea un nuevo prefab."""
        try:
            # Crear estructura del prefab
            prefab_data = {
                'name': name,
                'type': prefab_type,
                'version': version,
                'parameters': parameters or {},
                'mesh': {},
                'materials': [],
                'animations': [],
                'physics': {},
                'scripts': [],
                'dependencies': []
            }
            
            # Guardar prefab
            output_path = self.cache_path / f"{name}.json"
            with open(output_path, 'w') as f:
                json.dump(prefab_data, f, indent=2)
                
            # Registrar prefab
            self.register_prefab(output_path)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al crear prefab {name}: {e}")
            return None
            
    def add_mesh(self,
                prefab_path: Union[str, Path],
                mesh_path: Union[str, Path]) -> bool:
        """Añade un mesh a un prefab."""
        try:
            prefab_path = Path(prefab_path)
            mesh_path = Path(mesh_path)
            
            if not prefab_path.exists() or not mesh_path.exists():
                return False
                
            # Leer prefab
            with open(prefab_path, 'r') as f:
                prefab_data = json.load(f)
                
            # Añadir mesh
            prefab_data['mesh'] = {
                'path': str(mesh_path),
                'type': mesh_path.suffix[1:]
            }
            
            # Guardar prefab
            with open(prefab_path, 'w') as f:
                json.dump(prefab_data, f, indent=2)
                
            # Actualizar metadatos
            if prefab_path.stem in self.metadata:
                self.metadata[prefab_path.stem].has_mesh = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir mesh a prefab {prefab_path}: {e}")
            return False
            
    def add_material(self,
                    prefab_path: Union[str, Path],
                    material_path: Union[str, Path]) -> bool:
        """Añade un material a un prefab."""
        try:
            prefab_path = Path(prefab_path)
            material_path = Path(material_path)
            
            if not prefab_path.exists() or not material_path.exists():
                return False
                
            # Leer prefab
            with open(prefab_path, 'r') as f:
                prefab_data = json.load(f)
                
            # Añadir material
            material_info = {
                'path': str(material_path),
                'type': material_path.suffix[1:]
            }
            prefab_data['materials'].append(material_info)
            
            # Guardar prefab
            with open(prefab_path, 'w') as f:
                json.dump(prefab_data, f, indent=2)
                
            # Actualizar metadatos
            if prefab_path.stem in self.metadata:
                self.metadata[prefab_path.stem].has_materials = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir material a prefab {prefab_path}: {e}")
            return False
            
    def add_animation(self,
                     prefab_path: Union[str, Path],
                     animation_path: Union[str, Path]) -> bool:
        """Añade una animación a un prefab."""
        try:
            prefab_path = Path(prefab_path)
            animation_path = Path(animation_path)
            
            if not prefab_path.exists() or not animation_path.exists():
                return False
                
            # Leer prefab
            with open(prefab_path, 'r') as f:
                prefab_data = json.load(f)
                
            # Añadir animación
            animation_info = {
                'path': str(animation_path),
                'type': animation_path.suffix[1:]
            }
            prefab_data['animations'].append(animation_info)
            
            # Guardar prefab
            with open(prefab_path, 'w') as f:
                json.dump(prefab_data, f, indent=2)
                
            # Actualizar metadatos
            if prefab_path.stem in self.metadata:
                self.metadata[prefab_path.stem].has_animations = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir animación a prefab {prefab_path}: {e}")
            return False
            
    def add_physics(self,
                   prefab_path: Union[str, Path],
                   physics_data: Dict) -> bool:
        """Añade configuración de física a un prefab."""
        try:
            prefab_path = Path(prefab_path)
            if not prefab_path.exists():
                return False
                
            # Leer prefab
            with open(prefab_path, 'r') as f:
                prefab_data = json.load(f)
                
            # Añadir física
            prefab_data['physics'] = physics_data
            
            # Guardar prefab
            with open(prefab_path, 'w') as f:
                json.dump(prefab_data, f, indent=2)
                
            # Actualizar metadatos
            if prefab_path.stem in self.metadata:
                self.metadata[prefab_path.stem].has_physics = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir física a prefab {prefab_path}: {e}")
            return False
            
    def add_script(self,
                  prefab_path: Union[str, Path],
                  script_path: Union[str, Path]) -> bool:
        """Añade un script a un prefab."""
        try:
            prefab_path = Path(prefab_path)
            script_path = Path(script_path)
            
            if not prefab_path.exists() or not script_path.exists():
                return False
                
            # Leer prefab
            with open(prefab_path, 'r') as f:
                prefab_data = json.load(f)
                
            # Añadir script
            script_info = {
                'path': str(script_path),
                'type': script_path.suffix[1:]
            }
            prefab_data['scripts'].append(script_info)
            
            # Guardar prefab
            with open(prefab_path, 'w') as f:
                json.dump(prefab_data, f, indent=2)
                
            # Actualizar metadatos
            if prefab_path.stem in self.metadata:
                self.metadata[prefab_path.stem].has_scripts = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir script a prefab {prefab_path}: {e}")
            return False
            
    def add_dependency(self,
                      prefab_path: Union[str, Path],
                      dependency_path: Union[str, Path]) -> bool:
        """Añade una dependencia a un prefab."""
        try:
            prefab_path = Path(prefab_path)
            dependency_path = Path(dependency_path)
            
            if not prefab_path.exists() or not dependency_path.exists():
                return False
                
            # Leer prefab
            with open(prefab_path, 'r') as f:
                prefab_data = json.load(f)
                
            # Añadir dependencia
            if str(dependency_path) not in prefab_data['dependencies']:
                prefab_data['dependencies'].append(str(dependency_path))
                
            # Guardar prefab
            with open(prefab_path, 'w') as f:
                json.dump(prefab_data, f, indent=2)
                
            # Actualizar metadatos
            if prefab_path.stem in self.metadata:
                self.metadata[prefab_path.stem].dependencies.append(str(dependency_path))
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir dependencia a prefab {prefab_path}: {e}")
            return False
            
    def set_parameter(self,
                     prefab_path: Union[str, Path],
                     name: str,
                     value: Union[float, int, bool, str]) -> bool:
        """Establece un parámetro en un prefab."""
        try:
            prefab_path = Path(prefab_path)
            if not prefab_path.exists():
                return False
                
            # Leer prefab
            with open(prefab_path, 'r') as f:
                prefab_data = json.load(f)
                
            # Establecer parámetro
            prefab_data['parameters'][name] = value
            
            # Guardar prefab
            with open(prefab_path, 'w') as f:
                json.dump(prefab_data, f, indent=2)
                
            # Actualizar metadatos
            if prefab_path.stem in self.metadata:
                self.metadata[prefab_path.stem].parameters[name] = value
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al establecer parámetro en prefab {prefab_path}: {e}")
            return False
            
    def validate_prefab(self, file_path: Union[str, Path]) -> Dict[str, bool]:
        """Valida la integridad de un prefab."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {'exists': False}
                
            # Leer prefab
            with open(file_path, 'r') as f:
                prefab_data = json.load(f)
                
            # Verificar características
            has_name = 'name' in prefab_data
            has_type = 'type' in prefab_data
            has_version = 'version' in prefab_data
            has_parameters = 'parameters' in prefab_data
            has_dependencies = 'dependencies' in prefab_data
            
            return {
                'exists': True,
                'has_name': has_name,
                'has_type': has_type,
                'has_version': has_version,
                'has_parameters': has_parameters,
                'has_dependencies': has_dependencies,
                'is_valid': all([has_name, has_type, has_version, has_parameters])
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar prefab {file_path}: {e}")
            return {'exists': False}
            
    def get_prefab_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de todos los prefabs registrados."""
        stats = {
            'total_prefabs': len(self.metadata),
            'with_mesh': 0,
            'with_materials': 0,
            'with_animations': 0,
            'with_physics': 0,
            'with_scripts': 0,
            'types': {},
            'versions': {}
        }
        
        for metadata in self.metadata.values():
            if metadata.has_mesh:
                stats['with_mesh'] += 1
            if metadata.has_materials:
                stats['with_materials'] += 1
            if metadata.has_animations:
                stats['with_animations'] += 1
            if metadata.has_physics:
                stats['with_physics'] += 1
            if metadata.has_scripts:
                stats['with_scripts'] += 1
            stats['types'][metadata.type] = stats['types'].get(metadata.type, 0) + 1
            stats['versions'][metadata.version] = stats['versions'].get(metadata.version, 0) + 1
                
        return stats 