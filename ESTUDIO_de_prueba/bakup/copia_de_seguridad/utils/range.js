// range.js
// Simula la función range() de Python en JavaScript.
// Permite crear secuencias numéricas fácilmente.
//
// Ejemplo de uso:
// [...range(1, 5)] => [1, 2, 3, 4]

/**
 * range: Genera una secuencia de números como en Python.
 * @param {number} start - Inicio o fin de la secuencia.
 * @param {number} stop - Fin de la secuencia.
 * @param {number} step - Paso de la secuencia.
 * @returns {object} Un iterable con Symbol.iterator
 */
export default function range(start, stop, step) {
  return {
    [Symbol.iterator]() {
      if (stop === undefined) {
        stop = start;
        start = 0;
      }
      if (step === undefined) {
        step = 1;
      }
      let i = start - step;
      return {
        next() {
          i += step;
          if ((step > 0 && i < stop) || (step < 0 && i > stop)) {
            return {
              value: i,
              done: false,
            };
          }
          return {
            value: undefined,
            done: true,
          };
        },
      };
    },
  };
} 