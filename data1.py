from pymongo import MongoClient
from bson import ObjectId
import random
from faker import Faker
from datetime import datetime

# Conexión a la base de datos
client = MongoClient('mongodb+srv://admin2:211024@proyect1.eolzon9.mongodb.net/')
db = client['Proyecto_1']

fake = Faker()

# Insertar datos falsos en la colección Películas
for _ in range(1000):  # Insertar 10 películas de ejemplo
    pelicula = {
        "titulo": fake.text(20),
        "genero": fake.word(),
        "director": fake.name(),
        "anio_lanzamiento": fake.year(),
        "sinopsis": fake.text(),
        "clasificacion_edad": random.choice(["PG", "PG-13", "R"]),
        "actores": [
            {
                "nombre": fake.name(),
                "fecha_nacimiento": fake.date_of_birth().strftime("%Y-%m-%d"),  # Convertir a cadena
                "nacionalidad": fake.country()
            }
            for _ in range(random.randint(3, 5))
        ],
        "taquilla": {
            "ingresos": random.randint(1000000, 10000000),
            "fecha_recaudacion": fake.date()
        },
        "resenas": [
            {
                "comentario": fake.text(),
                "calificacion": random.randint(1, 5),
                "fecha_resena": fake.date()
            }
            for _ in range(random.randint(1, 3))
        ],
        "premios": [
            {
                "nombre_premio": fake.word(),
                "anno": fake.year(),
                "categoria": fake.word(),
                "persona_ganadora": {
                    "nombre": fake.name(),
                    "cargo": fake.word()
                }
            }
            for _ in range(random.randint(1, 3))
        ],
        "staff_produccion": [
            {
                "nombre": fake.name(),
                "cargo": fake.word()
            }
            for _ in range(random.randint(1, 5))
        ]
    }
    db.peliculas.insert_one(pelicula)

# Insertar datos falsos en otras colecciones (Estudios de Cine, Géneros Cinematográficos, Usuarios, Funciones) de manera similar.
# ...

# Cerrar la conexión
client.close()
