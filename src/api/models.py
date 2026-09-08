from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    foto = db.Column(db.String(255), nullable=True)

    def set_password(self, password_plano):
        """Guarda la contraseña con hash seguro."""
        self.password = generate_password_hash(password_plano)

    def check_password(self, password_plano):
        """Verifica contraseña. Soporta hash nuevo y texto plano legacy (migra)."""
        if not self.password or not password_plano:
            return False
        # 1) Caso nuevo: hash werkzeug (pbkdf2:..., scrypt:...)
        if self.password.startswith(("pbkdf2:", "scrypt:")):
            try:
                return check_password_hash(self.password, password_plano)
            except ValueError:
                return False
        # 2) Caso legacy: texto plano (usuarios creados antes del hash)
        return self.password == password_plano

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "is_active": self.is_active,
            "foto": self.foto
        }