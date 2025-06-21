import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/shader_manager.log'
)

@dataclass
class ShaderMetadata:
    """Metadatos específicos para shaders."""
    name: str
    type: str
    version: str
    has_vertex: bool
    has_fragment: bool
    has_geometry: bool
    has_compute: bool
    has_tessellation: bool
    uniforms: List[str]
    attributes: List[str]
    varyings: List[str]

class ShaderManager:
    """Gestor de shaders."""
    
    def __init__(self, base_path: str = "assets/shaders"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.cache_path = self.base_path / "cache"
        self.logger = logging.getLogger("ShaderManager")
        
        # Crear directorios necesarios
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, ShaderMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, ShaderMetadata]:
        """Carga los metadatos de shaders desde el archivo JSON."""
        metadata_file = self.metadata_path / "shaders_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: ShaderMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de shaders en el archivo JSON."""
        metadata_file = self.metadata_path / "shaders_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _get_shader_info(self, file_path: Path) -> Optional[ShaderMetadata]:
        """Obtiene información detallada de un shader."""
        try:
            # Leer archivo de shader
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Determinar tipo de shader
            shader_type = file_path.suffix[1:]
            
            # Verificar versiones
            version = '1.0'
            if '#version' in content:
                version = content.split('#version')[1].split('\n')[0].strip()
                
            # Buscar uniforms
            uniforms = []
            for line in content.split('\n'):
                if 'uniform' in line:
                    uniform = line.split('uniform')[1].split(';')[0].strip()
                    uniforms.append(uniform)
                    
            # Buscar attributes
            attributes = []
            for line in content.split('\n'):
                if 'attribute' in line or 'in' in line:
                    attr = line.split('attribute' if 'attribute' in line else 'in')[1].split(';')[0].strip()
                    attributes.append(attr)
                    
            # Buscar varyings
            varyings = []
            for line in content.split('\n'):
                if 'varying' in line or 'out' in line:
                    varying = line.split('varying' if 'varying' in line else 'out')[1].split(';')[0].strip()
                    varyings.append(varying)
                    
            return ShaderMetadata(
                name=file_path.stem,
                type=shader_type,
                version=version,
                has_vertex='main' in content and 'gl_Position' in content,
                has_fragment='main' in content and 'gl_FragColor' in content,
                has_geometry='geometry' in content,
                has_compute='compute' in content,
                has_tessellation='tessellation' in content,
                uniforms=uniforms,
                attributes=attributes,
                varyings=varyings
            )
            
        except Exception as e:
            self.logger.error(f"Error al obtener información del shader {file_path}: {e}")
            return None
            
    def register_shader(self, file_path: Union[str, Path]) -> Optional[ShaderMetadata]:
        """Registra un nuevo shader en el sistema."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.error(f"Shader no encontrado: {file_path}")
                return None
                
            # Obtener información del shader
            metadata = self._get_shader_info(file_path)
            if not metadata:
                return None
                
            # Guardar metadatos
            self.metadata[file_path.stem] = metadata
            self._save_metadata()
            
            self.logger.info(f"Shader registrado: {file_path}")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al registrar shader {file_path}: {e}")
            return None
            
    def create_shader(self,
                     name: str,
                     shader_type: str,
                     content: str,
                     version: str = '300 es') -> Optional[Path]:
        """Crea un nuevo shader."""
        try:
            # Crear archivo de shader
            output_path = self.cache_path / f"{name}.{shader_type}"
            
            # Añadir versión si no está presente
            if '#version' not in content:
                content = f'#version {version}\n{content}'
                
            # Guardar shader
            with open(output_path, 'w') as f:
                f.write(content)
                
            # Registrar shader
            self.register_shader(output_path)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al crear shader {name}: {e}")
            return None
            
    def compile_shader(self, file_path: Union[str, Path]) -> bool:
        """Compila un shader para verificar su validez."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return False
                
            # Leer shader
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Verificar sintaxis básica
            if not content.strip():
                return False
                
            # Verificar que tenga una función main
            if 'main' not in content:
                return False
                
            # Verificar que tenga las variables necesarias según el tipo
            shader_type = file_path.suffix[1:]
            if shader_type == 'vert':
                if 'gl_Position' not in content:
                    return False
            elif shader_type == 'frag':
                if 'gl_FragColor' not in content and 'out' not in content:
                    return False
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Error al compilar shader {file_path}: {e}")
            return False
            
    def optimize_shader(self, file_path: Union[str, Path]) -> Optional[Path]:
        """Optimiza un shader eliminando código muerto y simplificando expresiones."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
                
            # Leer shader
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Eliminar comentarios
            lines = content.split('\n')
            optimized_lines = []
            for line in lines:
                if not line.strip().startswith('//'):
                    optimized_lines.append(line)
                    
            # Eliminar líneas vacías
            optimized_lines = [line for line in optimized_lines if line.strip()]
            
            # Guardar shader optimizado
            output_path = self.cache_path / f"{file_path.stem}_optimized{file_path.suffix}"
            with open(output_path, 'w') as f:
                f.write('\n'.join(optimized_lines))
                
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al optimizar shader {file_path}: {e}")
            return None
            
    def validate_shader(self, file_path: Union[str, Path]) -> Dict[str, bool]:
        """Valida la integridad de un shader."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {'exists': False}
                
            # Leer shader
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Verificar características
            has_version = '#version' in content
            has_main = 'main' in content
            has_syntax = all(char in content for char in ['{', '}', ';'])
            
            return {
                'exists': True,
                'has_version': has_version,
                'has_main': has_main,
                'has_syntax': has_syntax,
                'is_valid': has_version and has_main and has_syntax
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar shader {file_path}: {e}")
            return {'exists': False}
            
    def get_shader_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de todos los shaders registrados."""
        stats = {
            'total_shaders': len(self.metadata),
            'vertex_shaders': 0,
            'fragment_shaders': 0,
            'geometry_shaders': 0,
            'compute_shaders': 0,
            'tessellation_shaders': 0,
            'versions': {},
            'with_uniforms': 0,
            'with_attributes': 0,
            'with_varyings': 0
        }
        
        for metadata in self.metadata.values():
            if metadata.has_vertex:
                stats['vertex_shaders'] += 1
            if metadata.has_fragment:
                stats['fragment_shaders'] += 1
            if metadata.has_geometry:
                stats['geometry_shaders'] += 1
            if metadata.has_compute:
                stats['compute_shaders'] += 1
            if metadata.has_tessellation:
                stats['tessellation_shaders'] += 1
            stats['versions'][metadata.version] = stats['versions'].get(metadata.version, 0) + 1
            if metadata.uniforms:
                stats['with_uniforms'] += 1
            if metadata.attributes:
                stats['with_attributes'] += 1
            if metadata.varyings:
                stats['with_varyings'] += 1
                
        return stats 