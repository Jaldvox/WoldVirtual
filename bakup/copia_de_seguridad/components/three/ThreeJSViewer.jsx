import React, { useRef, useEffect } from 'react';
// Importar Three.js
import * as THREE from 'three';

/**
 * Componente base para visualizar escenas Three.js.
 * Recibe props para datos de escena y eventos.
 *
 * FALTANTE / PRÓXIMAS FASES:
 * - Renderizado dinámico de entidades y assets desde sceneData (actualmente solo un cubo fijo).
 * - Integración de controles avanzados (OrbitControls, navegación, etc.).
 * - Recepción y sincronización de estado desde Reflex (props, WebSocket, REST).
 * - Emisión de eventos de usuario (clic, drag, selección) hacia el backend.
 * - Soporte para modelos glTF, texturas, materiales PBR, luces avanzadas.
 * - Optimización: limpieza de recursos, resize, pooling, LOD.
 * - Modularización y mejor tipado (TypeScript recomendado).
 * - Documentar la estructura esperada de sceneData y eventos.
 */
const ThreeJSViewer = ({ sceneData }) => {
  const mountRef = useRef(null);

  useEffect(() => {
    // Inicializar escena, cámara y renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, mountRef.current.clientWidth / mountRef.current.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
    mountRef.current.appendChild(renderer.domElement);

    // Ejemplo: añadir un cubo
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshStandardMaterial({ color: 0x0077ff });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    // Luz básica
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(5, 10, 7.5);
    scene.add(light);

    camera.position.z = 5;

    // Animación
    const animate = function () {
      requestAnimationFrame(animate);
      cube.rotation.x += 0.01;
      cube.rotation.y += 0.01;
      renderer.render(scene, camera);
    };
    animate();

    // FALTA: renderizado dinámico de entidades y assets desde sceneData
    // FALTA: integración de controles avanzados y eventos

    // Limpieza
    return () => {
      mountRef.current.removeChild(renderer.domElement);
    };
  }, [sceneData]);

  return (
    <div ref={mountRef} style={{ width: '100%', height: '400px', borderRadius: '1em', background: '#111' }}>
      {/* Aquí se renderiza la escena Three.js */}
    </div>
  );
};

export default ThreeJSViewer; 