# 🐍 Guía Completa: Instalación de Reflex desde Cero
### Para WoldVirtual Crypto 3D

---

## 📋 Requisitos Previos

### **🔧 Software Necesario**
- **Python 3.8 o superior** (recomendado: Python 3.11)
- **Node.js 16 o superior** (para el frontend)
- **Git** (para clonar repositorios)
- **Editor de código** (VS Code recomendado)

### **✅ Verificar Instalaciones**
```bash
# Verificar Python
python --version
# Debe mostrar: Python 3.8.x o superior

# Verificar pip
pip --version
# Debe mostrar la versión de pip

# Verificar Node.js
node --version
# Debe mostrar: v16.x.x o superior

# Verificar npm
npm --version
# Debe mostrar la versión de npm
```

---

## 🚀 Instalación Paso a Paso

### **1. 🏗️ Crear Entorno Virtual (RECOMENDADO)**

```bash
# Crear carpeta del proyecto
mkdir mi_proyecto_reflex
cd mi_proyecto_reflex

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate

# Verificar que el entorno está activo
# Debe aparecer (venv) al inicio de la línea de comandos
```

### **2. 📦 Instalar Reflex**

```bash
# Actualizar pip primero
python -m pip install --upgrade pip

# Instalar Reflex
pip install reflex

# Verificar instalación
reflex --version
# Debe mostrar la versión de Reflex instalada
```

### **3. 🎯 Inicializar Proyecto Reflex**

```bash
# Inicializar proyecto Reflex
reflex init

# Esto creará automáticamente:
# - rxconfig.py (configuración)
# - requirements.txt (dependencias)
# - assets/ (recursos)
# - .gitignore
# - Y estructura básica
```

### **4. 📁 Estructura de Proyecto Generada**

```
mi_proyecto_reflex/
├── 📁 venv/                    # Entorno virtual
├── 📁 assets/                  # Recursos estáticos
├── 📁 .web/                    # Archivos generados (auto)
├── 📄 rxconfig.py             # Configuración principal
├── 📄 requirements.txt        # Dependencias Python
├── 📄 mi_proyecto_reflex.py   # Aplicación principal
└── 📄 .gitignore             # Archivos a ignorar en Git
```

### **5. 🔧 Configuración Inicial (rxconfig.py)**

```python
import reflex as rx

config = rx.Config(
    app_name="mi_proyecto_reflex",
    plugins=[rx.plugins.TailwindV3Plugin()],
)
```

### **6. 🎨 Aplicación Básica (mi_proyecto_reflex.py)**

```python
import reflex as rx

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("¡Hola, Reflex!", font_size="2em"),
            rx.text("Mi primera aplicación Reflex funcionando"),
            rx.button(
                "Click me!",
                on_click=lambda: rx.toast("¡Funciona!"),
                color_scheme="blue"
            ),
            spacing="1.5em",
            font_size="2em",
        ),
        width="100%",
        height="100vh"
    )

# Crear la aplicación
app = rx.App()

# Agregar página
app.add_page(index, route="/")
```

### **7. 🚀 Ejecutar la Aplicación**

```bash
# Ejecutar servidor de desarrollo
reflex run

# Esto hará:
# 1. Instalar dependencias frontend (primera vez)
# 2. Compilar la aplicación
# 3. Iniciar servidor backend (puerto 8000)
# 4. Iniciar servidor frontend (puerto 3000)
# 5. Abrir navegador automáticamente
```

---

## 🔍 Comandos Útiles de Reflex

### **📋 Comandos Básicos**

```bash
# Inicializar proyecto
reflex init

# Ejecutar aplicación
reflex run

# Ejecutar solo backend
reflex run --backend-only

# Ejecutar solo frontend
reflex run --frontend-only

# Compilar para producción
reflex export

# Limpiar archivos generados
reflex clean

# Ver ayuda
reflex --help
```

### **🔧 Comandos de Desarrollo**

```bash
# Instalar dependencias
pip install -r requirements.txt

# Actualizar Reflex
pip install --upgrade reflex

# Ver versión
reflex --version

# Limpiar cache
reflex clean
rm -rf .web
```

---

## 📂 Estructura Recomendada para Proyectos Grandes

```
mi_proyecto_grande/
├── 📁 venv/                    # Entorno virtual
├── 📁 assets/                  # Recursos estáticos
│   ├── 🖼️ images/
│   ├── 🎨 styles/
│   └── 📄 data/
├── 📁 components/              # Componentes reutilizables
│   ├── 📄 __init__.py
│   ├── 📄 navbar.py
│   ├── 📄 footer.py
│   └── 📄 sidebar.py
├── 📁 pages/                   # Páginas de la aplicación
│   ├── 📄 __init__.py
│   ├── 📄 home.py
│   ├── 📄 about.py
│   └── 📄 contact.py
├── 📁 utils/                   # Utilidades
│   ├── 📄 __init__.py
│   ├── 📄 database.py
│   └── 📄 helpers.py
├── 📁 states/                  # Estados de la aplicación
│   ├── 📄 __init__.py
│   └── 📄 app_state.py
├── 📄 rxconfig.py             # Configuración
├── 📄 requirements.txt        # Dependencias
├── 📄 main.py                 # Aplicación principal
└── 📄 README.md              # Documentación
```

