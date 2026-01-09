import feedparser
import requests
from bs4 import BeautifulSoup
from app import app
from models import db, Article, Category, User
from datetime import datetime
from werkzeug.security import generate_password_hash
import re

RSS_FEEDS = {
    "f1": "https://es.motorsport.com/rss/f1/news/",
    "motogp": "https://es.motorsport.com/rss/motogp/news/",
    "indycar": "https://es.motorsport.com/rss/indycar/news/",
    "wec": "https://es.motorsport.com/rss/wec/news/",
}


def obtener_texto_completo(url):
    """Intenta obtener texto, si falla devuelve None."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            cuerpo = soup.find("div", class_="ms-article__content")
            if not cuerpo:
                cuerpo = soup.find("div", class_="article-content")

            if cuerpo:
                parrafos = cuerpo.find_all("p")
                texto = "\n\n".join([p.get_text().strip() for p in parrafos])
                if "Sigue leyendo" in texto:
                    texto = texto.split("Sigue leyendo")[0]
                return texto
    except:
        return None
    return None


def actualizar_noticias_auto():
    with app.app_context():
        print("📡 ACTUALIZANDO 24 NOTICIAS (CON ENLACES)...")

        # --- Configuración de Usuario y Categorías ---
        bot = User.query.filter_by(username="MotorSport_Bot").first()
        if not bot:
            bot = User(
                username="MotorSport_Bot",
                email="bot@motorsport.com",
                password_hash=generate_password_hash("bot123"),
                role="admin",
            )
            db.session.add(bot)
            db.session.commit()

        cats_db = {c.slug: c for c in Category.query.all()}
        nombres_cat = {
            "f1": "Fórmula 1",
            "motogp": "MotoGP",
            "indycar": "IndyCar",
            "wec": "WEC",
        }
        for slug, url in RSS_FEEDS.items():
            if slug not in cats_db:
                nueva_cat = Category(name=nombres_cat[slug], slug=slug)
                db.session.add(nueva_cat)
                cats_db[slug] = nueva_cat
        db.session.commit()
        # ---------------------------------------------

        nuevas = 0
        for slug, url in RSS_FEEDS.items():
            print(f"   ⏳ {slug.upper()} (Buscando 6)...", end=" ")
            feed = feedparser.parse(url)

            # --- AQUÍ ESTÁ EL CAMBIO: de [:3] pasamos a [:6] ---
            for entry in feed.entries[:6]:
                if Article.query.filter_by(title=entry.title).first():
                    continue

                # 1. Intentamos el texto completo
                contenido = obtener_texto_completo(entry.link)

                # 2. Si falla, usamos resumen + BOTÓN HTML
                if not contenido or len(contenido) < 100:
                    summary_clean = re.sub(r"<.*?>", "", entry.summary)
                    if "Sigue leyendo" in summary_clean:
                        summary_clean = summary_clean.split("Sigue leyendo")[0]

                    contenido = (
                        f"{summary_clean}...\n\n"
                        f'<div class="mt-4">'
                        f'  <a href="{entry.link}" target="_blank" class="btn btn-danger">'
                        f'    <i class="bi bi-box-arrow-up-right"></i> Leer artículo completo en MotorSport.com'
                        f"  </a>"
                        f"</div>"
                    )

                # Imagen
                img = "https://upload.wikimedia.org/wikipedia/commons/d/d4/Race_car_placeholder.jpg"
                if "media_content" in entry:
                    img = entry.media_content[0]["url"]
                elif "enclosures" in entry and len(entry.enclosures) > 0:
                    img = entry.enclosures[0]["href"]

                nuevo_art = Article(
                    title=entry.title,
                    content=contenido,
                    image=img,
                    date=datetime.now(),
                    author_id=bot.id,
                    category_id=cats_db[slug].id,
                )
                db.session.add(nuevo_art)
                nuevas += 1
            print("OK.")

        db.session.commit()
        print(f"✅ {nuevas} noticias añadidas.")


if __name__ == "__main__":
    actualizar_noticias_auto()
