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
    filename='assets/logs/config_manager.log'
)

@dataclass
class ConfigMetadata:
    """Metadatos específicos para configuraciones."""
    name: str
    type: str
    version: str
    has_graphics: bool
    has_audio: bool
    has_input: bool
    has_network: bool
    has_physics: bool
    has_ui: bool
    parameters: Dict[str, Union[float, int, bool, str]]

class ConfigManager:
    """Gestor de configuraciones."""
    
    def __init__(self, base_path: str = "assets/configs"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.cache_path = self.base_path / "cache"
        self.logger = logging.getLogger("ConfigManager")
        
        # Crear directorios necesarios
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, ConfigMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, ConfigMetadata]:
        """Carga los metadatos de configuraciones desde el archivo JSON."""
        metadata_file = self.metadata_path / "configs_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: ConfigMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de configuraciones en el archivo JSON."""
        metadata_file = self.metadata_path / "configs_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _get_config_info(self, file_path: Path) -> Optional[ConfigMetadata]:
        """Obtiene información detallada de una configuración."""
        try:
            # Leer archivo de configuración
            with open(file_path, 'r') as f:
                content = json.load(f)
                
            # Extraer información
            name = content.get('name', file_path.stem)
            config_type = content.get('type', 'unknown')
            version = content.get('version', '1.0')
            
            # Verificar características
            has_graphics = 'graphics' in content
            has_audio = 'audio' in content
            has_input = 'input' in content
            has_network = 'network' in content
            has_physics = 'physics' in content
            has_ui = 'ui' in content
            
            # Obtener parámetros
            parameters = content.get('parameters', {})
            
            return ConfigMetadata(
                name=name,
                type=config_type,
                version=version,
                has_graphics=has_graphics,
                has_audio=has_audio,
                has_input=has_input,
                has_network=has_network,
                has_physics=has_physics,
                has_ui=has_ui,
                parameters=parameters
            )
            
        except Exception as e:
            self.logger.error(f"Error al obtener información de la configuración {file_path}: {e}")
            return None
            
    def register_config(self, file_path: Union[str, Path]) -> Optional[ConfigMetadata]:
        """Registra una nueva configuración en el sistema."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.error(f"Configuración no encontrada: {file_path}")
                return None
                
            # Obtener información de la configuración
            metadata = self._get_config_info(file_path)
            if not metadata:
                return None
                
            # Guardar metadatos
            self.metadata[file_path.stem] = metadata
            self._save_metadata()
            
            self.logger.info(f"Configuración registrada: {file_path}")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al registrar configuración {file_path}: {e}")
            return None
            
    def create_config(self,
                     name: str,
                     config_type: str,
                     version: str = '1.0',
                     parameters: Optional[Dict] = None) -> Optional[Path]:
        """Crea una nueva configuración."""
        try:
            # Crear estructura de la configuración
            config_data = {
                'name': name,
                'type': config_type,
                'version': version,
                'parameters': parameters or {},
                'graphics': {},
                'audio': {},
                'input': {},
                'network': {},
                'physics': {},
                'ui': {}
            }
            
            # Guardar configuración
            output_path = self.cache_path / f"{name}.json"
            with open(output_path, 'w') as f:
                json.dump(config_data, f, indent=2)
                
            # Registrar configuración
            self.register_config(output_path)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al crear configuración {name}: {e}")
            return None
            
    def add_graphics_config(self,
                          config_path: Union[str, Path],
                          graphics_data: Dict) -> bool:
        """Añade configuración de gráficos."""
        try:
            config_path = Path(config_path)
            if not config_path.exists():
                return False
                
            # Leer configuración
            with open(config_path, 'r') as f:
                config_data = json.load(f)
                
            # Añadir configuración de gráficos
            config_data['graphics'] = graphics_data
            
            # Guardar configuración
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
                
            # Actualizar metadatos
            if config_path.stem in self.metadata:
                self.metadata[config_path.stem].has_graphics = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir configuración de gráficos a {config_path}: {e}")
            return False
            
    def add_audio_config(self,
                        config_path: Union[str, Path],
                        audio_data: Dict) -> bool:
        """Añade configuración de audio."""
        try:
            config_path = Path(config_path)
            if not config_path.exists():
                return False
                
            # Leer configuración
            with open(config_path, 'r') as f:
                config_data = json.load(f)
                
            # Añadir configuración de audio
            config_data['audio'] = audio_data
            
            # Guardar configuración
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
                
            # Actualizar metadatos
            if config_path.stem in self.metadata:
                self.metadata[config_path.stem].has_audio = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir configuración de audio a {config_path}: {e}")
            return False
            
    def add_input_config(self,
                        config_path: Union[str, Path],
                        input_data: Dict) -> bool:
        """Añade configuración de entrada."""
        try:
            config_path = Path(config_path)
            if not config_path.exists():
                return False
                
            # Leer configuración
            with open(config_path, 'r') as f:
                config_data = json.load(f)
                
            # Añadir configuración de entrada
            config_data['input'] = input_data
            
            # Guardar configuración
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
                
            # Actualizar metadatos
            if config_path.stem in self.metadata:
                self.metadata[config_path.stem].has_input = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir configuración de entrada a {config_path}: {e}")
            return False
            
    def add_network_config(self,
                          config_path: Union[str, Path],
                          network_data: Dict) -> bool:
        """Añade configuración de red."""
        try:
            config_path = Path(config_path)
            if not config_path.exists():
                return False
                
            # Leer configuración
            with open(config_path, 'r') as f:
                config_data = json.load(f)
                
            # Añadir configuración de red
            config_data['network'] = network_data
            
            # Guardar configuración
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
                
            # Actualizar metadatos
            if config_path.stem in self.metadata:
                self.metadata[config_path.stem].has_network = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir configuración de red a {config_path}: {e}")
            return False
            
    def add_physics_config(self,
                          config_path: Union[str, Path],
                          physics_data: Dict) -> bool:
        """Añade configuración de física."""
        try:
            config_path = Path(config_path)
            if not config_path.exists():
                return False
                
            # Leer configuración
            with open(config_path, 'r') as f:
                config_data = json.load(f)
                
            # Añadir configuración de física
            config_data['physics'] = physics_data
            
            # Guardar configuración
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
                
            # Actualizar metadatos
            if config_path.stem in self.metadata:
                self.metadata[config_path.stem].has_physics = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir configuración de física a {config_path}: {e}")
            return False
            
    def add_ui_config(self,
                     config_path: Union[str, Path],
                     ui_data: Dict) -> bool:
        """Añade configuración de interfaz de usuario."""
        try:
            config_path = Path(config_path)
            if not config_path.exists():
                return False
                
            # Leer configuración
            with open(config_path, 'r') as f:
                config_data = json.load(f)
                
            # Añadir configuración de UI
            config_data['ui'] = ui_data
            
            # Guardar configuración
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
                
            # Actualizar metadatos
            if config_path.stem in self.metadata:
                self.metadata[config_path.stem].has_ui = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir configuración de UI a {config_path}: {e}")
            return False
            
    def set_parameter(self,
                     config_path: Union[str, Path],
                     name: str,
                     value: Union[float, int, bool, str]) -> bool:
        """Establece un parámetro en una configuración."""
        try:
            config_path = Path(config_path)
            if not config_path.exists():
                return False
                
            # Leer configuración
            with open(config_path, 'r') as f:
                config_data = json.load(f)
                
            # Establecer parámetro
            config_data['parameters'][name] = value
            
            # Guardar configuración
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
                
            # Actualizar metadatos
            if config_path.stem in self.metadata:
                self.metadata[config_path.stem].parameters[name] = value
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al establecer parámetro en configuración {config_path}: {e}")
            return False
            
    def validate_config(self, file_path: Union[str, Path]) -> Dict[str, bool]:
        """Valida la integridad de una configuración."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {'exists': False}
                
            # Leer configuración
            with open(file_path, 'r') as f:
                config_data = json.load(f)
                
            # Verificar características
            has_name = 'name' in config_data
            has_type = 'type' in config_data
            has_version = 'version' in config_data
            has_parameters = 'parameters' in config_data
            
            return {
                'exists': True,
                'has_name': has_name,
                'has_type': has_type,
                'has_version': has_version,
                'has_parameters': has_parameters,
                'is_valid': all([has_name, has_type, has_version, has_parameters])
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar configuración {file_path}: {e}")
            return {'exists': False}
            
    def get_config_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de todas las configuraciones registradas."""
        stats = {
            'total_configs': len(self.metadata),
            'with_graphics': 0,
            'with_audio': 0,
            'with_input': 0,
            'with_network': 0,
            'with_physics': 0,
            'with_ui': 0,
            'types': {},
            'versions': {}
        }
        
        for metadata in self.metadata.values():
            if metadata.has_graphics:
                stats['with_graphics'] += 1
            if metadata.has_audio:
                stats['with_audio'] += 1
            if metadata.has_input:
                stats['with_input'] += 1
            if metadata.has_network:
                stats['with_network'] += 1
            if metadata.has_physics:
                stats['with_physics'] += 1
            if metadata.has_ui:
                stats['with_ui'] += 1
            stats['types'][metadata.type] = stats['types'].get(metadata.type, 0) + 1
            stats['versions'][metadata.version] = stats['versions'].get(metadata.version, 0) + 1
                
        return stats 