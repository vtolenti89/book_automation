from flask import Flask

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')

    from .routes.frontend import frontend_bp
    from .routes.sla_editor import sla_bp

    app.register_blueprint(frontend_bp)
    app.register_blueprint(sla_bp, url_prefix="/api/sla")

    return app
