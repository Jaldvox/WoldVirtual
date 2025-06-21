from flask import Flask, render_template_string, request, jsonify
from flask_socketio import SocketIO, emit
import hashlib
import time
import random # Para generar el código temporal

# Importamos los módulos necesarios
from blockchain import Blockchain
from usuarios import registrar_usuario, verificar_credenciales # Asumiendo que estas funciones usan la Blockchain

app = Flask(__name__)
socketio = SocketIO(app)

# Instanciamos la Blockchain (global para simplificar en este ejemplo)
blockchain = Blockchain()

# Diccionario para almacenar códigos temporales: {username: {'code': '1234', 'timestamp': time.time(), 'password': 'hashed_password'}}
temporal_codes = {}

def generate_temporal_code():
    """Genera un código temporal de 4 dígitos."""
    return str(random.randint(1000, 9999))

# HTML, CSS y JavaScript incluidos en una plantilla de cadena
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metaverso Crypto 3D</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }
        .header {
            background-color: #007bff;
            color: white;
            padding: 10px 0;
            text-align: center;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }
        .nav {
            display: flex;
            justify-content: center;
            background-color: #0056b3;
            padding: 10px 0;
        }
        .nav a {
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            font-weight: bold;
        }
        .nav a:hover {
            background-color: #003d80;
        }
        .container {
            margin-top: 100px;
            padding: 20px;
        }
        .section {
            background-color: #fff;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1, h2 {
            margin-top: 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Metaverso Crypto 3D</h1>
    </div>
    <div class="nav">
        <a href="#home">Inicio</a>
        <a href="#registration">Registro</a> <!-- Enlace añadido para Registro -->
        <a href="#usuarios">Usuarios</a>
        <a href="#recursos">Recursos</a>
        <a href="#blockchain">Blockchain</a>
        <a href="#database">Base de Datos</a>
        <a href="#compresion">Compresión</a>
        <a href="#servidor">Servidor</a>
    </div>
    <div class="container">
        <div id="home" class="section">
            <h2>Metaverso Crypto 3D descentralizado</h2>
            <p>Próximamente en esta página principal, se darán más detalles sobre el proyecto. Tenemos diferentes secciones que explicarán su función, dentro de cada módulo programado en Python.</p>
        </div>

        <!-- Sección de Registro -->
        <div id="registration" class="section">
            <h2>Registro de Usuario</h2>
            <form id="registrationForm">
                <label for="regUsername">Usuario:</label><br>
                <input type="text" id="regUsername" name="username" required><br><br>
                <label for="regPassword">Contraseña:</label><br>
                <input type="password" id="regPassword" name="password" required><br><br>
                <button type="button" onclick="requestTemporalCode()">Solicitar Código</button>
            </form>
            <div id="codeVerification" style="display:none;">
                <label for="temporalCode">Código Temporal:</label><br>
                <input type="text" id="temporalCode" name="temporal_code" required><br><br>
                <button type="button" onclick="verifyTemporalCode()">Verificar Código</button>
            </div>
            <p id="registrationMessage"></p>
        </div>
        <!-- Fin Sección de Registro -->

        <div id="usuarios" class="section">
            <h2>Usuarios</h2>
            <p>El módulo de usuarios permite registrar nuevos usuarios, verificar credenciales y manejar acciones específicas para cada usuario.</p>
        </div>
        <div id="recursos" class="section">
            <h2>Recursos</h2>
            <p>El módulo de recursos gestiona la asignación de recursos como CPU y ancho de banda a los usuarios, y monitorea el uso de estos recursos.</p>
        </div>
        <div id="blockchain" class="section">
            <h2>Blockchain</h2>
            <p>El módulo de blockchain permite crear y gestionar una cadena de bloques, añadiendo transacciones y validando la integridad de la cadena.</p>
        </div>
        <div id="database" class="section">
            <h2>Base de Datos</h2>
            <p>El módulo de base de datos se encarga de conectar a una base de datos PostgreSQL, ejecutar consultas y manejar los resultados.</p>
        </div>
        <div id="compresion" class="section">
            <h2>Compresión</h2>
            <p>El módulo de compresión permite comprimir y guardar datos en archivos, así como cargar y descomprimir estos datos cuando sea necesario.</p>
        </div>
        <div id="servidor" class="section">
            <h2>Servidor</h2>
            <p>El módulo de servidor utiliza Flask y Socket.IO para manejar las rutas web y la transmisión de datos en tiempo real.</p>
        </div>
    </div>

    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    <script>
        const socket = io();

        // Manejadores existentes para el stream de audio (los mantenemos)
        // document.getElementById('sendButton').addEventListener('click', () => {
        //     const audioData = document.getElementById('audioInput').value;
        //     socket.emit('audio_stream', audioData);
        // });

        // socket.on('audio_stream', (data) => {
        //     console.log('Received audio data:', data);
        // });

        // Nuevas funciones para el registro
        function requestTemporalCode() {
            const username = document.getElementById('regUsername').value;
            const password = document.getElementById('regPassword').value;
            if (username && password) {
                socket.emit('request_code', { username: username, password: password });
            } else {
                document.getElementById('registrationMessage').innerText = 'Por favor, ingresa usuario y contraseña.';
            }
        }

        function verifyTemporalCode() {
            const username = document.getElementById('regUsername').value; // Necesitamos el usuario de nuevo para la verificación
            const temporalCode = document.getElementById('temporalCode').value;
             if (username && temporalCode) {
                socket.emit('verify_code', { username: username, code: temporalCode });
            } else {
                document.getElementById('registrationMessage').innerText = 'Por favor, ingresa el código temporal.';
            }
        }

        socket.on('code_requested', (data) => {
            document.getElementById('registrationMessage').innerText = data.message;
            if (data.success) {
                document.getElementById('codeVerification').style.display = 'block';
                document.getElementById('registrationForm').style.display = 'none'; // Ocultar el formulario inicial
            }
        });

        socket.on('registration_status', (data) => {
            document.getElementById('registrationMessage').innerText = data.message;
            if (data.success) {
                // Opcionalmente redirigir o mostrar mensaje de éxito y ocultar formulario
                document.getElementById('codeVerification').style.display = 'none';
                // document.getElementById('registrationForm').style.display = 'none'; // Ya está oculto
            } else {
                 // Mostrar la verificación de código de nuevo si falla, o el formulario inicial dependiendo del error
                 document.getElementById('codeVerification').style.display = 'block'; // Asumimos que un fallo significa reintentar el código
            }
        });

    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

# Manejador existente para el stream de audio
@socketio.on('audio_stream')
def handle_audio(data):
    socketio.emit('audio_stream', data)

# Nuevo evento de SocketIO para solicitar código temporal
@socketio.on('request_code')
def handle_request_code(data):
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        emit('code_requested', {'success': False, 'message': 'Usuario y contraseña son requeridos.'})
        return

    # Verificar si el usuario ya existe (verificación simplificada contra transacciones pendientes/minadas)
    # Se necesitaría una verificación más robusta en una aplicación real
    user_exists = False
    for block in blockchain.chain:
        if isinstance(block.get('data'), list):
            for transaction in block['data']:
                if transaction.get('type') == 'registro_usuario' and transaction.get('username') == username:
                    user_exists = True
                    break
        if user_exists: break
    for transaction in blockchain.pending_transactions:
        if transaction.get('type') == 'registro_usuario' and transaction.get('username') == username:
            user_exists = True
            break

    if user_exists:
         emit('code_requested', {'success': False, 'message': 'El usuario ya existe.'})
         return

    # Generar y almacenar código temporal
    code = generate_temporal_code()
    # Almacenamos la contraseña temporalmente para usarla al verificar el código
    temporal_codes[username] = {'code': code, 'timestamp': time.time(), 'password': password}
    print(f"Código generado {code} para el usuario {username}") # Log para demostración

    # En una aplicación real, enviarías este código por email/SMS.
    # Para este ejemplo, simplemente le diremos al usuario que lo ingrese.
    emit('code_requested', {'success': True, 'message': f'Código temporal generado. Por favor, ingresa el código para {username}. (Código: {code})'}) # Mostramos el código para la demo

# Nuevo evento de SocketIO para verificar código temporal y completar registro
@socketio.on('verify_code')
def handle_verify_code(data):
    username = data.get('username')
    code = data.get('code')

    if not username or not code:
        emit('registration_status', {'success': False, 'message': 'Usuario y código son requeridos.'})
        return

    stored_code_info = temporal_codes.get(username)

    if not stored_code_info:
        emit('registration_status', {'success': False, 'message': 'Solicita un código primero.'})
        return

    stored_code = stored_code_info['code']
    stored_timestamp = stored_code_info['timestamp']
    stored_password = stored_code_info['password'] # Recuperamos la contraseña almacenada

    # Verificar si el código es correcto y no ha expirado (30 segundos)
    if code == stored_code and (time.time() - stored_timestamp) <= 30:
        # Código válido, proceder con el registro a través de la blockchain
        try:
            # Usamos la función registrar_usuario del módulo usuarios.py
            registrar_usuario(blockchain, username, stored_password)
            # Limpiamos el código temporal después de un registro exitoso
            del temporal_codes[username]
            emit('registration_status', {'success': True, 'message': 'Usuario registrado con éxito en la blockchain. Se minará en el próximo bloque.'})
        except Exception as e:
            # Manejar posibles errores durante el registro en la blockchain
            emit('registration_status', {'success': False, 'message': f'Error al registrar usuario: {e}'})
    elif (time.time() - stored_timestamp) > 30:
        # Código expirado
        del temporal_codes[username] # Limpiar código expirado
        emit('registration_status', {'success': False, 'message': 'El código temporal ha expirado. Solicita uno nuevo.'})
    else:
        # Código incorrecto
        emit('registration_status', {'success': False, 'message': 'Código temporal incorrecto.'})


if __name__ == '__main__':
    # Nota: Ejecutar directamente con app.run() no funcionará con SocketIO.
    # Usar socketio.run(app, debug=True) como ya estaba presente.
    socketio.run(app, debug=True)
from flask import Flask, render_template_string, request, jsonify
from flask_socketio import SocketIO, emit
import hashlib
import time
import random # Para generar el código temporal

# Importamos los módulos necesarios
from blockchain import Blockchain
from usuarios import registrar_usuario, verificar_credenciales # Asumiendo que estas funciones usan la Blockchain

app = Flask(__name__)
socketio = SocketIO(app)

# Instanciamos la Blockchain (global para simplificar en este ejemplo)
blockchain = Blockchain()

# Diccionario para almacenar códigos temporales: {username: {'code': '1234', 'timestamp': time.time(), 'password': 'hashed_password'}}
temporal_codes = {}

def generate_temporal_code():
    """Genera un código temporal de 4 dígitos."""
    return str(random.randint(1000, 9999))

# HTML, CSS y JavaScript incluidos en una plantilla de cadena
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metaverso Crypto 3D</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }
        .header {
            background-color: #007bff;
            color: white;
            padding: 10px 0;
            text-align: center;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }
        .nav {
            display: flex;
            justify-content: center;
            background-color: #0056b3;
            padding: 10px 0;
        }
        .nav a {
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            font-weight: bold;
        }
        .nav a:hover {
            background-color: #003d80;
        }
        .container {
            margin-top: 100px;
            padding: 20px;
        }
        .section {
            background-color: #fff;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1, h2 {
            margin-top: 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Metaverso Crypto 3D</h1>
    </div>
    <div class="nav">
        <a href="#home">Inicio</a>
        <a href="#registration">Registro</a> <!-- Enlace añadido para Registro -->
        <a href="#usuarios">Usuarios</a>
        <a href="#recursos">Recursos</a>
        <a href="#blockchain">Blockchain</a>
        <a href="#database">Base de Datos</a>
        <a href="#compresion">Compresión</a>
        <a href="#servidor">Servidor</a>
    </div>
    <div class="container">
        <div id="home" class="section">
            <h2>Metaverso Crypto 3D descentralizado</h2>
            <p>Próximamente en esta página principal, se darán más detalles sobre el proyecto. Tenemos diferentes secciones que explicarán su función, dentro de cada módulo programado en Python.</p>
        </div>

        <!-- Sección de Registro -->
        <div id="registration" class="section">
            <h2>Registro de Usuario</h2>
            <form id="registrationForm">
                <label for="regUsername">Usuario:</label><br>
                <input type="text" id="regUsername" name="username" required><br><br>
                <label for="regPassword">Contraseña:</label><br>
                <input type="password" id="regPassword" name="password" required><br><br>
                <button type="button" onclick="requestTemporalCode()">Solicitar Código</button>
            </form>
            <div id="codeVerification" style="display:none;">
                <label for="temporalCode">Código Temporal:</label><br>
                <input type="text" id="temporalCode" name="temporal_code" required><br><br>
                <button type="button" onclick="verifyTemporalCode()">Verificar Código</button>
            </div>
            <p id="registrationMessage"></p>
        </div>
        <!-- Fin Sección de Registro -->

        <div id="usuarios" class="section">
            <h2>Usuarios</h2>
            <p>El módulo de usuarios permite registrar nuevos usuarios, verificar credenciales y manejar acciones específicas para cada usuario.</p>
        </div>
        <div id="recursos" class="section">
            <h2>Recursos</h2>
            <p>El módulo de recursos gestiona la asignación de recursos como CPU y ancho de banda a los usuarios, y monitorea el uso de estos recursos.</p>
        </div>
        <div id="blockchain" class="section">
            <h2>Blockchain</h2>
            <p>El módulo de blockchain permite crear y gestionar una cadena de bloques, añadiendo transacciones y validando la integridad de la cadena.</p>
        </div>
        <div id="database" class="section">
            <h2>Base de Datos</h2>
            <p>El módulo de base de datos se encarga de conectar a una base de datos PostgreSQL, ejecutar consultas y manejar los resultados.</p>
        </div>
        <div id="compresion" class="section">
            <h2>Compresión</h2>
            <p>El módulo de compresión permite comprimir y guardar datos en archivos, así como cargar y descomprimir estos datos cuando sea necesario.</p>
        </div>
        <div id="servidor" class="section">
            <h2>Servidor</h2>
            <p>El módulo de servidor utiliza Flask y Socket.IO para manejar las rutas web y la transmisión de datos en tiempo real.</p>
        </div>
    </div>

    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    <script>
        const socket = io();

        // Manejadores existentes para el stream de audio (los mantenemos)
        // document.getElementById('sendButton').addEventListener('click', () => {
        //     const audioData = document.getElementById('audioInput').value;
        //     socket.emit('audio_stream', audioData);
        // });

        // socket.on('audio_stream', (data) => {
        //     console.log('Received audio data:', data);
        // });

        // Nuevas funciones para el registro
        function requestTemporalCode() {
            const username = document.getElementById('regUsername').value;
            const password = document.getElementById('regPassword').value;
            if (username && password) {
                socket.emit('request_code', { username: username, password: password });
            } else {
                document.getElementById('registrationMessage').innerText = 'Por favor, ingresa usuario y contraseña.';
            }
        }

        function verifyTemporalCode() {
            const username = document.getElementById('regUsername').value; // Necesitamos el usuario de nuevo para la verificación
            const temporalCode = document.getElementById('temporalCode').value;
             if (username && temporalCode) {
                socket.emit('verify_code', { username: username, code: temporalCode });
            } else {
                document.getElementById('registrationMessage').innerText = 'Por favor, ingresa el código temporal.';
            }
        }

        socket.on('code_requested', (data) => {
            document.getElementById('registrationMessage').innerText = data.message;
            if (data.success) {
                document.getElementById('codeVerification').style.display = 'block';
                document.getElementById('registrationForm').style.display = 'none'; // Ocultar el formulario inicial
            }
        });

        socket.on('registration_status', (data) => {
            document.getElementById('registrationMessage').innerText = data.message;
            if (data.success) {
                // Opcionalmente redirigir o mostrar mensaje de éxito y ocultar formulario
                document.getElementById('codeVerification').style.display = 'none';
                // document.getElementById('registrationForm').style.display = 'none'; // Ya está oculto
            } else {
                 // Mostrar la verificación de código de nuevo si falla, o el formulario inicial dependiendo del error
                 document.getElementById('codeVerification').style.display = 'block'; // Asumimos que un fallo significa reintentar el código
            }
        });

    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

# Manejador existente para el stream de audio
@socketio.on('audio_stream')
def handle_audio(data):
    socketio.emit('audio_stream', data)

# Nuevo evento de SocketIO para solicitar código temporal
@socketio.on('request_code')
def handle_request_code(data):
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        emit('code_requested', {'success': False, 'message': 'Usuario y contraseña son requeridos.'})
        return

    # Verificar si el usuario ya existe (verificación simplificada contra transacciones pendientes/minadas)
    # Se necesitaría una verificación más robusta en una aplicación real
    user_exists = False
    for block in blockchain.chain:
        if isinstance(block.get('data'), list):
            for transaction in block['data']:
                if transaction.get('type') == 'registro_usuario' and transaction.get('username') == username:
                    user_exists = True
                    break
        if user_exists: break
    for transaction in blockchain.pending_transactions:
        if transaction.get('type') == 'registro_usuario' and transaction.get('username') == username:
            user_exists = True
            break

    if user_exists:
         emit('code_requested', {'success': False, 'message': 'El usuario ya existe.'})
         return

    # Generar y almacenar código temporal
    code = generate_temporal_code()
    # Almacenamos la contraseña temporalmente para usarla al verificar el código
    temporal_codes[username] = {'code': code, 'timestamp': time.time(), 'password': password}
    print(f"Código generado {code} para el usuario {username}") # Log para demostración

    # En una aplicación real, enviarías este código por email/SMS.
    # Para este ejemplo, simplemente le diremos al usuario que lo ingrese.
    emit('code_requested', {'success': True, 'message': f'Código temporal generado. Por favor, ingresa el código para {username}. (Código: {code})'}) # Mostramos el código para la demo

# Nuevo evento de SocketIO para verificar código temporal y completar registro
@socketio.on('verify_code')
def handle_verify_code(data):
    username = data.get('username')
    code = data.get('code')

    if not username or not code:
        emit('registration_status', {'success': False, 'message': 'Usuario y código son requeridos.'})
        return

    stored_code_info = temporal_codes.get(username)

    if not stored_code_info:
        emit('registration_status', {'success': False, 'message': 'Solicita un código primero.'})
        return

    stored_code = stored_code_info['code']
    stored_timestamp = stored_code_info['timestamp']
    stored_password = stored_code_info['password'] # Recuperamos la contraseña almacenada

    # Verificar si el código es correcto y no ha expirado (30 segundos)
    if code == stored_code and (time.time() - stored_timestamp) <= 30:
        # Código válido, proceder con el registro a través de la blockchain
        try:
            # Usamos la función registrar_usuario del módulo usuarios.py
            registrar_usuario(blockchain, username, stored_password)
            # Limpiamos el código temporal después de un registro exitoso
            del temporal_codes[username]
            emit('registration_status', {'success': True, 'message': 'Usuario registrado con éxito en la blockchain. Se minará en el próximo bloque.'})
        except Exception as e:
            # Manejar posibles errores durante el registro en la blockchain
            emit('registration_status', {'success': False, 'message': f'Error al registrar usuario: {e}'})
    elif (time.time() - stored_timestamp) > 30:
        # Código expirado
        del temporal_codes[username] # Limpiar código expirado
        emit('registration_status', {'success': False, 'message': 'El código temporal ha expirado. Solicita uno nuevo.'})
    else:
        # Código incorrecto
        emit('registration_status', {'success': False, 'message': 'Código temporal incorrecto.'})


if __name__ == '__main__':
    # Nota: Ejecutar directamente con app.run() no funcionará con SocketIO.
    # Usar socketio.run(app, debug=True) como ya estaba presente.
    socketio.run(app, debug=True)
from flask import Flask, render_template_string
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# HTML, CSS y JavaScript incluidos en una plantilla de cadena
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metaverso Crypto 3D</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }
        .header {
            background-color: #007bff;
            color: white;
            padding: 10px 0;
            text-align: center;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }
        .nav {
            display: flex;
            justify-content: center;
            background-color: #0056b3;
            padding: 10px 0;
        }
        .nav a {
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            font-weight: bold;
        }
        .nav a:hover {
            background-color: #003d80;
        }
        .container {
            margin-top: 100px;
            padding: 20px;
        }
        .section {
            background-color: #fff;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1, h2 {
            margin-top: 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Metaverso Crypto 3D</h1>
    </div>
    <div class="nav">
        <a href="./Metaverso_Crypto/inicio/Blockchain_Principal/secciones/inicio.html">Inicio</a>
        <a href="#usuarios">Usuarios</a>
        <a href="#recursos">Recursos</a>
        <a href="#blockchain">Blockchain</a>
        <a href="#database">Base de Datos</a>
        <a href="#compresion">Compresión</a>
        <a href="#servidor">Servidor</a>
    </div>
    <div class="container">
        <div id="home" class="section">
            <h2>Metaverso Crypto 3D descentralizado</h2>
            <p>Próximamente en esta página principal, se darán más detalles sobre el proyecto. Tenemos diferentes secciones que explicarán su función, dentro de cada módulo programado en Python.</p>
        </div>
        <div id="usuarios" class="section">
            <h2>Usuarios</h2>
            <p>El módulo de usuarios permite registrar nuevos usuarios, verificar credenciales y manejar acciones específicas para cada usuario.</p>
        </div>
        <div id="recursos" class="section">
            <h2>Recursos</h2>
            <p>El módulo de recursos gestiona la asignación de recursos como CPU y ancho de banda a los usuarios, y monitorea el uso de estos recursos.</p>
        </div>
        <div id="blockchain" class="section">
            <h2>Blockchain</h2>
            <p>El módulo de blockchain permite crear y gestionar una cadena de bloques, añadiendo transacciones y validando la integridad de la cadena.</p>
        </div>
        <div id="database" class="section">
            <h2>Base de Datos</h2>
            <p>El módulo de base de datos se encarga de conectar a una base de datos PostgreSQL, ejecutar consultas y manejar los resultados.</p>
        </div>
        <div id="compresion" class="section">
            <h2>Compresión</h2>
            <p>El módulo de compresión permite comprimir y guardar datos en archivos, así como cargar y descomprimir estos datos cuando sea necesario.</p>
        </div>
        <div id="servidor" class="section">
            <h2>Servidor</h2>
            <p>El módulo de servidor utiliza Flask y Socket.IO para manejar las rutas web y la transmisión de datos en tiempo real.</p>
        </div>
    </div>

    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    <script>
        const socket = io();

        document.getElementById('sendButton').addEventListener('click', () => {
            const audioData = document.getElementById('audioInput').value;
            socket.emit('audio_stream', audioData);
        });

        socket.on('audio_stream', (data) => {
            console.log('Received audio data:', data);
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@socketio.on('audio_stream')
def handle_audio(data):
    socketio.emit('audio_stream', data)

if __name__ == '__main__':
    socketio.run(app, debug=True)
