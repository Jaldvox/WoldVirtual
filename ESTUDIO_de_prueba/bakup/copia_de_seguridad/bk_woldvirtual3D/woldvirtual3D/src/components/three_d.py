"""
Componentes específicos para 3D en Wold Virtual 3D
Componentes para manejo de escenas, objetos y cámaras 3D
"""

from reflex import html, script
from typing import Optional, List, Dict, Any, Tuple


class Scene3D:
    """Componente para escenas 3D"""
    
    @staticmethod
    def basic(
        scene_id: str = "threejs-scene",
        width: str = "100%",
        height: str = "600px",
        background_color: str = "#87CEEB",
        **kwargs
    ):
        """Escena 3D básica con configuración predefinida"""
        return html.div(
            html.canvas(
                id=scene_id,
                class_name="w-full h-full",
                style={
                    "width": width,
                    "height": height,
                    "background-color": background_color
                }
            ),
            script(src="/static/js/three.min.js"),
            script(src="/static/js/scene.js"),
            class_name="relative",
            **kwargs
        )
    
    @staticmethod
    def interactive(
        scene_id: str = "interactive-scene",
        controls: bool = True,
        lights: bool = True,
        **kwargs
    ):
        """Escena 3D interactiva con controles y luces"""
        return html.div(
            html.canvas(
                id=scene_id,
                class_name="w-full h-full cursor-grab active:cursor-grabbing"
            ),
            script(src="/static/js/three.min.js"),
            script(src="/static/js/controls.js") if controls else None,
            script(src="/static/js/lights.js") if lights else None,
            script(src="/static/js/interactive-scene.js"),
            class_name="relative",
            **kwargs
        )


class Object3D:
    """Componente para objetos 3D"""
    
    @staticmethod
    def cube(
        position: Tuple[float, float, float] = (0, 0, 0),
        size: float = 1.0,
        color: str = "#00ff00",
        **kwargs
    ):
        """Objeto cubo 3D"""
        return html.div(
            script(f"""
                const geometry = new THREE.BoxGeometry({size}, {size}, {size});
                const material = new THREE.MeshBasicMaterial({{ color: '{color}' }});
                const cube = new THREE.Mesh(geometry, material);
                cube.position.set({position[0]}, {position[1]}, {position[2]});
                scene.add(cube);
            """),
            **kwargs
        )
    
    @staticmethod
    def sphere(
        position: Tuple[float, float, float] = (0, 0, 0),
        radius: float = 0.5,
        color: str = "#ff0000",
        **kwargs
    ):
        """Objeto esfera 3D"""
        return html.div(
            script(f"""
                const geometry = new THREE.SphereGeometry({radius}, 32, 32);
                const material = new THREE.MeshBasicMaterial({{ color: '{color}' }});
                const sphere = new THREE.Mesh(geometry, material);
                sphere.position.set({position[0]}, {position[1]}, {position[2]});
                scene.add(sphere);
            """),
            **kwargs
        )
    
    @staticmethod
    def plane(
        position: Tuple[float, float, float] = (0, 0, 0),
        size: Tuple[float, float] = (10, 10),
        color: str = "#cccccc",
        **kwargs
    ):
        """Objeto plano 3D"""
        return html.div(
            script(f"""
                const geometry = new THREE.PlaneGeometry({size[0]}, {size[1]});
                const material = new THREE.MeshBasicMaterial({{ 
                    color: '{color}',
                    side: THREE.DoubleSide 
                }});
                const plane = new THREE.Mesh(geometry, material);
                plane.position.set({position[0]}, {position[1]}, {position[2]});
                plane.rotation.x = -Math.PI / 2;
                scene.add(plane);
            """),
            **kwargs
        )


class Camera3D:
    """Componente para cámaras 3D"""
    
    @staticmethod
    def perspective(
        fov: float = 75,
        aspect: float = 16/9,
        near: float = 0.1,
        far: float = 1000,
        position: Tuple[float, float, float] = (0, 1, 5),
        **kwargs
    ):
        """Cámara perspectiva con configuración personalizable"""
        return html.div(
            script(f"""
                const camera = new THREE.PerspectiveCamera({fov}, {aspect}, {near}, {far});
                camera.position.set({position[0]}, {position[1]}, {position[2]});
            """),
            **kwargs
        )
    
    @staticmethod
    def orthographic(
        left: float = -10,
        right: float = 10,
        top: float = 10,
        bottom: float = -10,
        near: float = 0.1,
        far: float = 1000,
        position: Tuple[float, float, float] = (0, 0, 5),
        **kwargs
    ):
        """Cámara ortográfica para vistas 2D/3D"""
        return html.div(
            script(f"""
                const camera = new THREE.OrthographicCamera({left}, {right}, {top}, {bottom}, {near}, {far});
                camera.position.set({position[0]}, {position[1]}, {position[2]});
            """),
            **kwargs
        )


class Light3D:
    """Componente para luces 3D"""
    
    @staticmethod
    def ambient(
        color: str = "#ffffff",
        intensity: float = 0.5,
        **kwargs
    ):
        """Luz ambiental para iluminación general"""
        return html.div(
            script(f"""
                const ambientLight = new THREE.AmbientLight('{color}', {intensity});
                scene.add(ambientLight);
            """),
            **kwargs
        )
    
    @staticmethod
    def directional(
        color: str = "#ffffff",
        intensity: float = 0.8,
        position: Tuple[float, float, float] = (1, 1, 1),
        **kwargs
    ):
        """Luz direccional para sombras y profundidad"""
        return html.div(
            script(f"""
                const directionalLight = new THREE.DirectionalLight('{color}', {intensity});
                directionalLight.position.set({position[0]}, {position[1]}, {position[2]}).normalize();
                scene.add(directionalLight);
            """),
            **kwargs
        )
    
    @staticmethod
    def point(
        color: str = "#ffffff",
        intensity: float = 1.0,
        position: Tuple[float, float, float] = (0, 5, 0),
        distance: float = 0,
        decay: float = 2,
        **kwargs
    ):
        """Luz puntual para iluminación localizada"""
        return html.div(
            script(f"""
                const pointLight = new THREE.PointLight('{color}', {intensity}, {distance}, {decay});
                pointLight.position.set({position[0]}, {position[1]}, {position[2]});
                scene.add(pointLight);
            """),
            **kwargs
        )
    
    @staticmethod
    def spot(
        color: str = "#ffffff",
        intensity: float = 1.0,
        position: Tuple[float, float, float] = (0, 5, 0),
        target: Tuple[float, float, float] = (0, 0, 0),
        angle: float = 0.3,
        penumbra: float = 0.1,
        distance: float = 0,
        decay: float = 2,
        **kwargs
    ):
        """Luz spot para iluminación focalizada"""
        return html.div(
            script(f"""
                const spotLight = new THREE.SpotLight('{color}', {intensity}, {distance}, {angle}, {penumbra}, {decay});
                spotLight.position.set({position[0]}, {position[1]}, {position[2]});
                spotLight.target.position.set({target[0]}, {target[1]}, {target[2]});
                scene.add(spotLight);
                scene.add(spotLight.target);
            """),
            **kwargs
        ) 