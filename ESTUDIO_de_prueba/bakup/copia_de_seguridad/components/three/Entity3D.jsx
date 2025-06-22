import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

/**
 * Crea una entidad 3D (mesh) a partir de los datos recibidos del backend.
 * Soporta cubos y modelos glTF (por URL). Se puede ampliar para más tipos.
 * @param {Object} obj - Datos del objeto (instance_id, asset_url, asset_type, color, transform, etc.)
 * @param {Function} onEvent - Callback para eventos (ej. clic)
 * @returns {THREE.Mesh|THREE.Group|null}
 *
 * FALTANTE / PRÓXIMAS FASES:
 * - Soporte para más tipos de entidades: planos, esferas, luces, cámaras, etc.
 * - Integración de animaciones (GLTF y personalizadas).
 * - Manejo de eventos avanzados: drag, hover, selección múltiple.
 * - Sincronización de estado en tiempo real con Reflex (WebSocket).
 * - Optimización: instancing, pooling, LOD.
 * - Integración de materiales PBR y texturas desde IPFS/Arweave.
 * - Documentar y tipar mejor los datos de entrada (TypeScript recomendado).
 */
function Entity3D(obj, onEvent) {
  // Cubo simple
  if (obj.asset_type === '3d_model' && obj.asset_url.endsWith('.cube')) {
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshStandardMaterial({ color: obj.color || '#0077ff' });
    const mesh = new THREE.Mesh(geometry, material);
    if (obj.transform) {
      mesh.position.set(...(obj.transform.position || [0,0,0]));
      mesh.rotation.set(...(obj.transform.rotation || [0,0,0]));
      mesh.scale.set(...(obj.transform.scale || [1,1,1]));
    }
    mesh.userData = { instance_id: obj.instance_id };
    // FALTA: conectar eventos (onEvent) y lógica avanzada
    return mesh;
  }
  // Modelo glTF
  if (obj.asset_type === '3d_model' && obj.asset_url.endsWith('.gltf')) {
    const group = new THREE.Group();
    const loader = new GLTFLoader();
    loader.load(obj.asset_url, (gltf) => {
      group.add(gltf.scene);
      if (obj.transform) {
        group.position.set(...(obj.transform.position || [0,0,0]));
        group.rotation.set(...(obj.transform.rotation || [0,0,0]));
        group.scale.set(...(obj.transform.scale || [1,1,1]));
      }
      group.userData = { instance_id: obj.instance_id };
      // FALTA: integración de animaciones y eventos
    });
    return group;
  }
  // Otros tipos pueden añadirse aquí
  // FALTA: soporte para planos, esferas, luces, cámaras, etc.
  return null;
}

export default Entity3D; 