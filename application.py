from flask import Flask, Blueprint
from flask_cors import CORS
from flask_migrate import upgrade as _upgrade
from sqlalchemy import create_engine

from deepstroy.config.config_provider import ConfigProvider
from deepstroy.domain.data_access_layer.db import db, migrate
from deepstroy.domain.data_access_layer.engine import add_engine_pidguard, app_db_engine_provider
from deepstroy.modules.forecast.forecast_routes import forecast_blueprint
from deepstroy.modules.modeling.modeling_route import modeling_blueprint


def create_app(config=ConfigProvider):
    """Application factory, used to create application"""
    app = Flask(__name__)
    app.config.from_object(config)

    app.url_map.strict_slashes = False

    app_db_engine_provider.set_engine(create_engine(
        config.SQLALCHEMY_DATABASE_URI,
        isolation_level='READ COMMITTED',
        pool_pre_ping=True,
    ))
    app_db_engine = app_db_engine_provider.get_engine()
    add_engine_pidguard(app_db_engine)

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
    api_blueprint.register_blueprint(forecast_blueprint)
    api_blueprint.register_blueprint(modeling_blueprint)

    app.register_blueprint(api_blueprint)
