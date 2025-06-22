# Hooks Personalizados

Este directorio contiene los hooks personalizados utilizados en toda la aplicación para manejar la lógica de negocio y el estado.

## Estructura

```
hooks/
├── useWallet.js         # Gestión de wallet y Web3
├── useScene.js          # Gestión de escenas 3D
├── useAsset.js          # Gestión de activos
├── useUser.js           # Gestión de usuario
├── useFileUpload.js     # Subida de archivos
├── useTheme.js          # Gestión de tema
└── useNotification.js   # Sistema de notificaciones
```

## Hooks Disponibles

### 1. useWallet
Gestiona la conexión con wallets y operaciones Web3.

```javascript
const { 
  account,
  connect,
  disconnect,
  isConnecting,
  error 
} = useWallet();
```

#### Características
- Conexión con MetaMask y otros proveedores
- Manejo de estado de la wallet
- Operaciones de firma
- Gestión de red

### 2. useScene
Maneja la lógica de escenas 3D.

```javascript
const {
  scene,
  loadScene,
  saveScene,
  updateScene,
  deleteScene
} = useScene();
```

#### Características
- Carga de escenas
- Guardado de cambios
- Actualización de propiedades
- Gestión de assets en escena

### 3. useAsset
Gestiona los activos digitales.

```javascript
const {
  assets,
  uploadAsset,
  deleteAsset,
  updateAsset,
  getAssetDetails
} = useAsset();
```

#### Características
- Subida de activos
- Gestión de metadatos
- Operaciones CRUD
- Validación de tipos

### 4. useUser
Maneja la información y estado del usuario.

```javascript
const {
  user,
  updateProfile,
  getProfile,
  logout,
  isAuthenticated
} = useUser();
```

#### Características
- Gestión de perfil
- Autenticación
- Preferencias
- Estado de sesión

### 5. useFileUpload
Gestiona la subida de archivos.

```javascript
const {
  uploadFile,
  progress,
  error,
  reset
} = useFileUpload();
```

#### Características
- Subida de archivos
- Barra de progreso
- Validación de tipos
- Manejo de errores

### 6. useTheme
Maneja el tema de la aplicación.

```javascript
const {
  isDark,
  toggleTheme,
  colors,
  setTheme
} = useTheme();
```

#### Características
- Modo claro/oscuro
- Colores personalizados
- Persistencia de tema
- Accesibilidad

### 7. useNotification
Gestiona las notificaciones del sistema.

```javascript
const {
  showSuccess,
  showError,
  showWarning,
  showInfo
} = useNotification();
```

#### Características
- Diferentes tipos de notificaciones
- Personalización de mensajes
- Duración configurable
- Posicionamiento

## Uso de los Hooks

### Ejemplo Básico
```javascript
import { useWallet, useScene } from '../hooks';

function MyComponent() {
  const { account, connect } = useWallet();
  const { scene, loadScene } = useScene();

  // Usar los hooks...
}
```

### Combinación de Hooks
```javascript
function ComplexComponent() {
  const { user } = useUser();
  const { scene } = useScene();
  const { showSuccess } = useNotification();

  // Lógica combinada...
}
```

## Buenas Prácticas

1. **Nombrado**
   - Usar prefijo 'use'
   - Nombres descriptivos
   - Consistencia en el estilo

2. **Implementación**
   - Mantener hooks pequeños
   - Reutilizar lógica común
   - Manejar errores apropiadamente

3. **Rendimiento**
   - Usar useCallback y useMemo
   - Evitar re-renders innecesarios
   - Limpiar efectos secundarios

4. **Testing**
   - Pruebas unitarias
   - Mocks de dependencias
   - Casos de error

## Contribución

1. Crear nuevo hook:
   - Seguir estructura existente
   - Documentar con JSDoc
   - Incluir ejemplos de uso

2. Modificar hook existente:
   - Mantener compatibilidad
   - Actualizar documentación
   - Añadir tests

3. Eliminar hook:
   - Verificar dependencias
   - Actualizar imports
   - Documentar cambios 