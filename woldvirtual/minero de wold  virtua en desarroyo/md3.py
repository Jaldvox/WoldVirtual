# Este archivo ahora contendrá el backend web para compartir recursos informáticos.

from flask import Flask, request, jsonify

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# --- Almacenamiento temporal para proveedores de recursos registrados ---
# En un sistema real, esto sería una base de datos (SQL, NoSQL, etc.)
# Ampliamos la estructura para almacenar el porcentaje de compartición deseado
registered_providers = {}
# Ejemplo de estructura:
# {
#     "provider_id_1": {
#         "available_bandwidth_mbps": 100,
#         "location": "...",
#         "contact_info": "...",
#         "device_type": "general" or "specialized", # Añadimos tipo de dispositivo
#         "sharing_percentage": 0 # Porcentaje de compartición deseado (0-100)
#     },
#     "provider_id_2": { ... }
# }


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
    Añadimos 'device_type' a los datos esperados.
    Ejemplo de datos esperados:
    {
        "provider_id": "unique_id_del_pc",
        "available_bandwidth_mbps": 100,
        "location": "geo_coordinates_or_region",
        "contact_info": "ip_address_or_hostname",
        "device_type": "general" # o "specialized"
        # ... otros datos relevantes
    }
    """
    if not request.is_json:
        return jsonify({"success": False, "message": "La solicitud debe ser JSON"}), 415 # Unsupported Media Type

    provider_data = request.get_json()

    # --- Validar datos recibidos (ejemplo básico) ---
    required_fields = ["provider_id", "available_bandwidth_mbps", "contact_info", "device_type"]
    if not all(field in provider_data for field in required_fields):
        return jsonify({"success": False, "message": f"Faltan campos requeridos. Se esperan: {required_fields}"}), 400 # Bad Request

    provider_id = provider_data.get("provider_id")
    device_type = provider_data.get("device_type").lower() # Convertir a minúsculas para comparación

    if device_type not in ["general", "specialized"]:
         return jsonify({"success": False, "message": "Tipo de dispositivo inválido. Use 'general' o 'specialized'."}), 400

    # --- Lógica para registrar o actualizar el proveedor ---
    if provider_id in registered_providers:
        # Si ya existe, actualizar sus datos (ej. ancho de banda, tipo de dispositivo)
        print(f"Actualizando datos del proveedor: {provider_id}")
        # Mantener el porcentaje de compartición existente si no se envía uno nuevo
        current_percentage = registered_providers[provider_id].get("sharing_percentage", 0)
        registered_providers[provider_id].update(provider_data)
        registered_providers[provider_id]["sharing_percentage"] = current_percentage # Asegurar que se mantiene si no se actualiza
        message = "Datos del proveedor actualizados exitosamente."
    else:
        # Si es nuevo, registrarlo e inicializar el porcentaje de compartición a 0
        print(f"Registrando nuevo proveedor: {provider_id}")
        registered_providers[provider_id] = provider_data
        registered_providers[provider_id]["sharing_percentage"] = 0 # Inicializar porcentaje
        message = "Proveedor registrado exitosamente."

    print(f"Proveedores registrados actualmente: {len(registered_providers)}")
    # print(registered_providers) # Descomentar para ver los datos registrados

    return jsonify({"success": True, "message": message}), 200 # OK

@app.route('/set_sharing_percentage', methods=['POST'])
def set_sharing_percentage():
    """
    Ruta para establecer el porcentaje de compartición de recursos para un proveedor.
    Espera recibir datos JSON:
    {
        "provider_id": "unique_id_del_pc",
        "percentage": 30 # Porcentaje deseado (0-100)
    }
    """
    if not request.is_json:
        return jsonify({"success": False, "message": "La solicitud debe ser JSON"}), 415

    request_data = request.get_json()

    # --- Validar datos recibidos ---
    required_fields = ["provider_id", "percentage"]
    if not all(field in request_data for field in required_fields):
        return jsonify({"success": False, "message": f"Faltan campos requeridos. Se esperan: {required_fields}"}), 400

    provider_id = request_data.get("provider_id")
    percentage = request_data.get("percentage")

    # Validar que el porcentaje sea un número entre 0 y 100
    if not isinstance(percentage, (int, float)) or not (0 <= percentage <= 100):
        return jsonify({"success": False, "message": "El porcentaje debe ser un número entre 0 y 100."}), 400

    # --- Verificar si el proveedor existe ---
    if provider_id not in registered_providers:
        return jsonify({"success": False, "message": "Proveedor no encontrado."}), 404 # Not Found

    # --- Aplicar la lógica de límites de porcentaje ---
    provider_info = registered_providers[provider_id]
    device_type = provider_info.get("device_type", "general").lower() # Default a general si no está definido

    if device_type == "general" and percentage > 50:
        return jsonify({
            "success": False,
            "message": "Para dispositivos generales, el porcentaje máximo recomendado es 50%."
            # Podrías decidir si forzar el 50% o simplemente retornar un error/advertencia
        }), 400 # Bad Request, o podrías usar 200 con un mensaje de advertencia

    # --- Almacenar el porcentaje deseado ---
    provider_info["sharing_percentage"] = percentage
    registered_providers[provider_id] = provider_info # Asegurar que se guarda en el diccionario principal

    print(f"Porcentaje de compartición establecido para {provider_id}: {percentage}%")
    # print(registered_providers[provider_id]) # Descomentar para ver los datos actualizados

    return jsonify({"success": True, "message": f"Porcentaje de compartición establecido a {percentage}% para {provider_id}."}), 200

# --- Aquí se añadirán más rutas para: ---
# - Reporte periódico de recursos (si es diferente del registro inicial)
# - Solicitudes de recursos del metaverso
# - Orquestación de conexiones
# - etc.

# --- Lógica de ejecución del servidor ---
if __name__ == '__main__':
    print("Iniciando servidor Flask...")
    # Para que sea accesible desde otras máquinas en la red, usa host='0.0.0.0'
    # Si solo necesitas acceder desde tu máquina, puedes usar host='127.0.0.1'
    app.run(debug=True, host='0.0.0.0', port=5000)
