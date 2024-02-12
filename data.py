import pandas as pd
from pymongo import MongoClient

# Reemplaza 'usuario' y 'contraseña' con tus credenciales de MongoDB Atlas
cadena_conexion = f"mongodb+srv://admin2:211024@proyect1.eolzon9.mongodb.net/"

# Conectar a MongoDB Atlas
client = MongoClient(cadena_conexion)

# Conectar a MongoDB Atlas
db = client["Lab03"]
collection = db["movies"]

# Cargar datos desde el archivo .csv
data = pd.read_csv("CCGeneral1.csv")

# Convertir el DataFrame a formato JSON
data_json = data.to_dict(orient='records')

# Insertar los datos en MongoDB Atlas
collection.insert_many(data_json)

# Cerrar la conexión
client.close()