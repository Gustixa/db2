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
        "fecha_resena": fake.date(),
        "usuario": fake.user_name()  # Añadido el nombre de usuario a la reseña
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

# Insertar datos falsos en la colección Usuarios
usuarios_ids = []
for _ in range(50):
    usuario_tipo = random.choice(['administrador', 'usuario_comun'])
    usuario = {
        "nombre_usuario": fake.user_name(),
        "contrasena": fake.password(),
        "correo": fake.email(),
        "fecha_creacion": fake.date(),
        "fecha_actualizacion": fake.date(),
        "tipo": usuario_tipo  # Campo que indica si es administrador o usuario común
    }
    usuario_id = db.usuarios.insert_one(usuario).inserted_id
    usuarios_ids.append(usuario_id)

# Insertar datos falsos en la colección Películas utilizando referencias
for _ in range(1000):
    es_cartelera = random.choice([True, False])  # Indica si la película está en la cartelera
    num_actores = random.randint(3, 5)
    
    # Seleccionar actores al azar
    actores_seleccionados = random.sample(actores_ids, num_actores)
    
    # Seleccionar usuario al azar para la reseña
    usuario_resena = random.choice(usuarios_ids)
    
    # Insertar la película con reseña embebida
    pelicula = {
        "titulo": fake.text(20),
        "genero": random.choice(generos_ids),
        "director": fake.name(),
        "anio_lanzamiento": fake.year(),
        "sinopsis": fake.text(),
        "clasificacion_edad": random.choice(["PG", "PG-13", "R"]),
        "actores": actores_seleccionados,
        "taquilla": taquilla_id,
        "resenas": {
            "comentario": fake.text(),
            "calificacion": random.randint(1, 5),
            "fecha_resena": fake.date(),
            "usuario": usuario_resena
        },
        "premios": random.sample(premios_ids, random.randint(1, 3)),
        "staff_produccion": random.sample(staff_ids, random.randint(1, 5)),
        "casa_productora": random.choice(casas_productoras_ids),  # Referencia a una casa productora
        "en_cartelera": es_cartelera
    }
    
    pelicula_id = db.peliculas.insert_one(pelicula).inserted_id

    # Actualizar información de actores con las películas en las que participaron
    db.actores.update_many(
        {"_id": {"$in": actores_seleccionados}},
        {"$addToSet": {"peliculas_participadas": pelicula_id}}
    )

# Insertar datos falsos en la colección Proyecciones y actualizar información de películas con las proyecciones asociadas
proyecciones_ids = []
for _ in range(500):
    sala = fake.word()
    asientos_vendidos = random.randint(50, 200)
    dolares_recaudados = random.randint(5000, 20000)
    fecha_proyeccion = fake.date_time_this_year()

    # Seleccionar película al azar para la proyección
    pelicula_proyeccion = random.choice(list(db.peliculas.find({}, {"_id": 1})))
    
    # Insertar la proyección con referencia a la película
    proyeccion = {
        "sala": sala,
        "asientos_vendidos": asientos_vendidos,
        "dolares_recaudados": dolares_recaudados,
        "fecha_proyeccion": fecha_proyeccion,
        "pelicula": pelicula_proyeccion["_id"]
    }

    proyeccion_id = db.proyecciones.insert_one(proyeccion).inserted_id
    proyecciones_ids.append(proyeccion_id)

    # Actualizar información de películas con las proyecciones asociadas
    db.peliculas.update_one(
        {"_id": pelicula_proyeccion["_id"]},
        {"$addToSet": {"proyecciones": proyeccion_id}}
    )

# Cerrar la conexión
client.close()
