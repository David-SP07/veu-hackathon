from models.dbModels import Centro

# <-------------------> VER CENTROS <------------------->
def obtener_centros_service():
    centros = Centro.query.all()

    centros_list = []
    for centro in centros:
        centros_list.append({
            'id': centro.id,
            'nombre': centro.nombre,
            'latitud': centro.latitud,
            'longitud': centro.longitud
        })

    return {"respuesta": centros_list, "status": 200}


# <-------------------> REGISTRAR CENTRO <------------------->
def registrar_centro_service(data):
    try:
        nombre = data.get("nombre")
        latitud = data.get("latitud")
        longitud = data.get("longitud")

        if not all([nombre, latitud, longitud]):
            return {"respuesta": {"mensaje": "Faltan datos requeridos."}, "status": 400}

        nuevo_centro = Centro(
            nombre=nombre,
            latitud=latitud,
            longitud=longitud
        )
        from app import db  # importar aquí para evitar errores circulares
        db.session.add(nuevo_centro)
        db.session.commit()

        return {
            "respuesta": {
                "mensaje": "Centro registrado exitosamente.",
                "centro_id": nuevo_centro.id
            },
            "status": 201
        }
    except Exception as e:
        from app import db
        db.session.rollback()
        return {"respuesta": {"mensaje": f"Error al registrar el centro: {str(e)}"}, "status": 500}