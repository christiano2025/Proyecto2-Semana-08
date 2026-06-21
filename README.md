[README.md](https://github.com/user-attachments/files/29170243/README.md)
# Proyecto de inicio de sesión seguro

**Alumno:** Christian Ortega Alfaro

Este proyecto es una página web hecha con Python y Flask.

Su función principal es permitir que una persona pueda registrarse, iniciar sesión, entrar a una página privada y cerrar su sesión.

Los usuarios se guardan en una base de datos MySQL. Las contraseñas no se guardan directamente, sino que se convierten en un texto cifrado para proteger la información del usuario.

## 1. ¿Qué se puede hacer en el proyecto?

- Registrar un usuario nuevo.
- Iniciar sesión con un usuario registrado.
- Entrar a un dashboard privado.
- Cerrar sesión.
- Proteger los formularios con CSRF.
- Guardar las contraseñas de forma segura.

## 2. Herramientas utilizadas

- Python
- Flask
- MySQL
- Flask-Login
- Flask-WTF
- HTML
- Bootstrap 5

## 3. Archivos del proyecto

```text
app.py              Archivo principal donde están las rutas de la página.
config.py           Guarda la configuración de las variables de entorno.
db.py               Realiza la conexión con MySQL.
forms.py            Contiene los formularios de registro e inicio de sesión.
models.py           Busca la información de los usuarios en la base de datos.
requirements.txt    Contiene las librerías utilizadas.

Templates
base.html           Plantilla principal de las páginas.
login.html          Página para iniciar sesión.
register.html       Página para registrar un usuario.
dashboard.html      Página privada para usuarios registrados.
```

## 4. Pasos para ejecutar el proyecto

### Crear un entorno virtual

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
pip install Flask-Login Flask-WTF WTForms mysql-connector-python
```

### Crear la base de datos

En MySQL se deben ejecutar las siguientes instrucciones:

```sql
CREATE DATABASE secure_notes;

USE secure_notes;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
```

### Iniciar la aplicación

```powershell
python app.py
```

Después se debe abrir esta dirección en el navegador:

```text
http://127.0.0.1:5000
```

## 5. ¿Cómo funciona?

Cuando una persona se registra, el sistema recibe su nombre de usuario y contraseña. Flask la convierte en un hash para que no quede visible.

Cuando la persona inicia sesión, el programa compara la contraseña escrita con la contraseña protegida de la base de datos. Si los datos son correctos, permite entrar al dashboard.

La ruta del dashboard usa `login_required`, por eso una persona que no haya iniciado sesión no puede entrar directamente.

## 6. Rutas de la página

- `/` → Envía al usuario a la página de inicio de sesión.
- `/login` → Permite iniciar sesión.
- `/register` → Permite crear un usuario nuevo.
- `/dashboard` → Muestra la página privada.
- `/logout` → Cierra la sesión del usuario.

## 7. Seguridad Automatizada

El proyecto cuenta con un pipeline de seguridad implementado mediante GitHub Actions. Cada vez que se realiza un cambio en la rama principal (`main`), se ejecuta automáticamente un análisis de seguridad utilizando la herramienta Bandit.

### Workflow utilizado

```yaml
name: Security Pipeline

on:
  push:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - run: pip install -r requirements.txt

      - run: bandit -r app.py
```
## 8. Conclusión

Este proyecto sirve para aprender cómo funciona un sistema de autenticación en Flask. También permite practicar el uso de formularios, sesiones, bases de datos y protección de contraseñas.
