# Primero importamos las herramientas necesarias de Flask,
# autenticación, protección CSRF, cifrado de contraseñas y variables de entorno.
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

# En esta parte importamos los módulos propios del proyecto.
from db import get_db
from forms import LoginForm, RegisterForm
from models import get_user_by_username, get_user_by_id, User

# Esta sección sirve para cargar las variables de entorno y configurar
# inicialmente la aplicación Flask.
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# Este comando csrf = CSRFProtect(app) sirve para activar la protección CSRF y configurar
# la gestión de las sesiones de usuario.
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # Indica que los usuarios no autenticados serán enviados a la ruta "login".

# Recuperamos los datos del usuario
# correspondiente a la sesión activa.
@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id) # Convertimos los datos en un objeto
    if user:
        return User(user["id"], user["username"], user["password"])
    return None

# Redirigamos en esta parte a la página principal
# al formulario de inicio de sesión.
@app.route("/")
def index():
    return redirect(url_for("login"))

# Validamos las credenciales del usuario
# e iniciar su sesión cuando los datos son correctos.
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)

        if user and check_password_hash(user["password"], form.password.data):
            login_user(User(user["id"], user["username"], user["password"]))
            return redirect(url_for("dashboard"))

    return render_template("login.html", form=form)

# Esta sección sirve para registrar nuevos usuarios
# y almacenar sus contraseñas de manera cifrada.
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        db = get_db()
        cursor = db.cursor()

        hashed = generate_password_hash(form.password.data)

        cursor.execute(
            "INSERT INTO usuarios (username, password) VALUES (%s, %s)",
            (form.username.data, hashed)
        )

        db.commit()
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

# Con este codigo mostramos el panel principal
# únicamente a los usuarios autenticados.
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# cerramos la sesion del usuario y automaticamente
# redirigirlo a la página de inicio de sesión.
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Esta codigo sirve para iniciar la aplicación Flask
# cuando el archivo se ejecuta directamente.
# debug=False desactiva el modo de depuración, evitando mostrar información técnica sensible
if __name__ == "__main__":
    app.run(debug=False)
