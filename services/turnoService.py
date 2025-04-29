from models.dbModels import Turno, db, Centro
from datetime import datetime

def round_to_nearest_half_hour(dt):
    # Redondear hacia abajo al múltiplo más cercano de 30 minutos
    minutes = (dt.minute // 30) * 30
    return dt.replace(minute=minutes, second=0, microsecond=0)


# <-------------------> RESERVAR TURNO <------------------->
def reservar_turno_service(data):
    conductor_id = data.get('conductor_id')
    unidad_id = data.get('unidad_id')
    centro_id = data.get('centro_id')
    fecha_inicio = data.get('fecha_inicio')
    fecha_fin = data.get('fecha_fin')

    if not all([conductor_id, unidad_id, centro_id, fecha_inicio, fecha_fin]):
        return {"respuesta": {"error": "Faltan datos para reservar el turno."}, "status": 400}

    try:
        # Convertir las fechas a objetos datetime
        fecha_inicio_dt = datetime.fromisoformat(fecha_inicio)
        fecha_fin_dt = datetime.fromisoformat(fecha_fin)

        # Redondear las fechas a los intervalos más cercanos de 30 minutos
        fecha_inicio_dt = round_to_nearest_half_hour(fecha_inicio_dt)
        fecha_fin_dt = round_to_nearest_half_hour(fecha_fin_dt)

    except ValueError:
        return {"respuesta": {"error": "Formato de fecha inválido. Usa ISO 8601."}, "status": 400}

    # Validar que no haya conflicto de turnos para la unidad
    turnos_existentes = Turno.query.filter(
        Turno.unidad_id == unidad_id,
        Turno.estado == 'Reservado',
        Turno.fecha_inicio < fecha_fin_dt,
        Turno.fecha_fin > fecha_inicio_dt
    ).all()

    if turnos_existentes:
        return {"respuesta": {"error": "La unidad ya tiene un turno reservado en ese horario."}, "status": 409}

    # Crear el nuevo turno
    nuevo_turno = Turno(
        conductor_id=conductor_id,
        unidad_id=unidad_id,
        centro_id=centro_id,
        fecha_inicio=fecha_inicio_dt,
        fecha_fin=fecha_fin_dt,
        estado="Reservado"
    )

    db.session.add(nuevo_turno)
    db.session.commit()

    return {"respuesta": {"mensaje": "Turno reservado exitosamente."}, "status": 201}

# <-------------------> VER MIS TURNOS <------------------->
def obtener_mis_turnos_service(conductor_id):
    # Filtra los turnos por conductor_id y ordena por fecha_inicio descendente
    turnos = Turno.query.filter_by(conductor_id=conductor_id).order_by(Turno.fecha_inicio.desc()).all()

    if not turnos:
        return {"respuesta": {"error": "No se encontraron turnos para este conductor."}, "status": 404}

    # Construcción de la lista de turnos con formato adecuado
    turnos_list = [
        {
            'id': turno.id,
            'centro_id': turno.centro_id,
            'unidad_id': turno.unidad_id,
            'fecha_inicio': turno.fecha_inicio.isoformat() if isinstance(turno.fecha_inicio, datetime) else str(turno.fecha_inicio),
            'fecha_fin': turno.fecha_fin.isoformat() if isinstance(turno.fecha_fin, datetime) else str(turno.fecha_fin),
            'estado': turno.estado
        }
        for turno in turnos
    ]

    return {"respuesta": turnos_list, "status": 200}


# <-------------------> OBTENER CENTROS <------------------->
def obtener_centros_service():
    centros = Centro.query.all()  # Obtiene todos los centros desde la base de datos
    return {"respuesta": centros, "status": 200}