import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
import numpy as np
from PIL import Image
import cv2
from dataclasses import dataclass

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/texture_manager.log'
)

@dataclass
class TextureMetadata:
    """Metadatos específicos para texturas."""
    width: int
    height: int
    channels: int
    format: str
    mipmaps: bool
    compression: Optional[str]
    color_space: str
    has_alpha: bool

class TextureManager:
    """Gestor de texturas."""
    
    def __init__(self, base_path: str = "assets/textures"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.cache_path = self.base_path / "cache"
        self.logger = logging.getLogger("TextureManager")
        
        # Crear directorios necesarios
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, TextureMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, TextureMetadata]:
        """Carga los metadatos de texturas desde el archivo JSON."""
        metadata_file = self.metadata_path / "textures_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: TextureMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de texturas en el archivo JSON."""
        metadata_file = self.metadata_path / "textures_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _get_texture_info(self, file_path: Path) -> Optional[TextureMetadata]:
        """Obtiene información detallada de una textura."""
        try:
            # Cargar imagen
            image = Image.open(file_path)
            
            # Obtener información básica
            width, height = image.size
            channels = len(image.getbands())
            format = image.format.lower()
            
            # Verificar canal alfa
            has_alpha = 'A' in image.getbands()
            
            # Determinar espacio de color
            if image.mode == 'RGB':
                color_space = 'RGB'
            elif image.mode == 'RGBA':
                color_space = 'RGBA'
            elif image.mode == 'L':
                color_space = 'GRAY'
            else:
                color_space = image.mode
                
            return TextureMetadata(
                width=width,
                height=height,
                channels=channels,
                format=format,
                mipmaps=False,  # Se generarán después si es necesario
                compression=None,  # Se aplicará después si es necesario
                color_space=color_space,
                has_alpha=has_alpha
            )
            
        except Exception as e:
            self.logger.error(f"Error al obtener información de la textura {file_path}: {e}")
            return None
            
    def register_texture(self, file_path: Union[str, Path]) -> Optional[TextureMetadata]:
        """Registra una nueva textura en el sistema."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.error(f"Textura no encontrada: {file_path}")
                return None
                
            # Obtener información de la textura
            metadata = self._get_texture_info(file_path)
            if not metadata:
                return None
                
            # Guardar metadatos
            self.metadata[file_path.stem] = metadata
            self._save_metadata()
            
            self.logger.info(f"Textura registrada: {file_path}")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al registrar textura {file_path}: {e}")
            return None
            
    def generate_mipmaps(self, file_path: Union[str, Path], levels: int = 4) -> bool:
        """Genera mipmaps para una textura."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return False
                
            # Cargar imagen
            image = Image.open(file_path)
            
            # Crear directorio para mipmaps
            mipmap_dir = self.cache_path / f"{file_path.stem}_mipmaps"
            mipmap_dir.mkdir(exist_ok=True)
            
            # Generar mipmaps
            current_image = image
            for i in range(levels):
                # Redimensionar
                width = current_image.width // 2
                height = current_image.height // 2
                if width < 1 or height < 1:
                    break
                    
                current_image = current_image.resize((width, height), Image.LANCZOS)
                
                # Guardar mipmap
                output_path = mipmap_dir / f"mipmap_{i}{file_path.suffix}"
                current_image.save(output_path)
                
            # Actualizar metadatos
            if file_path.stem in self.metadata:
                self.metadata[file_path.stem].mipmaps = True
                self._save_metadata()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error al generar mipmaps para {file_path}: {e}")
            return False
            
    def compress_texture(self, 
                        file_path: Union[str, Path],
                        quality: int = 85,
                        format: str = 'jpg') -> Optional[Path]:
        """Comprime una textura."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
                
            # Cargar imagen
            image = Image.open(file_path)
            
            # Convertir a RGB si es necesario
            if image.mode in ['RGBA', 'LA']:
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
                
            # Guardar imagen comprimida
            output_path = self.cache_path / f"{file_path.stem}_compressed.{format}"
            image.save(output_path, quality=quality, optimize=True)
            
            # Actualizar metadatos
            if file_path.stem in self.metadata:
                self.metadata[file_path.stem].compression = format
                self._save_metadata()
                
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al comprimir textura {file_path}: {e}")
            return None
            
    def resize_texture(self, 
                      file_path: Union[str, Path],
                      max_size: int = 2048,
                      maintain_aspect: bool = True) -> Optional[Path]:
        """Redimensiona una textura manteniendo la proporción."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
                
            # Cargar imagen
            image = Image.open(file_path)
            
            # Calcular nuevas dimensiones
            if maintain_aspect:
                ratio = min(max_size / image.width, max_size / image.height)
                new_size = (int(image.width * ratio), int(image.height * ratio))
            else:
                new_size = (max_size, max_size)
                
            # Redimensionar
            resized = image.resize(new_size, Image.LANCZOS)
            
            # Guardar imagen redimensionada
            output_path = self.cache_path / f"{file_path.stem}_resized{file_path.suffix}"
            resized.save(output_path)
            
            # Actualizar metadatos
            if file_path.stem in self.metadata:
                self.metadata[file_path.stem].width = new_size[0]
                self.metadata[file_path.stem].height = new_size[1]
                self._save_metadata()
                
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al redimensionar textura {file_path}: {e}")
            return None
            
    def convert_format(self, 
                      file_path: Union[str, Path],
                      target_format: str,
                      quality: int = 85) -> Optional[Path]:
        """Convierte una textura a otro formato."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
                
            # Cargar imagen
            image = Image.open(file_path)
            
            # Guardar en nuevo formato
            output_path = self.cache_path / f"{file_path.stem}.{target_format}"
            image.save(output_path, format=target_format.upper(), quality=quality)
            
            # Actualizar metadatos
            if file_path.stem in self.metadata:
                self.metadata[file_path.stem].format = target_format
                self._save_metadata()
                
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al convertir textura {file_path}: {e}")
            return None
            
    def validate_texture(self, file_path: Union[str, Path]) -> Dict[str, bool]:
        """Valida la integridad de una textura."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {'exists': False}
                
            # Cargar imagen
            image = Image.open(file_path)
            
            # Verificar dimensiones
            width, height = image.size
            is_power_of_two = (width & (width - 1) == 0) and (height & (height - 1) == 0)
            
            return {
                'exists': True,
                'is_valid': True,
                'is_power_of_two': is_power_of_two,
                'has_alpha': 'A' in image.getbands(),
                'is_square': width == height
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar textura {file_path}: {e}")
            return {'exists': False}
            
    def get_texture_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de todas las texturas registradas."""
        stats = {
            'total_textures': len(self.metadata),
            'total_pixels': 0,
            'formats': {},
            'color_spaces': {},
            'with_alpha': 0,
            'with_mipmaps': 0,
            'compressed': 0
        }
        
        for metadata in self.metadata.values():
            stats['total_pixels'] += metadata.width * metadata.height
            stats['formats'][metadata.format] = stats['formats'].get(metadata.format, 0) + 1
            stats['color_spaces'][metadata.color_space] = stats['color_spaces'].get(metadata.color_space, 0) + 1
            if metadata.has_alpha:
                stats['with_alpha'] += 1
            if metadata.mipmaps:
                stats['with_mipmaps'] += 1
            if metadata.compression:
                stats['compressed'] += 1
                
        return stats 