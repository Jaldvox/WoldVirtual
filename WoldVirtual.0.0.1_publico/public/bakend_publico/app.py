# bakend/app.py

import os
from datetime import timedelta
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, current_user
from flask_cors import CORS
from models import db, bcrypt, User, VerificationCode
import hashlib
import time
from functools import wraps

# --- Decorador para verificar si el usuario es administrador ---

def admin_required():
    
    def wrapper(fn):
        @wraps(fn)
        @jwt_required() # Asegura que el usuario esté logueado
        def decorator(*args, **kwargs):
            print(f"DEBUG: Verificando rol para usuario ID: {current_user.id}, Rol: {current_user.role}")
            if current_user.role != 'admin':
                return jsonify({"message": "Acceso denegado: Se requiere rol de administrador."}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

# --- Rutas de la API ---
# ... (resto de tus rutas) ...

def create_app():

    app = Flask(__name__)

    # ... dentro de create_app()
    # Inicialización de JWTManager (ya lo tienes)
    jwt = JWTManager(app)

    # NUEVO: Función para cargar usuario desde el ID del token
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()

    # --- Manejo de Errores para Flask-JWT-Extended ---
    # ... (tus manejadores de error de JWT que ya tienes) ...

    # Configuración de la aplicación
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'user.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'clave_secreta_para_jwt'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

    # Inicialización de extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    CORS(app)

    # Add root route to show backend is running
    @app.route('/')
    def home():
        return jsonify({'message': 'Backend server is running!'}), 200

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Faltan datos'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'El usuario ya existe'}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        code, hash_value, expires_at = VerificationCode.generate_code()
        verification_code = VerificationCode(code=code, hash=hash_value, expires_at=expires_at, user_id=user.id)
        db.session.add(verification_code)
        db.session.commit()

        return jsonify({'message': 'Usuario registrado', 'code': code, 'hash': hash_value}), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        code = data.get('code')
        hash_value = data.get('hash')

        user = User.query.filter_by(username=username).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({'error': 'Credenciales inválidas'}), 401

        if not VerificationCode.verify_code(code, hash_value):
            return jsonify({'error': 'Código inválido o expirado'}), 401

        session_hash = hashlib.sha256(f"{username}{time.time()}".encode()).hexdigest()
        user.session_hash = session_hash
        db.session.commit()

        return jsonify({'message': 'Inicio de sesión exitoso', 'session_hash': session_hash, 'profile': user.to_dict()}), 200

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        user_list = [{'id': user.id, 'username': user.username, 'session_hash': user.session_hash} for user in users]
        return jsonify(user_list), 200

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    print(" * Backend server is running on http://localhost:5000")
    app.run(debug=True, port=5000)