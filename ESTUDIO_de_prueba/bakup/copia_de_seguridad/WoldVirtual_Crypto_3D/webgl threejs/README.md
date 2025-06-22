# WebGL Three.js - Motor 3D del Metaverso WoldVirtual

## 🌟 Descripción
Esta carpeta contiene la implementación avanzada del motor 3D basado en Three.js que proporciona la experiencia visual inmersiva del metaverso WoldVirtual Crypto 3D. Incluye gestión completa de escenas, modelos 3D, iluminación PBR, efectos visuales avanzados y integración con blockchain.

## 🚀 Características Principales

### 🎮 Experiencia 3D Inmersiva
- **Renderizado PBR (Physically Based Rendering)** para realismo visual
- **Sistema de iluminación dinámica** con sombras en tiempo real
- **Gestión de sombras avanzada** con mapas de sombra de alta resolución
- **Optimización de rendimiento** con LOD (Level of Detail)
- **Carga asíncrona de assets** para mejor experiencia de usuario

### 🔗 Integración Blockchain
- **Conectividad Web3** para transacciones en tiempo real
- **Gestión de NFTs** para assets digitales
- **Smart Contracts** para propiedad y comercio
- **IPFS Integration** para almacenamiento descentralizado

### 🎨 Interfaz de Usuario
- **React + TypeScript** para desarrollo robusto
- **Tailwind CSS** para estilos modernos y responsivos
- **Framer Motion** para animaciones fluidas
- **Zustand** para gestión de estado eficiente

## 🏗️ Estructura de Carpetas

```
webgl threejs/
├── WoldVirtualCrypto3D/          # Aplicación principal
│   ├── src/
│   │   ├── backend/              # Servidor backend con Reflex
│   │   │   ├── api/              # Endpoints de API
│   │   │   ├── blockchain/       # Integración blockchain
│   │   │   ├── database/         # Modelos de base de datos
│   │   │   ├── state/            # Gestión de estado
│   │   │   └── utils/            # Utilidades backend
│   │   ├── frontend/             # Aplicación frontend React
│   │   │   ├── components/       # Componentes React
│   │   │   │   ├── three/        # Componentes Three.js
│   │   │   │   │   ├── core/     # Núcleo del motor 3D
│   │   │   │   │   ├── controls/ # Controles de cámara
│   │   │   │   │   ├── lighting/ # Sistema de iluminación
│   │   │   │   │   ├── materials/ # Materiales PBR
│   │   │   │   │   ├── objects/  # Objetos 3D
│   │   │   │   │   ├── performance/ # Optimizaciones
│   │   │   │   │   └── scenes/   # Escenas 3D
│   │   │   │   └── UI/           # Componentes de interfaz
│   │   │   ├── hooks/            # Hooks personalizados
│   │   │   ├── pages/            # Páginas de la aplicación
│   │   │   ├── providers/        # Providers de contexto
│   │   │   ├── services/         # Servicios de API
│   │   │   ├── store/            # Gestión de estado global
│   │   │   ├── styles/           # Estilos CSS
│   │   │   ├── types/            # Definiciones TypeScript
│   │   │   └── utils/            # Utilidades frontend
│   │   ├── public/               # Assets públicos
│   │   │   ├── models/           # Modelos 3D
│   │   │   └── textures/         # Texturas
│   │   └── docs/                 # Documentación técnica
├── app.py                        # Aplicación Reflex simplificada
├── rxconfig.py                   # Configuración de Reflex
└── requirements.txt              # Dependencias Python
```

## 🛠️ Tecnologías Implementadas

### Frontend
- **React 18** - Biblioteca para interfaces de usuario
- **TypeScript** - Tipado estático para mayor robustez
- **Three.js** - Motor 3D para WebGL
- **@react-three/fiber** - Renderer React para Three.js
- **@react-three/drei** - Utilidades para Three.js
- **Vite** - Build tool rápido y moderno
- **Tailwind CSS** - Framework CSS utilitario
- **Framer Motion** - Biblioteca de animaciones
- **Zustand** - Gestión de estado ligera

### Backend
- **Reflex** - Framework full-stack Python
- **FastAPI** - Framework web para APIs
- **SQLAlchemy** - ORM para base de datos
- **Web3.py** - Integración con Ethereum
- **Socket.IO** - Comunicación en tiempo real
- **IPFS HTTP Client** - Almacenamiento descentralizado

