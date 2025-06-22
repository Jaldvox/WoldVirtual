import os
import json
import logging
import logging.handlers
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/log_manager.log'
)

@dataclass
class LogMetadata:
    """Metadatos específicos para logs."""
    name: str
    type: str
    level: str
    created: str
    last_modified: str
    size: int
    line_count: int
    error_count: int
    warning_count: int
    info_count: int
    debug_count: int

class LogManager:
    """Gestor de logs."""
    
    def __init__(self, base_path: str = "assets/logs"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.logger = logging.getLogger("LogManager")
        
        # Crear directorios necesarios
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, LogMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, LogMetadata]:
        """Carga los metadatos de logs desde el archivo JSON."""
        metadata_file = self.metadata_path / "logs_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: LogMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de logs en el archivo JSON."""
        metadata_file = self.metadata_path / "logs_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _get_log_info(self, file_path: Path) -> Optional[LogMetadata]:
        """Obtiene información detallada de un archivo de log."""
        try:
            if not file_path.exists():
                return None
                
            # Obtener información básica
            name = file_path.stem
            log_type = name.split('_')[0] if '_' in name else 'general'
            size = file_path.stat().st_size
            created = datetime.fromtimestamp(file_path.stat().st_ctime).isoformat()
            last_modified = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            
            # Contar líneas y niveles
            line_count = 0
            error_count = 0
            warning_count = 0
            info_count = 0
            debug_count = 0
            
            with open(file_path, 'r') as f:
                for line in f:
                    line_count += 1
                    if 'ERROR' in line:
                        error_count += 1
                    elif 'WARNING' in line:
                        warning_count += 1
                    elif 'INFO' in line:
                        info_count += 1
                    elif 'DEBUG' in line:
                        debug_count += 1
                        
            # Determinar nivel principal
            if error_count > 0:
                level = 'ERROR'
            elif warning_count > 0:
                level = 'WARNING'
            elif info_count > 0:
                level = 'INFO'
            else:
                level = 'DEBUG'
                
            return LogMetadata(
                name=name,
                type=log_type,
                level=level,
                created=created,
                last_modified=last_modified,
                size=size,
                line_count=line_count,
                error_count=error_count,
                warning_count=warning_count,
                info_count=info_count,
                debug_count=debug_count
            )
            
        except Exception as e:
            self.logger.error(f"Error al obtener información de log {file_path}: {e}")
            return None
            
    def create_logger(self,
                     name: str,
                     log_type: str = 'general',
                     level: str = 'INFO',
                     max_size: int = 1024 * 1024,  # 1MB
                     backup_count: int = 5) -> Optional[logging.Logger]:
        """Crea un nuevo logger."""
        try:
            # Crear logger
            logger = logging.getLogger(name)
            logger.setLevel(getattr(logging, level.upper()))
            
            # Crear manejador de archivo
            log_file = self.base_path / f"{log_type}_{name}.log"
            handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=max_size,
                backupCount=backup_count
            )
            
            # Configurar formato
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            
            # Añadir manejador
            logger.addHandler(handler)
            
            # Registrar metadatos
            metadata = LogMetadata(
                name=name,
                type=log_type,
                level=level,
                created=datetime.now().isoformat(),
                last_modified=datetime.now().isoformat(),
                size=0,
                line_count=0,
                error_count=0,
                warning_count=0,
                info_count=0,
                debug_count=0
            )
            self.metadata[name] = metadata
            self._save_metadata()
            
            return logger
            
        except Exception as e:
            self.logger.error(f"Error al crear logger {name}: {e}")
            return None
            
    def get_logger(self, name: str) -> Optional[logging.Logger]:
        """Obtiene un logger existente."""
        try:
            if name not in self.metadata:
                return None
                
            return logging.getLogger(name)
            
        except Exception as e:
            self.logger.error(f"Error al obtener logger {name}: {e}")
            return None
            
    def update_log_metadata(self, name: str) -> bool:
        """Actualiza los metadatos de un log."""
        try:
            if name not in self.metadata:
                return False
                
            # Buscar archivo de log
            log_type = self.metadata[name].type
            log_file = self.base_path / f"{log_type}_{name}.log"
            
            # Actualizar metadatos
            metadata = self._get_log_info(log_file)
            if metadata:
                self.metadata[name] = metadata
                self._save_metadata()
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"Error al actualizar metadatos de log {name}: {e}")
            return False
            
    def rotate_logs(self, name: str) -> bool:
        """Rota los archivos de log."""
        try:
            if name not in self.metadata:
                return False
                
            # Buscar archivo de log
            log_type = self.metadata[name].type
            log_file = self.base_path / f"{log_type}_{name}.log"
            
            # Rotar log
            logger = logging.getLogger(name)
            for handler in logger.handlers:
                if isinstance(handler, logging.handlers.RotatingFileHandler):
                    handler.doRollover()
                    
            # Actualizar metadatos
            self.update_log_metadata(name)
            return True
            
        except Exception as e:
            self.logger.error(f"Error al rotar logs de {name}: {e}")
            return False
            
    def clear_logs(self, name: str) -> bool:
        """Limpia los archivos de log."""
        try:
            if name not in self.metadata:
                return False
                
            # Buscar archivo de log
            log_type = self.metadata[name].type
            log_file = self.base_path / f"{log_type}_{name}.log"
            
            # Limpiar log
            with open(log_file, 'w') as f:
                f.write('')
                
            # Actualizar metadatos
            self.update_log_metadata(name)
            return True
            
        except Exception as e:
            self.logger.error(f"Error al limpiar logs de {name}: {e}")
            return False
            
    def get_log_content(self,
                       name: str,
                       lines: int = 100,
                       level: Optional[str] = None) -> List[str]:
        """Obtiene el contenido de un log."""
        try:
            if name not in self.metadata:
                return []
                
            # Buscar archivo de log
            log_type = self.metadata[name].type
            log_file = self.base_path / f"{log_type}_{name}.log"
            
            if not log_file.exists():
                return []
                
            # Leer líneas
            content = []
            with open(log_file, 'r') as f:
                for line in f:
                    if level is None or level.upper() in line:
                        content.append(line.strip())
                        if len(content) >= lines:
                            break
                            
            return content
            
        except Exception as e:
            self.logger.error(f"Error al obtener contenido de log {name}: {e}")
            return []
            
    def get_log_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de los logs."""
        stats = {
            'total_logs': len(self.metadata),
            'total_size': 0,
            'total_lines': 0,
            'total_errors': 0,
            'total_warnings': 0,
            'total_info': 0,
            'total_debug': 0,
            'types': {},
            'levels': {
                'ERROR': 0,
                'WARNING': 0,
                'INFO': 0,
                'DEBUG': 0
            }
        }
        
        for metadata in self.metadata.values():
            stats['total_size'] += metadata.size
            stats['total_lines'] += metadata.line_count
            stats['total_errors'] += metadata.error_count
            stats['total_warnings'] += metadata.warning_count
            stats['total_info'] += metadata.info_count
            stats['total_debug'] += metadata.debug_count
            
            stats['types'][metadata.type] = stats['types'].get(metadata.type, 0) + 1
            stats['levels'][metadata.level] = stats['levels'].get(metadata.level, 0) + 1
            
        return stats 