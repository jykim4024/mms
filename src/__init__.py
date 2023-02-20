from flask import Flask, render_template
import config

def page_not_found(e):
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    from .views import main_views, auth_views, info_views
    from .views.pages import board_main

    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(info_views.bp)
    app.register_blueprint(board_main.bp)
    app.register_error_handler(404,page_not_found)

    return app