from models.dbModels import Conductor, Turno, Historial

# <-------------------> VER PERFIL CONDUCTOR <------------------->
def obtener_perfil_conductor_service(conductor_id):
    conductor = Conductor.query.get(conductor_id)

    if not conductor:
        return {"respuesta": {"error": "Conductor no encontrado."}, "status": 404}

    perfil = {
        "id": conductor.id,
        "nombre": conductor.nombre,
        "email": conductor.email,
        "puntos": conductor.puntos,
        "fecha_registro": conductor.fecha_registro.isoformat()
    }

    return {"respuesta": perfil, "status": 200}


# <-------------------> VER HISTORIAL DE TURNOS <------------------->
def obtener_estadisticas_conductor_service(conductor_id):
    turnos_completados = Turno.query.filter_by(conductor_id=conductor_id, estado="Completado").count()
    
    historiales = Historial.query.join(Turno).filter(Turno.conductor_id == conductor_id).all()

    total_km = sum(historial.distancia_recorrida or 0 for historial in historiales)
    total_ingresos = sum(historial.ingresos_generados or 0 for historial in historiales)

    estadisticas = {
        "turnos_completados": turnos_completados,
        "total_kilometros": round(total_km, 2),
        "total_ingresos": round(total_ingresos, 2)
    }

    return {"respuesta": estadisticas, "status": 200}

def obtener_estadisticas_conductor(conductor_id):
    conductor = Conductor.query.get(conductor_id)
    if not conductor:
        return {"error": "Conductor no encontrado"}

    turnos = Turno.query.filter_by(conductor_id=conductor_id).all()

    turnos_completados = sum(1 for t in turnos if t.estado == 'Completado')
    reservas_activas = sum(1 for t in turnos if t.estado == 'Reservado')
    
    total_kilometros = 0
    total_ingresos = 0
    for turno in turnos:
        if turno.historial:
            total_kilometros += turno.historial.distancia_recorrida or 0
            total_ingresos += turno.historial.ingresos_generados or 0

    return {
        "nombre": conductor.nombre,
        "fecha_registro": conductor.fecha_registro.isoformat(),
        "turnos_completados": turnos_completados,
        "reservas_activas": reservas_activas,
        "total_kilometros": round(total_kilometros, 2),
        "total_ingresos": round(total_ingresos, 2)
    }