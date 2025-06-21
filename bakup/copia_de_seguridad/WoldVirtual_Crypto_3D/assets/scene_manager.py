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
    filename='assets/logs/scene_manager.log'
)

@dataclass
class SceneMetadata:
    """Metadatos específicos para escenas."""
    name: str
    version: str
    has_environment: bool
    has_lighting: bool
    has_physics: bool
    has_audio: bool
    has_scripts: bool
    objects: List[str]
    dependencies: List[str]
    parameters: Dict[str, Union[float, int, bool, str]]

class SceneManager:
    """Gestor de escenas."""
    
    def __init__(self, base_path: str = "assets/scenes"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.cache_path = self.base_path / "cache"
        self.logger = logging.getLogger("SceneManager")
        
        # Crear directorios necesarios
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, SceneMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, SceneMetadata]:
        """Carga los metadatos de escenas desde el archivo JSON."""
        metadata_file = self.metadata_path / "scenes_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: SceneMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de escenas en el archivo JSON."""
        metadata_file = self.metadata_path / "scenes_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _get_scene_info(self, file_path: Path) -> Optional[SceneMetadata]:
        """Obtiene información detallada de una escena."""
        try:
            # Leer archivo de escena
            with open(file_path, 'r') as f:
                content = json.load(f)
                
            # Extraer información
            name = content.get('name', file_path.stem)
            version = content.get('version', '1.0')
            
            # Verificar características
            has_environment = 'environment' in content
            has_lighting = 'lighting' in content
            has_physics = 'physics' in content
            has_audio = 'audio' in content
            has_scripts = 'scripts' in content
            
            # Obtener objetos y dependencias
            objects = content.get('objects', [])
            dependencies = content.get('dependencies', [])
            
            # Obtener parámetros
            parameters = content.get('parameters', {})
            
            return SceneMetadata(
                name=name,
                version=version,
                has_environment=has_environment,
                has_lighting=has_lighting,
                has_physics=has_physics,
                has_audio=has_audio,
                has_scripts=has_scripts,
                objects=objects,
                dependencies=dependencies,
                parameters=parameters
            )
            
        except Exception as e:
            self.logger.error(f"Error al obtener información de la escena {file_path}: {e}")
            return None
            
    def register_scene(self, file_path: Union[str, Path]) -> Optional[SceneMetadata]:
        """Registra una nueva escena en el sistema."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.error(f"Escena no encontrada: {file_path}")
                return None
                
            # Obtener información de la escena
            metadata = self._get_scene_info(file_path)
            if not metadata:
                return None
                
            # Guardar metadatos
            self.metadata[file_path.stem] = metadata
            self._save_metadata()
            
            self.logger.info(f"Escena registrada: {file_path}")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al registrar escena {file_path}: {e}")
            return None
            
    def create_scene(self,
                    name: str,
                    version: str = '1.0',
                    parameters: Optional[Dict] = None) -> Optional[Path]:
        """Crea una nueva escena."""
        try:
            # Crear estructura de la escena
            scene_data = {
                'name': name,
                'version': version,
                'parameters': parameters or {},
                'environment': {},
                'lighting': {},
                'physics': {},
                'audio': {},
                'scripts': [],
                'objects': [],
                'dependencies': []
            }
            
            # Guardar escena
            output_path = self.cache_path / f"{name}.json"
            with open(output_path, 'w') as f:
                json.dump(scene_data, f, indent=2)
                
            # Registrar escena
            self.register_scene(output_path)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al crear escena {name}: {e}")
            return None
            
    def add_environment(self,
                       scene_path: Union[str, Path],
                       environment_data: Dict) -> bool:
        """Añade configuración de ambiente a una escena."""
        try:
            scene_path = Path(scene_path)
            if not scene_path.exists():
                return False
                
            # Leer escena
            with open(scene_path, 'r') as f:
                scene_data = json.load(f)
                
            # Añadir ambiente
            scene_data['environment'] = environment_data
            
            # Guardar escena
            with open(scene_path, 'w') as f:
                json.dump(scene_data, f, indent=2)
                
            # Actualizar metadatos
            if scene_path.stem in self.metadata:
                self.metadata[scene_path.stem].has_environment = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir ambiente a escena {scene_path}: {e}")
            return False
            
    def add_lighting(self,
                    scene_path: Union[str, Path],
                    lighting_data: Dict) -> bool:
        """Añade configuración de iluminación a una escena."""
        try:
            scene_path = Path(scene_path)
            if not scene_path.exists():
                return False
                
            # Leer escena
            with open(scene_path, 'r') as f:
                scene_data = json.load(f)
                
            # Añadir iluminación
            scene_data['lighting'] = lighting_data
            
            # Guardar escena
            with open(scene_path, 'w') as f:
                json.dump(scene_data, f, indent=2)
                
            # Actualizar metadatos
            if scene_path.stem in self.metadata:
                self.metadata[scene_path.stem].has_lighting = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir iluminación a escena {scene_path}: {e}")
            return False
            
    def add_physics(self,
                   scene_path: Union[str, Path],
                   physics_data: Dict) -> bool:
        """Añade configuración de física a una escena."""
        try:
            scene_path = Path(scene_path)
            if not scene_path.exists():
                return False
                
            # Leer escena
            with open(scene_path, 'r') as f:
                scene_data = json.load(f)
                
            # Añadir física
            scene_data['physics'] = physics_data
            
            # Guardar escena
            with open(scene_path, 'w') as f:
                json.dump(scene_data, f, indent=2)
                
            # Actualizar metadatos
            if scene_path.stem in self.metadata:
                self.metadata[scene_path.stem].has_physics = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir física a escena {scene_path}: {e}")
            return False
            
    def add_audio(self,
                 scene_path: Union[str, Path],
                 audio_data: Dict) -> bool:
        """Añade configuración de audio a una escena."""
        try:
            scene_path = Path(scene_path)
            if not scene_path.exists():
                return False
                
            # Leer escena
            with open(scene_path, 'r') as f:
                scene_data = json.load(f)
                
            # Añadir audio
            scene_data['audio'] = audio_data
            
            # Guardar escena
            with open(scene_path, 'w') as f:
                json.dump(scene_data, f, indent=2)
                
            # Actualizar metadatos
            if scene_path.stem in self.metadata:
                self.metadata[scene_path.stem].has_audio = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir audio a escena {scene_path}: {e}")
            return False
            
    def add_script(self,
                  scene_path: Union[str, Path],
                  script_path: Union[str, Path]) -> bool:
        """Añade un script a una escena."""
        try:
            scene_path = Path(scene_path)
            script_path = Path(script_path)
            
            if not scene_path.exists() or not script_path.exists():
                return False
                
            # Leer escena
            with open(scene_path, 'r') as f:
                scene_data = json.load(f)
                
            # Añadir script
            script_info = {
                'path': str(script_path),
                'type': script_path.suffix[1:]
            }
            scene_data['scripts'].append(script_info)
            
            # Guardar escena
            with open(scene_path, 'w') as f:
                json.dump(scene_data, f, indent=2)
                
            # Actualizar metadatos
            if scene_path.stem in self.metadata:
                self.metadata[scene_path.stem].has_scripts = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir script a escena {scene_path}: {e}")
            return False
            
    def add_object(self,
                  scene_path: Union[str, Path],
                  object_path: Union[str, Path],
                  transform: Optional[Dict] = None) -> bool:
        """Añade un objeto a una escena."""
        try:
            scene_path = Path(scene_path)
            object_path = Path(object_path)
            
            if not scene_path.exists() or not object_path.exists():
                return False
                
            # Leer escena
            with open(scene_path, 'r') as f:
                scene_data = json.load(f)
                
            # Añadir objeto
            object_info = {
                'path': str(object_path),
                'type': object_path.suffix[1:],
                'transform': transform or {
                    'position': [0, 0, 0],
                    'rotation': [0, 0, 0],
                    'scale': [1, 1, 1]
                }
            }
            scene_data['objects'].append(object_info)
            
            # Guardar escena
            with open(scene_path, 'w') as f:
                json.dump(scene_data, f, indent=2)
                
            # Actualizar metadatos
            if scene_path.stem in self.metadata:
                self.metadata[scene_path.stem].objects.append(str(object_path))
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir objeto a escena {scene_path}: {e}")
            return False
            
    def add_dependency(self,
                      scene_path: Union[str, Path],
                      dependency_path: Union[str, Path]) -> bool:
        """Añade una dependencia a una escena."""
        try:
            scene_path = Path(scene_path)
            dependency_path = Path(dependency_path)
            
            if not scene_path.exists() or not dependency_path.exists():
                return False
                
            # Leer escena
            with open(scene_path, 'r') as f:
                scene_data = json.load(f)
                
            # Añadir dependencia
            if str(dependency_path) not in scene_data['dependencies']:
                scene_data['dependencies'].append(str(dependency_path))
                
            # Guardar escena
            with open(scene_path, 'w') as f:
                json.dump(scene_data, f, indent=2)
                
            # Actualizar metadatos
            if scene_path.stem in self.metadata:
                self.metadata[scene_path.stem].dependencies.append(str(dependency_path))
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir dependencia a escena {scene_path}: {e}")
            return False
            
    def set_parameter(self,
                     scene_path: Union[str, Path],
                     name: str,
                     value: Union[float, int, bool, str]) -> bool:
        """Establece un parámetro en una escena."""
        try:
            scene_path = Path(scene_path)
            if not scene_path.exists():
                return False
                
            # Leer escena
            with open(scene_path, 'r') as f:
                scene_data = json.load(f)
                
            # Establecer parámetro
            scene_data['parameters'][name] = value
            
            # Guardar escena
            with open(scene_path, 'w') as f:
                json.dump(scene_data, f, indent=2)
                
            # Actualizar metadatos
            if scene_path.stem in self.metadata:
                self.metadata[scene_path.stem].parameters[name] = value
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al establecer parámetro en escena {scene_path}: {e}")
            return False
            
    def validate_scene(self, file_path: Union[str, Path]) -> Dict[str, bool]:
        """Valida la integridad de una escena."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {'exists': False}
                
            # Leer escena
            with open(file_path, 'r') as f:
                scene_data = json.load(f)
                
            # Verificar características
            has_name = 'name' in scene_data
            has_version = 'version' in scene_data
            has_parameters = 'parameters' in scene_data
            has_objects = 'objects' in scene_data
            has_dependencies = 'dependencies' in scene_data
            
            return {
                'exists': True,
                'has_name': has_name,
                'has_version': has_version,
                'has_parameters': has_parameters,
                'has_objects': has_objects,
                'has_dependencies': has_dependencies,
                'is_valid': all([has_name, has_version, has_parameters])
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar escena {file_path}: {e}")
            return {'exists': False}
            
    def get_scene_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de todas las escenas registradas."""
        stats = {
            'total_scenes': len(self.metadata),
            'with_environment': 0,
            'with_lighting': 0,
            'with_physics': 0,
            'with_audio': 0,
            'with_scripts': 0,
            'total_objects': 0,
            'versions': {}
        }
        
        for metadata in self.metadata.values():
            if metadata.has_environment:
                stats['with_environment'] += 1
            if metadata.has_lighting:
                stats['with_lighting'] += 1
            if metadata.has_physics:
                stats['with_physics'] += 1
            if metadata.has_audio:
                stats['with_audio'] += 1
            if metadata.has_scripts:
                stats['with_scripts'] += 1
            stats['total_objects'] += len(metadata.objects)
            stats['versions'][metadata.version] = stats['versions'].get(metadata.version, 0) + 1
                
        return stats 