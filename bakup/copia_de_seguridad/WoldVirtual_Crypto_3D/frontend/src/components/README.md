# Componentes

Este directorio contiene los componentes reutilizables de la interfaz de usuario.

## Estructura

```
components/
├── Navbar.js           # Barra de navegación principal
├── Scene3D.js          # Renderizador de escenas 3D
├── SceneCard.js        # Tarjeta de visualización de escena
├── AssetCard.js        # Tarjeta de visualización de activo
├── WalletConnect.js    # Conexión con wallet
├── LoadingSpinner.js   # Indicador de carga
└── ErrorBoundary.js    # Manejo de errores
```

## Componentes Disponibles

### 1. Navbar
Barra de navegación principal de la aplicación.

```javascript
import { Navbar } from '../components';

function App() {
  return (
    <Navbar
      user={user}
      onConnect={handleConnect}
      onDisconnect={handleDisconnect}
    />
  );
}
```

#### Características
- Navegación principal
- Estado de conexión
- Menú de usuario
- Búsqueda global

### 2. Scene3D
Renderizador de escenas 3D usando Three.js.

```javascript
import { Scene3D } from '../components';

function SceneViewer() {
  return (
    <Scene3D
      sceneData={data}
      onLoad={handleLoad}
      onError={handleError}
    />
  );
}
```

#### Características
- Renderizado 3D
- Controles de cámara
- Interacción con objetos
- Optimización de rendimiento

### 3. SceneCard
Tarjeta para visualizar información de escenas.

```javascript
import { SceneCard } from '../components';

function SceneList() {
  return scenes.map(scene => (
    <SceneCard
      key={scene.id}
      scene={scene}
      onClick={handleClick}
    />
  ));
}
```

#### Características
- Vista previa de escena
- Información básica
- Acciones rápidas
- Estado de carga

### 4. AssetCard
Tarjeta para visualizar información de activos.

```javascript
import { AssetCard } from '../components';

function AssetList() {
  return assets.map(asset => (
    <AssetCard
      key={asset.id}
      asset={asset}
      onBuy={handleBuy}
    />
  ));
}
```

#### Características
- Vista previa de activo
- Información de precio
- Estado de propiedad
- Acciones de compra

### 5. WalletConnect
Componente para conectar wallets.

```javascript
import { WalletConnect } from '../components';

function ConnectWallet() {
  return (
    <WalletConnect
      onConnect={handleConnect}
      onDisconnect={handleDisconnect}
    />
  );
}
```

#### Características
- Lista de wallets
- Estado de conexión
- Manejo de errores
- Persistencia

### 6. LoadingSpinner
Indicador de carga.

```javascript
import { LoadingSpinner } from '../components';

function LoadingState() {
  return (
    <LoadingSpinner
      size="lg"
      color="brand.500"
    />
  );
}
```

#### Características
- Diferentes tamaños
- Colores personalizables
- Mensajes opcionales
- Animaciones

### 7. ErrorBoundary
Manejo de errores en componentes.

```javascript
import { ErrorBoundary } from '../components';

function App() {
  return (
    <ErrorBoundary
      fallback={ErrorComponent}
      onError={handleError}
    >
      <MainContent />
    </ErrorBoundary>
  );
}
```

#### Características
- Captura de errores
- Componente de fallback
- Logging de errores
- Recuperación

## Uso de Componentes

### Ejemplo de Composición
```javascript
import { Navbar, Scene3D, SceneCard } from '../components';

function MainPage() {
  return (
    <>
      <Navbar />
      <main>
        <Scene3D />
        <div className="scenes-grid">
          {scenes.map(scene => (
            <SceneCard key={scene.id} scene={scene} />
          ))}
        </div>
      </main>
    </>
  );
}
```

### Ejemplo de Props
```javascript
<Scene3D
  sceneData={data}
  cameraPosition={[0, 5, 10]}
  onObjectClick={handleClick}
  showGrid={true}
  showAxes={true}
  backgroundColor="#000000"
/>
```

## Buenas Prácticas

1. **Diseño**
   - Componentes pequeños
   - Props tipadas
   - Documentación clara
   - Estilos modulares

2. **Rendimiento**
   - Memoización
   - Lazy loading
   - Optimización de renders
   - Code splitting

3. **Accesibilidad**
   - ARIA labels
   - Navegación por teclado
   - Contraste adecuado
   - Textos alternativos

4. **Testing**
   - Pruebas unitarias
   - Pruebas de integración
   - Pruebas de accesibilidad
   - Snapshot testing

## Contribución

1. **Nuevo Componente**
   - Crear archivo separado
   - Documentar props
   - Añadir tests
   - Incluir ejemplos

2. **Modificación**
   - Mantener compatibilidad
   - Actualizar documentación
   - Verificar tests
   - Actualizar ejemplos

3. **Eliminación**
   - Verificar dependencias
   - Actualizar imports
   - Documentar cambios
   - Migrar funcionalidad 