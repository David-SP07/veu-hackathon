from flask import Blueprint, request, jsonify
from services.centroService import obtener_centros_service, registrar_centro_service

centro_bp = Blueprint('centro_bp', __name__)

# <-------------------> VER CENTROS <------------------->
@centro_bp.route('/api/centros', methods=['GET'])
def get_centros():
    resultado = obtener_centros_service()
    return jsonify(resultado["respuesta"]), resultado["status"]

# <-------------------> REGISTRAR CENTRO <------------------->
@centro_bp.route('/api/centro/register', methods=['POST'])
def registrar_centro():
    data = request.get_json()
    resultado = registrar_centro_service(data)
    return jsonify(resultado["respuesta"]), resultado["status"]