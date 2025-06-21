import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
import numpy as np
import soundfile as sf
import librosa
from dataclasses import dataclass

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/audio_manager.log'
)

@dataclass
class AudioMetadata:
    """Metadatos específicos para archivos de audio."""
    duration: float
    sample_rate: int
    channels: int
    format: str
    bit_depth: int
    bitrate: int
    is_compressed: bool
    has_metadata: bool

class AudioManager:
    """Gestor de archivos de audio."""
    
    def __init__(self, base_path: str = "assets/audio"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.cache_path = self.base_path / "cache"
        self.logger = logging.getLogger("AudioManager")
        
        # Crear directorios necesarios
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, AudioMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, AudioMetadata]:
        """Carga los metadatos de audio desde el archivo JSON."""
        metadata_file = self.metadata_path / "audio_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: AudioMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de audio en el archivo JSON."""
        metadata_file = self.metadata_path / "audio_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _get_audio_info(self, file_path: Path) -> Optional[AudioMetadata]:
        """Obtiene información detallada de un archivo de audio."""
        try:
            # Cargar audio
            audio, sample_rate = librosa.load(file_path, sr=None)
            
            # Obtener información del archivo
            info = sf.info(file_path)
            
            # Determinar si está comprimido
            is_compressed = file_path.suffix.lower() in ['.mp3', '.ogg', '.m4a']
            
            # Calcular bitrate
            bitrate = int(os.path.getsize(file_path) * 8 / info.duration)
            
            return AudioMetadata(
                duration=info.duration,
                sample_rate=sample_rate,
                channels=info.channels,
                format=file_path.suffix[1:],
                bit_depth=info.subtype,
                bitrate=bitrate,
                is_compressed=is_compressed,
                has_metadata=bool(librosa.get_duration(path=file_path))
            )
            
        except Exception as e:
            self.logger.error(f"Error al obtener información del audio {file_path}: {e}")
            return None
            
    def register_audio(self, file_path: Union[str, Path]) -> Optional[AudioMetadata]:
        """Registra un nuevo archivo de audio en el sistema."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.error(f"Audio no encontrado: {file_path}")
                return None
                
            # Obtener información del audio
            metadata = self._get_audio_info(file_path)
            if not metadata:
                return None
                
            # Guardar metadatos
            self.metadata[file_path.stem] = metadata
            self._save_metadata()
            
            self.logger.info(f"Audio registrado: {file_path}")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al registrar audio {file_path}: {e}")
            return None
            
    def convert_format(self, 
                      file_path: Union[str, Path],
                      target_format: str,
                      sample_rate: Optional[int] = None,
                      channels: Optional[int] = None) -> Optional[Path]:
        """Convierte un archivo de audio a otro formato."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
                
            # Cargar audio
            audio, sr = librosa.load(file_path, sr=sample_rate)
            
            # Reducir canales si es necesario
            if channels and audio.ndim > 1 and audio.shape[1] != channels:
                if channels == 1:
                    audio = librosa.to_mono(audio.T)
                else:
                    audio = librosa.resample(audio, orig_sr=sr, target_sr=sr)
                    
            # Guardar en nuevo formato
            output_path = self.cache_path / f"{file_path.stem}.{target_format}"
            sf.write(output_path, audio, sr)
            
            # Actualizar metadatos
            if file_path.stem in self.metadata:
                self.metadata[file_path.stem].format = target_format
                if sample_rate:
                    self.metadata[file_path.stem].sample_rate = sample_rate
                if channels:
                    self.metadata[file_path.stem].channels = channels
                self._save_metadata()
                
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al convertir audio {file_path}: {e}")
            return None
            
    def normalize_audio(self, file_path: Union[str, Path]) -> Optional[Path]:
        """Normaliza el volumen de un archivo de audio."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
                
            # Cargar audio
            audio, sr = librosa.load(file_path, sr=None)
            
            # Normalizar
            audio_norm = librosa.util.normalize(audio)
            
            # Guardar audio normalizado
            output_path = self.cache_path / f"{file_path.stem}_normalized{file_path.suffix}"
            sf.write(output_path, audio_norm, sr)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al normalizar audio {file_path}: {e}")
            return None
            
    def trim_silence(self, 
                    file_path: Union[str, Path],
                    top_db: int = 20) -> Optional[Path]:
        """Elimina el silencio al inicio y final de un archivo de audio."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
                
            # Cargar audio
            audio, sr = librosa.load(file_path, sr=None)
            
            # Eliminar silencio
            audio_trim, _ = librosa.effects.trim(audio, top_db=top_db)
            
            # Guardar audio recortado
            output_path = self.cache_path / f"{file_path.stem}_trimmed{file_path.suffix}"
            sf.write(output_path, audio_trim, sr)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al recortar silencio de {file_path}: {e}")
            return None
            
    def extract_features(self, file_path: Union[str, Path]) -> Dict[str, np.ndarray]:
        """Extrae características de un archivo de audio."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {}
                
            # Cargar audio
            audio, sr = librosa.load(file_path, sr=None)
            
            # Extraer características
            features = {
                'mfcc': librosa.feature.mfcc(y=audio, sr=sr),
                'spectral_centroid': librosa.feature.spectral_centroid(y=audio, sr=sr),
                'spectral_bandwidth': librosa.feature.spectral_bandwidth(y=audio, sr=sr),
                'spectral_rolloff': librosa.feature.spectral_rolloff(y=audio, sr=sr),
                'zero_crossing_rate': librosa.feature.zero_crossing_rate(y=audio),
                'chroma': librosa.feature.chroma_stft(y=audio, sr=sr),
                'mel': librosa.feature.melspectrogram(y=audio, sr=sr)
            }
            
            return features
            
        except Exception as e:
            self.logger.error(f"Error al extraer características de {file_path}: {e}")
            return {}
            
    def validate_audio(self, file_path: Union[str, Path]) -> Dict[str, bool]:
        """Valida la integridad de un archivo de audio."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {'exists': False}
                
            # Cargar audio
            audio, sr = librosa.load(file_path, sr=None)
            
            # Verificar características
            is_mono = audio.ndim == 1
            is_stereo = audio.ndim == 2 and audio.shape[1] == 2
            has_silence = np.mean(np.abs(audio)) < 0.01
            is_clipped = np.max(np.abs(audio)) >= 1.0
            
            return {
                'exists': True,
                'is_valid': True,
                'is_mono': is_mono,
                'is_stereo': is_stereo,
                'has_silence': has_silence,
                'is_clipped': is_clipped
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar audio {file_path}: {e}")
            return {'exists': False}
            
    def get_audio_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de todos los archivos de audio registrados."""
        stats = {
            'total_audio': len(self.metadata),
            'total_duration': 0,
            'formats': {},
            'sample_rates': {},
            'channels': {},
            'compressed': 0,
            'with_metadata': 0
        }
        
        for metadata in self.metadata.values():
            stats['total_duration'] += metadata.duration
            stats['formats'][metadata.format] = stats['formats'].get(metadata.format, 0) + 1
            stats['sample_rates'][metadata.sample_rate] = stats['sample_rates'].get(metadata.sample_rate, 0) + 1
            stats['channels'][metadata.channels] = stats['channels'].get(metadata.channels, 0) + 1
            if metadata.is_compressed:
                stats['compressed'] += 1
            if metadata.has_metadata:
                stats['with_metadata'] += 1
                
        return stats 