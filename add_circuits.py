from app import app
from models import db, Circuit


def agregar_circuitos():
    with app.app_context():
        # Lista ampliada a 10 circuitos legendarios
        circuitos_nuevos = [
            {
                "name": "Spa-Francorchamps",
                "country": "Bélgica",
                "audio": "/static/sounds/spa.mp3",
                "img": "https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Belgium_Circuit.png",
            },
            {
                "name": "Mónaco",
                "country": "Mónaco",
                "audio": "/static/sounds/monaco.mp3",
                "img": "https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Monoco_Circuit.png",
            },
            {
                "name": "Silverstone",
                "country": "Reino Unido",
                "audio": "/static/sounds/silverstone.mp3",
                "img": "https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Great_Britain_Circuit.png",
            },
            {
                "name": "Suzuka",
                "country": "Japón",
                "audio": "/static/sounds/suzuka.mp3",
                "img": "https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Japan_Circuit.png",
            },
            {
                "name": "Interlagos",
                "country": "Brasil",
                "audio": "/static/sounds/interlagos.mp3",
                "img": "https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Brazil_Circuit.png",
            },
            {
                "name": "Red Bull Ring",
                "country": "Austria",
                "audio": "/static/sounds/redbullring.mp3",
                "img": "https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Austria_Circuit.png",
            },
            {
                "name": "Circuit de Barcelona-Catalunya",
                "country": "España",
                "audio": "/static/sounds/catalunya.mp3",
                "img": "https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Spain_Circuit.png",
            },
            {
                "name": "Zandvoort",
                "country": "Países Bajos",
                "audio": "/static/sounds/zandvoort.mp3",
                "img": "https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Netherlands_Circuit.png",
            },
            {
                "name": "Bahrain International Circuit",
                "country": "Bahréin",
                "audio": "/static/sounds/bahrain.mp3",
                "img": "https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Bahrain_Circuit.png",
            },
            # Nota: Monza ya debería estar en tu base de datos si ejecutaste seed.py
        ]

        print("🏎️  Ampliando la parrilla a 10 circuitos...")

        count = 0
        for c in circuitos_nuevos:
            # Comprobamos si ya existe por nombre para no duplicar
            existe = Circuit.query.filter_by(name=c["name"]).first()

            if not existe:
                nuevo = Circuit(
                    name=c["name"],
                    country=c["country"],
                    audio_path=c["audio"],
                    image_path=c["img"],
                )
                db.session.add(nuevo)
                print(f"✅ Añadido: {c['name']}")
                count += 1
            else:
                print(f"ℹ️  Ya existe: {c['name']}")

        db.session.commit()

        total = Circuit.query.count()
        print(f"\n🏁 Proceso terminado. Total de circuitos en DB: {total}")


if __name__ == "__main__":
    agregar_circuitos()
