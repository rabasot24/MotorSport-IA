from app import app
from models import db, Vehicle
import random


def cargar_leyendas():
    with app.app_context():
        print("🏛️  Abriendo las puertas del Salón de la Fama...")

        # 1. Limpiamos lo anterior
        try:
            db.session.query(Vehicle).delete()
            db.session.commit()
            print("🧹 Garaje anterior limpiado.")
        except Exception as e:
            db.session.rollback()
            print("⚠️ Nota: No se pudo limpiar la tabla o estaba vacía.")

        # --- LA LISTA DE LOS 50 ELEGIDOS ---
        leyendas = [
            # --- FÓRMULA 1 CLÁSICA ---
            {
                "name": "McLaren MP4/4",
                "image": "https://upload.wikimedia.org/wikipedia/commons/2/23/Ayrton_Senna_1988_Monaco.jpg",
                "description": "1988. La obra maestra de Gordon Murray. Ganó 15 de 16 carreras con Senna y Prost.",
                "year": 1988,
                "category": "F1 Clásico",
            },
            {
                "name": "Ferrari F2004",
                "image": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Michael_Schumacher_Ferrari_F2004.jpg",
                "description": "2004. La cumbre de la era V10. Schumacher rompió casi todos los récords de vuelta.",
                "year": 2004,
                "category": "F1 Clásico",
            },
            {
                "name": "Williams FW14B",
                "image": "https://upload.wikimedia.org/wikipedia/commons/6/67/Nigel_Mansell_-_Williams_FW14B_-_1992_Monaco_Grand_Prix.jpg",
                "description": "1992. El coche de 'otro planeta'. Suspensión activa y control de tracción.",
                "year": 1992,
                "category": "F1 Clásico",
            },
            {
                "name": "Lotus 72",
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Emerson_Fittipaldi_Lotus_72D_1972.jpg/1280px-Emerson_Fittipaldi_Lotus_72D_1972.jpg",
                "description": "1970. Revolucionó la F1 moviendo los radiadores a los pontones laterales.",
                "year": 1970,
                "category": "F1 Clásico",
            },
            {
                "name": "Mercedes W196",
                "image": "https://upload.wikimedia.org/wikipedia/commons/6/66/Mercedes-Benz_W196_Streamliner.jpg",
                "description": "1954. La 'Flecha de Plata' de Fangio con carrocería aerodinámica.",
                "year": 1954,
                "category": "F1 Clásico",
            },
            {
                "name": "Tyrrell P34",
                "image": "https://upload.wikimedia.org/wikipedia/commons/b/b3/Tyrrell_P34_Goodwood.jpg",
                "description": "1976. El legendario 'Six-Wheeler'. El único coche de 6 ruedas que ganó una carrera.",
                "year": 1976,
                "category": "F1 Clásico",
            },
            {
                "name": "Brawn BGP 001",
                "image": "https://upload.wikimedia.org/wikipedia/commons/b/b8/Jenson_Button_2009_Japan_2.jpg",
                "description": "2009. Ganó el mundial contra todo pronóstico gracias al difusor doble.",
                "year": 2009,
                "category": "F1 Clásico",
            },
            {
                "name": "Renault R25",
                "image": "https://upload.wikimedia.org/wikipedia/commons/7/73/Fernando_Alonso_2005_Canada.jpg",
                "description": "2005. El coche que destronó a Ferrari y llevó a Alonso a su primer título.",
                "year": 2005,
                "category": "F1 Clásico",
            },
            # --- RALLY MONSTERS ---
            {
                "name": "Audi Sport Quattro S1",
                "image": "https://upload.wikimedia.org/wikipedia/commons/5/52/Audi_Quattro_S1_E2.jpg",
                "description": "El rey del Grupo B. Introdujo la tracción total en los rallys.",
                "year": 1985,
                "category": "Rally Legend",
            },
            {
                "name": "Lancia Stratos HF",
                "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Lancia_Stratos_HF_Group_4.jpg",
                "description": "El primer coche diseñado desde cero para ganar rallys con motor Ferrari.",
                "year": 1974,
                "category": "Rally Legend",
            },
            {
                "name": "Subaru Impreza 22B",
                "image": "https://upload.wikimedia.org/wikipedia/commons/1/1d/Subaru_Impreza_22B_STI.jpg",
                "description": "La leyenda azul y dorada de Colin McRae.",
                "year": 1998,
                "category": "Rally Legend",
            },
            {
                "name": "Peugeot 205 T16",
                "image": "https://upload.wikimedia.org/wikipedia/commons/a/a2/Peugeot_205_T16_Grand_Raid.jpg",
                "description": "Motor central y chasis tubular. Dominó el Grupo B.",
                "year": 1984,
                "category": "Rally Legend",
            },
            {
                "name": "Lancia Delta Integrale",
                "image": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Lancia_Delta_HF_Integrale_Evoluzione_II.jpg",
                "description": "Ganó 6 títulos de constructores consecutivos. Una bestia italiana.",
                "year": 1991,
                "category": "Rally Legend",
            },
            {
                "name": "Toyota Celica GT-Four",
                "image": "https://upload.wikimedia.org/wikipedia/commons/7/73/Toyota_Celica_GT-Four_ST205_WRC.jpg",
                "description": "El arma de Carlos Sainz. Famoso por su ingeniería avanzada.",
                "year": 1994,
                "category": "Rally Legend",
            },
            # --- LE MANS ---
            {
                "name": "Porsche 917K",
                "image": "https://upload.wikimedia.org/wikipedia/commons/1/13/Porsche_917_K_%28Gulf%29.jpg",
                "description": "Dio a Porsche su primera victoria en Le Mans. Famoso por la película de Steve McQueen.",
                "year": 1970,
                "category": "Endurance",
            },
            {
                "name": "Mazda 787B",
                "image": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Mazda_787B_2011.jpg",
                "description": "El único coche con motor rotativo (Wankel) que ganó Le Mans.",
                "year": 1991,
                "category": "Endurance",
            },
            {
                "name": "Ford GT40 MkII",
                "image": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Ford_GT40_Mk_II_Goodwood_Festival_of_Speed_2015_01.jpg",
                "description": "Construido para destruir a Ferrari en Le Mans. Logró un histórico 1-2-3.",
                "year": 1966,
                "category": "Endurance",
            },
            {
                "name": "Sauber C9",
                "image": "https://upload.wikimedia.org/wikipedia/commons/2/27/Sauber_Mercedes_C9.jpg",
                "description": "Alcanzó los 400 km/h en la recta de Mulsanne.",
                "year": 1989,
                "category": "Endurance",
            },
            {
                "name": "McLaren F1 GTR",
                "image": "https://upload.wikimedia.org/wikipedia/commons/9/9c/McLaren_F1_GTR_Longtail.jpg",
                "description": "Un coche de calle adaptado que ganó Le Mans en su primer intento.",
                "year": 1995,
                "category": "Endurance",
            },
            # --- SUPERCOCHES ---
            {
                "name": "Ferrari F40",
                "image": "https://upload.wikimedia.org/wikipedia/commons/c/cb/F40_Ferrari_20090509.jpg",
                "description": "El último coche aprobado por Enzo Ferrari. V8 biturbo salvaje.",
                "year": 1987,
                "category": "Supercar",
            },
            {
                "name": "Nissan Skyline GT-R R34",
                "image": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Nissan_Skyline_GT-R_V-Spec_II_N%C3%BCr_%28BNR34%29.jpg",
                "description": "Godzilla. Icono JDM con motor RB26DETT.",
                "year": 1999,
                "category": "JDM Legend",
            },
            {
                "name": "Toyota Supra MK4",
                "image": "https://upload.wikimedia.org/wikipedia/commons/6/61/Toyota_Supra_MkIV_white.jpg",
                "description": "Famoso por su motor 2JZ indestructible capaz de soportar 1000CV.",
                "year": 1994,
                "category": "JDM Legend",
            },
            {
                "name": "Honda NSX-R",
                "image": "https://upload.wikimedia.org/wikipedia/commons/e/ea/Honda_NSX-R_%28NA2%29_front.jpg",
                "description": "El Ferrari japonés. Puesto a punto por Ayrton Senna.",
                "year": 1992,
                "category": "JDM Legend",
            },
            {
                "name": "Lamborghini Countach",
                "image": "https://upload.wikimedia.org/wikipedia/commons/0/06/Lamborghini_Countach_LP5000_QV.jpg",
                "description": "El coche póster de los 80. Diseño de cuña extremo creado por Gandini.",
                "year": 1974,
                "category": "Supercar",
            },
            {
                "name": "Bugatti Veyron",
                "image": "https://upload.wikimedia.org/wikipedia/commons/c/c9/Bugatti_Veyron_16.4_%E2%80%93_Frontansicht_%281%29%2C_5._April_2012%2C_D%C3%BCsseldorf.jpg",
                "description": "El primer coche de producción en superar los 400 km/h y los 1000 CV.",
                "year": 2005,
                "category": "Hypercar",
            },
            {
                "name": "Porsche 959",
                "image": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Porsche_959_Front.jpg",
                "description": "El coche más avanzado de los 80. Trajo tecnología del futuro a la calle.",
                "year": 1986,
                "category": "Supercar",
            },
            {
                "name": "Dodge Viper GTS",
                "image": "https://upload.wikimedia.org/wikipedia/commons/0/02/Dodge_Viper_GTS_Coupe_Blue.jpg",
                "description": "Fuerza bruta americana. Motor V10 de camión en un chasis deportivo.",
                "year": 1996,
                "category": "Muscle Car",
            },
            {
                "name": "Lexus LFA",
                "image": "https://upload.wikimedia.org/wikipedia/commons/4/4c/Lexus_LFA_Nurburgring_Package.jpg",
                "description": "El mejor sonido de la historia gracias a su motor V10 Yamaha.",
                "year": 2010,
                "category": "Supercar",
            },
            {
                "name": "Shelby Cobra 427",
                "image": "https://upload.wikimedia.org/wikipedia/commons/7/75/Shelby_AC_Cobra_427.jpg",
                "description": "Chasis británico ligero, motor V8 americano masivo.",
                "year": 1965,
                "category": "Classic",
            },
            {
                "name": "Aston Martin DB5",
                "image": "https://upload.wikimedia.org/wikipedia/commons/1/1e/Aston_Martin_DB5_01.jpg",
                "description": "El coche de James Bond. Icono del cine mundial.",
                "year": 1963,
                "category": "Classic",
            },
            {
                "name": "Mercedes 300 SL",
                "image": "https://upload.wikimedia.org/wikipedia/commons/2/29/1955_Mercedes-Benz_300_SL_Gullwing_Coupe_front_left.jpg",
                "description": "El 'Alas de Gaviota'. El coche más rápido de su época.",
                "year": 1954,
                "category": "Classic",
            },
            {
                "name": "Jaguar E-Type",
                "image": "https://upload.wikimedia.org/wikipedia/commons/9/91/Jaguar_E-Type_Series_1_3.8_Litre_Fixed_Head_Coupe.jpg",
                "description": "El coche más bello jamás fabricado según Enzo Ferrari.",
                "year": 1961,
                "category": "Classic",
            },
            {
                "name": "Ford Mustang Shelby GT350",
                "image": "https://upload.wikimedia.org/wikipedia/commons/d/d1/1966_Shelby_GT350.jpg",
                "description": "Definió la era de los Muscle Cars. Potencia V8.",
                "year": 1965,
                "category": "Muscle Car",
            },
            {
                "name": "Chevrolet Corvette C2",
                "image": "https://upload.wikimedia.org/wikipedia/commons/6/69/1963_Chevrolet_Corvette_Sting_Ray_Coupe_Split_Window.jpg",
                "description": "El 'Sting Ray'. Famoso por su ventana trasera partida.",
                "year": 1963,
                "category": "Muscle Car",
            },
            {
                "name": "Koenigsegg Agera RS",
                "image": "https://upload.wikimedia.org/wikipedia/commons/8/8f/Koenigsegg_Agera_RS_Geneva_2015.jpg",
                "description": "Rompió el récord de velocidad mundial (447 km/h) en 2017.",
                "year": 2015,
                "category": "Hypercar",
            },
            {
                "name": "Pagani Zonda",
                "image": "https://upload.wikimedia.org/wikipedia/commons/3/30/Pagani_Zonda_C12_S.jpg",
                "description": "Arte sobre ruedas con motor AMG.",
                "year": 1999,
                "category": "Hypercar",
            },
            {
                "name": "Alfa Romeo 33 Stradale",
                "image": "https://upload.wikimedia.org/wikipedia/commons/7/74/Alfa_Romeo_33_Stradale_Front.jpg",
                "description": "Posiblemente el coche más bonito de todos los tiempos.",
                "year": 1967,
                "category": "Classic",
            },
            {
                "name": "BMW M3 E30",
                "image": "https://upload.wikimedia.org/wikipedia/commons/e/ec/BMW_M3_E30.jpg",
                "description": "El padre de los sedanes deportivos modernos.",
                "year": 1986,
                "category": "Classic",
            },
            {
                "name": "Mazda MX-5 (NA)",
                "image": "https://upload.wikimedia.org/wikipedia/commons/f/f6/1990_Mazda_Miata_Blue.jpg",
                "description": "El 'Miata'. Revivió el concepto de roadster ligero.",
                "year": 1989,
                "category": "Classic",
            },
        ]

        print(f"📦 Cargando {len(leyendas)} vehículos legendarios...")

        for i, car in enumerate(leyendas, 1):
            # LÓGICA DE SEGURIDAD:
            # Extraemos la marca del nombre (Ej: "Ferrari F40" -> "Ferrari")
            marca_calculada = car["name"].split(" ")[0]

            # Aseguramos que existan 'year' y 'category' si faltan
            anio = car.get("year", 2000)
            categoria = car.get("category", "Legend")

            nuevo = Vehicle(
                name=car["name"],
                image=car["image"],
                description=car["description"],
                # AQUÍ ESTABA EL PROBLEMA: AÑADIMOS LOS CAMPOS OBLIGATORIOS
                manufacturer=marca_calculada,
                year=anio,
                category=categoria,
            )
            db.session.add(nuevo)
            print(f"   ├─ [{i}/{len(leyendas)}] {car['name']} añadido.")

        db.session.commit()
        print("\n🏁 ¡PROCESO TERMINADO! Tu garaje ahora vale millones.")


if __name__ == "__main__":
    cargar_leyendas()
