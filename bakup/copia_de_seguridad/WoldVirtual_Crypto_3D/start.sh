#!/bin/bash

# =============================================================================
# Script de lanzamiento para Linux/Mac - WoldVirtual Crypto 3D
# =============================================================================

echo ""
echo "============================================================================="
echo "  WoldVirtual Crypto 3D - Metaverso Cripto 3D"
echo "  Version: 0.0.9"
echo "============================================================================="
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 no está instalado"
    echo "💡 Por favor instala Python desde https://python.org"
    exit 1
fi

# Verificar si estamos en el directorio correcto
if [ ! -f "WoldVirtual_Crypto_3D.py" ]; then
    echo "❌ Error: No se encontró WoldVirtual_Crypto_3D.py"
    echo "💡 Asegúrate de ejecutar este script desde el directorio del proyecto"
    exit 1
fi

# Verificar dependencias
echo "🔍 Verificando dependencias..."
python3 -c "import reflex, web3, numpy, pillow, fastapi, sqlalchemy, pydantic" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Faltan dependencias"
    echo "📦 Instalando dependencias..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error instalando dependencias"
        exit 1
    fi
fi

echo "✅ Dependencias verificadas"
echo ""

# Lanzar la aplicación
echo "🚀 Iniciando WoldVirtual Crypto 3D..."
echo ""
python3 WoldVirtual_Crypto_3D.py

# Si llegamos aquí, la aplicación se cerró
echo ""
echo "👋 WoldVirtual Crypto 3D se ha cerrado" 