### Blockchain
- **Ethereum** - Blockchain principal
- **Smart Contracts** - Contratos para NFTs y tokens
- **MetaMask** - Wallet integration
- **IPFS** - Almacenamiento descentralizado

## 🚀 Instalación y Configuración

### Prerrequisitos
- Node.js 18+ y npm
- Python 3.8+
- Git

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd WoldVirtual_Crypto_3D/webgl threejs
```

### 2. Configurar el frontend
```bash
cd WoldVirtualCrypto3D
npm install
```

### 3. Configurar el backend
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:
```env
# API Configuration
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# Blockchain Configuration
VITE_NFT_CONTRACT_ADDRESS=your_nft_contract_address
VITE_TOKEN_CONTRACT_ADDRESS=your_token_contract_address

# IPFS Configuration
VITE_IPFS_GATEWAY=https://ipfs.io/ipfs/
```

## 🎯 Uso

### Desarrollo
```bash
# Terminal 1: Frontend
cd WoldVirtualCrypto3D
npm run dev

# Terminal 2: Backend
cd ..
python -m reflex run
```

### Producción
```bash
# Construir frontend
cd WoldVirtualCrypto3D
npm run build

# Ejecutar backend
cd ..
python -m reflex run --env prod
```

## 🎮 Características del Motor 3D

### Sistema de Escenas
- **Gestión dinámica de escenas** con carga/descarga automática
- **Transiciones suaves** entre diferentes entornos
- **Optimización de memoria** con limpieza automática

### Sistema de Iluminación
- **Iluminación PBR** para realismo fotográfico
- **Sombras dinámicas** con mapas de alta resolución
- **Iluminación ambiental** y direccional configurable
- **Efectos de post-procesado** (Bloom, Chromatic Aberration)

### Controles de Cámara
- **Controles de primera persona** para inmersión
- **Controles de tercera persona** para exploración
- **Transiciones suaves** entre modos
- **Colisión de cámara** para evitar clipping

### Optimización de Rendimiento
- **LOD (Level of Detail)** para modelos complejos
- **Frustum Culling** para renderizado eficiente
- **Instancing** para objetos repetidos
- **Texture Atlasing** para reducir draw calls

## 🔧 Configuración Avanzada

### Personalización de Materiales
```typescript
// Ejemplo de material PBR personalizado
const customMaterial = new THREE.MeshStandardMaterial({
  color: 0xffffff,
  roughness: 0.5,
  metalness: 0.8,
  normalMap: normalTexture,
  aoMap: aoTexture,
  roughnessMap: roughnessTexture,
  metalnessMap: metalnessTexture
});
```

### Configuración de Efectos
```typescript
// Configuración de efectos post-procesado
const effects = {
  bloom: {
    intensity: 1.0,
    luminanceThreshold: 0.9,
    luminanceSmoothing: 0.025
  },
  chromaticAberration: {
    offset: [0.0005, 0.0005]
  }
};
```

## 📊 Monitoreo y Debugging

### Métricas de Rendimiento
- **FPS Counter** en tiempo real
- **Memory Usage** tracking
- **Draw Calls** optimization
- **Texture Memory** monitoring

### Herramientas de Debug
- **Three.js Inspector** integration
- **Performance Profiler** built-in
- **Error Boundary** para captura de errores
- **Logging System** comprehensivo

## 🤝 Contribución

### Guías de Desarrollo
1. **Fork** el repositorio
2. **Crear** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abrir** un Pull Request

### Estándares de Código
- **TypeScript** estricto para frontend
- **PEP 8** para Python
- **ESLint** y **Prettier** para JavaScript/TypeScript
- **Black** para Python formatting

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

- **Documentación**: `/docs` folder
- **Issues**: GitHub Issues
- **Discord**: [Link al servidor]
- **Email**: support@woldvirtual.com

## 🔮 Roadmap

### Próximas Características
- [ ] **Multiplayer** en tiempo real
- [ ] **VR/AR** support
- [ ] **AI NPCs** con comportamiento inteligente
- [ ] **Procedural Generation** de mundos
- [ ] **Advanced Physics** engine
- [ ] **Audio Spatial** system

### Mejoras Técnicas
- [ ] **WebGPU** migration
- [ ] **WebAssembly** optimizations
- [ ] **Service Worker** para offline support
- [ ] **Progressive Web App** features

---

**¡Bienvenido al futuro del metaverso! 🌍✨** 