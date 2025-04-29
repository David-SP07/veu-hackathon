from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from services.vehiculoService import registrar_vehiculo_service, eliminar_vehiculo_service, obtener_estado_unidad_service, verificar_turno_activo
from flask_login import login_required
from models.dbModels import Unidad

vehiculo_bp = Blueprint('vehiculo_bp', __name__)

# <-------------------> ESTADO DE LA UNIDAD <------------------->
@vehiculo_bp.route('/api/vehiculo/estado/<int:unidad_id>', methods=['GET'])
def obtener_estado_unidad(unidad_id):
    resultado = obtener_estado_unidad_service(unidad_id)
    return jsonify(resultado["respuesta"]), resultado["status"]

# <-------------------> REGISTRAR VEHÍCULO <------------------->
@vehiculo_bp.route('/api/vehiculo/register', methods=['POST'])
def registrar_vehiculo():
    data = request.get_json()
    resultado = registrar_vehiculo_service(data)
    return jsonify(resultado["respuesta"]), resultado["status"]

# <-------------------> ELIMINAR VEHÍCULO <------------------->
@vehiculo_bp.route('/api/vehiculo/delete/<int:unidad_id>', methods=['DELETE'])
def eliminar_vehiculo(unidad_id):
    resultado = eliminar_vehiculo_service(unidad_id)
    return jsonify(resultado["respuesta"]), resultado["status"]

# <-------------------> VEHÍCULO ACTIVO <------------------->
@vehiculo_bp.route('/estadovehiculoactivo', methods=['GET'])
@login_required
def estado_vehiculo_activo():
    resultado = verificar_turno_activo()  # Llamada al servicio que verificará el estado del vehículo
    if resultado['vehiculo']:
        # Si hay un vehículo activo, muestra la información
        return render_template('estadovehiculoactivo.html', vehiculo=resultado['vehiculo'])
    else:
        # Si no hay vehículo activo, redirige a la página de "vehículo inactivo"
        return redirect(url_for('vehiculo_bp.estado_vehiculo_inactivo'))
    

# <-------------------> VEHÍCULO INACTIVO <------------------->
@vehiculo_bp.route('/estadovehiculoinaactivo', methods=['GET'])
@login_required
def estado_vehiculo_inactivo():
    return render_template('estadovehiculoinaactivo.html')

@vehiculo_bp.route('/api/unidades', methods=['GET'])
def obtener_unidades():
    unidades = Unidad.query.all()
    unidades_data = [{
        'id': unidad.id,
        'nombre': unidad.nombre
    } for unidad in unidades]
    return jsonify(unidades_data), 200