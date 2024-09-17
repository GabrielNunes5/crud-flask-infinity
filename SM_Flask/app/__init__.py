from flask import Flask
from app.config.settings import Config
from app.database import db
from app.routes.aluno import alunos_bp
from app.routes.professor import professores_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(alunos_bp)
    app.register_blueprint(professores_bp)

    return app
