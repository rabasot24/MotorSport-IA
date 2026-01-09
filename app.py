from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from config import Config
from models import db, User, Vehicle, Article, Circuit, Category
import random

app = Flask(__name__)
app.config.from_object(Config)

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
    noticias = Article.query.order_by(Article.date.desc()).limit(3).all()
    vehiculos = Vehicle.query.limit(4).all()
    return render_template("home.html", noticias=noticias, vehiculos=vehiculos)


@app.route("/noticias")
def noticias():
    # AÑADIMOS: .order_by(Article.date.desc())
    noticias = Article.query.order_by(Article.date.desc()).all()
    return render_template("noticias.html", noticias=noticias)


@app.route("/noticias/<int:id>")
def noticia_detalle(id):
    noticia = Article.query.get_or_404(id)
    return render_template("noticia_detalle.html", noticia=noticia)


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
    # Muestra la bienvenida (Esto arregla el error de BuildError)
    return render_template("quiz_intro.html")


@app.route("/quiz/start")
def quiz_start():
    # Inicia nueva partida
    all_circuits = Circuit.query.with_entities(Circuit.id).all()
    ids = [c.id for c in all_circuits]
    random.shuffle(ids)

    session["quiz_indices"] = ids[:10]
    session["quiz_score"] = 0
    session["quiz_round"] = 1
    session["total_rounds"] = len(session["quiz_indices"])

    return redirect(url_for("quiz_juego"))


@app.route("/quiz/juego")
def quiz_juego():
    # Logica de mostrar pregunta
    if "quiz_indices" not in session:
        return redirect(url_for("quiz"))  # Redirige a la portada si no hay sesión

    if not session["quiz_indices"]:
        return redirect(url_for("quiz_final"))

    current_circuit_id = session["quiz_indices"][0]
    pregunta = Circuit.query.get(current_circuit_id)

    circuitos = Circuit.query.all()
    opciones = [pregunta.name]
    otros = [c.name for c in circuitos if c.id != pregunta.id]
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
    total = session.get("total_rounds", 10)
    session.pop("quiz_indices", None)

    return render_template("quiz_final.html", score=score, total=total * 10)


# --- ADMIN PANEL ---


@app.route("/admin")
@login_required
def admin_panel():
    if current_user.role != "admin":
        flash("Acceso denegado.")
        return redirect(url_for("perfil"))

    noticias = Article.query.order_by(Article.date.desc()).all()
    return render_template("admin.html", noticias=noticias)


@app.route("/admin/crear-noticia", methods=["POST"])
@login_required
def crear_noticia():
    if current_user.role != "admin":
        return redirect(url_for("home"))

    titulo = request.form.get("titulo")
    contenido = request.form.get("contenido")
    imagen = request.form.get("imagen")
    categoria = Category.query.first()

    nueva_noticia = Article(
        title=titulo,
        content=contenido,
        image=imagen,
        author_id=current_user.id,
        category_id=categoria.id if categoria else None,
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


if __name__ == "__main__":
    app.run(debug=True)
