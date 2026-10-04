import sqlite3
import os
from werkzeug.security import generate_password_hash

def get_db_connection(app_config):
    """Abre e retorna uma nova conexão direta com o SQLite usando o módulo os"""
    db_path = app_config['DATABASE']
    
    # Garante que a pasta do banco existe usando o os
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    # Permite acessar as colunas pelo nome (ex: row['username'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db(app):
    """Cria a tabela de usuários via SQL puro e insere dados iniciais se estiver vazia"""
    conn = get_db_connection(app.config)
    cursor = conn.cursor()
    
    # Comando SQL puro para criar a tabela
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()

    # Verifica se já existem usuários cadastrados
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    
    if count == 0:
        admin_hash = generate_password_hash('123456')
        critico_hash = generate_password_hash('oscar2026')
        
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', ('admin', admin_hash))
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', ('critico', critico_hash))
        conn.commit()
    
    # Fecha a conexão após a inicialização
    conn.close()