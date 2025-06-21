import React from 'react';
import { ColorModeProvider } from './components/UI/ColorModeProvider';
import ThreeCanvas from './components/three/ThreeCanvas';
import UserProfile from './components/UI/UserProfile';

// Estilos básicos adaptativos
const appStyles = {
  minHeight: '100vh',
  display: 'flex',
  flexDirection: 'column',
  background: 'linear-gradient(135deg, #7b92e6 0%, #4e54c8 100%)',
};
const headerStyles = {
  background: '#ffe000',
  color: '#222',
  padding: '0.5em 2em',
  fontWeight: 'bold',
  fontSize: '1.5em',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  borderRadius: '1em 1em 0 0',
  minHeight: 60,
};
const mainStyles = {
  flex: 1,
  display: 'flex',
  flexDirection: 'row',
  gap: 32,
  justifyContent: 'center',
  alignItems: 'flex-start',
  padding: '2em 1em',
};
const leftPanel = {
  minWidth: 320,
  maxWidth: 400,
  flex: '0 1 400px',
};
const centerPanel = {
  flex: 1,
  minWidth: 350,
  maxWidth: 900,
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
};

// App principal
export default function App() {
  return (
    <ColorModeProvider>
      <div style={appStyles}>
        {/* Barra superior */}
        <header style={headerStyles}>
          <span>WoldVirtual</span>
          <nav style={{ display: 'flex', gap: 24, fontSize: '1em' }}>
            <a href="#mapa" style={{ color: '#222', textDecoration: 'none' }}>Mapa del proyecto</a>
            <a href="#libro" style={{ color: '#222', textDecoration: 'none' }}>Libro blanco</a>
            <a href="#codigo" style={{ color: '#222', textDecoration: 'none' }}>Código abierto</a>
            <span style={{ background: '#222', color: '#fff', borderRadius: 8, padding: '0.2em 0.7em', marginLeft: 12, fontSize: '0.9em' }}>Binance Smart Chain</span>
          </nav>
        </header>
        {/* Área principal */}
        <main style={mainStyles}>
          {/* Panel izquierdo: perfil de usuario */}
          <div style={leftPanel}>
            <UserProfile />
          </div>
          {/* Panel central: escena 3D */}
          <div style={centerPanel}>
            <h2 style={{ color: '#222', marginBottom: 12 }}>Área 3D Interactiva</h2>
            <ThreeCanvas />
            {/* Espacio para mensajes, advertencias, controles futuros */}
            <div style={{ marginTop: 16, color: '#666', fontSize: '0.95em' }}>
              <em>El área 3D se ajusta automáticamente al tamaño de la ventana.<br />Prueba redimensionar para ver el diseño adaptativo.</em>
            </div>
          </div>
        </main>
        {/* Footer opcional */}
        <footer style={{ textAlign: 'center', color: '#fff', padding: 12, fontSize: '0.95em', opacity: 0.7 }}>
          WoldVirtual &copy; {new Date().getFullYear()} | Proyecto modular, escalable y descentralizado.
        </footer>
      </div>
    </ColorModeProvider>
  );
}
// NOTA: Puedes mejorar el diseño con media queries, styled-components o Tailwind en futuras fases.
// Pruebas adaptativas: redimensiona la ventana, prueba en móvil y desktop, revisa el contraste y la accesibilidad. 