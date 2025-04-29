from flask import Blueprint, request, jsonify
from services.turnoService import reservar_turno_service, obtener_mis_turnos_service

turno_bp = Blueprint('turno_bp', __name__)

# <-------------------> RESERVAR TURNO <------------------->
@turno_bp.route('/api/reservar-turno', methods=['POST'])
def reservar_turno():
    data = request.get_json()  # Obtener datos del formulario (JSON)
    resultado = reservar_turno_service(data)  # Llamar al servicio
    return jsonify(resultado["respuesta"]), resultado["status"]


# <-------------------> VER MIS TURNOS <------------------->
@turno_bp.route('/api/mis-turnos/<int:conductor_id>', methods=['GET'])
def obtener_mis_turnos(conductor_id):
    resultado = obtener_mis_turnos_service(conductor_id)
    return jsonify(resultado["respuesta"]), resultado["status"]