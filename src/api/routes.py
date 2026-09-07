from flask import Blueprint, request, jsonify, session
from models import db, User

api = Blueprint("api", __name__)

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
    body = request.get_json()

    if body is None:
        return jsonify({"error": "El cuerpo de la solicitud no puede estar vacío"}), 400
    if 'nombre' not in body:
        return jsonify({"error": "El campo 'nombre' es requerido"}), 400
    if 'email' not in body:
        return jsonify({"error": "El campo 'email' es requerido"}), 400
    if 'password' not in body:
        return jsonify({"error": "El campo 'password' es requerido"}), 400

    # Verificar que el email no exista ya
    usuario_existente = User.query.filter_by(email=body['email']).first()
    if usuario_existente:
        return jsonify({"error": "Ese email ya está registrado"}), 400

    nuevo_usuario = User(
        nombre=body['nombre'],
        email=body['email'],
        password=body['password'],
        is_active=body.get('is_active', True)
    )

    db.session.add(nuevo_usuario)
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
