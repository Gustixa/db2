from pymongo import MongoClient
from bson import ObjectId
import random
from faker import Faker
from datetime import datetime

# Conexión a la base de datos
client = MongoClient('mongodb+srv://admin2:211024@proyect1.eolzon9.mongodb.net/')
db = client['Proyecto_1']

fake = Faker()

# Insertar datos falsos en la colección Géneros Cinematográficos
generos_ids = []
for _ in range(20):
    genero = {"nombre_genero": fake.word()}
    genero_id = db.generos_cinematograficos.insert_one(genero).inserted_id
    generos_ids.append(genero_id)

# Insertar datos falsos en la colección Actores
actores_ids = []
for _ in range(200):
    actor = {
        "nombre": fake.name(),
        "fecha_nacimiento": fake.date_of_birth().strftime("%Y-%m-%d"),
        "nacionalidad": fake.country()
    }
    actor_id = db.actores.insert_one(actor).inserted_id
    actores_ids.append(actor_id)

# Insertar datos falsos en la colección Taquilla
taquilla = {
    "ingresos": random.randint(1000000, 10000000),
    "fecha_recaudacion": fake.date()
}
taquilla_id = db.taquilla.insert_one(taquilla).inserted_id

# Insertar datos falsos en la colección Reseñas
resenas_ids = []
for _ in range(200):
    resena = {
        "comentario": fake.text(),
        "calificacion": random.randint(1, 5),
        "fecha_resena": fake.date()
    }
    resena_id = db.resenas.insert_one(resena).inserted_id
    resenas_ids.append(resena_id)

# Insertar datos falsos en la colección Premios
premios_ids = []
for _ in range(100):
    premio = {
        "nombre_premio": fake.word(),
        "anno": fake.year(),
        "categoria": fake.word()
    }
    premio_id = db.premios.insert_one(premio).inserted_id
    premios_ids.append(premio_id)

# Insertar datos falsos en la colección Staff de Producción
staff_ids = []
for _ in range(100):
    staff = {
        "nombre": fake.name(),
        "cargo": fake.word()
    }
    staff_id = db.staff_produccion.insert_one(staff).inserted_id
    staff_ids.append(staff_id)

# Insertar datos falsos en la colección Casas Productoras
casas_productoras_ids = []
for _ in range(50):
    casa_productora = {
        "nombre": fake.company(),
        "pais": fake.country(),
        "anio_fundacion": fake.year()
    }
    casa_productora_id = db.casas_productoras.insert_one(casa_productora).inserted_id
    casas_productoras_ids.append(casa_productora_id)
# Insertar datos falsos en la colección Películas utilizando referencias
for _ in range(1000):
    es_cartelera = random.choice([True, False])  # Indica si la película está en la cartelera
    pelicula = {
        "titulo": fake.text(20),
        "genero": random.choice(generos_ids),
        "director": fake.name(),
        "anio_lanzamiento": fake.year(),
        "sinopsis": fake.text(),
        "clasificacion_edad": random.choice(["PG", "PG-13", "R"]),
        "actores": random.sample(actores_ids, random.randint(3, 5)),
        "taquilla": taquilla_id,
        "resenas": random.sample(resenas_ids, random.randint(1, 3)),
        "premios": random.sample(premios_ids, random.randint(1, 3)),
        "staff_produccion": random.sample(staff_ids, random.randint(1, 5)),
        "casa_productora": random.choice(casas_productoras_ids),  # Referencia a una casa productora
        "en_cartelera": es_cartelera
    }
    db.peliculas.insert_one(pelicula)

# Cerrar la conexión
client.close()
