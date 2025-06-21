import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/settings_manager.log'
)

@dataclass
class SettingMetadata:
    """Metadatos específicos para configuraciones."""
    name: str
    type: str
    created: str
    last_modified: str
    version: str
    is_default: bool
    is_custom: bool
    is_system: bool
    category: str
    value: Any
    default_value: Any
    description: str
    constraints: Dict[str, Any]

class SettingsManager:
    """Gestor de configuraciones."""
    
    def __init__(self, base_path: str = "assets/settings"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.data_path = self.base_path / "data"
        self.logger = logging.getLogger("SettingsManager")
        
        # Crear directorios necesarios
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, SettingMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, SettingMetadata]:
        """Carga los metadatos de configuraciones desde el archivo JSON."""
        metadata_file = self.metadata_path / "settings_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: SettingMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de configuraciones en el archivo JSON."""
        metadata_file = self.metadata_path / "settings_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _validate_value(self,
                       value: Any,
                       constraints: Dict[str, Any]) -> bool:
        """Valida un valor según las restricciones."""
        try:
            # Verificar tipo
            if 'type' in constraints:
                if not isinstance(value, eval(constraints['type'])):
                    return False
                    
            # Verificar rango
            if 'min' in constraints and value < constraints['min']:
                return False
            if 'max' in constraints and value > constraints['max']:
                return False
                
            # Verificar opciones
            if 'options' in constraints and value not in constraints['options']:
                return False
                
            # Verificar patrón
            if 'pattern' in constraints:
                import re
                if not re.match(constraints['pattern'], str(value)):
                    return False
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Error al validar valor: {e}")
            return False
            
    def create_setting(self,
                      name: str,
                      setting_type: str,
                      value: Any,
                      category: str,
                      description: str,
                      constraints: Optional[Dict[str, Any]] = None,
                      is_default: bool = False,
                      is_custom: bool = False,
                      is_system: bool = False) -> Optional[SettingMetadata]:
        """Crea una nueva configuración."""
        try:
            # Validar valor
            if constraints and not self._validate_value(value, constraints):
                self.logger.error(f"Valor inválido para configuración {name}")
                return None
                
            # Crear metadatos
            now = datetime.now().isoformat()
            metadata = SettingMetadata(
                name=name,
                type=setting_type,
                created=now,
                last_modified=now,
                version='1.0',
                is_default=is_default,
                is_custom=is_custom,
                is_system=is_system,
                category=category,
                value=value,
                default_value=value,
                description=description,
                constraints=constraints or {}
            )
            
            # Guardar metadatos
            self.metadata[name] = metadata
            self._save_metadata()
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al crear configuración {name}: {e}")
            return None
            
    def get_setting(self,
                   name: str,
                   default: Optional[Any] = None) -> Optional[Any]:
        """Obtiene el valor de una configuración."""
        try:
            if name not in self.metadata:
                return default
                
            return self.metadata[name].value
            
        except Exception as e:
            self.logger.error(f"Error al obtener configuración {name}: {e}")
            return default
            
    def set_setting(self,
                   name: str,
                   value: Any) -> bool:
        """Establece el valor de una configuración."""
        try:
            if name not in self.metadata:
                return False
                
            # Validar valor
            if not self._validate_value(value, self.metadata[name].constraints):
                self.logger.error(f"Valor inválido para configuración {name}")
                return False
                
            # Actualizar metadatos
            metadata = self.metadata[name]
            metadata.value = value
            metadata.last_modified = datetime.now().isoformat()
            self._save_metadata()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error al establecer configuración {name}: {e}")
            return False
            
    def reset_setting(self, name: str) -> bool:
        """Restablece una configuración a su valor por defecto."""
        try:
            if name not in self.metadata:
                return False
                
            # Restablecer valor
            metadata = self.metadata[name]
            metadata.value = metadata.default_value
            metadata.last_modified = datetime.now().isoformat()
            self._save_metadata()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error al restablecer configuración {name}: {e}")
            return False
            
    def delete_setting(self, name: str) -> bool:
        """Elimina una configuración."""
        try:
            if name not in self.metadata:
                return False
                
            # Verificar si es una configuración del sistema
            if self.metadata[name].is_system:
                self.logger.error(f"No se puede eliminar la configuración del sistema {name}")
                return False
                
            # Eliminar metadatos
            del self.metadata[name]
            self._save_metadata()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error al eliminar configuración {name}: {e}")
            return False
            
    def get_settings_by_category(self, category: str) -> List[SettingMetadata]:
        """Obtiene todas las configuraciones de una categoría."""
        try:
            return [
                metadata for metadata in self.metadata.values()
                if metadata.category == category
            ]
            
        except Exception as e:
            self.logger.error(f"Error al obtener configuraciones de categoría {category}: {e}")
            return []
            
    def get_default_settings(self) -> List[SettingMetadata]:
        """Obtiene todas las configuraciones por defecto."""
        try:
            return [
                metadata for metadata in self.metadata.values()
                if metadata.is_default
            ]
            
        except Exception as e:
            self.logger.error(f"Error al obtener configuraciones por defecto: {e}")
            return []
            
    def get_custom_settings(self) -> List[SettingMetadata]:
        """Obtiene todas las configuraciones personalizadas."""
        try:
            return [
                metadata for metadata in self.metadata.values()
                if metadata.is_custom
            ]
            
        except Exception as e:
            self.logger.error(f"Error al obtener configuraciones personalizadas: {e}")
            return []
            
    def get_system_settings(self) -> List[SettingMetadata]:
        """Obtiene todas las configuraciones del sistema."""
        try:
            return [
                metadata for metadata in self.metadata.values()
                if metadata.is_system
            ]
            
        except Exception as e:
            self.logger.error(f"Error al obtener configuraciones del sistema: {e}")
            return []
            
    def validate_setting(self, name: str) -> Dict[str, bool]:
        """Valida una configuración."""
        try:
            if name not in self.metadata:
                return {'exists': False}
                
            metadata = self.metadata[name]
            
            return {
                'exists': True,
                'has_value': metadata.value is not None,
                'has_default': metadata.default_value is not None,
                'has_description': bool(metadata.description),
                'has_constraints': bool(metadata.constraints),
                'is_valid': self._validate_value(metadata.value, metadata.constraints)
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar configuración {name}: {e}")
            return {'exists': False}
            
    def get_settings_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de las configuraciones."""
        stats = {
            'total_settings': len(self.metadata),
            'default_settings': 0,
            'custom_settings': 0,
            'system_settings': 0,
            'categories': {},
            'types': {},
            'constraint_counts': {
                '0': 0,
                '1-2': 0,
                '3-5': 0,
                '5+': 0
            }
        }
        
        for metadata in self.metadata.values():
            if metadata.is_default:
                stats['default_settings'] += 1
            if metadata.is_custom:
                stats['custom_settings'] += 1
            if metadata.is_system:
                stats['system_settings'] += 1
                
            stats['categories'][metadata.category] = stats['categories'].get(metadata.category, 0) + 1
            stats['types'][metadata.type] = stats['types'].get(metadata.type, 0) + 1
            
            # Clasificar por número de restricciones
            constraint_count = len(metadata.constraints)
            if constraint_count == 0:
                stats['constraint_counts']['0'] += 1
            elif constraint_count <= 2:
                stats['constraint_counts']['1-2'] += 1
            elif constraint_count <= 5:
                stats['constraint_counts']['3-5'] += 1
            else:
                stats['constraint_counts']['5+'] += 1
                
        return stats 