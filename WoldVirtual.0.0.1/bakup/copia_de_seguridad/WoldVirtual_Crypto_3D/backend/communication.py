"""Módulo de comunicación centralizado para el backend."""
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import json
import asyncio
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='backend/logs/communication.log'
)

class CommunicationManager:
    """Gestor de comunicación entre componentes del backend."""
    
    def __init__(self):
        self.logger = logging.getLogger("CommunicationManager")
        self.message_queue = asyncio.Queue()
        self.subscribers: Dict[str, list] = {}
        self.message_history: Dict[str, list] = {}
        
    async def publish(self, topic: str, message: Dict[str, Any]) -> bool:
        """Publica un mensaje en un tópico específico."""
        try:
            # Añadir timestamp al mensaje
            message['timestamp'] = datetime.now().isoformat()
            
            # Guardar en historial
            if topic not in self.message_history:
                self.message_history[topic] = []
            self.message_history[topic].append(message)
            
            # Notificar a suscriptores
            if topic in self.subscribers:
                for subscriber in self.subscribers[topic]:
                    await self.message_queue.put({
                        'topic': topic,
                        'message': message,
                        'subscriber': subscriber
                    })
                    
            self.logger.info(f"Mensaje publicado en tópico {topic}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al publicar mensaje: {e}")
            return False
            
    async def subscribe(self, topic: str, callback) -> bool:
        """Suscribe una función callback a un tópico."""
        try:
            if topic not in self.subscribers:
                self.subscribers[topic] = []
            self.subscribers[topic].append(callback)
            self.logger.info(f"Nueva suscripción al tópico {topic}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al suscribir: {e}")
            return False
            
    async def unsubscribe(self, topic: str, callback) -> bool:
        """Cancela la suscripción de una función callback a un tópico."""
        try:
            if topic in self.subscribers and callback in self.subscribers[topic]:
                self.subscribers[topic].remove(callback)
                self.logger.info(f"Suscripción cancelada del tópico {topic}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error al cancelar suscripción: {e}")
            return False
            
    async def get_message_history(self, topic: str, limit: int = 100) -> list:
        """Obtiene el historial de mensajes de un tópico."""
        try:
            if topic in self.message_history:
                return self.message_history[topic][-limit:]
            return []
            
        except Exception as e:
            self.logger.error(f"Error al obtener historial: {e}")
            return []
            
    async def clear_message_history(self, topic: Optional[str] = None):
        """Limpia el historial de mensajes."""
        try:
            if topic:
                if topic in self.message_history:
                    self.message_history[topic] = []
            else:
                self.message_history.clear()
                
            self.logger.info(f"Historial de mensajes limpiado para tópico: {topic}")
            
        except Exception as e:
            self.logger.error(f"Error al limpiar historial: {e}")
            
    async def process_messages(self):
        """Procesa los mensajes en la cola."""
        while True:
            try:
                message_data = await self.message_queue.get()
                topic = message_data['topic']
                message = message_data['message']
                callback = message_data['subscriber']
                
                await callback(topic, message)
                self.message_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"Error al procesar mensaje: {e}")
                
    def get_subscriber_count(self, topic: str) -> int:
        """Obtiene el número de suscriptores de un tópico."""
        return len(self.subscribers.get(topic, []))
        
    def get_topic_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de los tópicos."""
        stats = {
            'total_topics': len(self.subscribers),
            'total_subscribers': sum(len(subs) for subs in self.subscribers.values()),
            'topics': {}
        }
        
        for topic, subscribers in self.subscribers.items():
            stats['topics'][topic] = {
                'subscriber_count': len(subscribers),
                'message_count': len(self.message_history.get(topic, [])),
                'last_message': self.message_history.get(topic, [])[-1] if topic in self.message_history else None
            }
            
        return stats

# Instancia global del gestor de comunicación
communication_manager = CommunicationManager() 