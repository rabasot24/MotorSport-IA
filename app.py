from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "motorsport_secret_key_2025"


# Cargar datos mock
def cargar_noticias():
    try:
        with open("mockdata/noticias.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️  Advertencia: No se encontró noticias.json")
        return []
    except json.JSONDecodeError as e:
        print(f"⚠️  Error al leer noticias.json: {e}")
        return []


def cargar_vehiculos():
    try:
        with open("mockdata/vehiculos.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️  Advertencia: No se encontró vehiculos.json")
        return []
    except json.JSONDecodeError as e:
        print(f"⚠️  Error al leer vehiculos.json: {e}")
        return []


# Rutas principales
@app.route("/")
def home():
    print("🏠 Cargando página de inicio...")
    noticias = cargar_noticias()[:3]  # Últimas 3 noticias
    vehiculos = cargar_vehiculos()[:4]  # 4 vehículos destacados
    return render_template("home.html", noticias=noticias, vehiculos=vehiculos)


@app.route("/noticias")
def noticias():
    print("📰 Cargando noticias...")
    todas_noticias = cargar_noticias()
    return render_template("noticias.html", noticias=todas_noticias)


@app.route("/noticias/<int:id>")
def noticia_detalle(id):
    noticias = cargar_noticias()
    noticia = next((n for n in noticias if n["id"] == id), None)
    if noticia:
        return render_template("noticia_detalle.html", noticia=noticia)
    return redirect(url_for("noticias"))


@app.route("/vehiculos")
def vehiculos():
    print("🏎️  Cargando vehículos...")
    todos_vehiculos = cargar_vehiculos()
    return render_template("vehiculos.html", vehiculos=todos_vehiculos)


@app.route("/vehiculos/<int:id>")
def vehiculo_detalle(id):
    vehiculos_list = cargar_vehiculos()
    vehiculo = next((v for v in vehiculos_list if v["id"] == id), None)
    if vehiculo:
        return render_template("vehiculo_detalle.html", vehiculo=vehiculo)
    return redirect(url_for("vehiculos"))


@app.route("/quiz")
def quiz():
    print("🎯 Cargando quiz...")
    return render_template("quiz.html")


@app.route("/perfil")
def perfil():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("perfil.html")


@app.route("/admin")
def admin():
    if "user" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("admin.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # Simulación de login exitoso
        session["user"] = email
        session["role"] = "user"
        return redirect(url_for("perfil"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# API endpoints para AJAX
@app.route("/api/vehiculos")
def api_vehiculos():
    vehiculos_list = cargar_vehiculos()
    categoria = request.args.get("categoria")
    busqueda = request.args.get("q")

    if categoria and categoria != "Todas las categorías":
        vehiculos_list = [v for v in vehiculos_list if v.get("categoria") == categoria]

    if busqueda:
        vehiculos_list = [
            v for v in vehiculos_list if busqueda.lower() in v["nombre"].lower()
        ]

    return jsonify(vehiculos_list)


@app.route("/api/noticias")
def api_noticias():
    noticias = cargar_noticias()
    return jsonify(noticias)


# Manejo de errores
@app.errorhandler(404)
def page_not_found(e):
    return (
        "<h1>404 - Página no encontrada</h1><p>La página que buscas no existe.</p>",
        404,
    )


@app.errorhandler(500)
def internal_error(e):
    return f"<h1>500 - Error del servidor</h1><p>Error: {str(e)}</p>", 500


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 SERVIDOR FLASK INICIADO")
    print("=" * 60)
    print("📍 URL: http://127.0.0.1:5000")
    print("📍 URL alternativa: http://localhost:5000")
    print("⏹️  Para detener: Presiona Ctrl+C")
    print("=" * 60)

    # Verificar archivos
    if os.path.exists("mockdata/noticias.json"):
        print("✅ noticias.json encontrado")
    else:
        print("❌ noticias.json NO encontrado")

    if os.path.exists("mockdata/vehiculos.json"):
        print("✅ vehiculos.json encontrado")
    else:
        print("❌ vehiculos.json NO encontrado")

    if os.path.exists("templates/home.html"):
        print("✅ home.html encontrado")
    else:
        print("❌ home.html NO encontrado")

    print("=" * 60)

    app.run(debug=True, host="127.0.0.1", port=5000)
