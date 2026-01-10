import requests
from flask_wtf.csrf import CSRFProtect
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from config import Config
from models import db, User, Vehicle, Article, Circuit, Category, Comment
import random
from sqlalchemy.sql.expression import func
from sqlalchemy import or_


app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)

# Inicializar DB y Login Manager
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- RUTAS PUBLICAS ---


@app.route("/")
def home():
    # 1. Noticias: Las 3 más recientes
    noticias = Article.query.order_by(Article.date.desc()).limit(3).all()

    # 2. Showroom: 4 vehículos aleatorios para la portada
    coches = Vehicle.query.order_by(func.random()).limit(4).all()

    return render_template("home.html", noticias=noticias, coches=coches)


@app.route("/noticias")
def noticias():
    # Detectamos en qué página estamos (por defecto la 1)
    page = request.args.get("page", 1, type=int)

    # En lugar de .all(), usamos .paginate()
    # per_page=5 significa que salen 5 noticias por página
    paginacion = Article.query.order_by(Article.date.desc()).paginate(
        page=page, per_page=5, error_out=False
    )

    return render_template("noticias.html", paginacion=paginacion)


# --- BUSCADOR GLOBAL (CORREGIDO) ---
@app.route("/buscar")
def buscar():
    query = request.args.get("q")
    noticias_encontradas = []
    coches_encontrados = []

    if query:
        # 1. Buscar en NOTICIAS (Título o Contenido)
        noticias_encontradas = Article.query.filter(
            or_(Article.title.contains(query), Article.content.contains(query))
        ).all()

        # 2. Buscar en VEHÍCULOS (Nombre o Equipo)
        coches_encontrados = Vehicle.query.filter(
            or_(Vehicle.name.contains(query), Vehicle.manufacturer.contains(query))
        ).all()

    # Pasamos ambas listas a la plantilla 'buscar.html'
    return render_template(
        "buscar.html",
        query=query,
        noticias=noticias_encontradas,
        coches=coches_encontrados,
    )


@app.route("/noticias/<int:id>")
def noticia_detalle(id):
    noticia = Article.query.get_or_404(id)
    return render_template("noticia_detalle.html", noticia=noticia)


@app.route("/noticia/<int:id>/comentar", methods=["POST"])
@login_required
def publicar_comentario(id):
    contenido = request.form.get("comentario")

    if not contenido:
        flash("El comentario no puede estar vacío.")
        return redirect(url_for("noticia_detalle", id=id))

    # Crear nuevo comentario
    nuevo_comentario = Comment(
        content=contenido, user_id=current_user.id, article_id=id
    )

    db.session.add(nuevo_comentario)
    db.session.commit()

    flash("¡Comentario publicado!")
    return redirect(url_for("noticia_detalle", id=id))


@app.route("/vehiculos")
def vehiculos():
    vehiculos = Vehicle.query.order_by(Vehicle.category).all()
    return render_template("vehiculos.html", vehiculos=vehiculos)


@app.route("/vehiculos/<int:id>")
def vehiculo_detalle(id):
    vehiculo = Vehicle.query.get_or_404(id)
    return render_template("vehiculo_detalle.html", vehiculo=vehiculo)


