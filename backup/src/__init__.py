from flask import Flask
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # blueprint
    from .views import main_views, auth_views, info_views, vac_views, mgmt_views, test_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(info_views.bp)
    app.register_blueprint(vac_views.bp)
    app.register_blueprint(mgmt_views.bp)
    app.register_blueprint(test_views.bp)

    # Filter
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app