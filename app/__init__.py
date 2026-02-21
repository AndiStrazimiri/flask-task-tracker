#new line

from flask import Flask
from app.config import Config
from app.extension import db, migrate
from app.logger import logger
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from app.api.task_routes import task_bp
    from app.auth.routes import auth_bp    # <-- new

    app.register_blueprint(task_bp, url_prefix="/tasks")
    app.register_blueprint(auth_bp, url_prefix="/auth")  # <-- new

    # root route (optional)
    @app.route("/")
    def index():
        return "<h2>Task Tracker API</h2><p><a href='/tasks/'>Open Tasks UI</a></p>"

    logger.info("App created and blueprints registered")
    return app

