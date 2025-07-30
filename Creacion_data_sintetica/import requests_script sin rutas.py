import requests
import os
import pandas as pd
import random
from datetime import datetime, timedelta
from uuid import uuid4

# CONFIGURA TU API KEY AQUÍ
API_KEY = '51425029-473b8fc89f2a01cd210f9fc88'

# Carpetas
IMAGES_DIR = 'imagenes_descargadas'
os.makedirs(IMAGES_DIR, exist_ok=True)

# Temáticas de búsqueda
tematicas = ['comida', 'viajes', 'moda', 'tecnología', 'mascotas', 'deporte', 'salud', 'educación', 'arte', 'naturaleza']

# Parámetros de búsqueda
NUM_IMAGENES = 200
IMAGENES_POR_TEMATICA = NUM_IMAGENES // len(tematicas)

datos = []

for tema in tematicas:
    print(f"Descargando imágenes de temática: {tema}")
    page = 1
    descargadas = 0

    while descargadas < IMAGENES_POR_TEMATICA:
        url = f"https://pixabay.com/api/?key={API_KEY}&q={tema}&image_type=photo&per_page=20&page={page}"
        response = requests.get(url)
        data = response.json()

        if 'hits' not in data or not data['hits']:
            break

        for hit in data['hits']:
            image_url = hit['webformatURL']
            post_id = str(uuid4())[:8]
            post_date = datetime.now() - timedelta(days=random.randint(0, 365))
            filename = f"{post_id}.jpg"
            image_path = os.path.join(IMAGES_DIR, filename)

            try:
                img_data = requests.get(image_url).content
                with open(image_path, 'wb') as handler:
                    handler.write(img_data)
                
                datos.append({
                    'ID_Publicacion': post_id,
                    'Fecha_Publicacion': post_date.strftime('%Y-%m-%d'),
                    'Imagen': filename
                })

                descargadas += 1
                if descargadas >= IMAGENES_POR_TEMATICA:
                    break
            except Exception as e:
                print(f"Error descargando imagen: {e}")

        page += 1

# Guardar CSV
df = pd.DataFrame(datos)
df.to_csv('publicaciones_pixabay.csv', index=False)
print("✅ Descarga completa. CSV generado como 'publicaciones_pixabay.csv'")
