@echo off
REM =============================================================================
REM Script de lanzamiento para Windows - WoldVirtual Crypto 3D
REM =============================================================================

echo.
echo =============================================================================
echo   WoldVirtual Crypto 3D - Metaverso Cripto 3D
echo   Version: 0.0.9
echo =============================================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo 💡 Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

REM Verificar si estamos en el directorio correcto
if not exist "WoldVirtual_Crypto_3D.py" (
    echo ❌ Error: No se encontró WoldVirtual_Crypto_3D.py
    echo 💡 Asegúrate de ejecutar este script desde el directorio del proyecto
    pause
    exit /b 1
)

REM Verificar dependencias
echo 🔍 Verificando dependencias...
python -c "import reflex, web3, numpy, pillow, fastapi, sqlalchemy, pydantic" >nul 2>&1
if errorlevel 1 (
    echo ❌ Faltan dependencias
    echo 📦 Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error instalando dependencias
        pause
        exit /b 1
    )
)

echo ✅ Dependencias verificadas
echo.

REM Lanzar la aplicación
echo 🚀 Iniciando WoldVirtual Crypto 3D...
echo.
python WoldVirtual_Crypto_3D.py

REM Si llegamos aquí, la aplicación se cerró
echo.
echo 👋 WoldVirtual Crypto 3D se ha cerrado
pause 