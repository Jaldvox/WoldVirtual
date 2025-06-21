"""Módulo para manejar eventos del sistema."""
import logging
from typing import Dict, Any, Optional, Callable
from pathlib import Path
import json
import asyncio
from datetime import datetime

from .communication import communication_manager
from .connections import connection_manager

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='backend/logs/events.log'
)

class EventManager:
    """Gestor de eventos del sistema."""
    
    def __init__(self):
        self.logger = logging.getLogger("EventManager")
        self.event_handlers: Dict[str, list] = {}
        self.event_history: Dict[str, list] = {}
        
    async def register_event_handler(self,
                                   event_type: str,
                                   handler: Callable) -> bool:
        """Registra un manejador para un tipo de evento."""
        try:
            if event_type not in self.event_handlers:
                self.event_handlers[event_type] = []
                
            if handler not in self.event_handlers[event_type]:
                self.event_handlers[event_type].append(handler)
                self.logger.info(f"Manejador registrado para evento {event_type}")
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"Error al registrar manejador: {e}")
            return False
            
    async def unregister_event_handler(self,
                                     event_type: str,
                                     handler: Callable) -> bool:
        """Elimina un manejador de eventos."""
        try:
            if event_type in self.event_handlers and handler in self.event_handlers[event_type]:
                self.event_handlers[event_type].remove(handler)
                self.logger.info(f"Manejador eliminado para evento {event_type}")
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"Error al eliminar manejador: {e}")
            return False
            
    async def trigger_event(self,
                          event_type: str,
                          event_data: Dict[str, Any]) -> bool:
        """Dispara un evento del sistema."""
        try:
            # Añadir metadatos al evento
            event = {
                'type': event_type,
                'data': event_data,
                'timestamp': datetime.now().isoformat()
            }
            
            # Guardar en historial
            if event_type not in self.event_history:
                self.event_history[event_type] = []
            self.event_history[event_type].append(event)
            
            # Notificar a los manejadores
            if event_type in self.event_handlers:
                for handler in self.event_handlers[event_type]:
                    try:
                        await handler(event)
                    except Exception as e:
                        self.logger.error(f"Error en manejador de evento {event_type}: {e}")
                        
            # Publicar evento en el sistema de comunicación
            await communication_manager.publish(
                'system_events',
                {
                    'event_type': event_type,
                    'event_data': event_data,
                    'timestamp': event['timestamp']
                }
            )
            
            self.logger.info(f"Evento disparado: {event_type}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al disparar evento: {e}")
            return False
            
    def get_event_history(self,
                         event_type: Optional[str] = None,
                         limit: int = 100) -> Dict[str, list]:
        """Obtiene el historial de eventos."""
        try:
            if event_type:
                if event_type in self.event_history:
                    return {event_type: self.event_history[event_type][-limit:]}
                return {event_type: []}
                
            return {
                event_type: events[-limit:]
                for event_type, events in self.event_history.items()
            }
            
        except Exception as e:
            self.logger.error(f"Error al obtener historial de eventos: {e}")
            return {}
            
    async def clear_event_history(self, event_type: Optional[str] = None):
        """Limpia el historial de eventos."""
        try:
            if event_type:
                if event_type in self.event_history:
                    self.event_history[event_type] = []
            else:
                self.event_history.clear()
                
            self.logger.info(f"Historial de eventos limpiado para tipo: {event_type}")
            
        except Exception as e:
            self.logger.error(f"Error al limpiar historial de eventos: {e}")
            
    def get_event_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de eventos."""
        stats = {
            'total_events': sum(len(events) for events in self.event_history.values()),
            'event_types': len(self.event_history),
            'handlers': {
                event_type: len(handlers)
                for event_type, handlers in self.event_handlers.items()
            },
            'events_by_type': {
                event_type: len(events)
                for event_type, events in self.event_history.items()
            }
        }
        
        return stats

# Instancia global del gestor de eventos
event_manager = EventManager()

# Registro de eventos del sistema
async def register_system_events():
    """Registra los eventos del sistema."""
    # Eventos de conexión
    await event_manager.register_event_handler(
        'connection_established',
        lambda event: connection_manager.update_connection_activity(
            event['data']['connection_id']
        )
    )
    
    await event_manager.register_event_handler(
        'connection_closed',
        lambda event: connection_manager.update_connection_activity(
            event['data']['connection_id']
        )
    )
    
    # Eventos de comunicación
    await event_manager.register_event_handler(
        'message_published',
        lambda event: communication_manager.get_message_history(
            event['data']['topic']
        )
    )
    
    # Eventos de error
    await event_manager.register_event_handler(
        'error_occurred',
        lambda event: logging.error(
            f"Error en {event['data']['component']}: {event['data']['message']}"
        )
    ) 