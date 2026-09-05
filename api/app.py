import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # Máximo: 5 MB

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

EXTENSIONES_PERMITIDAS = {"png", "jpg", "jpeg", "gif"}

def extension_permitida(nombre_archivo):
    return (
        "." in nombre_archivo
        and nombre_archivo.rsplit(".", 1)[1].lower() in EXTENSIONES_PERMITIDAS
    )