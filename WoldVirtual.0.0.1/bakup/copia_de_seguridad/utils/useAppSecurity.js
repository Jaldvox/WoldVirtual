import { useEffect, useState } from 'react';

/**
 * Hook de seguridad y validación para el frontend 3D.
 * - Chequea dependencias críticas (Three.js, loaders).
 * - Detecta entorno (desarrollo/producción) y muestra advertencias.
 * - Valida datos de entrada (entidades) antes de renderizar.
 * - Expone advertencias y errores para mostrar en la UI y consola.
 *
 * Ejemplo de uso:
 * const { warnings, errors, validateEntity } = useAppSecurity();
 * if (errors.length) return <div>Error crítico: {errors[0]}</div>;
 */
export default function useAppSecurity() {
  const [warnings, setWarnings] = useState([]);
  const [errors, setErrors] = useState([]);

  // Chequeo de dependencias críticas
  useEffect(() => {
    const localWarnings = [];
    const localErrors = [];
    if (!window.THREE && typeof THREE === 'undefined') {
      localErrors.push('Three.js no está cargado. La app 3D no funcionará.');
    }
    try {
      require('three/examples/jsm/loaders/GLTFLoader');
    } catch {
      localErrors.push('GLTFLoader no está disponible. No se podrán cargar modelos glTF.');
    }
    // Advertencia de entorno
    if (process.env.NODE_ENV !== 'production') {
      localWarnings.push('Estás en modo desarrollo. No exponer endpoints sensibles ni datos críticos.');
    }
    setWarnings(localWarnings);
    setErrors(localErrors);
    if (localWarnings.length) localWarnings.forEach(w => console.warn(w));
    if (localErrors.length) localErrors.forEach(e => console.error(e));
  }, []);

  // Validación de datos de entidad
  function validateEntity(entity) {
    if (!entity || typeof entity !== 'object') return false;
    if (!entity.asset_type || !entity.asset_url) return false;
    // Validar tipos y rangos básicos
    if (entity.position && !Array.isArray(entity.position)) return false;
    if (entity.color && typeof entity.color !== 'string' && typeof entity.color !== 'number') return false;
    // Validar URLs (solo http/https/ipfs)
    if (entity.asset_url && !/^https?:\/\//.test(entity.asset_url) && !entity.asset_url.startsWith('ipfs://')) return false;
    // FALTA: Validaciones más estrictas según el tipo de entidad
    return true;
  }

  return { warnings, errors, validateEntity };
} 