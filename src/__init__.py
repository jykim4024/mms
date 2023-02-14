from flask import Flask
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    from .views import main_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)

    return app