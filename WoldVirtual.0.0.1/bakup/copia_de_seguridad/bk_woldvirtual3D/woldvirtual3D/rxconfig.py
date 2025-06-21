"""
Configuración de Reflex para Wold Virtual 3D
"""

import reflex as rx

# Configuración del proyecto
config = rx.Config(
    app_name="wold_virtual_3d",
    db_url="sqlite:///wold_virtual.db",
    env=rx.Env.DEV,
    frontend_port=3000,
    backend_port=8000,
    api_url="http://localhost:8000",
    deploy_url="https://wold-virtual-3d.vercel.app",
    tailwind=None,  # Deshabilitamos Tailwind ya que usamos CSS personalizado
    plugins=[],
)

# Configuración de desarrollo
dev_config = rx.Config(
    app_name="wold_virtual_3d_dev",
    db_url="sqlite:///wold_virtual_dev.db",
    env=rx.Env.DEV,
    frontend_port=3001,
    backend_port=8001,
    api_url="http://localhost:8001",
    tailwind=None,
    plugins=[],
)

# Configuración de producción
prod_config = rx.Config(
    app_name="wold_virtual_3d_prod",
    db_url="sqlite:///wold_virtual_prod.db",
    env=rx.Env.PROD,
    frontend_port=3000,
    backend_port=8000,
    api_url="https://api.wold-virtual-3d.com",
    deploy_url="https://wold-virtual-3d.vercel.app",
    tailwind=None,
    plugins=[],
) 