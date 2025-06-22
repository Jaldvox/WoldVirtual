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
    filename='assets/logs/state_manager.log'
)

@dataclass
class StateMetadata:
    """Metadatos específicos para estados."""
    name: str
    type: str
    created: str
    last_modified: str
    version: str
    is_persistent: bool
    is_volatile: bool
    is_shared: bool
    dependencies: List[str]
    parameters: Dict[str, Any]

class StateManager:
    """Gestor de estados."""
    
    def __init__(self, base_path: str = "assets/states"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.data_path = self.base_path / "data"
        self.logger = logging.getLogger("StateManager")
        
        # Crear directorios necesarios
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, StateMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, StateMetadata]:
        """Carga los metadatos de estados desde el archivo JSON."""
        metadata_file = self.metadata_path / "states_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: StateMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de estados en el archivo JSON."""
        metadata_file = self.metadata_path / "states_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def create_state(self,
                    name: str,
                    state_type: str,
                    version: str = '1.0',
                    is_persistent: bool = True,
                    is_volatile: bool = False,
                    is_shared: bool = False,
                    dependencies: Optional[List[str]] = None,
                    parameters: Optional[Dict[str, Any]] = None) -> Optional[StateMetadata]:
        """Crea un nuevo estado."""
        try:
            # Crear metadatos
            now = datetime.now().isoformat()
            metadata = StateMetadata(
                name=name,
                type=state_type,
                created=now,
                last_modified=now,
                version=version,
                is_persistent=is_persistent,
                is_volatile=is_volatile,
                is_shared=is_shared,
                dependencies=dependencies or [],
                parameters=parameters or {}
            )
            
            # Guardar metadatos
            self.metadata[name] = metadata
            self._save_metadata()
            
            # Crear archivo de estado
            if is_persistent:
                state_file = self.data_path / f"{name}.json"
                with open(state_file, 'w') as f:
                    json.dump({}, f, indent=2)
                    
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al crear estado {name}: {e}")
            return None
            
    def get_state(self,
                 name: str,
                 default: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Obtiene el valor de un estado."""
        try:
            if name not in self.metadata:
                return default
                
            metadata = self.metadata[name]
            
            # Si es volátil, devolver parámetros
            if metadata.is_volatile:
                return metadata.parameters
                
            # Leer archivo de estado
            state_file = self.data_path / f"{name}.json"
            if state_file.exists():
                with open(state_file, 'r') as f:
                    return json.load(f)
                    
            return default
            
        except Exception as e:
            self.logger.error(f"Error al obtener estado {name}: {e}")
            return default
            
    def set_state(self,
                 name: str,
                 value: Dict[str, Any]) -> bool:
        """Establece el valor de un estado."""
        try:
            if name not in self.metadata:
                return False
                
            metadata = self.metadata[name]
            
            # Actualizar metadatos
            metadata.last_modified = datetime.now().isoformat()
            if metadata.is_volatile:
                metadata.parameters = value
            else:
                # Guardar en archivo
                state_file = self.data_path / f"{name}.json"
                with open(state_file, 'w') as f:
                    json.dump(value, f, indent=2)
                    
            self._save_metadata()
            return True
            
        except Exception as e:
            self.logger.error(f"Error al establecer estado {name}: {e}")
            return False
            
    def update_state(self,
                    name: str,
                    value: Dict[str, Any]) -> bool:
        """Actualiza el valor de un estado."""
        try:
            if name not in self.metadata:
                return False
                
            # Obtener estado actual
            current_state = self.get_state(name, {})
            if current_state is None:
                return False
                
            # Actualizar estado
            current_state.update(value)
            return self.set_state(name, current_state)
            
        except Exception as e:
            self.logger.error(f"Error al actualizar estado {name}: {e}")
            return False
            
    def delete_state(self, name: str) -> bool:
        """Elimina un estado."""
        try:
            if name not in self.metadata:
                return False
                
            metadata = self.metadata[name]
            
            # Eliminar archivo de estado
            if metadata.is_persistent:
                state_file = self.data_path / f"{name}.json"
                if state_file.exists():
                    state_file.unlink()
                    
            # Eliminar metadatos
            del self.metadata[name]
            self._save_metadata()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error al eliminar estado {name}: {e}")
            return False
            
    def get_states_by_type(self, state_type: str) -> List[StateMetadata]:
        """Obtiene todos los estados de un tipo específico."""
        try:
            return [
                metadata for metadata in self.metadata.values()
                if metadata.type == state_type
            ]
            
        except Exception as e:
            self.logger.error(f"Error al obtener estados de tipo {state_type}: {e}")
            return []
            
    def get_persistent_states(self) -> List[StateMetadata]:
        """Obtiene todos los estados persistentes."""
        try:
            return [
                metadata for metadata in self.metadata.values()
                if metadata.is_persistent
            ]
            
        except Exception as e:
            self.logger.error(f"Error al obtener estados persistentes: {e}")
            return []
            
    def get_volatile_states(self) -> List[StateMetadata]:
        """Obtiene todos los estados volátiles."""
        try:
            return [
                metadata for metadata in self.metadata.values()
                if metadata.is_volatile
            ]
            
        except Exception as e:
            self.logger.error(f"Error al obtener estados volátiles: {e}")
            return []
            
    def get_shared_states(self) -> List[StateMetadata]:
        """Obtiene todos los estados compartidos."""
        try:
            return [
                metadata for metadata in self.metadata.values()
                if metadata.is_shared
            ]
            
        except Exception as e:
            self.logger.error(f"Error al obtener estados compartidos: {e}")
            return []
            
    def validate_state(self, name: str) -> Dict[str, bool]:
        """Valida un estado."""
        try:
            if name not in self.metadata:
                return {'exists': False}
                
            metadata = self.metadata[name]
            
            # Verificar archivo de estado
            has_file = False
            if metadata.is_persistent:
                state_file = self.data_path / f"{name}.json"
                has_file = state_file.exists()
                
            return {
                'exists': True,
                'has_file': has_file,
                'is_persistent': metadata.is_persistent,
                'is_volatile': metadata.is_volatile,
                'is_shared': metadata.is_shared,
                'has_dependencies': bool(metadata.dependencies),
                'has_parameters': bool(metadata.parameters)
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar estado {name}: {e}")
            return {'exists': False}
            
    def get_state_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de los estados."""
        stats = {
            'total_states': len(self.metadata),
            'persistent_states': 0,
            'volatile_states': 0,
            'shared_states': 0,
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
            if metadata.is_persistent:
                stats['persistent_states'] += 1
            if metadata.is_volatile:
                stats['volatile_states'] += 1
            if metadata.is_shared:
                stats['shared_states'] += 1
                
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