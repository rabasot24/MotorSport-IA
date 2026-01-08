import json
import os
from app import app
from models import db, User, Vehicle, Article, Category, Circuit


def cargar_datos():
    # Contexto de la aplicación para acceder a la DB
    with app.app_context():
        print("Creando base de datos...")
        db.create_all()

        # 1. Crear ADMIN (Requisito Sprint 1)
        if not User.query.filter_by(email="admin@motorsport.com").first():
            admin = User(username="Admin", email="admin@motorsport.com", role="admin")
            admin.set_password("admin123")
            db.session.add(admin)
            print("✅ Usuario Admin creado (Pass: admin123)")

        # 2. Crear CATEGORÍA por defecto
        cat = Category.query.filter_by(slug="general").first()
        if not cat:
            cat = Category(name="Motor General", slug="general")
            db.session.add(cat)
            db.session.commit()

        # 3. Migrar NOTICIAS (desde mockdata/noticias.json)
        try:
            ruta_noticias = os.path.join("mockdata", "noticias.json")
            if os.path.exists(ruta_noticias):
                with open(ruta_noticias, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        if not Article.query.filter_by(title=item["titulo"]).first():
                            art = Article(
                                title=item["titulo"],
                                content=item["contenido"],
                                image=item["imagen"],
                                date=None,  # Usará la fecha actual
                                category_id=cat.id,
                            )
                            db.session.add(art)
                print("✅ Noticias migradas.")
        except Exception as e:
            print(f"❌ Error migrando noticias: {e}")

        # 4. Migrar VEHÍCULOS (desde mockdata/vehiculos.json)
        try:
            ruta_vehiculos = os.path.join("mockdata", "vehiculos.json")
            if os.path.exists(ruta_vehiculos):
                with open(ruta_vehiculos, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        if not Vehicle.query.filter_by(
                            name=item.get("nombre", "Sin nombre")
                        ).first():
                            veh = Vehicle(
                                name=item.get("nombre", "Desconocido"),
                                manufacturer=item.get("nombre", "").split(" ")[0],
                                year=item.get("año", 2000),
                                category=item.get("categoria", "General"),
                                description=item.get("descripcion", ""),
                                image=item.get("imagen", ""),
                                specs=item,  # Guardamos todo el JSON como specs
                            )
                            db.session.add(veh)
                print("✅ Vehículos migrados.")
        except Exception as e:
            print(f"❌ Error migrando vehículos: {e}")

        # 5. Crear CIRCUITOS para el QUIZ (Sección 11 PDF)
        # Como no tienes JSON de esto, los creamos aquí directos
        if not Circuit.query.first():
            c1 = Circuit(
                name="Monza", country="Italia", audio_path="/static/sounds/monza.mp3"
            )
            c2 = Circuit(
                name="Spa-Francorchamps",
                country="Bélgica",
                audio_path="/static/sounds/spa.mp3",
            )
            c3 = Circuit(
                name="Silverstone",
                country="Reino Unido",
                audio_path="/static/sounds/silverstone.mp3",
            )
            c4 = Circuit(
                name="Suzuka", country="Japón", audio_path="/static/sounds/suzuka.mp3"
            )
            db.session.add_all([c1, c2, c3, c4])
            print("✅ Circuitos para Quiz creados.")

        db.session.commit()
        print(
            "\n🚀 ¡BASE DE DATOS LISTA! Ya puedes borrar la carpeta mockdata si quieres."
        )


if __name__ == "__main__":
    cargar_datos()
