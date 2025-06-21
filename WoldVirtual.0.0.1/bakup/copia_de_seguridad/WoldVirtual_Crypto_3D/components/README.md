# Carpeta Components

## Descripción
Esta carpeta contiene todos los componentes reutilizables de la interfaz de usuario y la escena 3D del metaverso.

## Estructura de Archivos

### `scene.py`
- **Propósito**: Maneja la renderización 3D usando Three.js
- **Componentes Principales**:
  - `Scene3D`: Componente principal que encapsula la escena Three.js
  - Integración con React Three Fiber
  - Sistema de iluminación y controles de cámara
- **Funcionalidades**:
  - Renderizado de modelos 3D
  - Sistema de iluminación
  - Controles de cámara
  - Gestión de assets 3D

### `ui.py`
- **Propósito**: Componentes de la interfaz de usuario
- **Componentes Principales**:
  - `UI`: Componente principal de la interfaz
  - Barra de navegación
  - Controles de usuario
  - Indicadores de estado
- **Funcionalidades**:
  - Conexión de wallet
  - Navegación
  - Información del usuario
  - Controles de la escena

## Uso
```python
from components import Scene3D, UI

# En tu página principal
def index():
    return rx.vstack(
        Scene3D(),
        UI(),
    )
```

## Estilos
Los componentes utilizan los estilos definidos en `styles.py` en la raíz del proyecto.

## Dependencias
- Three.js
- React Three Fiber
- React Three Drei
- Reflex

## Convenciones
- Cada componente debe ser autocontenido
- Documentar props y métodos
- Seguir el patrón de diseño de Reflex
- Mantener la lógica de estado en `state.py` 