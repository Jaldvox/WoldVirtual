# Este archivo ahora contendrá el backend web para compartir recursos informáticos.

from flask import Flask, request, jsonify

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# --- Almacenamiento temporal para proveedores de recursos registrados ---
# En un sistema real, esto sería una base de datos (SQL, NoSQL, etc.)
registered_providers = {}

# --- Rutas del backend ---

@app.route('/')
def index():
    """Ruta de inicio simple para verificar que el servidor está funcionando."""
    return "Backend de Compartición de Recursos Informáticos funcionando."

@app.route('/status', methods=['GET'])
def status():
    """Ruta para obtener el estado del backend."""
    # También podemos incluir el número de proveedores registrados
    return jsonify({
        "status": "ok",
        "message": "Servidor listo para recibir solicitudes.",
        "registered_providers_count": len(registered_providers)
    })

@app.route('/register_provider', methods=['POST'])
def register_provider():
    """
    Ruta para que un PC proveedor de recursos se registre en el sistema.
    Espera recibir datos JSON con información del proveedor y sus recursos.
    Ejemplo de datos esperados:
    {
        "provider_id": "unique_id_del_pc",
        "available_bandwidth_mbps": 100,
        "location": "geo_coordinates_or_region",
        "contact_info": "ip_address_or_hostname"
        # ... otros datos relevantes
    }
    """
    if not request.is_json:
        return jsonify({"success": False, "message": "La solicitud debe ser JSON"}), 415 # Unsupported Media Type

    provider_data = request.get_json()

    # --- Validar datos recibidos (ejemplo básico) ---
    required_fields = ["provider_id", "available_bandwidth_mbps", "contact_info"]
    if not all(field in provider_data for field in required_fields):
        return jsonify({"success": False, "message": "Faltan campos requeridos"}), 400 # Bad Request

    provider_id = provider_data.get("provider_id")

    # --- Lógica para registrar o actualizar el proveedor ---
    if provider_id in registered_providers:
        # Si ya existe, actualizar sus datos (ej. ancho de banda)
        print(f"Actualizando datos del proveedor: {provider_id}")
        registered_providers[provider_id].update(provider_data)
        message = "Datos del proveedor actualizados exitosamente."
    else:
        # Si es nuevo, registrarlo
        print(f"Registrando nuevo proveedor: {provider_id}")
        registered_providers[provider_id] = provider_data
        message = "Proveedor registrado exitosamente."

    print(f"Proveedores registrados actualmente: {len(registered_providers)}")
    # print(registered_providers) # Descomentar para ver los datos registrados

    return jsonify({"success": True, "message": message}), 200 # OK

# --- Aquí se añadirán más rutas para: ---
# - Reporte periódico de recursos (si es diferente del registro inicial)
# - Solicitudes de recursos del metaverso
# - Orquestación de conexiones
# - etc.

# --- Lógica de ejecución del servidor ---
if __name__ == '__main__':
    # En un entorno de producción, usarías un servidor WSGI como Gunicorn o uWSGI.
    # Para desarrollo, podemos usar el servidor integrado de Flask.
    # debug=True permite recarga automática y mensajes de error detallados.
    print("Iniciando servidor Flask...")
    # Para que sea accesible desde otras máquinas en la red, usa host='0.0.0.0'
    # Si solo necesitas acceder desde tu máquina, puedes usar host='127.0.0.1'
    app.run(debug=True, host='0.0.0.0', port=5000)
