# app/models/user_model.py
from flask import current_app
from app.database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

class User:
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @classmethod
    def authenticate(cls, username, password):
        conn = get_db_connection(current_app.config)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()
        
        if row and check_password_hash(row['password_hash'], password):
            return cls(row['id'], row['username'], row['password_hash'])
        return None

    @classmethod
    def create(cls, username, password):
        """Insere um novo utilizador no banco usando SQL puro"""
        conn = get_db_connection(current_app.config)
        cursor = conn.cursor()
        try:
            password_hash = generate_password_hash(password)
            cursor.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Retorna False se o username já existir (UNIQUE constraint)
            return False
        finally:
            conn.close()