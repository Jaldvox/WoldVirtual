import React, { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';
import Entity3D from './Entity3D'; // Nuevo componente base para cualquier entidad 3D
import useAppSecurity from '../../utils/useAppSecurity';

/**
 * Canvas principal que renderiza la escena 3D completa según los datos del backend.
 * - Consume /api/get_scene_data
 * - Renderiza dinámicamente todos los objetos de la escena
 *
 * FALTANTE / PRÓXIMAS FASES:
 * - Soporte para más tipos de entidades (planos, esferas, luces, cámaras, etc.).
 * - Integración de controles avanzados (OrbitControls, navegación FPS, etc.).
 * - Sincronización en tiempo real con Reflex vía WebSocket (actualmente solo REST).
 * - Optimización: frustum culling, LOD, instancing, pooling de objetos.
 * - Integración de materiales PBR, texturas y assets desde IPFS/Arweave.
 * - Manejo de animaciones y blending entre estados.
 * - Gestión avanzada de eventos (drag, hover, selección múltiple, lógica de juego).
 * - Mejor tipado y modularización (TypeScript recomendado).
 * - Documentar la estructura esperada de sceneData y objetos.
 */
const ThreeCanvas = () => {
  const mountRef = useRef(null);
  const sceneRef = useRef();
  const cameraRef = useRef();
  const rendererRef = useRef();
  const [objects, setObjects] = useState([]);
  const [sceneEnv, setSceneEnv] = useState({});
  const [entityMeshes, setEntityMeshes] = useState([]);

  // Hook de seguridad y validación
  const { warnings, errors, validateEntity } = useAppSecurity();

  // Mostrar errores críticos en la UI
  if (errors.length) {
    return <div style={{ color: 'red', padding: 16 }}>Error crítico: {errors[0]}</div>;
  }
  // Mostrar advertencias en la UI (opcional)
  // Puedes personalizar el estilo o mostrar un banner
  // if (warnings.length) {
  //   return <div style={{ color: 'orange', padding: 16 }}>Advertencia: {warnings[0]}</div>;
  // }

  // Fetch inicial de la escena y objetos
  useEffect(() => {
    fetch('/api/get_scene_data')
      .then(res => res.json())
      .then(data => {
        setObjects(data.objects_in_scene || []);
        setSceneEnv(data.escena?.environment || {});
      });
  }, []);

  // Inicialización de Three.js
  useEffect(() => {
    const width = mountRef.current.clientWidth;
    const height = mountRef.current.clientHeight;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.z = 5;
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    mountRef.current.appendChild(renderer.domElement);

    // Iluminación básica (puede ampliarse con sceneEnv)
    const ambient = sceneEnv.lighting?.ambient || { color: '#ffffff', intensity: 0.5 };
    const ambientLight = new THREE.AmbientLight(ambient.color, ambient.intensity);
    scene.add(ambientLight);

    sceneRef.current = scene;
    cameraRef.current = camera;
    rendererRef.current = renderer;

    // FALTA: integración de controles avanzados (OrbitControls, FPS, etc.)

    // Animación
    const animate = function () {
      requestAnimationFrame(animate);
      renderer.render(scene, camera);
    };
    animate();

    // Limpieza
    return () => {
      mountRef.current.removeChild(renderer.domElement);
    };
  }, [sceneEnv]);

  // Renderizar entidades 3D dinámicamente
  useEffect(() => {
    if (!sceneRef.current) return;
    // Limpiar entidades previas
    while (sceneRef.current.children.length > 1) {
      sceneRef.current.remove(sceneRef.current.children[1]);
    }
    // Añadir entidades (solo si son válidas)
    const newMeshes = [];
    objects.forEach((obj) => {
      if (!validateEntity(obj)) return; // Validación de seguridad
      const mesh = Entity3D(obj, handleEntityEvent);
      if (mesh) {
        sceneRef.current.add(mesh);
        newMeshes.push(mesh);
      }
    });
    setEntityMeshes(newMeshes);
  }, [objects]);

  // Raycaster para detectar clics en entidades
  useEffect(() => {
    if (!rendererRef.current || !cameraRef.current || !entityMeshes.length) return;
    const renderer = rendererRef.current;
    const camera = cameraRef.current;
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    function onClick(event) {
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(entityMeshes);
      if (intersects.length > 0) {
        const instance_id = intersects[0].object.userData.instance_id;
        handleEntityEvent({ type: 'click', instance_id });
      }
    }
    renderer.domElement.addEventListener('click', onClick);
    return () => {
      renderer.domElement.removeEventListener('click', onClick);
    };
  }, [entityMeshes]);

  // Manejar evento en entidad 3D (ejemplo: clic)
  function handleEntityEvent({ type, instance_id }) {
    if (type === 'click') {
      fetch('/api/process_object_click', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instance_id }),
      })
        .then(res => res.json())
        .then(() => {
          // Refrescar la escena tras el evento
          fetch('/api/get_scene_data')
            .then(res => res.json())
            .then(data => {
              setObjects(data.objects_in_scene || []);
            });
        });
    }
  }

  return (
    <div ref={mountRef} style={{ width: '100%', height: '400px', borderRadius: '1em', background: '#111' }} />
  );
};

export default ThreeCanvas; 