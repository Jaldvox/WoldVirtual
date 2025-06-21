import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Callable
from dataclasses import dataclass
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/event_manager.log'
)

@dataclass
class EventMetadata:
    """Metadatos específicos para eventos."""
    name: str
    type: str
    created: str
    last_triggered: str
    trigger_count: int
    handlers: List[str]
    is_async: bool
    is_broadcast: bool
    parameters: Dict[str, Any]

class EventManager:
    """Gestor de eventos."""
    
    def __init__(self, base_path: str = "assets/events"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.logger = logging.getLogger("EventManager")
        
        # Crear directorios necesarios
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, EventMetadata] = self._load_metadata()
        
        # Registro de manejadores
        self.handlers: Dict[str, List[Callable]] = {}
        
    def _load_metadata(self) -> Dict[str, EventMetadata]:
        """Carga los metadatos de eventos desde el archivo JSON."""
        metadata_file = self.metadata_path / "events_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: EventMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de eventos en el archivo JSON."""
        metadata_file = self.metadata_path / "events_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def register_event(self,
                      name: str,
                      event_type: str,
                      is_async: bool = False,
                      is_broadcast: bool = False,
                      parameters: Optional[Dict[str, Any]] = None) -> Optional[EventMetadata]:
        """Registra un nuevo evento."""
        try:
            # Crear metadatos
            now = datetime.now().isoformat()
            metadata = EventMetadata(
                name=name,
                type=event_type,
                created=now,
                last_triggered=now,
                trigger_count=0,
                handlers=[],
                is_async=is_async,
                is_broadcast=is_broadcast,
                parameters=parameters or {}
            )
            
            # Guardar metadatos
            self.metadata[name] = metadata
            self._save_metadata()
            
            # Inicializar lista de manejadores
            self.handlers[name] = []
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al registrar evento {name}: {e}")
            return None
            
    def add_handler(self,
                   event_name: str,
                   handler: Callable,
                   handler_name: Optional[str] = None) -> bool:
        """Añade un manejador a un evento."""
        try:
            if event_name not in self.metadata:
                return False
                
            # Obtener nombre del manejador
            if handler_name is None:
                handler_name = handler.__name__
                
            # Añadir manejador
            if handler_name not in self.metadata[event_name].handlers:
                self.metadata[event_name].handlers.append(handler_name)
                self.handlers[event_name].append(handler)
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al añadir manejador a evento {event_name}: {e}")
            return False
            
    def remove_handler(self,
                      event_name: str,
                      handler_name: str) -> bool:
        """Elimina un manejador de un evento."""
        try:
            if event_name not in self.metadata:
                return False
                
            # Buscar manejador
            if handler_name in self.metadata[event_name].handlers:
                index = self.metadata[event_name].handlers.index(handler_name)
                self.metadata[event_name].handlers.pop(index)
                self.handlers[event_name].pop(index)
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al eliminar manejador de evento {event_name}: {e}")
            return False
            
    def trigger_event(self,
                     event_name: str,
                     **kwargs) -> bool:
        """Dispara un evento."""
        try:
            if event_name not in self.metadata:
                return False
                
            # Actualizar metadatos
            metadata = self.metadata[event_name]
            metadata.last_triggered = datetime.now().isoformat()
            metadata.trigger_count += 1
            self._save_metadata()
            
            # Ejecutar manejadores
            for handler in self.handlers[event_name]:
                try:
                    if metadata.is_async:
                        # Ejecutar de forma asíncrona
                        import asyncio
                        asyncio.create_task(handler(**kwargs))
                    else:
                        # Ejecutar de forma síncrona
                        handler(**kwargs)
                except Exception as e:
                    self.logger.error(f"Error al ejecutar manejador de evento {event_name}: {e}")
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Error al disparar evento {event_name}: {e}")
            return False
            
    def get_event(self, event_name: str) -> Optional[EventMetadata]:
        """Obtiene un evento específico."""
        try:
            return self.metadata.get(event_name)
            
        except Exception as e:
            self.logger.error(f"Error al obtener evento {event_name}: {e}")
            return None
            
    def get_events_by_type(self, event_type: str) -> List[EventMetadata]:
        """Obtiene todos los eventos de un tipo específico."""
        try:
            return [
                metadata for metadata in self.metadata.values()
                if metadata.type == event_type
            ]
            
        except Exception as e:
            self.logger.error(f"Error al obtener eventos de tipo {event_type}: {e}")
            return []
            
    def get_async_events(self) -> List[EventMetadata]:
        """Obtiene todos los eventos asíncronos."""
        try:
            return [
                metadata for metadata in self.metadata.values()
                if metadata.is_async
            ]
            
        except Exception as e:
            self.logger.error(f"Error al obtener eventos asíncronos: {e}")
            return []
            
    def get_broadcast_events(self) -> List[EventMetadata]:
        """Obtiene todos los eventos de broadcast."""
        try:
            return [
                metadata for metadata in self.metadata.values()
                if metadata.is_broadcast
            ]
            
        except Exception as e:
            self.logger.error(f"Error al obtener eventos de broadcast: {e}")
            return []
            
    def validate_event(self, event_name: str) -> Dict[str, bool]:
        """Valida un evento."""
        try:
            if event_name not in self.metadata:
                return {'exists': False}
                
            metadata = self.metadata[event_name]
            
            return {
                'exists': True,
                'has_handlers': bool(metadata.handlers),
                'has_parameters': bool(metadata.parameters),
                'is_async': metadata.is_async,
                'is_broadcast': metadata.is_broadcast
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar evento {event_name}: {e}")
            return {'exists': False}
            
    def get_event_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de los eventos."""
        stats = {
            'total_events': len(self.metadata),
            'async_events': 0,
            'broadcast_events': 0,
            'types': {},
            'handler_counts': {
                '0': 0,
                '1-5': 0,
                '6-10': 0,
                '10+': 0
            },
            'trigger_counts': {
                '0': 0,
                '1-10': 0,
                '11-50': 0,
                '50+': 0
            }
        }
        
        for metadata in self.metadata.values():
            if metadata.is_async:
                stats['async_events'] += 1
            if metadata.is_broadcast:
                stats['broadcast_events'] += 1
                
            stats['types'][metadata.type] = stats['types'].get(metadata.type, 0) + 1
            
            # Clasificar por número de manejadores
            handler_count = len(metadata.handlers)
            if handler_count == 0:
                stats['handler_counts']['0'] += 1
            elif handler_count <= 5:
                stats['handler_counts']['1-5'] += 1
            elif handler_count <= 10:
                stats['handler_counts']['6-10'] += 1
            else:
                stats['handler_counts']['10+'] += 1
                
            # Clasificar por número de disparos
            trigger_count = metadata.trigger_count
            if trigger_count == 0:
                stats['trigger_counts']['0'] += 1
            elif trigger_count <= 10:
                stats['trigger_counts']['1-10'] += 1
            elif trigger_count <= 50:
                stats['trigger_counts']['11-50'] += 1
            else:
                stats['trigger_counts']['50+'] += 1
                
        return stats 