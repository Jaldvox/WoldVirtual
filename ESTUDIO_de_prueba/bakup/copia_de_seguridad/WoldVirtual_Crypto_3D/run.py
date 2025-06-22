#!/usr/bin/env python3
"""
Script de lanzamiento simple para WoldVirtual Crypto 3D
Ejecuta: python run.py
"""

import sys
import os
from pathlib import Path

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Función principal de lanzamiento"""
    print("🚀 Lanzando WoldVirtual Crypto 3D...")
    
    try:
        # Importar y ejecutar la aplicación principal
        from WoldVirtual_Crypto_3D import main as app_main
        app_main()
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("💡 Asegúrate de que todas las dependencias estén instaladas:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 