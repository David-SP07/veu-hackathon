from models.dbModels import Unidad, db, Turno, Conductor, Centro
from flask_login import current_user


# <-------------------> VALIDAR TURNO ACTIVO <------------------->
def verificar_turno_activo():
    # Verifica si el usuario está autenticado
    if not current_user.is_authenticated:
        return {'vehiculo': None}  # Si no está autenticado, no puede tener un turno activo

    # Buscar un turno activo del conductor
    turno_activo = Turno.query.filter_by(conductor_id=current_user.id, estado='Reservado').first()

    if turno_activo:
        # Si tiene un turno activo, obtener la información del vehículo
        vehiculo_info = {
            'nombre': turno_activo.unidad.nombre,
            'centro': turno_activo.centro.nombre,
            'placa': turno_activo.unidad.placa,
            'modelo': turno_activo.unidad.modelo,
            'ano': turno_activo.unidad.year,
            'mantenimiento': "En buenas condiciones"  # Este dato puede venir de la unidad o historial
        }
        return {'vehiculo': vehiculo_info}  # Devuelve los detalles del vehículo
    else:
        # Si no hay turno activo, devolver None
        return {'vehiculo': None}  # No hay vehículo reservado

# <-------------------> ESTADO DE LA UNIDAD <------------------->
def obtener_estado_unidad_service(unidad_id):
    unidad = Unidad.query.get(unidad_id)

    if not unidad:
        return {"respuesta": {"error": "Unidad no encontrada."}, "status": 404}

    unidad_info = {
        "unidad_id": unidad.id,
        "nombre": unidad.nombre,
        "estado_salud": unidad.estado_salud
    }

    return {"respuesta": unidad_info, "status": 200}

# <-------------------> REGISTRAR VEHÍCULO <------------------->
from models.dbModels import Unidad, db

def registrar_vehiculo_service(data):
    nombre = data.get('nombre')
    centro_id = data.get('centro_id')
    estado_salud = data.get('estado_salud', 'Verde')

    placa = data.get('placa')
    modelo = data.get('modelo')
    year = data.get('year')

    if not all([nombre, centro_id, placa, modelo, year]):
        return {"respuesta": {"error": "Faltan datos requeridos."}, "status": 400}

    nueva_unidad = Unidad(
        nombre=nombre,
        centro_id=centro_id,
        estado_salud=estado_salud,
        placa=placa,
        modelo=modelo,
        year=year
    )
    db.session.add(nueva_unidad)
    db.session.commit()

    return {
        "respuesta": {
            "mensaje": "Vehículo registrado exitosamente.",
            "unidad_id": nueva_unidad.id
        },
        "status": 201
    }

# <-------------------> ELIMINAR VEHÍCULO <------------------->
def eliminar_vehiculo_service(unidad_id):
    unidad = Unidad.query.get(unidad_id)

    if not unidad:
        return {"respuesta": {"error": "Unidad no encontrada."}, "status": 404}

    db.session.delete(unidad)
    db.session.commit()

    return {"respuesta": {"mensaje": "Vehículo eliminado exitosamente."}, "status": 200}

# <-------------------> OBTENER CENTROS <------------------->
def obtener_centros_service():
    # Obtener todos los centros desde la base de datos
    centros = Centro.query.all()
    return centros