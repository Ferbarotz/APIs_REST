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