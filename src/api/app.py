import os
from flask import Flask, send_file, send_from_directory, redirect, session
from models import db, User
from routes import api

app = Flask(__name__)

# --- Configuración de la base de datos (SQLite) ---
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usuarios.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --- Configuración de subida de archivos ---
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # Máximo: 5 MB
# Clave para firmar las sesiones
app.config["SECRET_KEY"] = "clave-secreta-de-practica-apifernando"

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


@app.route("/registro")
def pagina_registro():
    return pagina("registro.html")


# ---- Página de la lista de usuarios (requiere sesión) ----
@app.route("/usuarios")
def pagina_usuarios():
    if "usuario_id" not in session:
        return redirect("/ingresar")
    ruta_html = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usuarios.html")
    return send_file(ruta_html)


# ---- Cerrar sesión ----
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/uploads/<path:nombre>")
def archivos_subidos(nombre):
    return send_from_directory(app.config["UPLOAD_FOLDER"], nombre)


# --- Crear las tablas la primera vez ---
with app.app_context():
    db.create_all()

# --- Arrancar el servidor ---
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
