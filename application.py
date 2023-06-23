from flask import Flask, Blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import upgrade as _upgrade
from sqlalchemy import create_engine

from tourmanique.config.config_provider import ConfigProvider
from tourmanique.domain.data_access_layer.db import db, migrate
from tourmanique.domain.data_access_layer.engine import add_engine_pidguard, app_db_engine_provider
from tourmanique.modules.auth.auth_routes import auth_blueprint
from tourmanique.modules.galleries.galleries_routers import galleries_blueprint
from tourmanique.modules.photos.photos_routes import photos_blueprint


def create_app(config=ConfigProvider):
    """Application factory, used to create application"""
    app = Flask(__name__)
    app.config.from_object(config)


    # without this /feeds will work but /feeds/ with the slash at the end won't
    app.url_map.strict_slashes = False
    jwt = JWTManager(app)

    app_db_engine_provider.set_engine(create_engine(
        config.SQLALCHEMY_DATABASE_URI,
        isolation_level='READ COMMITTED',
        pool_pre_ping=True,
    ))

    add_engine_pidguard(app_db_engine_provider.get_engine())

    # allow to call the api from any origin for now
    CORS(
        app,
    )

    register_blueprints(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # runs pending migrations
    with app.app_context():
        _upgrade()

    return app


def register_blueprints(app):
    """Register all blueprints for application"""
    api_blueprint = Blueprint('api', __name__, url_prefix='/api')
    api_blueprint.register_blueprint(photos_blueprint)
    api_blueprint.register_blueprint(auth_blueprint)
    api_blueprint.register_blueprint(galleries_blueprint)

    app.register_blueprint(api_blueprint)
