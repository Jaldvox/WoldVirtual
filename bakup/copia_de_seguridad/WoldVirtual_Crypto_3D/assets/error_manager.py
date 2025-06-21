import os
import json
import logging
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/error_manager.log'
)

@dataclass
class ErrorMetadata:
    """Metadatos específicos para errores."""
    code: str
    type: str
    message: str
    created: str
    last_occurred: str
    occurrence_count: int
    severity: str
    stack_trace: str
    context: Dict[str, Any]
    is_resolved: bool
    resolution: Optional[str]

class ErrorManager:
    """Gestor de errores."""
    
    def __init__(self, base_path: str = "assets/errors"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.logger = logging.getLogger("ErrorManager")
        
        # Crear directorios necesarios
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, ErrorMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, ErrorMetadata]:
        """Carga los metadatos de errores desde el archivo JSON."""
        metadata_file = self.metadata_path / "errors_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: ErrorMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de errores en el archivo JSON."""
        metadata_file = self.metadata_path / "errors_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _generate_error_code(self, error_type: str) -> str:
        """Genera un código único para el error."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"{error_type.upper()}_{timestamp}"
        
    def register_error(self,
                      error_type: str,
                      message: str,
                      severity: str = 'ERROR',
                      context: Optional[Dict[str, Any]] = None,
                      stack_trace: Optional[str] = None) -> Optional[ErrorMetadata]:
        """Registra un nuevo error."""
        try:
            # Generar código de error
            error_code = self._generate_error_code(error_type)
            
            # Obtener stack trace si no se proporciona
            if stack_trace is None:
                stack_trace = ''.join(traceback.format_stack())
                
            # Crear metadatos
            now = datetime.now().isoformat()
            metadata = ErrorMetadata(
                code=error_code,
                type=error_type,
                message=message,
                created=now,
                last_occurred=now,
                occurrence_count=1,
                severity=severity,
                stack_trace=stack_trace,
                context=context or {},
                is_resolved=False,
                resolution=None
            )
            
            # Guardar metadatos
            self.metadata[error_code] = metadata
            self._save_metadata()
            
            # Registrar en log
            self.logger.error(
                f"Error registrado: {error_code} - {message}",
                extra={'error_code': error_code, 'context': context}
            )
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al registrar error: {e}")
            return None
            
    def update_error(self,
                    error_code: str,
                    message: Optional[str] = None,
                    severity: Optional[str] = None,
                    context: Optional[Dict[str, Any]] = None,
                    stack_trace: Optional[str] = None) -> bool:
        """Actualiza un error existente."""
        try:
            if error_code not in self.metadata:
                return False
                
            # Actualizar metadatos
            metadata = self.metadata[error_code]
            metadata.last_occurred = datetime.now().isoformat()
            metadata.occurrence_count += 1
            
            if message:
                metadata.message = message
            if severity:
                metadata.severity = severity
            if context:
                metadata.context.update(context)
            if stack_trace:
                metadata.stack_trace = stack_trace
                
            self._save_metadata()
            
            # Registrar en log
            self.logger.error(
                f"Error actualizado: {error_code} - {metadata.message}",
                extra={'error_code': error_code, 'context': metadata.context}
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error al actualizar error {error_code}: {e}")
            return False
            
    def resolve_error(self,
                     error_code: str,
                     resolution: str) -> bool:
        """Marca un error como resuelto."""
        try:
            if error_code not in self.metadata:
                return False
                
            # Actualizar metadatos
            metadata = self.metadata[error_code]
            metadata.is_resolved = True
            metadata.resolution = resolution
            
            self._save_metadata()
            
            # Registrar en log
            self.logger.info(
                f"Error resuelto: {error_code} - {resolution}",
                extra={'error_code': error_code}
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error al resolver error {error_code}: {e}")
            return False
            
    def get_error(self, error_code: str) -> Optional[ErrorMetadata]:
        """Obtiene un error específico."""
        try:
            return self.metadata.get(error_code)
            
        except Exception as e:
            self.logger.error(f"Error al obtener error {error_code}: {e}")
            return None
            
    def get_errors_by_type(self,
                          error_type: str,
                          include_resolved: bool = False) -> List[ErrorMetadata]:
        """Obtiene todos los errores de un tipo específico."""
        try:
            errors = []
            for metadata in self.metadata.values():
                if metadata.type == error_type:
                    if not include_resolved and metadata.is_resolved:
                        continue
                    errors.append(metadata)
            return errors
            
        except Exception as e:
            self.logger.error(f"Error al obtener errores de tipo {error_type}: {e}")
            return []
            
    def get_errors_by_severity(self,
                             severity: str,
                             include_resolved: bool = False) -> List[ErrorMetadata]:
        """Obtiene todos los errores de una severidad específica."""
        try:
            errors = []
            for metadata in self.metadata.values():
                if metadata.severity == severity:
                    if not include_resolved and metadata.is_resolved:
                        continue
                    errors.append(metadata)
            return errors
            
        except Exception as e:
            self.logger.error(f"Error al obtener errores de severidad {severity}: {e}")
            return []
            
    def get_unresolved_errors(self) -> List[ErrorMetadata]:
        """Obtiene todos los errores no resueltos."""
        try:
            return [
                metadata for metadata in self.metadata.values()
                if not metadata.is_resolved
            ]
            
        except Exception as e:
            self.logger.error(f"Error al obtener errores no resueltos: {e}")
            return []
            
    def validate_error(self, error_code: str) -> Dict[str, bool]:
        """Valida un error."""
        try:
            if error_code not in self.metadata:
                return {'exists': False}
                
            metadata = self.metadata[error_code]
            
            return {
                'exists': True,
                'has_message': bool(metadata.message),
                'has_stack_trace': bool(metadata.stack_trace),
                'has_context': bool(metadata.context),
                'is_resolved': metadata.is_resolved,
                'has_resolution': bool(metadata.resolution) if metadata.is_resolved else True
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar error {error_code}: {e}")
            return {'exists': False}
            
    def get_error_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de los errores."""
        stats = {
            'total_errors': len(self.metadata),
            'resolved_errors': 0,
            'unresolved_errors': 0,
            'types': {},
            'severities': {
                'CRITICAL': 0,
                'ERROR': 0,
                'WARNING': 0,
                'INFO': 0
            },
            'occurrence_counts': {
                '1': 0,
                '2-5': 0,
                '6-10': 0,
                '10+': 0
            }
        }
        
        for metadata in self.metadata.values():
            if metadata.is_resolved:
                stats['resolved_errors'] += 1
            else:
                stats['unresolved_errors'] += 1
                
            stats['types'][metadata.type] = stats['types'].get(metadata.type, 0) + 1
            stats['severities'][metadata.severity] = stats['severities'].get(metadata.severity, 0) + 1
            
            # Clasificar por número de ocurrencias
            count = metadata.occurrence_count
            if count == 1:
                stats['occurrence_counts']['1'] += 1
            elif count <= 5:
                stats['occurrence_counts']['2-5'] += 1
            elif count <= 10:
                stats['occurrence_counts']['6-10'] += 1
            else:
                stats['occurrence_counts']['10+'] += 1
                
        return stats 