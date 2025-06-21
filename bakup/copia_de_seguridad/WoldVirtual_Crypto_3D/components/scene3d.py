"""Componente de escena 3D con funcionalidades avanzadas."""
import reflex as rx
from typing import Dict, List, Optional, Tuple
from ..state import State

class Scene3D(rx.Component):
    """Componente para la escena 3D con funcionalidades avanzadas."""
    
    def _get_imports(self):
        return {
            "three": "https://unpkg.com/three@0.158.0/build/three.module.js",
            "@react-three/fiber": "https://unpkg.com/@react-three/fiber@8.15.0/dist/react-three-fiber.umd.js",
            "@react-three/drei": "https://unpkg.com/@react-three/drei@9.88.0/dist/drei.umd.js",
            "zustand": "https://unpkg.com/zustand@4.4.1/umd/index.production.js"
        }
    
    def _get_custom_code(self):
        return """
        import { Canvas, useThree, useFrame } from '@react-three/fiber'
        import { 
            OrbitControls, 
            PerspectiveCamera,
            Environment,
            Grid,
            GizmoHelper,
            GizmoViewport,
            useHelper,
            Box,
            Sphere,
            Cylinder,
            Plane,
            PointLight,
            DirectionalLight,
            SpotLight
        } from '@react-three/drei'
        import { useRef, useState, useEffect } from 'react'
        import * as THREE from 'three'
        
        // Store para el estado de la escena
        const useStore = zustand.create((set) => ({
            selectedObject: null,
            setSelectedObject: (obj) => set({ selectedObject: obj }),
            objects: [],
            addObject: (obj) => set((state) => ({ objects: [...state.objects, obj] })),
            removeObject: (id) => set((state) => ({ 
                objects: state.objects.filter(obj => obj.id !== id) 
            })),
            updateObject: (id, props) => set((state) => ({
                objects: state.objects.map(obj => 
                    obj.id === id ? { ...obj, ...props } : obj
                )
            }))
        }))
        
        // Componente para objetos seleccionables
        function SelectableObject({ type, position, rotation, scale, material, id }) {
            const meshRef = useRef()
            const [hovered, setHovered] = useState(false)
            const [selected, setSelected] = useState(false)
            const store = useStore()
            
            // Manejar selección
            const handleClick = (e) => {
                e.stopPropagation()
                store.setSelectedObject({ id, type, position, rotation, scale, material })
                setSelected(true)
            }
            
            // Renderizar objeto según tipo
            const renderObject = () => {
                const props = {
                    position: position,
                    rotation: rotation,
                    scale: scale,
                    onClick: handleClick,
                    onPointerOver: () => setHovered(true),
                    onPointerOut: () => setHovered(false),
                    ref: meshRef
                }
                
                switch(type) {
                    case 'box':
                        return <Box {...props}><meshStandardMaterial {...material} /></Box>
                    case 'sphere':
                        return <Sphere {...props}><meshStandardMaterial {...material} /></Sphere>
                    case 'cylinder':
                        return <Cylinder {...props}><meshStandardMaterial {...material} /></Cylinder>
                    case 'plane':
                        return <Plane {...props}><meshStandardMaterial {...material} /></Plane>
                    default:
                        return null
                }
            }
            
            return renderObject()
        }
        
        // Componente para luces
        function Light({ type, position, intensity, color, angle, penumbra }) {
            switch(type) {
                case 'point':
                    return <PointLight position={position} intensity={intensity} color={color} />
                case 'directional':
                    return <DirectionalLight position={position} intensity={intensity} color={color} />
                case 'spot':
                    return <SpotLight 
                        position={position} 
                        intensity={intensity} 
                        color={color}
                        angle={angle}
                        penumbra={penumbra}
                    />
                default:
                    return null
            }
        }
        
        // Componente principal de la escena
        function Scene() {
            const store = useStore()
            const { camera } = useThree()
            
            // Configuración inicial de la cámara
            useEffect(() => {
                camera.position.set(5, 5, 5)
                camera.lookAt(0, 0, 0)
            }, [])
            
            // Actualizar frame
            useFrame((state, delta) => {
                // Aquí se pueden añadir animaciones y actualizaciones
            })
            
            return (
                <Canvas shadows>
                    <PerspectiveCamera makeDefault />
                    <OrbitControls 
                        enableDamping 
                        dampingFactor={0.05}
                        minDistance={3}
                        maxDistance={20}
                    />
                    
                    {/* Iluminación ambiente */}
                    <ambientLight intensity={0.5} />
                    
                    {/* Grid y ayudas visuales */}
                    <Grid 
                        infiniteGrid 
                        cellSize={1} 
                        cellThickness={0.5}
                        sectionSize={3}
                        sectionThickness={1}
                    />
                    <GizmoHelper>
                        <GizmoViewport />
                    </GizmoHelper>
                    
                    {/* Objetos de la escena */}
                    {store.objects.map(obj => (
                        <SelectableObject key={obj.id} {...obj} />
                    ))}
                    
                    {/* Luces de la escena */}
                    <Light 
                        type="directional"
                        position={[5, 5, 5]}
                        intensity={1}
                        color="#ffffff"
                    />
                    
                    {/* Ambiente */}
                    <Environment preset="sunset" />
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
            background="black",
        ) 