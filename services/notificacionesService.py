from models.dbModels import Notificacion, db

def enviar_notificacion_service(data):
    titulo = data.get('titulo')
    cuerpo = data.get('cuerpo')

    if not all([titulo, cuerpo]):
        return {"respuesta": {"error": "Título y cuerpo son obligatorios."}, "status": 400}

    # Guardamos la notificación en la base de datos
    nueva_notificacion = Notificacion(
        conductor_id=data.get('conductor_id'),
        mensaje=f"{titulo} - {cuerpo}",
        estado="Pendiente"
    )

    db.session.add(nueva_notificacion)
    db.session.commit()

    # Simulación de envío de notificación
    print(f"Simulando notificación: {titulo} - {cuerpo}")

    return {"respuesta": {"mensaje": "Notificación simulada correctamente."}, "status": 200}