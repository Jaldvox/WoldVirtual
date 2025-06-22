import reflex as rx
from state import WoldVirtualState

class Scene3D(rx.Component):
    """Componente para la escena 3D."""
    
    def _get_imports(self):
        return {
            "three": "https://unpkg.com/three@0.158.0/build/three.module.js",
            "@react-three/fiber": "https://unpkg.com/@react-three/fiber@8.15.0/dist/react-three-fiber.umd.js",
            "@react-three/drei": "https://unpkg.com/@react-three/drei@9.88.0/dist/drei.umd.js",
        }
    
    def _get_custom_code(self):
        return """
        import { Canvas } from '@react-three/fiber'
        import { OrbitControls, Box } from '@react-three/drei'
        
        function Scene() {
            return (
                <Canvas>
                    <ambientLight intensity={0.5} />
                    <pointLight position={[10, 10, 10]} />
                    <Box position={[-1.2, 0, 0]}>
                        <meshStandardMaterial color="orange" />
                    </Box>
                    <Box position={[1.2, 0, 0]}>
                        <meshStandardMaterial color="hotpink" />
                    </Box>
                    <OrbitControls />
                </Canvas>
            )
        }
        """
    
    def render(self):
        return rx.box(
            rx.script(self._get_custom_code()),
            width="100%",
            height="100%",
            position="absolute",
            top=0,
            left=0,
        ) 