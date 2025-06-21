# Utilidades

Este directorio contiene utilidades y funciones auxiliares utilizadas en toda la aplicación.

## Estructura

```
utils/
├── api.js           # Cliente API y endpoints
├── files.js         # Manejo de archivos
├── errors.js        # Manejo de errores
├── validation.js    # Validación de datos
├── constants.js     # Constantes globales
└── helpers.js       # Funciones auxiliares
```

## Utilidades Disponibles

### 1. API (`api.js`)
Cliente HTTP y endpoints de la API.

```javascript
import { api } from '../utils/api';

// Ejemplos de uso
const data = await api.get('/users');
const response = await api.post('/scenes', sceneData);
```

#### Características
- Configuración de axios
- Interceptores de peticiones
- Manejo de tokens
- Transformación de datos

### 2. Archivos (`files.js`)
Utilidades para manejo de archivos.

```javascript
import { 
  validateFile,
  readFile,
  formatFileSize 
} from '../utils/files';
```

#### Características
- Validación de tipos
- Lectura de archivos
- Formateo de tamaños
- Conversión de formatos

### 3. Errores (`errors.js`)
Manejo centralizado de errores.

```javascript
import { 
  handleError,
  ErrorTypes,
  createError 
} from '../utils/errors';
```

#### Características
- Tipos de errores
- Mensajes personalizados
- Logging de errores
- Recuperación de errores

### 4. Validación (`validation.js`)
Funciones de validación de datos.

```javascript
import { 
  validateEmail,
  validatePassword,
  validateWalletAddress 
} from '../utils/validation';
```

#### Características
- Validación de formularios
- Reglas personalizadas
- Mensajes de error
- Sanitización

### 5. Constantes (`constants.js`)
Constantes globales de la aplicación.

```javascript
import { 
  API_URL,
  FILE_TYPES,
  MAX_FILE_SIZE 
} from '../utils/constants';
```

#### Características
- URLs de API
- Tipos de archivo
- Límites de tamaño
- Configuración global

### 6. Helpers (`helpers.js`)
Funciones auxiliares generales.

```javascript
import { 
  formatDate,
  debounce,
  throttle 
} from '../utils/helpers';
```

#### Características
- Formateo de fechas
- Funciones de tiempo
- Manipulación de strings
- Utilidades de array

## Uso de las Utilidades

### Ejemplo de API
```javascript
import { api } from '../utils/api';

async function fetchUserData(userId) {
  try {
    const response = await api.get(`/users/${userId}`);
    return response.data;
  } catch (error) {
    handleError(error);
  }
}
```

### Ejemplo de Validación
```javascript
import { validateEmail, validatePassword } from '../utils/validation';

function validateForm(email, password) {
  const errors = {};
  
  if (!validateEmail(email)) {
    errors.email = 'Email inválido';
  }
  
  if (!validatePassword(password)) {
    errors.password = 'Contraseña inválida';
  }
  
  return errors;
}
```

## Buenas Prácticas

1. **Organización**
   - Mantener utilidades pequeñas
   - Agrupar por funcionalidad
   - Evitar dependencias circulares

2. **Documentación**
   - Documentar funciones
   - Incluir ejemplos
   - Especificar tipos

3. **Testing**
   - Pruebas unitarias
   - Casos de borde
   - Mocks necesarios

4. **Mantenimiento**
   - Revisar periodicamente
   - Actualizar dependencias
   - Optimizar rendimiento

## Contribución

1. **Nueva Utilidad**
   - Crear archivo separado
   - Documentar completamente
   - Añadir tests

2. **Modificación**
   - Mantener compatibilidad
   - Actualizar documentación
   - Verificar tests

3. **Eliminación**
   - Verificar dependencias
   - Actualizar imports
   - Documentar cambios 