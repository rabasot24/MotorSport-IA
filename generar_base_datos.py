import os
from app import app, db
from models import Vehicle

# Configuración de carpeta
CARPETA_FISICA = os.path.join("static", "img", "coches")

def buscar_imagen_local(nombre_coche):
    """
    Busca la foto en tu carpeta (prioridad .webp, luego .jpg).
    Convierte 'McLaren MP4/4' -> 'mclaren_mp4_4.webp'
    """
    # 1. Normalizar nombre (Minúsculas y guiones bajos)
    nombre_limpio = nombre_coche.lower().replace(" ", "_").replace("-", "_").replace("/", "_").strip()
    
    # 2. Rutas a comprobar
    ruta_webp = os.path.join(CARPETA_FISICA, f"{nombre_limpio}.webp")
    ruta_jpg = os.path.join(CARPETA_FISICA, f"{nombre_limpio}.jpg")
    
    # 3. Comprobación
    if os.path.exists(ruta_webp):
        return f"img/coches/{nombre_limpio}.webp"
    elif os.path.exists(ruta_jpg):
        return f"img/coches/{nombre_limpio}.jpg"
    else:
        print(f"⚠️ FOTO NO ENCONTRADA PARA: {nombre_limpio} (Se usará default)")
        return "img/default_car.jpg"