---

## 🛠️ Configuración Avanzada

### **⚙️ rxconfig.py Completo**

```python
import reflex as rx

config = rx.Config(
    app_name="mi_proyecto_reflex",
    
    # Puertos de desarrollo
    frontend_port=3000,
    backend_port=8000,
    
    # Base de datos
    db_url="sqlite:///reflex.db",
    
    # CORS para desarrollo
    cors_allowed_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    
    # Plugins
    plugins=[
        rx.plugins.TailwindV3Plugin(),
    ],
    
    # Configuración de Tailwind
    tailwind={
        "theme": {
            "extend": {
                "colors": {
                    "primary": "#3B82F6",
                    "secondary": "#10B981",
                }
            }
        }
    }
)
```

### **📦 requirements.txt Típico**

```txt
reflex>=0.4.0
sqlalchemy>=2.0.0
python-dotenv>=1.0.0
requests>=2.31.0
pillow>=10.0.0
```

---

## 🐛 Solución de Problemas Comunes

### **❌ Error: "reflex: command not found"**
```bash
# Solución: Asegúrate de que el entorno virtual esté activo
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstalar si es necesario
pip install reflex
```

### **❌ Error: "No module named 'reflex'"**
```bash
# Solución: Verificar instalación
pip list | grep reflex

# Reinstalar si no aparece
pip install reflex
```

### **❌ Error: "Port already in use"**
```bash
# Solución: Usar puertos diferentes
reflex run --frontend-port 3001 --backend-port 8001
```

### **❌ Error: "rxconfig.py not found"**
```bash
# Solución: Ejecutar desde la carpeta correcta
cd mi_proyecto_reflex
reflex init  # Si no existe
reflex run
```

### **❌ Error de dependencias frontend**
```bash
# Solución: Limpiar y reinstalar
reflex clean
rm -rf .web
reflex run
```

---

## 🎯 Ejemplo Completo: Aplicación "Hola Mundo"

### **1. Crear proyecto**
```bash
mkdir hola_reflex
cd hola_reflex
python -m venv venv
venv\Scripts\activate  # Windows
pip install reflex
reflex init
```

### **2. Editar hola_reflex.py**
```python
import reflex as rx

class State(rx.State):
    """Estado de la aplicación."""
    count: int = 0
    
    def increment(self):
        self.count += 1
    
    def decrement(self):
        self.count -= 1

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("¡Hola, Reflex!", font_size="3em", color="blue"),
            rx.text(f"Contador: {State.count}", font_size="2em"),
            rx.hstack(
                rx.button(
                    "-",
                    on_click=State.decrement,
                    color_scheme="red",
                    size="lg"
                ),
                rx.button(
                    "+",
                    on_click=State.increment,
                    color_scheme="green",
                    size="lg"
                ),
                spacing="1em"
            ),
            spacing="2em",
            align="center"
        ),
        width="100%",
        height="100vh",
        background="linear-gradient(45deg, #f0f9ff, #e0f2fe)"
    )

# Crear aplicación
app = rx.App()
app.add_page(index, route="/", title="Hola Reflex")
```

### **3. Ejecutar**
```bash
reflex run
```

---

## 🎉 ¡Listo para Usar!

### **✅ Checklist Final**
- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Reflex instalado
- [ ] Proyecto inicializado con `reflex init`
- [ ] Aplicación ejecutándose con `reflex run`
- [ ] Navegador abierto en http://localhost:3000

### **🚀 Próximos Pasos**
1. **Personalizar** tu aplicación en el archivo `.py` principal
2. **Añadir páginas** con `app.add_page()`
3. **Crear componentes** reutilizables
4. **Integrar base de datos** con SQLAlchemy
5. **Desplegar** tu aplicación

---

## 📞 Recursos Adicionales

- **📖 Documentación Oficial**: https://reflex.dev/docs/
- **🎓 Tutoriales**: https://reflex.dev/docs/tutorial/
- **💬 Comunidad**: https://discord.gg/T5WSbC2YtQ
- **🐛 Issues**: https://github.com/reflex-dev/reflex/issues
- **📚 Ejemplos**: https://github.com/reflex-dev/reflex-examples

---

**💡 Consejo Final**: Una vez que tengas tu proyecto organizado como quieres, simplemente ejecuta `reflex init` en la carpeta final y luego `reflex run`. ¡Así de simple!

**¡Ahora ya no hay excusas! 🚀**