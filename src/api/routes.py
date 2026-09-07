import os
from flask import Blueprint, request, jsonify, session, current_app
from werkzeug.utils import secure_filename
from models import db, User

api = Blueprint("api", __name__)

EXTENSIONES_PERMITIDAS = {"png", "jpg", "jpeg", "gif"}


def _extension_permitida(nombre_archivo):
    return (
        "." in nombre_archivo
        and nombre_archivo.rsplit(".", 1)[1].lower() in EXTENSIONES_PERMITIDAS
    )


# GET /api/usuarios  →  listar todos
@api.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = User.query.all()
    return jsonify([u.serialize() for u in usuarios]), 200


# GET /api/usuarios/<id>  →  ver uno solo
@api.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = db.session.get(User, id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario.serialize()), 200


# POST /api/usuarios  →  crear
@api.route('/usuarios', methods=['POST'])
def create_usuario():
    body = request.get_json(silent=True)
    form_data = request.form

    nombre = (body or form_data).get('nombre')
    email = (body or form_data).get('email')
    password = (body or form_data).get('password')

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es requerido"}), 400
    if not email:
        return jsonify({"error": "El campo 'email' es requerido"}), 400
    if not password:
        return jsonify({"error": "El campo 'password' es requerido"}), 400

    # Verificar que el email no exista ya
    usuario_existente = User.query.filter_by(email=email).first()
    if usuario_existente:
        return jsonify({"error": "Ese email ya está registrado"}), 400

    archivo = request.files.get('foto')
    if archivo and archivo.filename != '' and not _extension_permitida(archivo.filename):
        return jsonify({"error": "Formato no permitido. Usa png, jpg, jpeg o gif"}), 400

    is_active = True
    if body is not None:
        is_active = body.get('is_active', True)

    nuevo_usuario = User(
        nombre=nombre,
        email=email,
        password=password,
        is_active=is_active
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    if archivo and archivo.filename != '':
        nombre_seguro = secure_filename(archivo.filename)
        nombre_guardado = f"usuario_{nuevo_usuario.id}_{nombre_seguro}"
        ruta = os.path.join(current_app.config['UPLOAD_FOLDER'], nombre_guardado)
        archivo.save(ruta)
        nuevo_usuario.foto = f"/uploads/{nombre_guardado}"
        db.session.commit()

    return jsonify({
        "mensaje": "Usuario creado correctamente",
        "usuario": nuevo_usuario.serialize()
    }), 201


# POST /api/login  →  iniciar sesión
@api.route('/login', methods=['POST'])
def login_usuario():
    body = request.get_json()

    if body is None or 'email' not in body or 'password' not in body:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400

    usuario = User.query.filter_by(email=body['email']).first()
    if not usuario or body['password'] != usuario.password:
        return jsonify({"error": "Email o contraseña incorrectos"}), 401

    session['usuario_id'] = usuario.id
    session['usuario_nombre'] = usuario.nombre

    return jsonify({
        "mensaje": "Inicio de sesión exitoso",
        "usuario": usuario.serialize()
    }), 200


# PUT /api/usuarios/<id>  →  actualizar
@api.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    usuario = db.session.get(User, id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    body = request.get_json()
    if body is None:
        return jsonify({"error": "El cuerpo de la solicitud no puede estar vacío"}), 400

    if 'nombre' in body:
        usuario.nombre = body['nombre']
    if 'email' in body:
        existe = User.query.filter(User.email == body['email'], User.id != id).first()
        if existe:
            return jsonify({"error": "Ese email ya está registrado"}), 400
        usuario.email = body['email']
    if 'password' in body:
        usuario.password = body['password']
    if 'is_active' in body:
        usuario.is_active = body['is_active']

    db.session.commit()

    return jsonify({
        "mensaje": "Usuario actualizado correctamente",
        "usuario": usuario.serialize()
    }), 200


# DELETE /api/usuarios/<id>  →  borrar
@api.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = db.session.get(User, id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario eliminado correctamente"}), 200


# GET /api/yo  →  ver usuario logueado
@api.route('/yo', methods=['GET'])
def usuario_logueado():
    if "usuario_id" not in session:
        return jsonify({"error": "No has iniciado sesión"}), 401

    usuario = db.session.get(User, session['usuario_id'])
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(usuario.serialize()), 200


# POST /api/foto  →  subir foto del usuario logueado
@api.route('/foto', methods=['POST'])
def subir_foto_usuario():
    if "usuario_id" not in session:
        return jsonify({"error": "Debes iniciar sesión"}), 401

    usuario = db.session.get(User, session['usuario_id'])
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if 'foto' not in request.files:
        return jsonify({"error": "No se recibió ningún archivo"}), 400

    archivo = request.files['foto']

    if archivo.filename == '':
        return jsonify({"error": "No elegiste ningún archivo"}), 400

    if not _extension_permitida(archivo.filename):
        return jsonify({"error": "Formato no permitido. Usa png, jpg, jpeg o gif"}), 400

    nombre_seguro = secure_filename(archivo.filename)
    nombre_guardado = f"usuario_{usuario.id}_{nombre_seguro}"
    ruta = os.path.join(current_app.config['UPLOAD_FOLDER'], nombre_guardado)

    archivo.save(ruta)

    usuario.foto = f"/uploads/{nombre_guardado}"
    db.session.commit()

    return jsonify({
        "mensaje": "Foto actualizada correctamente",
        "usuario": usuario.serialize()
    }), 200
