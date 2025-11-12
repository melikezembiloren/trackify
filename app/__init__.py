from flask import Flask
from flask_jwt_extended import JWTManager
from app.config import Config
from app.extensions import db, migrate
from app.utils.models import Users, Operators, Lines, TV, TvCatalog, DefectCatalog, Defect
from app.controllers.auth_controller import auth_bp
from app.controllers.process_selection_controller import process_bp
from app.controllers.defect_entry_controller import defect_entry_bp
from app.controllers.get_defect_catalog_controller import defect_catalog_bp
from app.controllers.rework_controller import rework_bp
from app.controllers.get_solution_list import solution_bp
from app.controllers.get_all_list_controller import all_list_bp
from app.controllers.dashboard_controller import dashboard_bp
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    migrate.init_app(app, db)

    app.config['JWT_SECRET_KEY']   # güçlü bir key kullanın
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']    # JWT sadece cookie’de
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'        # tüm site için geçerli
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False     # geliştirme için kapalı, prod’da True yapabilirsiniz
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)  # access token 8 saat geçerli
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)  # refresh token 30 gün geçerli


    jwt = JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(defect_entry_bp)
    app.register_blueprint(process_bp)
    app.register_blueprint(defect_catalog_bp)
    app.register_blueprint(rework_bp)
    app.register_blueprint(solution_bp)
    app.register_blueprint(all_list_bp)
    app.register_blueprint(dashboard_bp)

    return app
