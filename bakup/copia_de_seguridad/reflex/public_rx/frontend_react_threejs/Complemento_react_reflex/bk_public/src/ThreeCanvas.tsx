import React from "react";

// Puedes definir aquí los tipos de props que quieras recibir desde Python
interface ThreeCanvasProps {
  sceneData?: any; // Ejemplo: datos de la escena enviados desde Reflex
  on_event?: () => void; // Handler recibido desde Reflex, sin argumentos
}

/**
 * Componente avanzado para integración Reflex + Three.js
 * Aquí puedes importar y usar Three.js, y comunicarte con Reflex vía props.
 */
const ThreeCanvas: React.FC<ThreeCanvasProps> = (props) => {
  // Enviar evento a Python al hacer clic
  const handleClick = () => {
    if (props.on_event) {
      props.on_event(); // Sin argumentos
    }
  };

  // Ejemplo: renderizar datos recibidos desde Python
  return (
    <div
      style={{ width: "100%", height: "400px", background: "#222", color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", borderRadius: "12px", cursor: "pointer" }}
      onClick={handleClick}
    >
      <p>Escena 3D (Three.js) - Integración avanzada</p>
      {props.sceneData && (
        <pre style={{ color: '#0f0', fontSize: '0.8em' }}>{JSON.stringify(props.sceneData, null, 2)}</pre>
      )}
    </div>
  );
};

export default ThreeCanvas; 