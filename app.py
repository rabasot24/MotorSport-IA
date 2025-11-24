from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import json
import os
import requests

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "motorsport_secret_key_2025_fallback")
DEBUG_MODE = os.environ.get("FLASK_DEBUG", "False").lower() == "true"

# Vehículos destacados/locales y función para pedir a NHTSA API
DESTACADOS = [
    {"marca": "Ferrari", "modelo": "F2004", "categoria": "Fórmula 1", "epoca": "2000s"},
    {"marca": "McLaren", "modelo": "MP4/4", "categoria": "Fórmula 1", "epoca": "1980s"},
    {"marca": "Audi", "modelo": "Quattro S1", "categoria": "Rally", "epoca": "1980s"},
    {"marca": "Ford", "modelo": "GT40", "categoria": "Le Mans", "epoca": "1960s"},
    {"marca": "Porsche", "modelo": "917", "categoria": "Le Mans", "epoca": "1970s"},
    {"marca": "Toyota", "modelo": "Supra", "categoria": "GT", "epoca": "1990s"},
]


def get_nhtsa_info(make, model_name):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{make}?format=json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        all_models = response.json().get("Results", [])
        filtered = [
            m
            for m in all_models
            if model_name.lower() in m.get("Model_Name", "").lower()
        ]
        return filtered
    except requests.RequestException as e:
        print(f"⚠️  Error de red consultando NHTSA: {e}")
        return []
    except Exception as e:
        print(f"⚠️  Error inesperado consultando NHTSA: {e}")
        return []


@app.route("/api/vehiculos/agrupados")
def api_vehiculos_agrupados():
    agrupados = {}
    for v in DESTACADOS:
        key = (v["categoria"], v["epoca"])
        if key not in agrupados:
            agrupados[key] = []
        info_api = get_nhtsa_info(v["marca"], v["modelo"])
        agrupados[key].append(
            {
                "marca": v["marca"],
                "modelo": v["modelo"],
                "categoria": v["categoria"],
                "epoca": v["epoca"],
                "info_api": info_api,
            }
        )
    res = []
    for (cat, epoca), vehs in agrupados.items():
        res.append({"categoria": cat, "epoca": epoca, "vehiculos": vehs})
    return jsonify(res)


# MOCK DATA/LOCAL FILES:
def cargar_json(filename):
    """Función auxiliar para cargar datos JSON de mockdata."""
    filepath = os.path.join("mockdata", filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Advertencia: No se encontró {filename}")
        return []
    except json.JSONDecodeError as e:
        print(f"⚠️  Error al leer {filename}: {e}")
        return []


def cargar_noticias():
    return cargar_json("noticias.json")


def cargar_vehiculos():
    return cargar_json("vehiculos.json")


# Rutas principales frontend
@app.route("/")
def home():
    noticias = cargar_noticias()[:3]
    vehiculos = cargar_vehiculos()[:4]
    return render_template("home.html", noticias=noticias, vehiculos=vehiculos)


@app.route("/noticias")
def noticias():
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
        # Modo demo (acepta cualquier login)
        session["user"] = email
        session["role"] = "user"
        return redirect(url_for("perfil"))
    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    session["user"] = email
    session["role"] = "user"
    return redirect(url_for("perfil"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# API endpoints mockdata (por si sigues usándolos)
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


@app.route("/api/vehiculos/detalles")
def api_vehiculos_detalles():
    vehiculos_list = cargar_vehiculos()
    return jsonify(vehiculos_list)


# ERRORES
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
    app.run(debug=DEBUG_MODE, host="127.0.0.1", port=5000)
