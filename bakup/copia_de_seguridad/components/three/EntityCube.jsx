import * as THREE from 'three';

/**
 * Crea un cubo Three.js con propiedades y eventos.
 * @param {Object} entity - Propiedades del cubo (posición, rotación, escala, color, id).
 * @param {Function} onEntityEvent - Callback para eventos (ej. clic).
 * @returns {THREE.Mesh}
 *
 * FALTANTE / PRÓXIMAS FASES:
 * - Integrar eventos avanzados: drag, hover, selección múltiple, animaciones.
 * - Sincronización de estado en tiempo real con Reflex (WebSocket).
 * - Optimización: instancing para cubos masivos, pooling.
 * - Integración de materiales PBR y texturas desde IPFS/Arweave.
 * - Mejor tipado y documentación de los datos de entrada (TypeScript recomendado).
 * - Unificar la gestión de eventos con el render loop principal y el raycaster global.
 * - Permitir cubos interactivos con lógica de juego (ej: recoger, mover, destruir).
 */
function EntityCube(entity, onEntityEvent) {
  const geometry = new THREE.BoxGeometry();
  const material = new THREE.MeshStandardMaterial({ color: entity.color || 0x0077ff });
  const cube = new THREE.Mesh(geometry, material);
  // Posición, rotación, escala
  if (entity.position) cube.position.set(...entity.position);
  if (entity.rotation) cube.rotation.set(...entity.rotation);
  if (entity.scale) cube.scale.set(...entity.scale);
  // Evento de clic
  cube.userData = { id: entity.id };
  cube.callback = (event) => {
    if (onEntityEvent) onEntityEvent({ type: 'click', id: entity.id });
  };
  // (La gestión real de eventos de clic se hace en el render loop principal)
  // FALTA: conectar eventos avanzados y lógica de interacción con Reflex
  return cube;
}

export default EntityCube; 