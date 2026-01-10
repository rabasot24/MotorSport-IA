import os
import requests
from app import app
from models import db, Vehicle

CARPETA_IMAGENES = os.path.join("static", "img", "coches")


def descargar_imagen(url, nombre_archivo):
    try:
        if not os.path.exists(CARPETA_IMAGENES):
            os.makedirs(CARPETA_IMAGENES)

        ruta_completa = os.path.join(CARPETA_IMAGENES, nombre_archivo)

        if os.path.exists(ruta_completa):
            return f"img/coches/{nombre_archivo}"

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            with open(ruta_completa, "wb") as f:
                f.write(response.content)
            return f"img/coches/{nombre_archivo}"
    except:
        return "img/default_car.jpg"
    return "img/default_car.jpg"


def cargar_garaje_masivo():
    with app.app_context():
        print("📖 ESCRIBIENDO LA ENCICLOPEDIA DEL MOTOR (50 Vehículos)...")

        # 1. Limpieza total para actualizar los textos
        db.drop_all()
        db.create_all()

        # 2. LISTA DE VEHÍCULOS CON HISTORIAS EXTENDIDAS
        flota = [
            # --- F1 LEYENDAS ---
            {
                "name": "McLaren MP4/4",
                "year": 1988,
                "cat": "F1 Legend",
                "desc": """HISTORIA:
Considerado unánimemente como el monoplaza más dominante en la historia de la Fórmula 1. Nacido de la mente de Gordon Murray y Steve Nichols, este coche fue la herramienta perfecta para una alineación de pilotos irrepetible: Ayrton Senna y Alain Prost.

TECNOLOGÍA:
La clave de su éxito fue la posición de conducción "lowline" (ultra baja), que permitió reducir drásticamente el área frontal y mejorar la eficiencia aerodinámica. Montaba el legendario motor Honda RA168E V6 Turbo, capaz de gestionar el consumo de combustible mejor que cualquier rival en una era de restricciones severas.

LEGADO:
Ganó 15 de las 16 carreras de la temporada 1988, perdiendo solo en Monza debido a un incidente fortuito. Senna consiguió su primer título mundial con este chasis. Es el estándar de oro contra el que se mide cualquier dominio en la F1.""",
                "url": "https://upload.wikimedia.org/wikipedia/commons/2/23/Ayrton_Senna_1988_Monaco.jpg",
                "engine": "Honda RA168E 1.5L V6T",
                "hp": 1200,
                "top": 330,
                "acc": 2.5,
                "w": 540,
            },
            {
                "name": "Ferrari F2004",
                "year": 2004,
                "cat": "F1 Legend",
                "desc": """EL REY DE LA VELOCIDAD:
El F2004 representa la cúspide absoluta de la era de los motores V10 atmosféricos. Diseñado por Rory Byrne y Ross Brawn, fue la máquina que otorgó a Michael Schumacher su séptimo y último título mundial.

POR QUÉ ES ESPECIAL:
Su motor 053 V10 gritaba a más de 19.000 revoluciones por minuto, produciendo un sonido que muchos puristas consideran el mejor de la historia. Aerodinámicamente era una evolución del F2003-GA, pero refinado hasta la perfección.

RÉCORDS:
Este coche fue tan rápido que sus récords de vuelta en circuitos como Monza, Melbourne y Nürburgring se mantuvieron vigentes durante casi 15 años, hasta que los coches modernos de 2018-2020 lograron batirlos con neumáticos mucho más anchos.""",
                "url": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Michael_Schumacher_Ferrari_F2004.jpg",
                "engine": "Ferrari 053 3.0L V10",
                "hp": 920,
                "top": 360,
                "acc": 2.1,
                "w": 605,
            },
            {
                "name": "Williams FW14B",
                "year": 1992,
                "cat": "F1 Legend",
                "desc": """EL COCHE ORDENADOR:
En 1992, Williams presentó un coche que parecía ciencia ficción. El FW14B, diseñado por Adrian Newey, incorporaba suspensión activa controlada electrónicamente, control de tracción, frenos ABS y cambio semiautomático.

DOMINIO:
Nigel Mansell ganó las primeras 5 carreras consecutivas de la temporada, un récord en aquel entonces. El sistema de suspensión activa mantenía el coche perfectamente nivelado en las curvas, permitiendo que la aerodinámica funcionara siempre en su punto óptimo.

FINAL DE UNA ERA:
Fue tan superior (a veces sacaba 2 segundos por vuelta al segundo clasificado) que la FIA terminó prohibiendo todas estas ayudas electrónicas para 1994, convirtiendo al FW14B en el coche tecnológicamente más avanzado de su década.""",
                "url": "https://upload.wikimedia.org/wikipedia/commons/6/67/Nigel_Mansell_-_Williams_FW14B_-_1992_Monaco_Grand_Prix.jpg",
                "engine": "Renault RS3C 3.5L V10",
                "hp": 760,
                "top": 340,
                "acc": 2.4,
                "w": 505,
            },
            {
                "name": "Mercedes W11",
                "year": 2020,
                "cat": "F1 Legend",
                "desc": """LA PERFECCIÓN NEGRA:
Pintado de negro en apoyo a la lucha contra el racismo, el W11 es estadísticamente el coche más rápido jamás construido para una sola vuelta de clasificación. Lewis Hamilton rompió todos los esquemas con él.

INNOVACIÓN DAS:
Introdujo el polémico sistema DAS (Dual Axis Steering), que permitía al piloto tirar del volante hacia sí mismo en las rectas para cambiar la alineación de las ruedas delanteras y calentar los neumáticos uniformemente.

LEGADO:
Ganó 13 de 17 carreras en una temporada acortada por la pandemia. Su carga aerodinámica era tal que en curvas como Pouhon (Spa) o Copse (Silverstone) los pilotos ni siquiera levantaban el pie del acelerador.""",
                "url": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Lewis_Hamilton_2020_Tuscan_GP.jpg",
                "engine": "1.6L V6 Turbo Híbrido",
                "hp": 1050,
                "top": 350,
                "acc": 2.3,
                "w": 746,
            },
            # --- RALLY LEYENDAS ---
            {
                "name": "Audi Quattro S1",
                "year": 1985,
                "cat": "Rally Monster",
                "desc": """EL MONSTRUO DEL GRUPO B:
El Audi Sport Quattro S1 E2 es la imagen definitiva de la locura del Grupo B. Audi revolucionó el mundo de los rallys al introducir la tracción total (Quattro) en un deporte dominado hasta entonces por los tracción trasera.

INGENIERÍA:
Para mejorar el reparto de pesos, movieron radiadores, ventiladores y baterías al maletero. Su motor de 5 cilindros emitía un sonido de "gorjeo" característico debido al turbo anti-lag.

PIKES PEAK:
Tras la cancelación del Grupo B por su peligrosidad, Walter Röhrl llevó este coche a la famosa subida de Pikes Peak en 1987, convirtiéndose en el primer piloto en bajar de los 11 minutos, un hito histórico.""",
                "url": "https://upload.wikimedia.org/wikipedia/commons/5/52/Audi_Quattro_S1_E2.jpg",
                "engine": "5 Cilindros 2.1L Turbo",
                "hp": 591,
                "top": 220,
                "acc": 3.1,
                "w": 1090,
            },
            {
                "name": "Lancia Stratos HF",
                "year": 1974,
                "cat": "Rally Legend",
                "desc": """EL PRIMER PURASANGRE:
Antes del Stratos, los coches de rally eran versiones modificadas de coches de calle. El Stratos fue el primero diseñado desde cero con el único objetivo de ganar el Mundial de Rallys.

DISEÑO:
Con una distancia entre ejes minúscula, forma de cuña diseñada por Bertone y un motor V6 "prestado" del Ferrari Dino, era una máquina nerviosa y letalmente rápida en asfalto y tierra.

PALMARÉS:
Ganó el título de constructores tres años seguidos (1974, 1975, 1976). Es recordado como uno de los coches más bellos y efectivos jamás creados, apodado 'la bête à gagner' (la bestia para ganar).""",
                "url": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Lancia_Stratos_HF_Group_4.jpg",
                "engine": "Ferrari V6 2.4L",
                "hp": 280,
                "top": 230,
                "acc": 4.5,
                "w": 980,
            },
            {
                "name": "Subaru Impreza 22B",
                "year": 1998,
                "cat": "JDM Icon",
                "desc": """EL UNICORNIO JAPONÉS:
Creado para celebrar el 40 aniversario de Subaru y su tercer título consecutivo de constructores en el WRC. El 22B es la versión de calle definitiva del coche de rally de Colin McRae.

DIFERENCIAS:
A diferencia del WRX STI normal, el 22B tiene una carrocería ensanchada a mano (widebody) inspirada en el coche de WRC, un motor EJ22 aumentado a 2.2 litros y una suspensión Bilstein específica.

COLECCIONISMO:
Solo se fabricaron 400 unidades para Japón, que se vendieron en menos de 30 minutos. Hoy en día es uno de los coches japoneses más caros y buscados del mundo.""",
                "url": "https://upload.wikimedia.org/wikipedia/commons/1/1d/Subaru_Impreza_22B_STI.jpg",
                "engine": "EJ22 Boxer 2.2L Turbo",
                "hp": 280,
                "top": 248,
                "acc": 4.7,
                "w": 1270,
            },
            # --- SUPERCARS ---
            {
                "name": "Ferrari F40",
                "year": 1987,
                "cat": "Supercar",
                "desc": """EL LEGADO DE ENZO:
El F40 fue el último coche presentado y aprobado personalmente por Enzo Ferrari antes de su muerte. Fue creado para celebrar el 40 aniversario de la marca y para ser el coche de calle más rápido del mundo.

PURA CONDUCCIÓN:
No tiene dirección asistida, ni frenos ABS, ni control de tracción, ni radio, ni manillas en las puertas (se abren con un cable). Es un coche de carreras matriculable. Su carrocería es de Kevlar y fibra de carbono, con una capa de pintura tan fina que se puede ver la trama de la fibra debajo.

EL TURBO:
Famoso por su entrega de potencia "explosiva". Cuando los dos turbos IHI soplan a máxima presión, el coche se vuelve salvaje, exigiendo el máximo respeto del conductor.""",
                "url": "https://upload.wikimedia.org/wikipedia/commons/c/cb/F40_Ferrari_20090509.jpg",
                "engine": "2.9L V8 Biturbo",
                "hp": 478,
                "top": 324,
                "acc": 4.1,
                "w": 1100,
            },
            {
                "name": "Bugatti Veyron",
                "year": 2005,
                "cat": "Hypercar",
                "desc": """EL CONCORDE DE LA CARRETERA:
El Veyron no fue diseñado para ser un coche, sino para redefinir lo que era posible. El Grupo Volkswagen perdió dinero con cada unidad vendida, pero logró su objetivo: crear el primer coche de producción con más de 1000 CV y capaz de superar los 400 km/h.

CIFRAS ABSURDAS:
Tiene un motor W16 (dos V8 unidos) con 4 turbos y 10 radiadores. A velocidad máxima, vacía su depósito de 100 litros en 12 minutos. Sus neumáticos Michelin PAX cuestan 30.000€ el juego y solo pueden ser cambiados en Francia.

MODO VELOCIDAD MÁXIMA:
Para superar los 375 km/h, el conductor debe insertar una segunda llave especial en el suelo, que baja la suspensión, cierra los difusores frontales y reduce el ángulo del alerón trasero.""",
                "url": "https://upload.wikimedia.org/wikipedia/commons/c/c9/Bugatti_Veyron_16.4_%E2%80%93_Frontansicht_%281%29%2C_5._April_2012%2C_D%C3%BCsseldorf.jpg",
                "engine": "8.0L W16 Quad-Turbo",
                "hp": 1001,
                "top": 407,
                "acc": 2.5,
                "w": 1888,
            },
            {
                "name": "Mazda 787B",
                "year": 1991,
                "cat": "Le Mans Legend",
                "desc": """LA FURIA ROTATIVA:
El Mazda 787B tiene un lugar único en la historia: es el único coche con motor rotativo (Wankel) que ha ganado las 24 Horas de Le Mans. Venció a los poderosos equipos europeos gracias a su fiabilidad y eficiencia.

EL SONIDO:
Su motor R26B de 4 rotores produce uno de los sonidos más agudos, ruidosos e inconfundibles del automovilismo. Los pilotos decían que era ensordecedor incluso con tapones.

PROHIBICIÓN:
Poco después de su victoria, la normativa cambió, prohibiendo efectivamente los motores rotativos en la competición principal, lo que convirtió su hazaña en algo irrepetible.""",
                "url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Mazda_787B_2011.jpg",
                "engine": "R26B 4-Rotor",
                "hp": 700,
                "top": 350,
                "acc": 2.5,
                "w": 830,
            },
            # --- JDM LEGENDS ---
            {
                "name": "Nissan Skyline GT-R R34",
                "year": 1999,
                "cat": "JDM Legend",
                "desc": """GODZILLA:
El R34 GT-R es el icono definitivo de la generación PlayStation y de la cultura del tuning japonés. Famoso por su aparición en la saga Fast & Furious y Gran Turismo, es mucho más que una cara bonita.

TECNOLOGÍA:
Adelantado a su tiempo, contaba con una pantalla multifunción en el salpicadero que mostraba fuerzas G, presión de turbo y temperaturas (años antes de que esto fuera común). Su sistema de tracción total ATTESA E-TS PRO enviaba potencia a las ruedas delanteras solo cuando detectaba pérdida de tracción, permitiendo derrapar como un trasera pero acelerar como un 4x4.

MOTOR RB26:
El bloque motor RB26DETT es legendario por su resistencia. Aunque salía de fábrica con "276 CV" (por un pacto de caballeros japonés), en realidad daba más de 330 CV, y con modificaciones básicas podía superar fácilmente los 600 CV.""",
                "url": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Nissan_Skyline_GT-R_V-Spec_II_N%C3%BCr_%28BNR34%29.jpg",
                "engine": "RB26DETT Twin-Turbo",
                "hp": 280,
                "top": 250,
                "acc": 4.9,
                "w": 1560,
            },
            {
                "name": "Toyota Supra MK4",
                "year": 1994,
                "cat": "JDM Legend",
                "desc": """LA LEYENDA DEL 2JZ:
El Supra MK4 (A80) es venerado casi religiosamente por una razón: su motor 2JZ-GTE. Este bloque de hierro fundido es tan robusto que los preparadores descubrieron que podía soportar más de 800 CV sin necesidad de abrir el motor para reforzar los componentes internos.

CULTURA POP:
Aunque al principio no fue un éxito de ventas debido a su precio, el cine y los videojuegos lo convirtieron en un mito. Su alerón trasero de "arco" es una de las siluetas más reconocibles de los años 90.

RENDIMIENTO:
En su versión de stock, era un gran turismo cómodo y rápido, capaz de competir con Porsche y Ferrari de la época por una fracción del precio. Hoy en día, encontrar una unidad totalmente original es casi imposible y valen fortunas.""",
                "url": "https://upload.wikimedia.org/wikipedia/commons/6/61/Toyota_Supra_MkIV_white.jpg",
                "engine": "3.0L 2JZ-GTE Twin-Turbo",
                "hp": 320,
                "top": 250,
                "acc": 4.6,
                "w": 1510,
            },
            {
                "name": "Dodge Viper GTS",
                "year": 1996,
                "cat": "Muscle Car",
                "desc": """FUERZA BRUTA AMERICANA:
El Viper fue la respuesta moderna al Shelby Cobra: un chasis ligero con un motor monstruosamente grande. De hecho, su motor V10 de 8.0 litros fue desarrollado originalmente por Chrysler para camionetas pickup, pero Lamborghini (entonces propiedad de Chrysler) ayudó a fundirlo en aluminio para este deportivo.

PELIGROSO:
Es conocido como "el coche que quiere matarte". No tiene control de tracción, ni control de estabilidad, ni frenos ABS (en sus primeras versiones). Es pura potencia mecánica a las ruedas traseras.

DISEÑO:
La versión GTS introdujo el techo de "doble burbuja", diseñado para que los pilotos pudieran usar casco cómodamente. Sus franjas blancas sobre pintura azul son una de las decoraciones más icónicas de la historia del automovilismo americano.""",
                "url": "https://upload.wikimedia.org/wikipedia/commons/0/02/Dodge_Viper_GTS_Coupe_Blue.jpg",
                "engine": "8.0L V10",
                "hp": 450,
                "top": 290,
                "acc": 4.0,
                "w": 1500,
            },
        ]

        # --- AÑADIENDO EL RESTO PARA LLEGAR A 50 (Versiones Resumidas pero Completas) ---
        # Para no hacer el script de 2000 líneas, generamos el resto con un bucle de datos
        otros_coches = [
            {
                "n": "Mercedes 300 SL",
                "y": 1954,
                "c": "Classic",
                "hp": 215,
                "desc": "El 'Alas de Gaviota'. Primer superdeportivo de la historia con inyección directa. Una obra de arte de la ingeniería alemana.",
            },
            {
                "n": "Aston Martin DB5",
                "y": 1964,
                "c": "Classic",
                "hp": 282,
                "desc": "El coche de James Bond. Elegancia británica atemporal. Famoso por sus gadgets en la gran pantalla y su clase en la carretera.",
            },
            {
                "n": "Shelby Cobra 427",
                "y": 1965,
                "c": "Muscle",
                "hp": 425,
                "desc": "Chasis británico AC Ace con un V8 Ford masivo. La definición de relación peso/potencia absurda. Aceleraba de 0 a 100 más rápido que muchos coches modernos.",
            },
            {
                "n": "Ford GT40",
                "y": 1966,
                "c": "Le Mans",
                "hp": 485,
                "desc": "Nacido de la venganza de Ford contra Ferrari. Logró un histórico 1-2-3 en Le Mans 66, rompiendo la hegemonía italiana.",
            },
            {
                "n": "Porsche 959",
                "y": 1986,
                "c": "Supercar",
                "hp": 450,
                "desc": "El coche más tecnológico de los 80. Introdujo el sistema de tracción total moderno y suspensión adaptativa. Originalmente pensado para el Grupo B.",
            },
            {
                "n": "Honda NSX-R",
                "y": 1992,
                "c": "JDM",
                "hp": 280,
                "desc": "Puesto a punto por Ayrton Senna. El primer superdeportivo de aluminio fiable y utilizable a diario. Cambió el estándar de calidad de Ferrari y Lamborghini.",
            },
            {
                "n": "Lexus LFA",
                "y": 2010,
                "c": "Supercar",
                "hp": 560,
                "desc": "Una obra maestra de fibra de carbono que tardó 10 años en desarrollarse. Su motor V10 Yamaha sube de vueltas tan rápido que necesita un tacómetro digital.",
            },
            {
                "n": "Pagani Zonda",
                "y": 1999,
                "c": "Hypercar",
                "hp": 555,
                "desc": "El sueño de Horacio Pagani. Artesanía italiana con corazón Mercedes AMG. Cada tornillo es una pieza de joyería.",
            },
            {
                "n": "Koenigsegg Agera RS",
                "y": 2015,
                "c": "Hypercar",
                "hp": 1160,
                "desc": "El coche que batió el récord de velocidad en carretera pública en Nevada (447 km/h). Ingeniería sueca sin compromisos.",
            },
            {
                "n": "Lamborghini Countach",
                "y": 1974,
                "c": "Classic",
                "hp": 375,
                "desc": "El diseño de cuña que definió los años 70 y 80. Sus puertas de tijera y su forma extrema lo convirtieron en el póster de habitación de toda una generación.",
            },
            {
                "n": "Lamborghini Miura",
                "y": 1966,
                "c": "Classic",
                "hp": 350,
                "desc": "El padre de los superdeportivos modernos. Fue el primero en colocar el motor V12 en posición central trasera. Bellísimo y peligroso.",
            },
            {
                "n": "Jaguar E-Type",
                "y": 1961,
                "c": "Classic",
                "hp": 265,
                "desc": "Enzo Ferrari lo llamó 'el coche más bello del mundo'. Un icono de los años 60 que combinaba altas prestaciones con un precio accesible.",
            },
            {
                "n": "Toyota 2000GT",
                "y": 1967,
                "c": "Classic",
                "hp": 150,
                "desc": "El primer supercoche japonés. Desarrollado con Yamaha, demostró al mundo que Japón podía hacer coches deportivos de clase mundial.",
            },
            {
                "n": "BMW M3 E30",
                "y": 1986,
                "c": "Classic",
                "hp": 200,
                "desc": "Nacido para homologar el coche de carreras del DTM. Es considerado uno de los mejores chasis de la historia por su equilibrio y pureza.",
            },
            {
                "n": "Porsche Carrera GT",
                "y": 2004,
                "c": "Supercar",
                "hp": 612,
                "desc": "Motor V10 derivado de la F1, cambio manual y embrague cerámico. Uno de los últimos superdeportivos analógicos verdaderos.",
            },
            {
                "n": "Ferrari LaFerrari",
                "y": 2013,
                "c": "Hypercar",
                "hp": 963,
                "desc": "El primer híbrido de Ferrari. Parte de la 'Santa Trinidad'. Usa tecnología KERS de la F1 para apoyar a su V12 atmosférico.",
            },
            {
                "n": "McLaren F1",
                "y": 1992,
                "c": "Supercar",
                "hp": 627,
                "desc": "El coche más rápido del mundo durante una década. Asiento central, motor BMW V12 recubierto de oro. La perfección técnica.",
            },
            {
                "n": "Alfa Romeo 33 Stradale",
                "y": 1967,
                "c": "Classic",
                "hp": 230,
                "desc": "Posiblemente el coche más bonito jamás dibujado. Un coche de carreras matriculable, curvoso, pequeño y extremadamente caro en su época.",
            },
            {
                "n": "Lancia Delta Integrale",
                "y": 1991,
                "c": "Rally",
                "hp": 215,
                "desc": "La evolución final del coche más exitoso del WRC. Ensanchado, turboalimentado y con tracción total. Un icono italiano.",
            },
            {
                "n": "Peugeot 205 T16",
                "y": 1984,
                "c": "Rally",
                "hp": 200,
                "desc": "Motor central y tracción total en un cuerpo que parecía un utilitario. La base del coche que dominó el Grupo B y el Dakar.",
            },
            {
                "n": "Ford Escort Cosworth",
                "y": 1992,
                "c": "Rally",
                "hp": 227,
                "desc": "Famoso por su alerón 'cola de ballena'. Era un coche de rally del Grupo A disfrazado de coche de calle.",
            },
            {
                "n": "Mitsubishi Evo VI",
                "y": 1999,
                "c": "JDM",
                "hp": 280,
                "desc": "La edición Tommi Mäkinen. Tracción total avanzada y una agilidad increíble en cualquier terreno.",
            },
            {
                "n": "Renault 5 Turbo",
                "y": 1980,
                "c": "Rally",
                "hp": 160,
                "desc": "Renault cogió su coche urbano, le puso el motor en el asiento de atrás y lo ensanchó desproporcionadamente. Una locura genial.",
            },
            {
                "n": "Alpine A110",
                "y": 1971,
                "c": "Rally",
                "hp": 140,
                "desc": "La Berlinette. Pequeño, ligero y ágil. Dominó los primeros años del campeonato internacional de rallys.",
            },
            {
                "n": "Lotus Elise S1",
                "y": 1996,
                "c": "Sport",
                "hp": 118,
                "desc": "'Menos es más'. Chasis de aluminio pegado, peso pluma (725kg). Ofrece una conexión con la carretera que pocos coches igualan.",
            },
            {
                "n": "Mazda MX-5 NA",
                "y": 1989,
                "c": "Classic",
                "hp": 115,
                "desc": "El coche que salvó a los roadsters. Fiabilidad japonesa con espíritu británico. Faros retráctiles y diversión pura.",
            },
            {
                "n": "Honda S2000",
                "y": 1999,
                "c": "JDM",
                "hp": 240,
                "desc": "El regalo de 50 cumpleaños de Honda. Su motor VTEC corta a 9000 rpm, ofreciendo una de las mejores cajas de cambios manuales.",
            },
            {
                "n": "Toyota AE86",
                "y": 1983,
                "c": "JDM",
                "hp": 130,
                "desc": "El Hachi-Roku. Leyenda del drift y del anime Initial D. Ligero, tracción trasera y perfecto para aprender a conducir.",
            },
            {
                "n": "Nissan 240Z",
                "y": 1969,
                "c": "Classic",
                "hp": 150,
                "desc": "El coche que puso a los deportivos japoneses en el mapa global. Bonito, rápido y fiable. Un clásico instantáneo.",
            },
            {
                "n": "Chevrolet Corvette C2",
                "y": 1963,
                "c": "Muscle",
                "hp": 360,
                "desc": "El Sting Ray. Famoso por su ventana trasera partida (Split Window) de 1963. Diseño inspirado en la vida marina.",
            },
            {
                "n": "Ford Mustang 1967",
                "y": 1967,
                "c": "Muscle",
                "hp": 320,
                "desc": "El Fastback. Icono de Bullitt. Definió la estética del muscle car americano junto al Camaro.",
            },
            {
                "n": "Pontiac GTO",
                "y": 1964,
                "c": "Muscle",
                "hp": 325,
                "desc": "Considerado por muchos el primer Muscle Car. Motor grande en coche mediano a precio bajo. Creó una tendencia.",
            },
            {
                "n": "Plymouth Superbird",
                "y": 1970,
                "c": "Muscle",
                "hp": 425,
                "desc": "Diseñado para NASCAR con un alerón trasero gigantesco y morro aerodinámico. Inconfundible y hoy en día muy valioso.",
            },
            {
                "n": "Mercedes CLK GTR",
                "y": 1998,
                "c": "Supercar",
                "hp": 600,
                "desc": "Un coche de carreras GT1 que aterrizó en la calle por obligación del reglamento. Extremadamente ancho, bajo y caro.",
            },
            {
                "n": "Porsche 911 GT1",
                "y": 1997,
                "c": "Supercar",
                "hp": 536,
                "desc": "La respuesta de Porsche al McLaren F1 y al CLK GTR. Un 911 mutado con motor central para ganar Le Mans.",
            },
            {
                "n": "Toyota GT-One",
                "y": 1998,
                "c": "Le Mans",
                "hp": 600,
                "desc": "Diseñado al límite del reglamento. Prácticamente un prototipo pintado de calle. Solo se hicieron 2 unidades de carretera.",
            },
            {
                "n": "Sauber C9",
                "y": 1989,
                "c": "Le Mans",
                "hp": 720,
                "desc": "La flecha de plata del Grupo C. Alcanzó los 400 km/h en Mulsanne. Potencia bruta de Mercedes V8 Turbo.",
            },
            {
                "n": "Jaguar XJ220",
                "y": 1992,
                "c": "Supercar",
                "hp": 542,
                "desc": "Iba a tener un V12, pero llegó con un V6 Turbo. A pesar de la decepción, fue el coche más rápido del mundo brevemente (342 km/h).",
            },
        ]

        print(f"⬇️  Completando el garaje hasta 50 vehículos...")

        # 3. GUARDAR LOS DETALLADOS
        count = 0
        for car in flota:
            count += 1
            safe_name = (
                car["name"]
                .lower()
                .replace(" ", "_")
                .replace("-", "_")
                .replace("/", "_")
                + ".jpg"
            )
            ruta_img = descargar_imagen(car["url"], safe_name)
            marca = car["name"].split(" ")[0]

            nuevo = Vehicle(
                name=car["name"],
                image=ruta_img,
                description=car["desc"],
                manufacturer=marca,
                year=car["year"],
                category=car["cat"],
                engine=car["engine"],
                horsepower=car["hp"],
                top_speed=car["top"],
                acceleration=car["acc"],
                weight=car["w"],
            )
            db.session.add(nuevo)
            print(f"   [{count}] ⭐ {car['name']} (Detallado)")

        # 4. GUARDAR LOS RESUMIDOS (Rellenando datos faltantes con genéricos para no fallar)
        for car in otros_coches:
            count += 1
            safe_name = car["n"].lower().replace(" ", "_") + ".jpg"
            # Usamos una imagen genérica o intentamos buscarla (aquí simplificado para no alargar el script infinito)
            # Si quieres fotos reales para estos también, habría que buscar URLs para cada uno.
            # Para este ejemplo, usaremos el placeholder si no tienes la URL en la lista de arriba.

            desc_larga = f"""HISTORIA RESUMIDA:
{car['desc']}

Este vehículo es un icono de su categoría ({car['c']}) y representa un hito en la ingeniería automotriz del año {car['y']}."""

            nuevo = Vehicle(
                name=car["n"],
                image="img/default_car.jpg",
                description=desc_larga,
                manufacturer=car["n"].split(" ")[0],
                year=car["y"],
                category=car["c"],
                engine="N/A",
                horsepower=car["hp"],
                top_speed=0,
                acceleration=0.0,
                weight=0,
            )
            db.session.add(nuevo)
            print(f"   [{count}] 🔹 {car['n']} (Añadido)")

        db.session.commit()
        print("\n🏁 ¡ENCICLOPEDIA COMPLETADA! 50 Vehículos listos.")


if __name__ == "__main__":
    cargar_garaje_masivo()
