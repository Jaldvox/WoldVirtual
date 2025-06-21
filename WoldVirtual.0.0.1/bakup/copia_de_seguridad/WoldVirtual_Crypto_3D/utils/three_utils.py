"""
Utilidades para Three.js en WoldVirtual Crypto 3D
Contiene helpers para geometría, materiales, renderizado y optimización 3D.
"""

import json
import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass
import math

logger = logging.getLogger(__name__)

# =============================================================================
# ESTRUCTURAS DE DATOS
# =============================================================================

@dataclass
class Vector3:
    """Representa un vector 3D."""
    x: float
    y: float
    z: float
    
    def to_dict(self) -> Dict[str, float]:
        """Convierte el vector a diccionario."""
        return {"x": self.x, "y": self.y, "z": self.z}
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'Vector3':
        """Crea un vector desde un diccionario."""
        return cls(data.get('x', 0), data.get('y', 0), data.get('z', 0))
    
    def distance_to(self, other: 'Vector3') -> float:
        """Calcula la distancia a otro vector."""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def normalize(self) -> 'Vector3':
        """Normaliza el vector."""
        length = math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        if length == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x/length, self.y/length, self.z/length)

@dataclass
class Quaternion:
    """Representa una rotación en cuaterniones."""
    x: float
    y: float
    z: float
    w: float
    
    def to_dict(self) -> Dict[str, float]:
        """Convierte el cuaternión a diccionario."""
        return {"x": self.x, "y": self.y, "z": self.z, "w": self.w}
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'Quaternion':
        """Crea un cuaternión desde un diccionario."""
        return cls(
            data.get('x', 0),
            data.get('y', 0),
            data.get('z', 0),
            data.get('w', 1)
        )

