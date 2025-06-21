# Backend de WoldVirtual Crypto 3D

Este directorio contiene toda la lógica del servidor y la API del metaverso WoldVirtual Crypto 3D.

## Estructura del Directorio

```
backend/
├── alembic/              # Configuración y scripts de migración de base de datos
├── main.py              # Punto de entrada principal de la aplicación
├── database.py          # Configuración y conexión a la base de datos
├── models.py            # Modelos de SQLAlchemy
├── schemas.py           # Esquemas Pydantic para validación
├── crud.py             # Operaciones CRUD
├── config.py           # Configuración de la aplicación
├── utils.py            # Utilidades generales
├── dependencies.py     # Dependencias de FastAPI
└── requirements.txt    # Dependencias de Python
```

## Componentes Principales

### 1. Base de Datos (`database.py`)
- Configuración de SQLAlchemy
- Conexión a la base de datos PostgreSQL
- Manejo de sesiones y transacciones

### 2. Modelos (`models.py`)
- Modelos de SQLAlchemy para:
  - Usuarios
  - Escenas 3D
  - Activos digitales
  - Transacciones
  - Contratos inteligentes

### 3. Esquemas (`schemas.py`)
- Esquemas Pydantic para:
  - Validación de datos de entrada
  - Serialización de respuestas
  - Modelos de datos compartidos

### 4. Operaciones CRUD (`crud.py`)
- Operaciones de base de datos para:
  - Crear, leer, actualizar y eliminar registros
  - Consultas complejas
  - Relaciones entre modelos

### 5. Configuración (`config.py`)
- Variables de entorno
- Configuración de la aplicación
- Constantes globales

### 6. Utilidades (`utils.py`)
- Funciones auxiliares
- Helpers de seguridad
- Utilidades de Web3

### 7. Dependencias (`dependencies.py`)
- Inyección de dependencias
- Middleware
- Autenticación y autorización

### 8. Migraciones (`alembic/`)
- Scripts de migración de base de datos
- Control de versiones del esquema
- Herramientas de actualización

## API Endpoints

### Usuarios
- `POST /api/users/` - Crear usuario
- `GET /api/users/{id}` - Obtener usuario
- `PUT /api/users/{id}` - Actualizar usuario
- `DELETE /api/users/{id}` - Eliminar usuario

### Escenas
- `POST /api/scenes/` - Crear escena
- `GET /api/scenes/` - Listar escenas
- `GET /api/scenes/{id}` - Obtener escena
- `PUT /api/scenes/{id}` - Actualizar escena
- `DELETE /api/scenes/{id}` - Eliminar escena

### Activos
- `POST /api/assets/` - Crear activo
- `GET /api/assets/` - Listar activos
- `GET /api/assets/{id}` - Obtener activo
- `PUT /api/assets/{id}` - Actualizar activo
- `DELETE /api/assets/{id}` - Eliminar activo

### Transacciones
- `POST /api/transactions/` - Crear transacción
- `GET /api/transactions/` - Listar transacciones
- `GET /api/transactions/{id}` - Obtener transacción

## Configuración

1. Crear archivo `.env` basado en `.env.example`
2. Configurar variables de entorno:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `ALGORITHM`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`

## Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
uvicorn main:app --reload
```

## Desarrollo

- Usar `pytest` para pruebas
- Seguir PEP 8 para estilo de código
- Documentar con docstrings
- Usar type hints

## Seguridad

- Autenticación JWT
- CORS configurado
- Validación de datos
- Sanitización de entradas
- Protección contra ataques comunes

## Monitoreo

- Logging configurado
- Métricas de rendimiento
- Trazabilidad de errores
- Monitoreo de recursos 