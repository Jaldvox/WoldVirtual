import React, { createContext, useContext, useState, useEffect } from 'react';

// Contexto para el modo de color (oscuro/claro/sistema)
export const ColorModeContext = createContext({
  colorMode: 'light',
  setColorMode: () => {},
  toggleColorMode: () => {},
});

/**
 * Proveedor de modo de color para React puro.
 * Permite alternar entre modo claro, oscuro y sistema.
 *
 * Ejemplo de uso:
 * <ColorModeProvider>
 *   <App />
 * </ColorModeProvider>
 *
 * Para cambiar el modo desde cualquier componente:
 * const { colorMode, toggleColorMode, setColorMode } = useContext(ColorModeContext);
 */
export function ColorModeProvider({ defaultMode = 'light', children }) {
  const [colorMode, setColorModeState] = useState(() => {
    // Intenta leer del localStorage o usa el modo por defecto
    return localStorage.getItem('colorMode') || defaultMode;
  });

  useEffect(() => {
    document.body.setAttribute('data-theme', colorMode);
    localStorage.setItem('colorMode', colorMode);
  }, [colorMode]);

  const setColorMode = (mode) => {
    if (["light", "dark", "system"].includes(mode)) {
      setColorModeState(mode);
    }
  };

  const toggleColorMode = () => {
    setColorModeState((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  return (
    <ColorModeContext.Provider value={{ colorMode, setColorMode, toggleColorMode }}>
      {children}
    </ColorModeContext.Provider>
  );
} 