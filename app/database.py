import sqlite3
import os
from werkzeug.security import generate_password_hash

class Database:
    """Context Manager personalizado para gerenciar conexões SQLite com 'with'"""
    def __init__(self, app_config):
        self.db_path = app_config['DATABASE']
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is not None:
                self.conn.rollback()  # Desfaz se houver erro
            else:
                self.conn.commit()   # Salva se correr tudo bem
            self.conn.close()

def init_db(app):
    """Cria a tabela de usuários via SQL puro e insere dados iniciais se estiver vazia"""
    with Database(app.config) as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')

        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        
        if count == 0:
            admin_hash = generate_password_hash('123456')
            critico_hash = generate_password_hash('oscar2026')
            
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', ('admin', admin_hash))
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', ('critico', critico_hash))