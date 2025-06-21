import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
import numpy as np
from dataclasses import dataclass
import trimesh
from trimesh.visual import Material, TextureVisuals

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='assets/logs/material_manager.log'
)

@dataclass
class MaterialMetadata:
    """Metadatos específicos para materiales."""
    name: str
    type: str
    has_texture: bool
    has_normal_map: bool
    has_roughness_map: bool
    has_metalness_map: bool
    has_emission_map: bool
    has_ao_map: bool
    is_pbr: bool
    is_transparent: bool

class MaterialManager:
    """Gestor de materiales."""
    
    def __init__(self, base_path: str = "assets/materials"):
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.cache_path = self.base_path / "cache"
        self.logger = logging.getLogger("MaterialManager")
        
        # Crear directorios necesarios
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar metadatos existentes
        self.metadata: Dict[str, MaterialMetadata] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, MaterialMetadata]:
        """Carga los metadatos de materiales desde el archivo JSON."""
        metadata_file = self.metadata_path / "materials_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return {k: MaterialMetadata(**v) for k, v in data.items()}
        return {}
        
    def _save_metadata(self):
        """Guarda los metadatos de materiales en el archivo JSON."""
        metadata_file = self.metadata_path / "materials_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(
                {k: v.__dict__ for k, v in self.metadata.items()},
                f,
                indent=2
            )
            
    def _get_material_info(self, file_path: Path) -> Optional[MaterialMetadata]:
        """Obtiene información detallada de un material."""
        try:
            # Cargar material
            material = trimesh.load(file_path)
            
            # Verificar características
            has_texture = hasattr(material.visual, 'texture')
            has_normal_map = hasattr(material.visual, 'normal_map')
            has_roughness_map = hasattr(material.visual, 'roughness_map')
            has_metalness_map = hasattr(material.visual, 'metalness_map')
            has_emission_map = hasattr(material.visual, 'emission_map')
            has_ao_map = hasattr(material.visual, 'ao_map')
            
            # Determinar tipo de material
            is_pbr = any([
                has_roughness_map,
                has_metalness_map,
                has_normal_map
            ])
            
            # Verificar transparencia
            is_transparent = (
                hasattr(material.visual, 'alpha') and
                material.visual.alpha < 1.0
            )
            
            return MaterialMetadata(
                name=file_path.stem,
                type='PBR' if is_pbr else 'Standard',
                has_texture=has_texture,
                has_normal_map=has_normal_map,
                has_roughness_map=has_roughness_map,
                has_metalness_map=has_metalness_map,
                has_emission_map=has_emission_map,
                has_ao_map=has_ao_map,
                is_pbr=is_pbr,
                is_transparent=is_transparent
            )
            
        except Exception as e:
            self.logger.error(f"Error al obtener información del material {file_path}: {e}")
            return None
            
    def register_material(self, file_path: Union[str, Path]) -> Optional[MaterialMetadata]:
        """Registra un nuevo material en el sistema."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.error(f"Material no encontrado: {file_path}")
                return None
                
            # Obtener información del material
            metadata = self._get_material_info(file_path)
            if not metadata:
                return None
                
            # Guardar metadatos
            self.metadata[file_path.stem] = metadata
            self._save_metadata()
            
            self.logger.info(f"Material registrado: {file_path}")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error al registrar material {file_path}: {e}")
            return None
            
    def create_pbr_material(self,
                          name: str,
                          base_color: Tuple[float, float, float, float] = (1, 1, 1, 1),
                          roughness: float = 0.5,
                          metalness: float = 0.0,
                          normal_scale: float = 1.0,
                          emission: Tuple[float, float, float] = (0, 0, 0),
                          ao_strength: float = 1.0) -> Optional[Path]:
        """Crea un nuevo material PBR."""
        try:
            # Crear material base
            material = Material(
                baseColorFactor=base_color,
                roughnessFactor=roughness,
                metallicFactor=metalness,
                normalScale=normal_scale,
                emissiveFactor=emission,
                occlusionStrength=ao_strength
            )
            
            # Crear visualización
            visual = TextureVisuals(material=material)
            
            # Guardar material
            output_path = self.cache_path / f"{name}.gltf"
            visual.export(output_path)
            
            # Registrar material
            self.register_material(output_path)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al crear material PBR {name}: {e}")
            return None
            
    def convert_to_pbr(self, file_path: Union[str, Path]) -> Optional[Path]:
        """Convierte un material estándar a PBR."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
                
            # Cargar material
            material = trimesh.load(file_path)
            
            # Convertir a PBR
            if not hasattr(material.visual, 'material'):
                material.visual.material = Material()
                
            # Configurar propiedades PBR
            material.visual.material.roughnessFactor = 0.5
            material.visual.material.metallicFactor = 0.0
            material.visual.material.normalScale = 1.0
            
            # Guardar material PBR
            output_path = self.cache_path / f"{file_path.stem}_pbr{file_path.suffix}"
            material.export(output_path)
            
            # Actualizar metadatos
            if file_path.stem in self.metadata:
                self.metadata[file_path.stem].type = 'PBR'
                self.metadata[file_path.stem].is_pbr = True
                self._save_metadata()
                
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al convertir material a PBR {file_path}: {e}")
            return None
            
    def add_texture(self,
                   file_path: Union[str, Path],
                   texture_path: Union[str, Path],
                   texture_type: str = 'base_color') -> Optional[Path]:
        """Añade una textura a un material."""
        try:
            file_path = Path(file_path)
            texture_path = Path(texture_path)
            
            if not file_path.exists() or not texture_path.exists():
                return None
                
            # Cargar material y textura
            material = trimesh.load(file_path)
            texture = trimesh.load(texture_path)
            
            # Añadir textura según el tipo
            if texture_type == 'base_color':
                material.visual.texture = texture
            elif texture_type == 'normal':
                material.visual.normal_map = texture
            elif texture_type == 'roughness':
                material.visual.roughness_map = texture
            elif texture_type == 'metalness':
                material.visual.metalness_map = texture
            elif texture_type == 'emission':
                material.visual.emission_map = texture
            elif texture_type == 'ao':
                material.visual.ao_map = texture
                
            # Guardar material con textura
            output_path = self.cache_path / f"{file_path.stem}_{texture_type}{file_path.suffix}"
            material.export(output_path)
            
            # Actualizar metadatos
            if file_path.stem in self.metadata:
                if texture_type == 'base_color':
                    self.metadata[file_path.stem].has_texture = True
                elif texture_type == 'normal':
                    self.metadata[file_path.stem].has_normal_map = True
                elif texture_type == 'roughness':
                    self.metadata[file_path.stem].has_roughness_map = True
                elif texture_type == 'metalness':
                    self.metadata[file_path.stem].has_metalness_map = True
                elif texture_type == 'emission':
                    self.metadata[file_path.stem].has_emission_map = True
                elif texture_type == 'ao':
                    self.metadata[file_path.stem].has_ao_map = True
                self._save_metadata()
                
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error al añadir textura a material {file_path}: {e}")
            return None
            
    def validate_material(self, file_path: Union[str, Path]) -> Dict[str, bool]:
        """Valida la integridad de un material."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {'exists': False}
                
            # Cargar material
            material = trimesh.load(file_path)
            
            # Verificar características
            has_material = hasattr(material.visual, 'material')
            has_texture = hasattr(material.visual, 'texture')
            is_valid = has_material or has_texture
            
            return {
                'exists': True,
                'has_material': has_material,
                'has_texture': has_texture,
                'is_valid': is_valid
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar material {file_path}: {e}")
            return {'exists': False}
            
    def get_material_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de todos los materiales registrados."""
        stats = {
            'total_materials': len(self.metadata),
            'pbr_materials': 0,
            'standard_materials': 0,
            'with_textures': 0,
            'with_normal_maps': 0,
            'with_roughness_maps': 0,
            'with_metalness_maps': 0,
            'with_emission_maps': 0,
            'with_ao_maps': 0,
            'transparent_materials': 0
        }
        
        for metadata in self.metadata.values():
            if metadata.is_pbr:
                stats['pbr_materials'] += 1
            else:
                stats['standard_materials'] += 1
            if metadata.has_texture:
                stats['with_textures'] += 1
            if metadata.has_normal_map:
                stats['with_normal_maps'] += 1
            if metadata.has_roughness_map:
                stats['with_roughness_maps'] += 1
            if metadata.has_metalness_map:
                stats['with_metalness_maps'] += 1
            if metadata.has_emission_map:
                stats['with_emission_maps'] += 1
            if metadata.has_ao_map:
                stats['with_ao_maps'] += 1
            if metadata.is_transparent:
                stats['transparent_materials'] += 1
                
        return stats 