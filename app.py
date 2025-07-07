from flask import Flask, request, redirect, render_template_string
import sqlite3
import hashlib
import os

# === Configuración inicial ===
DB_NAME = "usuarios.db"
PORT = 5800

app = Flask(__name__)

# === Crear base de datos y tabla si no existen ===
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# === Insertar usuario con contraseña hasheada ===
def agregar_usuario(nombre, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (nombre, password_hash))
    conn.commit()
    conn.close()

# === Verificar credenciales ===
def verificar_usuario(nombre, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombre = ? AND password_hash = ?", (nombre, password_hash))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

# === Página web principal ===
formulario_html = '''
<!DOCTYPE html>
<html>
<head><title>Login de Examen</title></head>
<body>
    <h2>Iniciar sesión</h2>
    <form method="POST">
        Usuario: <input type="text" name="usuario"><br>
        Contraseña: <input type="password" name="password"><br>
        <input type="submit" value="Ingresar">
    </form>
    {% if mensaje %}
        <p style="color:red;">{{ mensaje }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ""
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        if verificar_usuario(usuario, password):
            mensaje = f"✅ Bienvenido, {usuario}."
        else:
            mensaje = "❌ Usuario o contraseña incorrecta."
    return render_template_string(formulario_html, mensaje=mensaje)

# === Iniciar el servidor web ===
if __name__ == '__main__':
    init_db()

    # Si quieres agregar usuarios automáticamente al inicio (puedes comentar luego):
    agregar_usuario("Bastian", "clave123")
    agregar_usuario("Kevin", "clave123")
    agregar_usuario("Felipe", "clave123")
    agregar_usuario("Matias", "clave123")

    print(f"Servidor corriendo en http://localhost:{PORT}")
    app.run(port=PORT)

