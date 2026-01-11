# 🏎️ MotorSport - Portal del Automovilismo

**MotorSport** es una plataforma web interactiva especializada en el mundo del motor. Diseñada para ofrecer una experiencia completa a los aficionados, la aplicación combina información actualizada, una base de datos enciclopédica de vehículos legendarios y un sistema de participación comunitaria mediante gamificación.

El proyecto ha sido desarrollado como una aplicación Full-Stack utilizando **Python y Flask**, priorizando el rendimiento, la escalabilidad y una interfaz de usuario moderna.

---

## 🚀 Funcionalidades Principales

### 📖 Área de Información y Contenidos
* **Actualidad del Motor:** Blog de noticias con las últimas novedades de F1, WEC y Rally.
* **Showroom de Vehículos:** Fichas técnicas detalladas con especificaciones, historia y galería visual.
* **Experiencia Sonora:** Galería interactiva con grabaciones auténticas de motores icónicos (V10, V12, Boxer, etc.).

### 👤 Área de Usuario y Comunidad
* **Gestión de Perfiles:** Sistema seguro de Registro e Inicio de Sesión para personalizar la experiencia.
* **Quiz & Ranking:** Juego de preguntas interactivo que pone a prueba el conocimiento del usuario, con una tabla de clasificación global competitiva.
* **Sistema de Comentarios:** Posibilidad de debatir en las noticias e interactuar con otros usuarios.

### 🛠️ Administración
* **Panel de Control:** Los usuarios con rol de administrador pueden crear, editar y eliminar noticias, vehículos y **usuarios** mediante una interfaz gráfica, sin tocar código.

---

## 🏎️ Categorías del Catálogo

El garaje virtual de MotorSport abarca las disciplinas más importantes:

* **🏎️ Fórmula 1:** Monoplazas históricos y modernos de las principales escuderías.
* **⏱️ Resistencia (WEC):** Prototipos diseñados para pruebas de larga duración como Le Mans.
* **🌲 Rally (WRC):** Vehículos míticos adaptados a terrenos extremos.
* **💎 Superdeportivos y Clásicos:** Joyas de la ingeniería que marcaron tendencia fuera de las pistas.

---

## 💻 Tecnologías Empleadas

Este proyecto ha sido construido utilizando un stack tecnológico robusto y moderno:

### Backend (Lógica del Servidor)
* **Python 3.13:** Lenguaje principal.
* **Flask:** Framework web ligero y modular.
* **SQLAlchemy (ORM):** Gestión de base de datos relacional.
* **Flask-Login / Flask-WTF:** Gestión de sesiones y seguridad de usuarios.

### Frontend (Interfaz de Usuario)
* **HTML5 & CSS3:** Estructura y diseño.
* **Bootstrap 5:** Framework para diseño responsivo (adaptable a Móvil y PC) y modo oscuro.
* **JavaScript (Vanilla):** Interactividad en el cliente (AJAX, validaciones).
* **Jinja2:** Motor de plantillas para renderizado dinámico.

### Base de Datos
* **SQLite:** Base de datos relacional ligera y portátil (ideal para despliegue rápido).

---

## 🔧 Guía de Instalación y Despliegue

Sigue estos pasos detallados para ejecutar el proyecto en tu entorno local sin errores:

### 1. Clonar el repositorio

    git clone https://github.com/rabasot24/MotorSport-IA.git
    cd MotorSport-IA

### 2. Crear y Activar Entorno Virtual (IMPORTANTE)
Es necesario crear un entorno aislado para las librerías del proyecto.

* **En Windows:**
    1. Crear el entorno:
       
            python -m venv venv

    2. Activarlo:
       
            .\venv\Scripts\activate

    > **⚠️ SOLUCIÓN DE ERROR EN WINDOWS:**
    > Si al intentar activar (`.\venv\Scripts\activate`) te sale un error rojo diciendo *"la ejecución de scripts está deshabilitada"*, ejecuta este comando para dar permiso temporalmente y vuelve a intentar activar:
    > 
    >     Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

* **En Mac / Linux:**

        python3 -m venv venv
        source venv/bin/activate

    *(Sabrás que funciona porque verás `(venv)` al inicio de la terminal).*

### 3. Instalar Dependencias
Una vez activado el entorno, instala las librerías necesarias:

    pip install -r requirements.txt

### 4. Configuración de Seguridad (.env)
El proyecto necesita una clave secreta para funcionar correctamente.
1. Crea un archivo nuevo en la raíz del proyecto (junto a `app.py`) llamado **`.env`**.
2. Abre el archivo con el bloc de notas y pega el siguiente código dentro:

        SECRET_KEY="clave-secreta-desarrollo"

### 5. Base de Datos
El proyecto ya incluye una base de datos pre-cargada en la carpeta `instance/`. 
Si necesitas regenerarla desde cero (restablecer fábrica), puedes ejecutar:

    python generar_base_datos.py

### 6. Ejecutar la Aplicación

    python app.py

Abre tu navegador en: 👉 **`http://127.0.0.1:5000`**

---

## 🔐 Credenciales de Acceso

Para facilitar la corrección y pruebas, la base de datos incluye estas cuentas por defecto:

| Rol               | Usuario   | Contraseña | Permisos                                                                 |
| :---------------- | :-------- | :--------- | :----------------------------------------------------------------------- |
| **ADMINISTRADOR** | `admin@motorsport.com`   | `1234` | Acceso total al Panel (Crear/Editar/Borrar Noticias, Coches y Usuarios). |
| **USUARIO**       | `usuario` | `1234`     | Acceso a Quiz, Comentarios y Perfil.                                     |