def cargar_todo():
    with app.app_context():
        print("📖 RECONSTRUYENDO ENCICLOPEDIA CON FOTOS LOCALES...")

        # 1. Limpieza total
        db.drop_all()
        db.create_all()

        # ---------------------------------------------------------
        # PARTE 1: LOS COCHES DETALLADOS (Tu lista 'flota')
        # ---------------------------------------------------------
        flota = [
            {
                "name": "McLaren MP4/4",
                "year": 1988,
                "cat": "F1 Legend",
                "engine": "Honda RA168E 1.5L V6T", "hp": 1200, "top": 330, "acc": 2.5, "w": 540,
                "desc": "Considerado unánimemente como el monoplaza más dominante en la historia de la F1. Ganó 15 de 16 carreras en 1988 con Senna y Prost."
            },
            {
                "name": "Ferrari F2004",
                "year": 2004,
                "cat": "F1 Legend",
                "engine": "Ferrari 053 3.0L V10", "hp": 920, "top": 360, "acc": 2.1, "w": 605,
                "desc": "El rey de la velocidad. Su motor V10 a 19.000 rpm dio a Schumacher su último título. Posee récords de vuelta imbatidos durante 15 años."
            },
            {
                "name": "Williams FW14B",
                "year": 1992,
                "cat": "F1 Legend",
                "engine": "Renault RS3C 3.5L V10", "hp": 760, "top": 340, "acc": 2.4, "w": 505,
                "desc": "El coche ordenador. Suspensión activa, control de tracción y ABS. Tan superior que la FIA prohibió su tecnología."
            },
            {
                "name": "Mercedes W11",
                "year": 2020,
                "cat": "F1 Legend",
                "engine": "1.6L V6 Turbo Híbrido", "hp": 1050, "top": 350, "acc": 2.3, "w": 746,
                "desc": "La Perfección Negra. Estadísticamente el coche más rápido a una vuelta de la historia. Introdujo el sistema DAS."
            },
            {
                "name": "Audi Quattro S1",
                "year": 1985,
                "cat": "Rally Monster",
                "engine": "5 Cilindros 2.1L Turbo", "hp": 591, "top": 220, "acc": 3.1, "w": 1090,
                "desc": "El monstruo del Grupo B. Revolucionó los rallys con la tracción total y su sonido de 5 cilindros es legendario."
            },
            {
                "name": "Lancia Stratos HF",
                "year": 1974,
                "cat": "Rally Legend",
                "engine": "Ferrari V6 2.4L", "hp": 280, "top": 230, "acc": 4.5, "w": 980,
                "desc": "El primer coche diseñado exclusivamente para ganar rallys. Motor Ferrari y diseño de nave espacial."
            },
            {
                "name": "Subaru Impreza 22B",
                "year": 1998,
                "cat": "JDM Icon",
                "engine": "EJ22 Boxer 2.2L Turbo", "hp": 280, "top": 248, "acc": 4.7, "w": 1270,
                "desc": "El unicornio japonés. Creado para celebrar los títulos de WRC. Ensanchado a mano y extremadamente raro."
            },
            {
                "name": "Ferrari F40",
                "year": 1987,
                "cat": "Supercar",
                "engine": "2.9L V8 Biturbo", "hp": 478, "top": 324, "acc": 4.1, "w": 1100,
                "desc": "El legado de Enzo. Sin ayudas, sin radio, sin manillas. Pura fibra de carbono y violencia turboalimentada."
            },
            {
                "name": "Bugatti Veyron",
                "year": 2005,
                "cat": "Hypercar",
                "engine": "8.0L W16 Quad-Turbo", "hp": 1001, "top": 407, "acc": 2.5, "w": 1888,
                "desc": "El Concorde de la carretera. El primero en superar los 400 km/h y los 1000 CV. Una hazaña de ingeniería."
            },
            {
                "name": "Mazda 787B",
                "year": 1991,
                "cat": "Le Mans Legend",
                "engine": "R26B 4-Rotor", "hp": 700, "top": 350, "acc": 2.5, "w": 830,
                "desc": "La furia rotativa. El único ganador de Le Mans con motor Wankel. Su sonido es ensordecedor."
            },
            {
                "name": "Nissan Skyline GT-R R34",
                "year": 1999,
                "cat": "JDM Legend",
                "engine": "RB26DETT Twin-Turbo", "hp": 280, "top": 250, "acc": 4.9, "w": 1560,
                "desc": "Godzilla. Icono de la generación PlayStation. Tecnología punta y un motor capaz de duplicar su potencia fácilmente."
            },
            {
                "name": "Toyota Supra MK4",
                "year": 1994,
                "cat": "JDM Legend",
                "engine": "3.0L 2JZ-GTE Twin-Turbo", "hp": 320, "top": 250, "acc": 4.6, "w": 1510,
                "desc": "La leyenda del 2JZ. Famoso por su motor a prueba de balas capaz de soportar 1000CV. Estrella de cine."
            },
            {
                "name": "Dodge Viper GTS",
                "year": 1996,
                "cat": "Muscle Car",
                "engine": "8.0L V10", "hp": 450, "top": 290, "acc": 4.0, "w": 1500,
                "desc": "El coche que quiere matarte. Motor V10 de camión en un chasis deportivo sin control de tracción."
            }
        ]

        # ---------------------------------------------------------
        # PARTE 2: EL RESTO (Tu lista 'otros_coches')
        # ---------------------------------------------------------
        otros_coches = [
            {"n": "Mercedes 300 SL", "y": 1954, "c": "Classic", "hp": 215, "desc": "El 'Alas de Gaviota'. Primer superdeportivo de la historia."},
            {"n": "Aston Martin DB5", "y": 1964, "c": "Classic", "hp": 282, "desc": "El coche de James Bond. Elegancia británica atemporal."},
            {"n": "Shelby Cobra 427", "y": 1965, "c": "Muscle", "hp": 425, "desc": "Chasis británico ligero con un V8 Ford masivo."},
            {"n": "Ford GT40", "y": 1966, "c": "Le Mans", "hp": 485, "desc": "Nacido para ganar a Ferrari. Logró un 1-2-3 histórico."},
            {"n": "Porsche 959", "y": 1986, "c": "Supercar", "hp": 450, "desc": "El coche más tecnológico de los 80 con tracción total."},
            {"n": "Honda NSX-R", "y": 1992, "c": "JDM", "hp": 280, "desc": "Puesto a punto por Ayrton Senna. El Ferrari japonés fiable."},
            {"n": "Lexus LFA", "y": 2010, "c": "Supercar", "hp": 560, "desc": "El mejor sonido V10 de la historia. Obra maestra de carbono."},
            {"n": "Pagani Zonda", "y": 1999, "c": "Hypercar", "hp": 555, "desc": "Arte italiano con corazón Mercedes AMG."},
            {"n": "Koenigsegg Agera RS", "y": 2015, "c": "Hypercar", "hp": 1160, "desc": "Récord de velocidad (447 km/h) en carretera pública."},
            {"n": "Lamborghini Countach", "y": 1974, "c": "Classic", "hp": 375, "desc": "El diseño de cuña que definió los años 80."},
            {"n": "Lamborghini Miura", "y": 1966, "c": "Classic", "hp": 350, "desc": "El padre de los superdeportivos modernos con motor central."},
            {"n": "Jaguar E-Type", "y": 1961, "c": "Classic", "hp": 265, "desc": "El coche más bello del mundo según Enzo Ferrari."},
            {"n": "Toyota 2000GT", "y": 1967, "c": "Classic", "hp": 150, "desc": "El primer supercoche japonés desarrollado con Yamaha."},
            {"n": "BMW M3 E30", "y": 1986, "c": "Classic", "hp": 200, "desc": "Nacido para el DTM. Equilibrio perfecto."},
            {"n": "Porsche Carrera GT", "y": 2004, "c": "Supercar", "hp": 612, "desc": "Motor V10 de F1 y cambio manual. Analógico puro."},
            {"n": "Ferrari LaFerrari", "y": 2013, "c": "Hypercar", "hp": 963, "desc": "El híbrido definitivo de Maranello."},
            {"n": "McLaren F1", "y": 1992, "c": "Supercar", "hp": 627, "desc": "Asiento central y motor BMW V12 de oro."},
            {"n": "Alfa Romeo 33 Stradale", "y": 1967, "c": "Classic", "hp": 230, "desc": "Escultura en movimiento. Coche de carreras para calle."},
            {"n": "Lancia Delta Integrale", "y": 1991, "c": "Rally", "hp": 215, "desc": "La leyenda de los rallys italianos."},
            {"n": "Peugeot 205 T16", "y": 1984, "c": "Rally", "hp": 200, "desc": "Dominador del Grupo B y del Dakar."},
            {"n": "Ford Escort Cosworth", "y": 1992, "c": "Rally", "hp": 227, "desc": "Famoso por su alerón cola de ballena."},
            {"n": "Mitsubishi Evo VI", "y": 1999, "c": "JDM", "hp": 280, "desc": "Edición Tommi Makinen. Agilidad pura."},
            {"n": "Renault 5 Turbo", "y": 1980, "c": "Rally", "hp": 160, "desc": "El 'Culo Gordo' con motor central."},
            {"n": "Alpine A110", "y": 1971, "c": "Rally", "hp": 140, "desc": "Ligero y ágil, campeón de Montecarlo."},
            {"n": "Lotus Elise S1", "y": 1996, "c": "Sport", "hp": 118, "desc": "Ligereza extrema (725kg)."},
            {"n": "Mazda MX-5 NA", "y": 1989, "c": "Classic", "hp": 115, "desc": "El coche que salvó a los roadsters."},
            {"n": "Honda S2000", "y": 1999, "c": "JDM", "hp": 240, "desc": "Corte de inyección a 9000 RPM."},
            {"n": "Toyota AE86", "y": 1983, "c": "JDM", "hp": 130, "desc": "El rey del Drift y del Tofu."},
            {"n": "Nissan 240Z", "y": 1969, "c": "Classic", "hp": 150, "desc": "El deportivo japonés que conquistó América."},
            {"n": "Chevrolet Corvette C2", "y": 1963, "c": "Muscle", "hp": 360, "desc": "Sting Ray con ventana trasera partida."},
            {"n": "Ford Mustang 1967", "y": 1967, "c": "Muscle", "hp": 320, "desc": "Icono de Bullitt y del cine."},
            {"n": "Pontiac GTO", "y": 1964, "c": "Muscle", "hp": 325, "desc": "El primer Muscle Car verdadero."},
            {"n": "Plymouth Superbird", "y": 1970, "c": "Muscle", "hp": 425, "desc": "El coche del alerón gigante de NASCAR."},
            {"n": "Mercedes CLK GTR", "y": 1998, "c": "Supercar", "hp": 600, "desc": "Un coche de Le Mans con matrícula."},
            {"n": "Porsche 911 GT1", "y": 1997, "c": "Supercar", "hp": 536, "desc": "El 911 más extremo jamás fabricado."},
            {"n": "Toyota GT-One", "y": 1998, "c": "Le Mans", "hp": 600, "desc": "Prototipo de carreras disfrazado de calle."},
            {"n": "Sauber C9", "y": 1989, "c": "Le Mans", "hp": 720, "desc": "Flecha de plata que alcanzó 400 km/h."},
            {"n": "Jaguar XJ220", "y": 1992, "c": "Supercar", "hp": 542, "desc": "El gato más rápido de los 90."},
        ]

        contador = 0

        # PROCESAR LISTA 1 (Detallados)
        for car in flota:
            foto = buscar_imagen_local(car["name"])
            nuevo = Vehicle(
                name=car["name"],
                manufacturer=car["name"].split(" ")[0],
                year=car["year"],
                category=car["cat"],
                description=car["desc"],
                image=foto,
                engine=car["engine"],
                horsepower=car["hp"],
                top_speed=car["top"],
                acceleration=car["acc"],
                weight=car["w"]
            )
            db.session.add(nuevo)
            contador += 1
            print(f"✅ [DETALLADO] {car['name']} -> {foto}")

        # PROCESAR LISTA 2 (Resumidos)
        for car in otros_coches:
            foto = buscar_imagen_local(car["n"])
            nuevo = Vehicle(
                name=car["n"],
                manufacturer=car["n"].split(" ")[0],
                year=car["y"],
                category=car["c"],
                description=car["desc"],
                image=foto,
                # Rellenamos datos técnicos con genéricos porque no venían en tu script original
                engine="Clásico / Sport",
                horsepower=car["hp"],
                top_speed=250, 
                acceleration=5.0,
                weight=1200
            )
            db.session.add(nuevo)
            contador += 1
            print(f"🔹 [RESUMIDO]  {car['n']} -> {foto}")

        db.session.commit()
        print(f"\n🏁 ¡FIN! Base de datos cargada con {contador} vehículos.")

if __name__ == "__main__":
    cargar_todo()