# --- LOGIN Y REGISTRO ---


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("perfil"))
        else:
            flash("Credenciales incorrectas")

    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if User.query.filter_by(email=email).first():
        return redirect(url_for("login"))

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return redirect(url_for("perfil"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/perfil")
@login_required
def perfil():
    return render_template("perfil.html")


@app.route("/perfil/editar", methods=["POST"])
@login_required
def editar_perfil():
    nuevo_username = request.form.get("username")
    nuevo_email = request.form.get("email")
    bio = request.form.get("bio")

    current_user.username = nuevo_username
    current_user.email = nuevo_email
    current_user.settings = {"bio": bio}

    db.session.commit()
    flash("Perfil actualizado correctamente")
    return redirect(url_for("perfil"))


# --- QUIZ (JUEGO) ---


@app.route("/quiz")
def quiz():
    return render_template("quiz_intro.html")


@app.route("/quiz/start")
def quiz_start():
    # Inicia nueva partida
    all_circuits = Circuit.query.with_entities(Circuit.id).all()
    ids = [c.id for c in all_circuits]
    random.shuffle(ids)

    # Seleccionamos 10 preguntas
    session["quiz_indices"] = ids[:10]
    session["quiz_score"] = 0
    session["quiz_round"] = 1
    session["total_rounds"] = len(session["quiz_indices"])

    return redirect(url_for("quiz_juego"))


@app.route("/quiz/juego")
def quiz_juego():
    if "quiz_indices" not in session:
        return redirect(url_for("quiz"))

    if not session["quiz_indices"]:
        return redirect(url_for("quiz_final"))

    current_circuit_id = session["quiz_indices"][0]
    pregunta = Circuit.query.get(current_circuit_id)

    circuitos = Circuit.query.all()
    opciones = [pregunta.name]
    otros = [c.name for c in circuitos if c.id != pregunta.id]

    # Evitar error si hay pocos circuitos en la DB
    if len(otros) >= 2:
        opciones.extend(random.sample(otros, 2))
    else:
        opciones.extend(otros)
    random.shuffle(opciones)

    return render_template(
        "quiz.html",
        pregunta=pregunta,
        opciones=opciones,
        ronda=session["quiz_round"],
        total=session["total_rounds"],
        puntos=session["quiz_score"],
    )


@app.route("/quiz/submit", methods=["POST"])
def quiz_submit():
    pregunta_id = int(request.form.get("pregunta_id"))
    respuesta = request.form.get("respuesta")

    circuito = Circuit.query.get(pregunta_id)
    acierto = circuito.name == respuesta

    puntos_ganados = 10 if acierto else 0

    # Actualizamos la puntuación en la sesión
    session["quiz_score"] += puntos_ganados

    indices = session["quiz_indices"]
    if indices:
        indices.pop(0)
    session["quiz_indices"] = indices
    session["quiz_round"] += 1
    session.modified = True

    es_ultimo = len(indices) == 0

    return render_template(
        "quiz_resultado.html",
        acierto=acierto,
        respuesta_correcta=circuito.name,
        puntos_ronda=puntos_ganados,
        puntos_total=session["quiz_score"],
        es_ultimo=es_ultimo,
    )


@app.route("/quiz/final")
def quiz_final():
    score = session.get("quiz_score", 0)
    total = session.get("total_rounds", 0) * 10

    # --- GAMIFICACIÓN ---
    if current_user.is_authenticated:
        current_user.score += score
        db.session.commit()
        print(
            f"💰 Puntos guardados! Usuario: {current_user.username} | Total: {current_user.score}"
        )
    # --------------------

    session.pop("quiz_indices", None)
    session.pop("quiz_round", None)

    return render_template("quiz_final.html", score=score, total=total)


# --- ADMIN PANEL ---


@app.route("/admin")
@login_required
def admin_panel():
    if current_user.role != "admin":
        flash("Acceso denegado.")
        return redirect(url_for("perfil"))

    # Cargamos TODO: Noticias, Categorías y Vehículos
    noticias = Article.query.order_by(Article.date.desc()).all()
    categorias = Category.query.all()
    vehiculos = Vehicle.query.order_by(Vehicle.id.desc()).all()  # Nuevo

    return render_template(
        "admin.html", noticias=noticias, categorias=categorias, vehiculos=vehiculos
    )


@app.route("/admin/crear-noticia", methods=["POST"])
@login_required
def crear_noticia():
    if current_user.role != "admin":
        return redirect(url_for("home"))

    titulo = request.form.get("titulo")
    contenido = request.form.get("contenido")
    imagen = request.form.get("imagen")

    # 1. Recogemos el ID del desplegable
    categoria_id = request.form.get("categoria_id")

    nueva_noticia = Article(
        title=titulo,
        content=contenido,
        image=imagen,
        author_id=current_user.id,
        # 2. Guardamos la categoría correcta (convirtiendo a número)
        category_id=int(categoria_id) if categoria_id else None,
    )

    db.session.add(nueva_noticia)
    db.session.commit()
    return redirect(url_for("admin_panel"))


@app.route("/admin/borrar-noticia/<int:id>")
@login_required
def borrar_noticia(id):
    if current_user.role != "admin":
        return redirect(url_for("home"))

    noticia = Article.query.get_or_404(id)
    db.session.delete(noticia)
    db.session.commit()
    return redirect(url_for("admin_panel"))


@app.route("/admin/editar-noticia/<int:id>", methods=["GET", "POST"])
@login_required
def editar_noticia(id):
    if current_user.role != "admin":
        return redirect(url_for("home"))

    noticia = Article.query.get_or_404(id)

    if request.method == "POST":
        noticia.title = request.form.get("titulo")
        noticia.image = request.form.get("imagen")
        noticia.content = request.form.get("contenido")

        db.session.commit()
        flash("Noticia actualizada correctamente.")
        return redirect(url_for("admin_panel"))

    return render_template("editar_noticia.html", noticia=noticia)


@app.route("/ranking")
def ranking():
    top_users = User.query.order_by(User.score.desc()).limit(10).all()
    return render_template("ranking.html", users=top_users)


# --- MANEJADOR DE ERRORES (404) ---
@app.errorhandler(404)
def page_not_found(e):
    # Nota el ', 404' al final. Es importante para que el navegador sepa que es un error.
    return render_template("404.html"), 404


# --- GESTIÓN DE VEHÍCULOS (ADMIN) ---


@app.route("/admin/crear-vehiculo", methods=["POST"])
@login_required
def crear_vehiculo():
    if current_user.role != "admin":
        return redirect(url_for("home"))

    nombre = request.form.get("nombre")
    fabricante = request.form.get("fabricante")

    # 1. Gestión de imagen (automática o manual)
    imagen_url = request.form.get("imagen")
    if not imagen_url:
        # Importante: asegúrate de tener 'import requests' arriba del todo
        try:
            imagen_url = obtener_imagen_wikipedia(f"{fabricante} {nombre}")
        except:
            imagen_url = None

    # 2. LIMPIEZA DE DATOS NUMÉRICOS (Aquí estaba el error)
    # Si el campo viene vacío (""), lo convertimos a None. Si no, a int/float.
    hp_input = request.form.get("cv")
    speed_input = request.form.get("velocidad")
    accel_input = request.form.get("aceleracion")

    nuevo_coche = Vehicle(
        name=nombre,
        manufacturer=fabricante,
        category=request.form.get("categoria"),
        image=imagen_url,
        engine=request.form.get("motor"),
        # Conversión segura:
        horsepower=int(hp_input) if hp_input else None,
        top_speed=int(speed_input) if speed_input else None,
        acceleration=float(accel_input) if accel_input else None,
    )

    db.session.add(nuevo_coche)
    db.session.commit()
    flash("Vehículo añadido correctamente.")
    return redirect(url_for("admin_panel"))


@app.route("/admin/borrar-vehiculo/<int:id>")
@login_required
def borrar_vehiculo(id):
    if current_user.role != "admin":
        return redirect(url_for("home"))

    coche = Vehicle.query.get_or_404(id)
    db.session.delete(coche)
    db.session.commit()
    flash("Vehículo eliminado.")
    return redirect(url_for("admin_panel"))


# --- PÁGINAS LEGALES ---


@app.route("/privacidad")
def privacidad():
    return render_template("legales/privacidad.html")


@app.route("/terminos")
def terminos():
    return render_template("legales/terminos.html")


@app.route("/cookies")
def cookies():
    return render_template("legales/cookies.html")


if __name__ == "__main__":
    app.run(debug=True)
