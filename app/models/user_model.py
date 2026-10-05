from flask import current_app
from app.database import Database
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

class User:
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @classmethod
    def find_by_username(cls, username):
        """Método de classe para buscar um utilizador pelo nome"""
        with Database(current_app.config) as cursor:
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            if row:
                return cls(row['id'], row['username'], row['password_hash'])
        return None

    @classmethod
    def authenticate(cls, username, password):
        """Método de classe para autenticação segura"""
        user = cls.find_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    def save(self):
        """Método de instância para persistir um novo utilizador no banco"""
        with Database(current_app.config) as cursor:
            try:
                # Se o utilizador já tiver hash, usa-o; caso contrário, gera (útil para novos registos)
                if not self.password_hash.startswith('pbkdf2:'):
                    self.password_hash = generate_password_hash(self.password_hash)

                cursor.execute(
                    'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                    (self.username, self.password_hash)
                )
                return True
            except sqlite3.IntegrityError:
                # Retorna False se o username já existir (UNIQUE constraint)
                return False
    
    @classmethod
    def listar_filmes_destaque(cls, filme, filme2):
        with Database(current_app.config) as cursor:
            cursor.execute('SELECT * FROM filmes', (filme, filme2))
            row = cursor.fetchone()
            if row:
                return cls(row['id'], row['filme'], row['filme2'])
            return None