from flask import Flask
from backend.routes.user_routes import user_routes

app = Flask(__name__)

# Configuración de rutas
app.register_blueprint(user_routes)

@app.route('/')
def home():
    return "Página de administración inicial"

if __name__ == '__main__':
    app.run(debug=True)