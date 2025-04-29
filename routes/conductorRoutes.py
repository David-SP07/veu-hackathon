
from flask import Blueprint, jsonify
from services.conductorService import obtener_perfil_conductor_service, obtener_estadisticas_conductor_service

conductor_bp = Blueprint('conductor_bp', __name__)

# <-------------------> VER PERFIL CONDUCTOR <------------------->
@conductor_bp.route('/api/conductor/perfil/<int:conductor_id>', methods=['GET'])
def obtener_perfil_conductor(conductor_id):
    resultado = obtener_perfil_conductor_service(conductor_id)
    return jsonify(resultado["respuesta"]), resultado["status"]


# <-------------------> VER HISTORIAL DE TURNOS <------------------->
@conductor_bp.route('/api/conductor/estadisticas/<int:conductor_id>', methods=['GET'])
def obtener_estadisticas_conductor(conductor_id):
    resultado = obtener_estadisticas_conductor_service(conductor_id)
    return jsonify(resultado["respuesta"]), resultado["status"]