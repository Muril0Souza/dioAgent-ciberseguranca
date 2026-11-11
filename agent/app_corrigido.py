import sqlite3
import hashlib
import hmac
import os

def gerar_hash_senha(senha, salt=None, iterations=100000):
    if salt is None:
        salt = os.urandom(16)
    senha_bytes = senha.encode('utf-8')
    hash_bytes = hashlib.pbkdf2_hmac('sha256', senha_bytes, salt, iterations)
    return f"{iterations}${salt.hex()}${hash_bytes.hex()}"

def verificar_senha(senha, senha_hash):
    try:
        iterations, salt_hex, hash_hex = senha_hash.split('$')
        salt = bytes.fromhex(salt_hex)
        hash_esperado = bytes.fromhex(hash_hex)
        hash_computado = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt, int(iterations))
        return hmac.compare_digest(hash_computado, hash_esperado)
    except (ValueError, AttributeError):
        return False

def fazer_login(usuario, senha):
    conexao = sqlite3.connect('banco_de_dados.db')
    cursor = conexao.cursor()

    cursor.execute("SELECT senha_hash FROM usuarios WHERE username = ?", (usuario,))
    registro = cursor.fetchone()
    conexao.close()

    if registro is None:
        return "Acesso Negado."

    senha_hash = registro[0]

    if verificar_senha(senha, senha_hash):
        return "Acesso Permitido"
    else:
        return "Acesso Negado."