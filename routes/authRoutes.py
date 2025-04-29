from flask import Blueprint, request, jsonify
from services.authService import registrar_conductor, iniciar_sesion
from werkzeug.security import check_password_hash
from models.dbModels import Conductor
from flask_login import login_user

auth_bp = Blueprint('auth_bp', __name__)

# <-------------------> REGISTER <------------------->
@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    resultado = registrar_conductor(data)
    return jsonify(resultado["respuesta"]), resultado["status"]


# <-------------------> LOGIN <------------------->
@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()  # Obtenemos los datos en JSON
    email = data.get('email')
    password = data.get('password')

    # Buscar al conductor por email
    conductor = Conductor.query.filter_by(email=email).first()

    if conductor and check_password_hash(conductor.password_hash, password):
        # Si el correo y la contraseña son correctos
        login_user(conductor)  # Iniciar sesión

        # Retornar una respuesta de éxito con los datos del conductor
        return jsonify({
            "mensaje": "Login exitoso",
            "usuario": {
                "id": conductor.id,
                "nombre": conductor.nombre,
                "email": conductor.email,
                "puntos": conductor.puntos,
                "fecha_registro": conductor.fecha_registro
            }
        }), 200
    else:
        # Si el correo o la contraseña son incorrectos
        return jsonify({"mensaje": "Correo o contraseña incorrectos"}), 401