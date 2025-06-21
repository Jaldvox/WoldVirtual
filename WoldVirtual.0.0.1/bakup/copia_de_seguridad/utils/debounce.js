// debounce.js
// Ejecuta una función después de un retraso, ignorando llamadas repetidas en ese intervalo.
// Útil para evitar llamadas excesivas a endpoints o renders (ej: búsqueda en tiempo real).
//
// Ejemplo de uso:
// debounce('buscar', () => buscarAPI(valor), 300);

const debounce_timeout_id = {};

/**
 * debounce: Ejecuta una función después de un retraso, ignorando llamadas repetidas en ese intervalo.
 * @param {string} name - Nombre del evento.
 * @param {function} func - Función a ejecutar.
 * @param {number} delay - Milisegundos de espera.
 */
export default function debounce(name, func, delay) {
  const key = `${name}__${delay}`;
  clearTimeout(debounce_timeout_id[key]);
  debounce_timeout_id[key] = setTimeout(() => {
    func();
    delete debounce_timeout_id[key];
  }, delay);
} 