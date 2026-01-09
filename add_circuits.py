from app import app
from models import db, Circuit


def cargar_circuitos_sonido():
    with app.app_context():
        print("🔊 SINTONIZANDO MOTORES (COMPLETO)...")

        # 1. Limpieza de circuitos anteriores
        try:
            db.session.query(Circuit).delete()
            db.session.commit()
        except:
            db.session.rollback()

        # 2. Lista completa basada en tus archivos MP3
        datos = [
            {
                "name": "Mónaco",
                "country": "Mónaco",
                "image": "https://upload.wikimedia.org/wikipedia/commons/3/30/Circuit_de_Monaco_2004-present.svg",
                "audio": "monaco.mp3",
            },
            {
                "name": "Spa-Francorchamps",
                "country": "Bélgica",
                "image": "https://upload.wikimedia.org/wikipedia/commons/5/54/Spa-Francorchamps_of_Belgium.svg",
                "audio": "spa.mp3",
            },
            {
                "name": "Silverstone",
                "country": "Reino Unido",
                "image": "https://upload.wikimedia.org/wikipedia/commons/e/ee/Silverstone_Circuit_2024.svg",
                "audio": "silverstone.mp3",
            },
            {
                "name": "Monza",
                "country": "Italia",
                "image": "https://upload.wikimedia.org/wikipedia/commons/5/56/Monza_track_map.svg",
                "audio": "monza.mp3",
            },
            {
                "name": "Suzuka",
                "country": "Japón",
                "image": "https://upload.wikimedia.org/wikipedia/commons/0/07/Suzuka_circuit_map_2005.svg",
                "audio": "suzuka.mp3",
            },
            # --- NUEVOS AÑADIDOS SEGÚN TU FOTO ---
            {
                "name": "Bahrain",
                "country": "Baréin",
                "image": "https://upload.wikimedia.org/wikipedia/commons/2/29/Bahrain_International_Circuit--Grand_Prix_Layout.svg",
                "audio": "bahrain.mp3",
            },
            {
                "name": "Barcelona-Catalunya",
                "country": "España",
                "image": "https://upload.wikimedia.org/wikipedia/commons/2/20/Catalunya.svg",
                "audio": "catalunya.mp3",
            },
            {
                "name": "Interlagos",
                "country": "Brasil",
                "image": "https://upload.wikimedia.org/wikipedia/commons/9/9d/Interlagos_Circuit_2023.svg",
                "audio": "interlagos.mp3",
            },
            {
                "name": "Red Bull Ring",
                "country": "Austria",
                "image": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Red_Bull_Ring_2022.svg",
                "audio": "redbullring.mp3",
            },
            {
                "name": "Zandvoort",
                "country": "Países Bajos",
                "image": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Circuit_Zandvoort_2020.svg",
                "audio": "zandvoort.mp3",
            },
        ]

        count = 0
        for item in datos:
            nuevo = Circuit(
                name=item["name"],
                country=item["country"],
                image=item["image"],
                audio=f"sounds/{item['audio']}",  # Ruta relativa para Flask
            )
            db.session.add(nuevo)
            count += 1
            print(f"   🎧 {item['name']} cargado.")

        db.session.commit()
        print(f"✅ ¡LISTO! {count} pistas de audio cargadas.")


if __name__ == "__main__":
    cargar_circuitos_sonido()
