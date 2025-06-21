# Páginas

Este directorio contiene las páginas principales de la aplicación.

## Estructura

```
pages/
├── Home.js           # Página principal
├── Explore.js        # Exploración de escenas
├── Create.js         # Creación de escenas
├── Marketplace.js    # Mercado de activos
├── Profile.js        # Perfil de usuario
├── Scene.js          # Visualización de escena
└── Asset.js          # Detalles de activo
```

## Páginas Disponibles

### 1. Home
Página principal de la aplicación.

```javascript
import { Home } from '../pages';

function App() {
  return (
    <Route path="/" element={<Home />} />
  );
}
```

#### Características
- Dashboard principal
- Escenas destacadas
- Activos populares
- Noticias y actualizaciones

### 2. Explore
Exploración de escenas 3D.

```javascript
import { Explore } from '../pages';

function App() {
  return (
    <Route path="/explore" element={<Explore />} />
  );
}
```

#### Características
- Filtros de búsqueda
- Vista en cuadrícula
- Ordenamiento
- Paginación

### 3. Create
Creación y edición de escenas.

```javascript
import { Create } from '../pages';

function App() {
  return (
    <Route path="/create" element={<Create />} />
  );
}
```

#### Características
- Editor 3D
- Herramientas de diseño
- Importación de assets
- Guardado automático

### 4. Marketplace
Mercado de activos digitales.

```javascript
import { Marketplace } from '../pages';

function App() {
  return (
    <Route path="/marketplace" element={<Marketplace />} />
  );
}
```

#### Características
- Listado de activos
- Filtros de precio
- Categorías
- Sistema de compra

### 5. Profile
Perfil de usuario.

```javascript
import { Profile } from '../pages';

function App() {
  return (
    <Route path="/profile" element={<Profile />} />
  );
}
```

#### Características
- Información personal
- Escenas creadas
- Activos poseídos
- Configuración

### 6. Scene
Visualización de escena individual.

```javascript
import { Scene } from '../pages';

function App() {
  return (
    <Route path="/scene/:id" element={<Scene />} />
  );
}
```

#### Características
- Visualizador 3D
- Información detallada
- Interacción social
- Compartir

### 7. Asset
Detalles de activo individual.

```javascript
import { Asset } from '../pages';

function App() {
  return (
    <Route path="/asset/:id" element={<Asset />} />
  );
}
```

#### Características
- Vista previa 3D
- Información de precio
- Historial de ventas
- Acciones de compra

## Uso de Páginas

### Ejemplo de Rutas
```javascript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Home, Explore, Create, Marketplace, Profile, Scene, Asset } from '../pages';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/explore" element={<Explore />} />
        <Route path="/create" element={<Create />} />
        <Route path="/marketplace" element={<Marketplace />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/scene/:id" element={<Scene />} />
        <Route path="/asset/:id" element={<Asset />} />
      </Routes>
    </BrowserRouter>
  );
}
```

### Ejemplo de Layout
```javascript
function PageLayout({ children }) {
  return (
    <div className="page-container">
      <Navbar />
      <main className="page-content">
        {children}
      </main>
      <Footer />
    </div>
  );
}
```

## Buenas Prácticas

1. **Organización**
   - Páginas independientes
   - Componentes reutilizables
   - Lógica separada
   - Estilos modulares

2. **Rendimiento**
   - Lazy loading
   - Code splitting
   - Optimización de imágenes
   - Caché de datos

3. **SEO**
   - Meta tags
   - Títulos descriptivos
   - URLs amigables
   - Sitemap

4. **Accesibilidad**
   - Estructura semántica
   - Navegación clara
   - Contraste adecuado
   - Textos alternativos

## Contribución

1. **Nueva Página**
   - Crear archivo separado
   - Definir rutas
   - Implementar layout
   - Añadir tests

2. **Modificación**
   - Mantener compatibilidad
   - Actualizar rutas
   - Verificar tests
   - Actualizar documentación

3. **Eliminación**
   - Actualizar rutas
   - Migrar funcionalidad
   - Actualizar navegación
   - Documentar cambios 