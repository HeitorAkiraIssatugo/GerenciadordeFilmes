import os
from flask import Flask, session, redirect, url_for, request
from app.database import init_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua_chave_secreta_super_segura_para_desenvolvimento'
    
    # Caminho do banco SQLite utilizando o módulo os nativamente
    app.config['DATABASE'] = os.path.join(app.instance_path, 'cineapp.db')

    # Inicializa o banco de dados e cria a tabela na inicialização
    init_db(app)

    @app.before_request
    def check_auth():
        public_endpoints = ['auth.login', 'auth.register', 'static']
        if request.endpoint not in public_endpoints and 'user' not in session:
            return redirect(url_for('auth.login'))

    @app.route('/')
    def root():
        if 'user' in session:
            return redirect(url_for('auth.index'))
        return redirect(url_for('auth.login'))

    # Registra o Blueprint de autenticação
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    return app