@dataclass
class Transform:
    """Representa una transformación 3D."""
    position: Vector3
    rotation: Quaternion
    scale: Vector3
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la transformación a diccionario."""
        return {
            "position": self.position.to_dict(),
            "rotation": self.rotation.to_dict(),
            "scale": self.scale.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transform':
        """Crea una transformación desde un diccionario."""
        return cls(
            Vector3.from_dict(data.get('position', {})),
            Quaternion.from_dict(data.get('rotation', {})),
            Vector3.from_dict(data.get('scale', {'x': 1, 'y': 1, 'z': 1}))
        )

# =============================================================================
# UTILIDADES DE GEOMETRÍA
# =============================================================================

class GeometryUtils:
    """Utilidades para geometría 3D."""
    
    @staticmethod
    def create_box_geometry(width: float, height: float, depth: float) -> Dict[str, Any]:
        """
        Crea geometría de caja.
        
        Args:
            width: Ancho de la caja
            height: Alto de la caja
            depth: Profundidad de la caja
            
        Returns:
            Dict[str, Any]: Configuración de geometría
        """
        return {
            "type": "BoxGeometry",
            "parameters": {
                "width": width,
                "height": height,
                "depth": depth,
                "widthSegments": 1,
                "heightSegments": 1,
                "depthSegments": 1
            }
        }
    
    @staticmethod
    def create_sphere_geometry(radius: float, segments: int = 32) -> Dict[str, Any]:
        """
        Crea geometría de esfera.
        
        Args:
            radius: Radio de la esfera
            segments: Número de segmentos
            
        Returns:
            Dict[str, Any]: Configuración de geometría
        """
        return {
            "type": "SphereGeometry",
            "parameters": {
                "radius": radius,
                "widthSegments": segments,
                "heightSegments": segments
            }
        }
    
    @staticmethod
    def create_cylinder_geometry(radius: float, height: float, segments: int = 32) -> Dict[str, Any]:
        """
        Crea geometría de cilindro.
        
        Args:
            radius: Radio del cilindro
            height: Altura del cilindro
            segments: Número de segmentos
            
        Returns:
            Dict[str, Any]: Configuración de geometría
        """
        return {
            "type": "CylinderGeometry",
            "parameters": {
                "radiusTop": radius,
                "radiusBottom": radius,
                "height": height,
                "radialSegments": segments,
                "heightSegments": 1
            }
        }
    
    @staticmethod
    def create_plane_geometry(width: float, height: float, segments: int = 1) -> Dict[str, Any]:
        """
        Crea geometría de plano.
        
        Args:
            width: Ancho del plano
            height: Alto del plano
            segments: Número de segmentos
            
        Returns:
            Dict[str, Any]: Configuración de geometría
        """
        return {
            "type": "PlaneGeometry",
            "parameters": {
                "width": width,
                "height": height,
                "widthSegments": segments,
                "heightSegments": segments
            }
        }
    
    @staticmethod
    def create_terrain_geometry(
        width: float,
        height: float,
        width_segments: int,
        height_segments: int,
        height_map: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        Crea geometría de terreno.
        
        Args:
            width: Ancho del terreno
            height: Alto del terreno
            width_segments: Segmentos de ancho
            height_segments: Segmentos de alto
            height_map: Mapa de altura (opcional)
            
        Returns:
            Dict[str, Any]: Configuración de geometría
        """
        return {
            "type": "TerrainGeometry",
            "parameters": {
                "width": width,
                "height": height,
                "widthSegments": width_segments,
                "heightSegments": height_segments,
                "heightMap": height_map
            }
        }
    
    @staticmethod
    def calculate_bounding_box(vertices: List[Vector3]) -> Dict[str, Vector3]:
        """
        Calcula la caja de límites de un conjunto de vértices.
        
        Args:
            vertices: Lista de vértices
            
        Returns:
            Dict[str, Vector3]: Caja de límites con min y max
        """
        if not vertices:
            return {"min": Vector3(0, 0, 0), "max": Vector3(0, 0, 0)}
        
        min_x = min(v.x for v in vertices)
        min_y = min(v.y for v in vertices)
        min_z = min(v.z for v in vertices)
        max_x = max(v.x for v in vertices)
        max_y = max(v.y for v in vertices)
        max_z = max(v.z for v in vertices)
        
        return {
            "min": Vector3(min_x, min_y, min_z),
            "max": Vector3(max_x, max_y, max_z)
        }
    
    @staticmethod
    def calculate_center(vertices: List[Vector3]) -> Vector3:
        """
        Calcula el centro de un conjunto de vértices.
        
        Args:
            vertices: Lista de vértices
            
        Returns:
            Vector3: Centro calculado
        """
        if not vertices:
            return Vector3(0, 0, 0)
        
        total_x = sum(v.x for v in vertices)
        total_y = sum(v.y for v in vertices)
        total_z = sum(v.z for v in vertices)
        count = len(vertices)
        
        return Vector3(total_x/count, total_y/count, total_z/count)

# =============================================================================
# UTILIDADES DE MATERIALES
# =============================================================================

