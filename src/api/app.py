import os
from flask import Flask, send_file
from models import db, User
from routes import api

app = Flask(__name__)

# --- Configuración de la base de datos (SQLite) ---
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usuarios.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --- Configuración de subida de archivos ---
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # Máximo: 5 MB

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

EXTENSIONES_PERMITIDAS = {"png", "jpg", "jpeg", "gif"}

def extension_permitida(nombre_archivo):
    return (
        "." in nombre_archivo
        and nombre_archivo.rsplit(".", 1)[1].lower() in EXTENSIONES_PERMITIDAS
    )

# --- Conectar la base de datos y registrar las rutas ---
db.init_app(app)
app.register_blueprint(api, url_prefix="/api")


# ---- Páginas de la carpeta page/ ----
def pagina(nombre_archivo):
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "page", nombre_archivo)
    return send_file(ruta)


@app.route("/")
def pagina_home():
    return pagina("home.html")


@app.route("/ingresar")
def pagina_ingresar():
    return pagina("ingresar.html")


# ---- Página del formulario de usuarios ----
@app.route("/usuarios")
def pagina_usuarios():
    ruta_html = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usuarios.html")
    return send_file(ruta_html)


# --- Crear las tablas la primera vez ---
with app.app_context():
    db.create_all()

# --- Arrancar el servidor ---
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
