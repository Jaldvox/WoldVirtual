import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union
import numpy as np
from dataclasses import dataclass
import trimesh
from trimesh.exchange.gltf import load_gltf, export_gltf
import pygltflib

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/model_manager.log'
)

@dataclass
class ModelMetadata:
    """Metadatos específicos para modelos 3D."""
    vertices: int
    faces: int
    materials: int
    animations: int
    lod_level: Optional[int]
    bounds: Dict[str, List[float]]
    format: str
    version: str

class ModelManager:
    """Gestor de modelos 3D."""
    
    def __init__(self, base_path: str = "assets/models"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.cache_path = self.base_path / "cache"
        self.logger = logging.getLogger("ModelManager")
        
        # Crear directorios necesarios
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, ModelMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, ModelMetadata]:
        """Carga los metadatos de modelos desde el archivo JSON."""
        metadata_file = self.metadata_path / "models_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: ModelMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de modelos en el archivo JSON."""
        metadata_file = self.metadata_path / "models_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _get_model_info(self, file_path: Path) -> Optional[ModelMetadata]:
        """Obtiene información detallada de un modelo 3D."""
        try:
            # Cargar modelo según el formato
            if file_path.suffix.lower() in ['.glb', '.gltf']:
                model = pygltflib.GLTF2().load(str(file_path))
                mesh_count = len(model.meshes)
                material_count = len(model.materials)
                animation_count = len(model.animations)
                
                # Obtener información de geometría
                vertices = 0
                faces = 0
                for mesh in model.meshes:
                    for primitive in mesh.primitives:
                        if primitive.attributes.POSITION is not None:
                            vertices += len(model.accessors[primitive.attributes.POSITION].count)
                        if primitive.indices is not None:
                            faces += len(model.accessors[primitive.indices].count) // 3
                            
            else:
                # Usar trimesh para otros formatos
                mesh = trimesh.load(file_path)
                vertices = len(mesh.vertices)
                faces = len(mesh.faces)
                material_count = len(mesh.visual.material) if hasattr(mesh.visual, 'material') else 0
                animation_count = 0
                
            # Calcular límites del modelo
            bounds = {
                'min': mesh.bounds[0].tolist(),
                'max': mesh.bounds[1].tolist()
            }
            
            # Determinar nivel de LOD
            lod_level = None
            if 'lod' in file_path.stem.lower():
                try:
                    lod_level = int(file_path.stem.split('_')[-1].replace('lod', ''))
                except:
                    pass
                    
            return ModelMetadata(
                vertices=vertices,
                faces=faces,
                materials=material_count,
                animations=animation_count,
                lod_level=lod_level,
                bounds=bounds,
                format=file_path.suffix[1:],
                version='2.0' if file_path.suffix.lower() in ['.glb', '.gltf'] else '1.0'
            )
            
        except Exception as e:
            self.logger.error(f"Error al obtener información del modelo {file_path}: {e}")
            return None
            
    def register_model(self, file_path: Union[str, Path]) -> Optional[ModelMetadata]:
        """Registra un nuevo modelo en el sistema."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.error(f"Modelo no encontrado: {file_path}")
                return None
                
            # Obtener información del modelo
            metadata = self._get_model_info(file_path)
            if not metadata:
                return None
                
            # Guardar metadatos
            self.metadata[file_path.stem] = metadata
            self._save_metadata()
            
            self.logger.info(f"Modelo registrado: {file_path}")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al registrar modelo {file_path}: {e}")
            return None
            
    def optimize_model(self, file_path: Union[str, Path], target_vertices: int = 10000) -> bool:
        """Optimiza un modelo 3D reduciendo su complejidad."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return False
                
            # Cargar modelo
            mesh = trimesh.load(file_path)
            
            # Simplificar si es necesario
            if len(mesh.vertices) > target_vertices:
                ratio = target_vertices / len(mesh.vertices)
                mesh = mesh.simplify_quadratic_decimation(ratio)
                
            # Optimizar normales
            mesh.fix_normals()
            
            # Optimizar UVs
            if hasattr(mesh, 'visual') and hasattr(mesh.visual, 'uv'):
                mesh.visual.uv = np.clip(mesh.visual.uv, 0, 1)
                
            # Guardar modelo optimizado
            output_path = self.cache_path / f"{file_path.stem}_optimized{file_path.suffix}"
            mesh.export(output_path)
            
            # Actualizar metadatos
            self.register_model(output_path)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error al optimizar modelo {file_path}: {e}")
            return False
            
    def convert_format(self, 
                      file_path: Union[str, Path],
                      target_format: str,
                      optimize: bool = True) -> Optional[Path]:
        """Convierte un modelo a otro formato."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
                
            # Cargar modelo
            mesh = trimesh.load(file_path)
            
            # Optimizar si se solicita
            if optimize:
                mesh = mesh.simplify_quadratic_decimation(0.5)
                mesh.fix_normals()
                
            # Determinar formato de salida
            if target_format.lower() == 'glb':
                output_path = self.cache_path / f"{file_path.stem}.glb"
                mesh.export(output_path, file_type='glb')
            elif target_format.lower() == 'gltf':
                output_path = self.cache_path / f"{file_path.stem}.gltf"
                mesh.export(output_path, file_type='gltf')
            elif target_format.lower() == 'obj':
                output_path = self.cache_path / f"{file_path.stem}.obj"
                mesh.export(output_path, file_type='obj')
            else:
                self.logger.error(f"Formato no soportado: {target_format}")
                return None
                
            # Actualizar metadatos
            self.register_model(output_path)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al convertir modelo {file_path}: {e}")
            return None
            
    def generate_lod(self, 
                    file_path: Union[str, Path],
                    levels: List[float] = [0.5, 0.25, 0.1]) -> List[Path]:
        """Genera niveles de detalle (LOD) para un modelo."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return []
                
            # Cargar modelo
            mesh = trimesh.load(file_path)
            output_paths = []
            
            # Generar LODs
            for i, ratio in enumerate(levels):
                # Simplificar modelo
                lod_mesh = mesh.simplify_quadratic_decimation(ratio)
                
                # Guardar LOD
                output_path = self.cache_path / f"{file_path.stem}_lod{i}{file_path.suffix}"
                lod_mesh.export(output_path)
                
                # Actualizar metadatos
                self.register_model(output_path)
                output_paths.append(output_path)
                
            return output_paths
            
        except Exception as e:
            self.logger.error(f"Error al generar LODs para {file_path}: {e}")
            return []
            
    def validate_model(self, file_path: Union[str, Path]) -> Dict[str, bool]:
        """Valida la integridad de un modelo 3D."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {'exists': False}
                
            # Cargar modelo
            mesh = trimesh.load(file_path)
            
            return {
                'exists': True,
                'has_vertices': len(mesh.vertices) > 0,
                'has_faces': len(mesh.faces) > 0,
                'is_watertight': mesh.is_watertight,
                'is_volume': mesh.is_volume,
                'is_empty': mesh.is_empty,
                'is_convex': mesh.is_convex
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar modelo {file_path}: {e}")
            return {'exists': False}
            
    def get_model_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de todos los modelos registrados."""
        stats = {
            'total_models': len(self.metadata),
            'total_vertices': 0,
            'total_faces': 0,
            'total_materials': 0,
            'total_animations': 0,
            'formats': {}
        }
        
        for metadata in self.metadata.values():
            stats['total_vertices'] += metadata.vertices
            stats['total_faces'] += metadata.faces
            stats['total_materials'] += metadata.materials
            stats['total_animations'] += metadata.animations
            stats['formats'][metadata.format] = stats['formats'].get(metadata.format, 0) + 1
            
        return stats 