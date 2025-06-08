"""
Sistema de Compartición de Recursos Informáticos

Este sistema está compuesto por varios módulos que trabajan en conjunto para gestionar la compartición
de recursos informáticos entre diferentes dispositivos. El sistema está estructurado de la siguiente manera:

Módulos principales:
- md1: Servidor Flask principal que maneja las operaciones básicas del sistema
- md2: Gestiona el registro y monitoreo de proveedores de recursos
- md3: Maneja la lógica de compartición de recursos con control de porcentajes
- md4: Proporciona una interfaz web para visualizar el estado del sistema
- md5: Gestiona la interfaz de usuario y formularios
- md6: Registra eventos de compartición para auditoría
- md7: Controla los permisos de compartición
- md8: Procesa la compartición de documentos
- md9: Coordina el proceso general de compartición

Funcionalidades principales:
1. Registro de proveedores de recursos
2. Monitoreo del estado de los servidores
3. Control de permisos de compartición
4. Gestión de documentos compartidos
5. Auditoría de eventos de compartición
6. Interfaz web para visualización del estado
7. Control de porcentajes de recursos compartidos

El sistema utiliza múltiples servidores Flask corriendo en diferentes puertos:
- Puerto 5001: Servidor principal (md1)
- Puerto 5002: Servidor de registro (md2)
- Puerto 5003: Servidor de compartición (md3)
- Puerto 5004: Servidor de estado (md4)

Este sistema está diseñado para ser escalable y mantener un registro detallado de todas las operaciones
de compartición de recursos.

"""

from md1 import app as app1
from md2 import app as app2
from md3 import app as app3
from md4 import app as app4
from md5 import _reset_form_fields
from md6 import record_resource_sharing_event
from md7 import _check_sharing_permissions
from md8 import _process_document_share
from md9 import process_sharing




def main():
    print("Starting application...")
    
    # Initialize Flask servers
    app1.run(host='localhost', port=5001, debug=False)
    app2.run(host='localhost', port=5002, debug=False) 
    app3.run(host='localhost', port=5003, debug=False)
    app4.run(host='localhost', port=5004, debug=False)
    
    # Check server status
    server_status = app4.status()
    if not server_status:
        print("Server status check failed")
        return
        
    # Reset and initialize forms
    _reset_form_fields()
    
    # Process sharing workflow
    if _check_sharing_permissions():
        _process_document_share()
        record_resource_sharing_event()
        process_sharing()
    else:
        print("Insufficient permissions for sharing operations")

if __name__ == "__main__":
    main()






