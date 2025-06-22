# Frontend de WoldVirtual Crypto 3D

Este directorio contiene la interfaz de usuario del metaverso WoldVirtual Crypto 3D, construida con React y Chakra UI.

## Estructura del Directorio

```
frontend/
├── public/              # Archivos estáticos
├── src/
│   ├── components/      # Componentes reutilizables
│   ├── pages/          # Páginas principales
│   ├── hooks/          # Hooks personalizados
│   ├── utils/          # Utilidades y helpers
│   ├── context/        # Contextos de React
│   ├── assets/         # Recursos estáticos
│   ├── App.js          # Componente principal
│   ├── index.js        # Punto de entrada
│   └── theme.js        # Configuración de tema
└── package.json        # Dependencias y scripts
```

## Componentes Principales

### 1. Componentes (`components/`)
- `Navbar.js`: Barra de navegación principal
- `Scene3D.js`: Renderizador de escenas 3D
- `SceneCard.js`: Tarjeta de visualización de escena
- `AssetCard.js`: Tarjeta de visualización de activo
- `WalletConnect.js`: Conexión con wallet
- `LoadingSpinner.js`: Indicador de carga
- `ErrorBoundary.js`: Manejo de errores

### 2. Páginas (`pages/`)
- `Home.js`: Página principal
- `Explore.js`: Exploración de escenas
- `Create.js`: Creación de escenas
- `Marketplace.js`: Mercado de activos
- `Profile.js`: Perfil de usuario
- `Scene.js`: Visualización de escena
- `Asset.js`: Detalles de activo

### 3. Hooks Personalizados (`hooks/`)
- `useWallet.js`: Gestión de wallet
- `useScene.js`: Gestión de escenas
- `useAsset.js`: Gestión de activos
- `useUser.js`: Gestión de usuario
- `useFileUpload.js`: Subida de archivos
- `useTheme.js`: Gestión de tema
- `useNotification.js`: Sistema de notificaciones

### 4. Utilidades (`utils/`)
- `api.js`: Cliente API
- `files.js`: Manejo de archivos
- `errors.js`: Manejo de errores
- `validation.js`: Validación de datos
- `constants.js`: Constantes globales
- `helpers.js`: Funciones auxiliares

## Características Principales

1. **Renderizado 3D**
   - Integración con Three.js
   - Carga de modelos 3D
   - Interacción con escenas
   - Optimización de rendimiento

2. **Integración Web3**
   - Conexión con wallets
   - Interacción con smart contracts
   - Gestión de NFTs
   - Transacciones blockchain

3. **Gestión de Activos**
   - Subida de archivos
   - Previsualización 3D
   - Metadatos de activos
   - Marketplace integrado

4. **Experiencia de Usuario**
   - Diseño responsivo
   - Tema claro/oscuro
   - Animaciones fluidas
   - Feedback en tiempo real

## Instalación

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm start

# Construir para producción
npm run build
```

## Desarrollo

### Scripts Disponibles
- `npm start`: Inicia servidor de desarrollo
- `npm test`: Ejecuta pruebas
- `npm run build`: Construye para producción
- `npm run lint`: Ejecuta linter
- `npm run format`: Formatea código

### Convenciones
- Usar componentes funcionales
- Implementar hooks personalizados
- Seguir principios de diseño atómico
- Mantener componentes pequeños y reutilizables

### Estilo de Código
- Usar ESLint y Prettier
- Seguir guía de estilo de React
- Documentar componentes con JSDoc
- Escribir pruebas unitarias

## Optimización

- Code splitting
- Lazy loading
- Memoización
- Optimización de imágenes
- Caché de recursos

## Seguridad

- Validación de entradas
- Sanitización de datos
- Protección XSS
- Manejo seguro de claves
- HTTPS forzado

## Monitoreo

- Error tracking
- Analytics
- Performance monitoring
- User behavior tracking
- Crash reporting 