class MaterialUtils:
    """Utilidades para materiales 3D."""
    
    @staticmethod
    def create_basic_material(
        color: str = "#ffffff",
        transparent: bool = False,
        opacity: float = 1.0,
        wireframe: bool = False
    ) -> Dict[str, Any]:
        """
        Crea un material básico.
        
        Args:
            color: Color del material
            transparent: Si es transparente
            opacity: Opacidad (0-1)
            wireframe: Si mostrar como wireframe
            
        Returns:
            Dict[str, Any]: Configuración del material
        """
        return {
            "type": "MeshBasicMaterial",
            "parameters": {
                "color": color,
                "transparent": transparent,
                "opacity": opacity,
                "wireframe": wireframe
            }
        }
    
    @staticmethod
    def create_lambert_material(
        color: str = "#ffffff",
        transparent: bool = False,
        opacity: float = 1.0,
        emissive: str = "#000000"
    ) -> Dict[str, Any]:
        """
        Crea un material Lambert.
        
        Args:
            color: Color del material
            transparent: Si es transparente
            opacity: Opacidad (0-1)
            emissive: Color emisivo
            
        Returns:
            Dict[str, Any]: Configuración del material
        """
        return {
            "type": "MeshLambertMaterial",
            "parameters": {
                "color": color,
                "transparent": transparent,
                "opacity": opacity,
                "emissive": emissive
            }
        }
    
    @staticmethod
    def create_phong_material(
        color: str = "#ffffff",
        transparent: bool = False,
        opacity: float = 1.0,
        shininess: float = 30.0,
        specular: str = "#111111"
    ) -> Dict[str, Any]:
        """
        Crea un material Phong.
        
        Args:
            color: Color del material
            transparent: Si es transparente
            opacity: Opacidad (0-1)
            shininess: Brillo especular
            specular: Color especular
            
        Returns:
            Dict[str, Any]: Configuración del material
        """
        return {
            "type": "MeshPhongMaterial",
            "parameters": {
                "color": color,
                "transparent": transparent,
                "opacity": opacity,
                "shininess": shininess,
                "specular": specular
            }
        }
    
    @staticmethod
    def create_standard_material(
        color: str = "#ffffff",
        transparent: bool = False,
        opacity: float = 1.0,
        metalness: float = 0.0,
        roughness: float = 0.5,
        env_map: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crea un material estándar PBR.
        
        Args:
            color: Color del material
            transparent: Si es transparente
            opacity: Opacidad (0-1)
            metalness: Metalicidad (0-1)
            roughness: Rugosidad (0-1)
            env_map: Mapa de entorno (opcional)
            
        Returns:
            Dict[str, Any]: Configuración del material
        """
        material = {
            "type": "MeshStandardMaterial",
            "parameters": {
                "color": color,
                "transparent": transparent,
                "opacity": opacity,
                "metalness": metalness,
                "roughness": roughness
            }
        }
        
        if env_map:
            material["parameters"]["envMap"] = env_map
        
        return material
    
    @staticmethod
    def create_texture_material(
        texture_url: str,
        color: str = "#ffffff",
        transparent: bool = False,
        opacity: float = 1.0
    ) -> Dict[str, Any]:
        """
        Crea un material con textura.
        
        Args:
            texture_url: URL de la textura
            color: Color del material
            transparent: Si es transparente
            opacity: Opacidad (0-1)
            
        Returns:
            Dict[str, Any]: Configuración del material
        """
        return {
            "type": "MeshStandardMaterial",
            "parameters": {
                "color": color,
                "transparent": transparent,
                "opacity": opacity,
                "map": texture_url
            }
        }

# =============================================================================
# UTILIDADES DE ILUMINACIÓN
# =============================================================================

class LightingUtils:
    """Utilidades para iluminación 3D."""
    
    @staticmethod
    def create_ambient_light(color: str = "#ffffff", intensity: float = 0.5) -> Dict[str, Any]:
        """
        Crea una luz ambiental.
        
        Args:
            color: Color de la luz
            intensity: Intensidad de la luz
            
        Returns:
            Dict[str, Any]: Configuración de la luz
        """
        return {
            "type": "AmbientLight",
            "parameters": {
                "color": color,
                "intensity": intensity
            }
        }
    
    @staticmethod
    def create_directional_light(
        color: str = "#ffffff",
        intensity: float = 1.0,
        position: Vector3 = Vector3(0, 10, 0),
        cast_shadow: bool = True
    ) -> Dict[str, Any]:
        """
        Crea una luz direccional.
        
        Args:
            color: Color de la luz
            intensity: Intensidad de la luz
            position: Posición de la luz
            cast_shadow: Si proyecta sombras
            
        Returns:
            Dict[str, Any]: Configuración de la luz
        """
        return {
            "type": "DirectionalLight",
            "parameters": {
                "color": color,
                "intensity": intensity,
                "position": position.to_dict(),
                "castShadow": cast_shadow
            }
        }
    
    @staticmethod
    def create_point_light(
        color: str = "#ffffff",
        intensity: float = 1.0,
        position: Vector3 = Vector3(0, 10, 0),
        distance: float = 0.0,
        decay: float = 2.0
    ) -> Dict[str, Any]:
        """
        Crea una luz puntual.
        
        Args:
            color: Color de la luz
            intensity: Intensidad de la luz
            position: Posición de la luz
            distance: Distancia máxima
            decay: Decaimiento de la luz
            
        Returns:
            Dict[str, Any]: Configuración de la luz
        """
        return {
            "type": "PointLight",
            "parameters": {
                "color": color,
                "intensity": intensity,
                "position": position.to_dict(),
                "distance": distance,
                "decay": decay
            }
        }
    
    @staticmethod
    def create_spot_light(
        color: str = "#ffffff",
        intensity: float = 1.0,
        position: Vector3 = Vector3(0, 10, 0),
        target: Vector3 = Vector3(0, 0, 0),
        angle: float = 0.3,
        penumbra: float = 0.0,
        distance: float = 0.0,
        decay: float = 2.0
    ) -> Dict[str, Any]:
        """
        Crea una luz spot.
        
        Args:
            color: Color de la luz
            intensity: Intensidad de la luz
            position: Posición de la luz
            target: Objetivo de la luz
            angle: Ángulo del cono
            penumbra: Penumbra del cono
            distance: Distancia máxima
            decay: Decaimiento de la luz
            
        Returns:
            Dict[str, Any]: Configuración de la luz
        """
        return {
            "type": "SpotLight",
            "parameters": {
                "color": color,
                "intensity": intensity,
                "position": position.to_dict(),
                "target": target.to_dict(),
                "angle": angle,
                "penumbra": penumbra,
                "distance": distance,
                "decay": decay
            }
        }
    
    @staticmethod
    def create_hemisphere_light(
        sky_color: str = "#87ceeb",
        ground_color: str = "#8b4513",
        intensity: float = 1.0
    ) -> Dict[str, Any]:
        """
        Crea una luz hemisférica.
        
        Args:
            sky_color: Color del cielo
            ground_color: Color del suelo
            intensity: Intensidad de la luz
            
        Returns:
            Dict[str, Any]: Configuración de la luz
        """
        return {
            "type": "HemisphereLight",
            "parameters": {
                "skyColor": sky_color,
                "groundColor": ground_color,
                "intensity": intensity
            }
        }

# =============================================================================
# UTILIDADES DE CÁMARA
# =============================================================================

class CameraUtils:
    """Utilidades para cámaras 3D."""
    
    @staticmethod
    def create_perspective_camera(
        fov: float = 75.0,
        aspect: float = 16.0 / 9.0,
        near: float = 0.1,
        far: float = 1000.0,
        position: Vector3 = Vector3(0, 5, 10),
        look_at: Vector3 = Vector3(0, 0, 0)
    ) -> Dict[str, Any]:
        """
        Crea una cámara en perspectiva.
        
        Args:
            fov: Campo de visión
            aspect: Relación de aspecto
            near: Plano cercano
            far: Plano lejano
            position: Posición de la cámara
            look_at: Punto al que mira la cámara
            
        Returns:
            Dict[str, Any]: Configuración de la cámara
        """
        return {
            "type": "PerspectiveCamera",
            "parameters": {
                "fov": fov,
                "aspect": aspect,
                "near": near,
                "far": far,
                "position": position.to_dict(),
                "lookAt": look_at.to_dict()
            }
        }
    
    @staticmethod
    def create_orthographic_camera(
        left: float = -10.0,
        right: float = 10.0,
        top: float = 10.0,
        bottom: float = -10.0,
        near: float = 0.1,
        far: float = 1000.0,
        position: Vector3 = Vector3(0, 5, 10),
        look_at: Vector3 = Vector3(0, 0, 0)
    ) -> Dict[str, Any]:
        """
        Crea una cámara ortográfica.
        
        Args:
            left: Límite izquierdo
            right: Límite derecho
            top: Límite superior
            bottom: Límite inferior
            near: Plano cercano
            far: Plano lejano
            position: Posición de la cámara
            look_at: Punto al que mira la cámara
            
        Returns:
            Dict[str, Any]: Configuración de la cámara
        """
        return {
            "type": "OrthographicCamera",
            "parameters": {
                "left": left,
                "right": right,
                "top": top,
                "bottom": bottom,
                "near": near,
                "far": far,
                "position": position.to_dict(),
                "lookAt": look_at.to_dict()
            }
        }

# =============================================================================
# UTILIDADES DE OPTIMIZACIÓN
# =============================================================================

class OptimizationUtils:
    """Utilidades para optimización 3D."""
    
    @staticmethod
    def calculate_lod_levels(
        distances: List[float],
        polygon_counts: List[int]
    ) -> List[Dict[str, Any]]:
        """
        Calcula niveles de LOD (Level of Detail).
        
        Args:
            distances: Distancias para cada nivel
            polygon_counts: Número de polígonos para cada nivel
            
        Returns:
            List[Dict[str, Any]]: Configuración de LOD
        """
        lod_levels = []
        for i, (distance, polygons) in enumerate(zip(distances, polygon_counts)):
            lod_levels.append({
                "level": i,
                "distance": distance,
                "polygonCount": polygons,
                "enabled": True
            })
        return lod_levels
    
    @staticmethod
    def optimize_geometry_settings(
        polygon_count: int,
        texture_size: int,
        target_fps: int = 60
    ) -> Dict[str, Any]:
        """
        Calcula configuraciones óptimas de geometría.
        
        Args:
            polygon_count: Número de polígonos
            texture_size: Tamaño de textura
            target_fps: FPS objetivo
            
        Returns:
            Dict[str, Any]: Configuraciones optimizadas
        """
        # Calcular nivel de detalle basado en FPS objetivo
        if target_fps >= 60:
            lod_threshold = 10000
            texture_quality = "high"
        elif target_fps >= 30:
            lod_threshold = 5000
            texture_quality = "medium"
        else:
            lod_threshold = 2000
            texture_quality = "low"
        
        return {
            "lodThreshold": lod_threshold,
            "textureQuality": texture_quality,
            "enableFrustumCulling": True,
            "enableOcclusionCulling": polygon_count > 1000,
            "maxPolygonCount": polygon_count,
            "maxTextureSize": texture_size
        }
    
    @staticmethod
    def calculate_memory_usage(
        polygon_count: int,
        texture_count: int,
        texture_size: int
    ) -> Dict[str, float]:
        """
        Calcula el uso de memoria estimado.
        
        Args:
            polygon_count: Número de polígonos
            texture_count: Número de texturas
            texture_size: Tamaño de textura en píxeles
            
        Returns:
            Dict[str, float]: Uso de memoria en MB
        """
        # Estimación aproximada
        geometry_memory = polygon_count * 0.0001  # MB por polígono
        texture_memory = texture_count * (texture_size ** 2) * 4 / (1024 * 1024)  # MB
        
        return {
            "geometry": round(geometry_memory, 2),
            "textures": round(texture_memory, 2),
            "total": round(geometry_memory + texture_memory, 2)
        }

# =============================================================================
# UTILIDADES DE ANIMACIÓN
# =============================================================================

class AnimationUtils:
    """Utilidades para animación 3D."""
    
    @staticmethod
    def create_keyframe_animation(
        property_name: str,
        keyframes: List[Dict[str, Any]],
        duration: float = 1.0,
        loop: bool = False
    ) -> Dict[str, Any]:
        """
        Crea una animación de keyframes.
        
        Args:
            property_name: Nombre de la propiedad a animar
            keyframes: Lista de keyframes
            duration: Duración de la animación
            loop: Si la animación debe repetirse
            
        Returns:
            Dict[str, Any]: Configuración de la animación
        """
        return {
            "type": "KeyframeAnimation",
            "parameters": {
                "property": property_name,
                "keyframes": keyframes,
                "duration": duration,
                "loop": loop
            }
        }
    
    @staticmethod
    def create_rotation_animation(
        axis: str = "y",
        speed: float = 1.0,
        loop: bool = True
    ) -> Dict[str, Any]:
        """
        Crea una animación de rotación.
        
        Args:
            axis: Eje de rotación (x, y, z)
            speed: Velocidad de rotación
            loop: Si la animación debe repetirse
            
        Returns:
            Dict[str, Any]: Configuración de la animación
        """
        return {
            "type": "RotationAnimation",
            "parameters": {
                "axis": axis,
                "speed": speed,
                "loop": loop
            }
        }
    
    @staticmethod
    def create_scale_animation(
        scale_from: Vector3,
        scale_to: Vector3,
        duration: float = 1.0,
        loop: bool = False
    ) -> Dict[str, Any]:
        """
        Crea una animación de escala.
        
        Args:
            scale_from: Escala inicial
            scale_to: Escala final
            duration: Duración de la animación
            loop: Si la animación debe repetirse
            
        Returns:
            Dict[str, Any]: Configuración de la animación
        """
        return {
            "type": "ScaleAnimation",
            "parameters": {
                "scaleFrom": scale_from.to_dict(),
                "scaleTo": scale_to.to_dict(),
                "duration": duration,
                "loop": loop
            }
        }

# =============================================================================
# UTILIDADES DE FÍSICA
# =============================================================================

class PhysicsUtils:
    """Utilidades para física 3D."""
    
    @staticmethod
    def create_rigid_body(
        mass: float = 1.0,
        shape: str = "box",
        size: Vector3 = Vector3(1, 1, 1),
        position: Vector3 = Vector3(0, 0, 0),
        rotation: Quaternion = Quaternion(0, 0, 0, 1)
    ) -> Dict[str, Any]:
        """
        Crea un cuerpo rígido.
        
        Args:
            mass: Masa del cuerpo
            shape: Forma del cuerpo
            size: Tamaño del cuerpo
            position: Posición inicial
            rotation: Rotación inicial
            
        Returns:
            Dict[str, Any]: Configuración del cuerpo rígido
        """
        return {
            "type": "RigidBody",
            "parameters": {
                "mass": mass,
                "shape": shape,
                "size": size.to_dict(),
                "position": position.to_dict(),
                "rotation": rotation.to_dict()
            }
        }
    
    @staticmethod
    def create_collision_shape(
        shape: str = "box",
        size: Vector3 = Vector3(1, 1, 1),
        offset: Vector3 = Vector3(0, 0, 0)
    ) -> Dict[str, Any]:
        """
        Crea una forma de colisión.
        
        Args:
            shape: Tipo de forma
            size: Tamaño de la forma
            offset: Desplazamiento de la forma
            
        Returns:
            Dict[str, Any]: Configuración de la forma de colisión
        """
        return {
            "type": "CollisionShape",
            "parameters": {
                "shape": shape,
                "size": size.to_dict(),
                "offset": offset.to_dict()
            }
        }
    
    @staticmethod
    def create_constraint(
        body_a: str,
        body_b: str,
        constraint_type: str = "hinge",
        pivot_a: Vector3 = Vector3(0, 0, 0),
        pivot_b: Vector3 = Vector3(0, 0, 0)
    ) -> Dict[str, Any]:
        """
        Crea una restricción entre dos cuerpos.
        
        Args:
            body_a: ID del primer cuerpo
            body_b: ID del segundo cuerpo
            constraint_type: Tipo de restricción
            pivot_a: Punto de pivote en el primer cuerpo
            pivot_b: Punto de pivote en el segundo cuerpo
            
        Returns:
            Dict[str, Any]: Configuración de la restricción
        """
        return {
            "type": "Constraint",
            "parameters": {
                "bodyA": body_a,
                "bodyB": body_b,
                "constraintType": constraint_type,
                "pivotA": pivot_a.to_dict(),
                "pivotB": pivot_b.to_dict()
            }
        } 