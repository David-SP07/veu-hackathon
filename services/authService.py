from models.dbModels import Conductor, db
from werkzeug.security import generate_password_hash, check_password_hash

# <-------------------> REGISTER <------------------->
def registrar_conductor(data):
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    if not all([nombre, email, password]):
        return {"respuesta": {"error": "Todos los campos son obligatorios."}, "status": 400}

    if Conductor.query.filter_by(email=email).first():
        return {"respuesta": {"error": "El email ya está registrado."}, "status": 409}

    password_hash = generate_password_hash(password)

    nuevo_conductor = Conductor(
        nombre=nombre,
        email=email,
        password_hash=password_hash,
        puntos=0
    )

    db.session.add(nuevo_conductor)
    db.session.commit()

    print(data)

    return {"respuesta": {"mensaje": "Registro exitoso."}, "status": 201}


# <-------------------> LOGIN <------------------->
def iniciar_sesion(data):
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return {"respuesta": {"error": "Todos los campos son obligatorios."}, "status": 400}

    conductor = Conductor.query.filter_by(email=email).first()

    if not conductor:
        return {"respuesta": {"error": "Credenciales inválidas."}, "status": 401}

    if not check_password_hash(conductor.password_hash, password):
        return {"respuesta": {"error": "Credenciales inválidas."}, "status": 401}

    return {"respuesta": {
                "mensaje": "Inicio de sesión exitoso.",
                "conductor_id": conductor.id,
                "nombre": conductor.nombre
            }, "status": 200}