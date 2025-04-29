from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Conductor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)  
    puntos = db.Column(db.Integer, default=0)
    fecha_registro = db.Column(db.DateTime, default=db.func.now())

    is_active = db.Column(db.Boolean, default=True)
    
    # Relación: un conductor puede tener muchos turnos
    turnos = db.relationship('Turno', backref='conductor', lazy=True)

class Centro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    
    # Relación: un centro tiene muchas unidades
    unidades = db.relationship('Unidad', backref='centro', lazy=True)
    
    # Relación: un centro tiene muchos turnos (reserva de unidades en ese centro)
    turnos = db.relationship('Turno', backref='centro', lazy=True)

class Unidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    estado_salud = db.Column(db.String(20), default="Verde")
    centro_id = db.Column(db.Integer, db.ForeignKey('centro.id'), nullable=False)
    
    placa = db.Column(db.String(20), nullable=False)   # <--- Nueva columna
    modelo = db.Column(db.String(100), nullable=False) # <--- Nueva columna
    year = db.Column(db.Integer, nullable=False)       # <--- Nueva columna

    turnos = db.relationship('Turno', backref='unidad', lazy=True)
    mantenimientos = db.relationship('Mantenimiento', backref='unidad', lazy=True)

class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conductor_id = db.Column(db.Integer, db.ForeignKey('conductor.id'), nullable=False)
    unidad_id = db.Column(db.Integer, db.ForeignKey('unidad.id'), nullable=False)
    centro_id = db.Column(db.Integer, db.ForeignKey('centro.id'), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), default="Reservado")  # Reservado, Cancelado, Completado
    
    # Relación: un turno tiene un historial (opcionalmente lo puedes poner)
    historial = db.relationship('Historial', backref='turno', lazy=True, uselist=False)

class Historial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turno_id = db.Column(db.Integer, db.ForeignKey('turno.id'), nullable=False)
    distancia_recorrida = db.Column(db.Float)  # en km
    ingresos_generados = db.Column(db.Float)  # en mxn

class Mantenimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unidad_id = db.Column(db.Integer, db.ForeignKey('unidad.id'), nullable=False)
    fecha_programada = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.String(100))  # Ejemplo: "Cambio de batería", "Revisión general"

class Recompensa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    puntos_necesarios = db.Column(db.Integer, nullable=False)

class Notificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conductor_id = db.Column(db.Integer, db.ForeignKey('conductor.id'), nullable=False)
    mensaje = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.String(20), default="Pendiente")  # Pendiente, Leída
    fecha = db.Column(db.DateTime, default=db.func.now())

    conductor = db.relationship('Conductor', backref='notificaciones', lazy=True)