"""Módulo para manejar conexiones entre componentes del backend."""
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import json
import asyncio
from datetime import datetime

from .communication import communication_manager

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='backend/logs/connections.log'
)

class ConnectionManager:
    """Gestor de conexiones entre componentes."""
    
    def __init__(self):
        self.logger = logging.getLogger("ConnectionManager")
        self.connections: Dict[str, Dict[str, Any]] = {}
        self.connection_status: Dict[str, bool] = {}
        
    async def establish_connection(self,
                                source: str,
                                target: str,
                                connection_type: str,
                                metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Establece una conexión entre dos componentes."""
        try:
            connection_id = f"{source}_{target}_{connection_type}"
            
            if connection_id in self.connections:
                self.logger.warning(f"Conexión {connection_id} ya existe")
                return False
                
            self.connections[connection_id] = {
                'source': source,
                'target': target,
                'type': connection_type,
                'metadata': metadata or {},
                'created_at': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat(),
                'status': 'active'
            }
            
            self.connection_status[connection_id] = True
            
            # Notificar sobre la nueva conexión
            await communication_manager.publish(
                'connections',
                {
                    'event': 'connection_established',
                    'connection_id': connection_id,
                    'source': source,
                    'target': target,
                    'type': connection_type
                }
            )
            
            self.logger.info(f"Conexión establecida: {connection_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al establecer conexión: {e}")
            return False
            
    async def close_connection(self, connection_id: str) -> bool:
        """Cierra una conexión existente."""
        try:
            if connection_id not in self.connections:
                self.logger.warning(f"Conexión {connection_id} no existe")
                return False
                
            connection = self.connections[connection_id]
            connection['status'] = 'closed'
            connection['closed_at'] = datetime.now().isoformat()
            
            self.connection_status[connection_id] = False
            
            # Notificar sobre el cierre de la conexión
            await communication_manager.publish(
                'connections',
                {
                    'event': 'connection_closed',
                    'connection_id': connection_id,
                    'source': connection['source'],
                    'target': connection['target'],
                    'type': connection['type']
                }
            )
            
            self.logger.info(f"Conexión cerrada: {connection_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al cerrar conexión: {e}")
            return False
            
    def get_connection(self, connection_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene información de una conexión específica."""
        return self.connections.get(connection_id)
        
    def get_connections_by_component(self, component: str) -> Dict[str, Dict[str, Any]]:
        """Obtiene todas las conexiones de un componente."""
        return {
            conn_id: conn for conn_id, conn in self.connections.items()
            if conn['source'] == component or conn['target'] == component
        }
        
    def get_active_connections(self) -> Dict[str, Dict[str, Any]]:
        """Obtiene todas las conexiones activas."""
        return {
            conn_id: conn for conn_id, conn in self.connections.items()
            if conn['status'] == 'active'
        }
        
    async def update_connection_activity(self, connection_id: str) -> bool:
        """Actualiza la última actividad de una conexión."""
        try:
            if connection_id not in self.connections:
                return False
                
            self.connections[connection_id]['last_activity'] = datetime.now().isoformat()
            return True
            
        except Exception as e:
            self.logger.error(f"Error al actualizar actividad: {e}")
            return False
            
    def get_connection_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de las conexiones."""
        stats = {
            'total_connections': len(self.connections),
            'active_connections': len(self.get_active_connections()),
            'connection_types': {},
            'components': {}
        }
        
        for conn in self.connections.values():
            # Estadísticas por tipo
            conn_type = conn['type']
            if conn_type not in stats['connection_types']:
                stats['connection_types'][conn_type] = 0
            stats['connection_types'][conn_type] += 1
            
            # Estadísticas por componente
            for component in [conn['source'], conn['target']]:
                if component not in stats['components']:
                    stats['components'][component] = {
                        'total': 0,
                        'active': 0
                    }
                stats['components'][component]['total'] += 1
                if conn['status'] == 'active':
                    stats['components'][component]['active'] += 1
                    
        return stats

# Instancia global del gestor de conexiones
connection_manager = ConnectionManager() 