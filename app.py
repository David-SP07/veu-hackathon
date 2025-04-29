from flask import Flask, render_template, redirect, url_for
from models.dbModels import db
from flask_migrate import Migrate
from routes.authRoutes import auth_bp
from routes.centroRoutes import centro_bp
from routes.turnoRoutes import turno_bp
from routes.vehiculoRoutes import vehiculo_bp
from routes.notificacionesRoutes import notificaciones_bp
from routes.conductorRoutes import conductor_bp
from flask_cors import CORS 
from flask_login import LoginManager, login_required, current_user
from services.vehiculoService import verificar_turno_activo
from services.vehiculoService import obtener_centros_service
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user, logout_user

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    migrate = Migrate(app, db)

    CORS(app)

    login_manager.init_app(app)
    login_manager.login_view = "login_page"

    app.register_blueprint(auth_bp)
    app.register_blueprint(centro_bp)
    app.register_blueprint(turno_bp)
    app.register_blueprint(vehiculo_bp)
    app.register_blueprint(notificaciones_bp)
    app.register_blueprint(conductor_bp)

    # Ruta para dashboard
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/estado-vehiculo')
    def estadoVehiculo():
       return render_template('estadovehiculoactivo.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login_page():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))  # Si ya está logueado, lo redirigimos al dashboard
        return render_template('login.html')  # Si no está logueado, mostramos la página de login
    
    @app.route('/reservar-turno', methods=['GET'])
    def reservar_turno():
        # Aquí iría la lógica para cargar los datos si es necesario (ej. centros, unidades)
        return render_template('reservaTurno.html')
    
    @app.route('/alta-centro')
    def alta_centro():
        return render_template('altaCentro.html')
    
    @app.route('/mis-turnos')
    def mis_turnos():
        return render_template('misTurnos.html')
    
    @app.route('/mi-perfil')
    def mi_perfil():
        return render_template('miPerfil.html')
    
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login_page'))  # ← así sí funciona

    return app

@login_manager.user_loader
def load_user(user_id):
    # Suponiendo que tu modelo de usuario es "Conductor"
    return Conductor.query.get(int(user_id))


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()

    app.run(
        host='0.0.0.0', #Remove this line if you want to run on localhost
        port=5005,
        debug=True
    )