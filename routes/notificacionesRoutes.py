from flask import Blueprint, request, jsonify
from services.notificacionesService import enviar_notificacion_service
from models.dbModels import db

notificaciones_bp = Blueprint('notificaciones_bp', __name__)

# <-------------------> ENVÍO DE NOTIFICACIONES <------------------->
@notificaciones_bp.route('/api/notificar', methods=['POST'])
def enviar_notificacion():
    """
    Ruta para simular el envío de una notificación push.
    """
    data = request.get_json()
    resultado = enviar_notificacion_service(data)
    return jsonify(resultado["respuesta"]), resultado["status"]