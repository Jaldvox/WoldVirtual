// throttle.js
// Limita la frecuencia con la que se puede ejecutar una función.
// Útil para eventos de scroll, resize, o acciones rápidas del usuario.
//
// Ejemplo de uso:
// if (throttle('scroll', 200)) { ... }

const in_throttle = {};

/**
 * throttle: Limita la frecuencia de ejecución de una función.
 * @param {string} name - Nombre del evento.
 * @param {number} limit - Milisegundos entre ejecuciones.
 * @returns {boolean} true si se permite ejecutar, false si está limitado.
 */
export default function throttle(name, limit) {
  const key = `${name}__${limit}`;
  if (!in_throttle[key]) {
    in_throttle[key] = true;
    setTimeout(() => {
      delete in_throttle[key];
    }, limit);
    // Permitir ejecución
    return true;
  }
  // Está limitado
  return false;
} 