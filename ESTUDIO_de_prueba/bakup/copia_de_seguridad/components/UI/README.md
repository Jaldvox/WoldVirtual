# UI Components

Esta carpeta contendrá los componentes de interfaz de usuario (UI) para el frontend 3D del metaverso. Ejemplos: botones, menús, overlays, paneles de información, etc.

Cada componente debe ser modular y reutilizable.

# UserProfile.jsx

Componente de perfil de usuario para el metaverso 3D.

## ¿Qué hace?
- Muestra el perfil público y privado del usuario (avatar, nombre, estado, inventario).
- Permite editar el avatar, cambiar el estado (conectado/ausente) y añadir/eliminar assets del inventario.
- Consume los endpoints REST del backend Reflex:
  - `/api/get_user_public_profile`
  - `/api/get_user_private_profile`
  - `/api/update_user_avatar`
  - `/api/add_asset_to_user`
  - `/api/remove_asset_from_user`
  - `/api/set_user_status`

## ¿Cómo integrarlo?
1. Asegúrate de tener el hook `useUser` en `../../hooks/useUser.js`.
2. Importa y usa el componente en tu app principal o en cualquier página:

```jsx
import UserProfile from './components/UI/UserProfile';

function App() {
  return (
    <div>
      <UserProfile />
      {/* ...otros componentes... */}
    </div>
  );
}
```

## Dependencias
- React 17+
- El backend Reflex debe estar corriendo y exponer los endpoints mencionados.

## Notas
- El componente es totalmente funcional con el backend actual (usuario simulado).
- Cuando se implemente autenticación real, adapta el hook para manejar tokens/sesión.

---

# ColorModeProvider.jsx

Proveedor de modo de color (oscuro/claro/sistema) para React puro.

## ¿Qué hace?
- Permite alternar entre modo claro, oscuro y sistema en toda la app.
- Expone un contexto para acceder y cambiar el modo desde cualquier componente.

## Ejemplo de uso
```jsx
import { ColorModeProvider, ColorModeContext } from './components/UI/ColorModeProvider';

function App() {
  const { colorMode, toggleColorMode } = React.useContext(ColorModeContext);
  return (
    <ColorModeProvider>
      <button onClick={toggleColorMode}>Alternar modo: {colorMode}</button>
      {/* ...otros componentes... */}
    </ColorModeProvider>
  );
}
```

---

# CodeBlock.jsx

Componente para resaltar sintaxis de código usando Shiki.

## ¿Qué hace?
- Muestra bloques de código con resaltado de sintaxis para múltiples lenguajes y temas.
- Útil para documentación, tutoriales, foros, etc.

## Ejemplo de uso
```jsx
import CodeBlock from './components/UI/CodeBlock';

<CodeBlock code={"console.log('Hola mundo')"} language="js" theme="nord" />
```

## Dependencias
- Instala la librería shiki:
  ```bash
  npm install shiki
  ```

--- 