#LIBRARIES
from faker import Faker
import random
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector 
from mysql.connector import Error
import streamlit as st
from datetime import datetime, timedelta

#PAGE CONFIG PARAMETERS
st.set_page_config(layout="centered")

#EASY LOGO AND TITLE
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.image("https://maia.run/wp-content/uploads/2022/12/Emblema-MAIA-DIAPO-BLANCO-RGB-150x150.png", width = 101)
with col3:
    st.write(' ')
st.title('Dato sintético APP')


#LOAD PIXABAY DATA FOR REALISTIC IDS AND IMAGES
@st.cache_data
def load_pixabay_data():
    try:
        pixabay_df = pd.read_csv('publicaciones_pixabay.csv')
        return pixabay_df[['ID_Publicacion', 'Imagen']].values.tolist()
    except FileNotFoundError:
        st.warning("CSV de Pixabay no encontrado. Usando datos sintéticos genéricos.")
        return []

pixabay_data = load_pixabay_data()

#DATE CONFIGURATION (1 AGOSTO 2024 - 1 AGOSTO 2025)
fecha_inicio = datetime(2024, 8, 1)
fecha_fin = datetime(2025, 8, 1)

#FAKE ID'S CREATION
fake = Faker()
data = []
numbers= st.number_input("Number of data needed? Press enter to apply",min_value=0, max_value=10000000,step=1)

for i in range(0, numbers):
    # Seleccionar aleatoriamente un par ID-Imagen del CSV de Pixabay
    if pixabay_data:
        random_post = random.choice(pixabay_data)
        post_id = random_post[0]  # ID_Publicacion del CSV
        imagen_nombre = random_post[1]  # Imagen del CSV
    else:
        # Fallback si no hay datos de Pixabay
        post_id = fake.uuid4()
        imagen_nombre = fake.image_url()
    
    # Generar fecha aleatoria entre 1 agosto 2024 y 1 agosto 2025
    fecha_aleatoria = fake.date_between(start_date=fecha_inicio, end_date=fecha_fin)
    
    # Seleccionar formato primero para determinar métricas específicas
    formato = fake.random_element(elements=('Imagen', 'Carrusel', 'Reel'))
    
    # Determinar métricas según el formato
    if formato in ['Imagen', 'Carrusel']:
        # Para imágenes y carruseles: sin datos de video
        reproducciones = 'Sin datos'
        duracion_video = 'Sin datos'
        retencion = 'Sin datos'
    else:  # Reel
        # Para reels: métricas de video
        reproducciones = fake.random_int(min=50, max=10000)
        duracion_video = fake.random_int(min=15, max=300)
        retencion = round(fake.random.uniform(0.1, 1.0), 2)
    
    data.append({
        'id_post': post_id,
        'Fecha': fecha_aleatoria.strftime('%Y-%m-%d'),
        'Hora': fake.time(),
        'Canal': fake.random_element(elements=('Instagram', 'TikTok', 'Facebook', 'Twitter')),
        'Formato': formato,
        'Imagen': imagen_nombre, 
        'Alcance': fake.random_int(min=100, max=50000),
        'Interacciones': fake.random_int(min=10, max=5000),
        'Reproducciones': reproducciones,
        'Duracion_video': duracion_video,
        'DM': fake.random_int(min=0, max=100),
        'Retencion' : retencion,
        'Visitas_perfil' : fake.random_int(min=5, max=500),
        'Link_bio' : fake.random_int(min=0, max=50),
        'Visitas_producto' : fake.random_int(min=0, max=200),
        'Carrito': fake.random_int(min=0, max=50),
        'Compras': fake.random_int(min=0, max=20),
        'Valor_compra': round(fake.random.uniform(10.0, 500.0), 2),
        'Contacto': fake.random_int(min=0, max=10),
        'Inversion': 0 if fake.boolean(chance_of_getting_true=30) else round(fake.random.uniform(50.0, 1000.0), 2),
        'ROI': round(fake.random.uniform(0.5, 5.0), 2),
        'Engagement': round(fake.random.uniform(0.01, 0.15), 3),
        'CPC': round(fake.random.uniform(0.1, 2.0), 2),
        }) 
    
    
#FAKE DF CREATION
count = numbers
st.dataframe(data[:count])
df = pd.DataFrame(data[:count])

#OPTION TO DOWNLOAD DATAFRAME IN CSV
st.subheader('Download the table')
csv_download = st.button("Create your DATA")
if csv_download:
    output = df.to_csv(index_label = False) 
    st.download_button(
        label = "Download CSV file", 
        data = output, 
        file_name = "data.csv",
        mime = "text/csv"
        )
    
#DB INPUTS
st.title("Database Connection")
host = st.text_input("Host: ")
database = st.text_input("Database: ")
user = st.text_input("User: ")
password = st.text_input("Password: ")

#BUTTON CHECKER 
if st.button("Connect"):
    try:
        connection = mysql.connector.connect(host=host, database=database, user=user, password=password, connection_timeout=180)
        cursor=connection.cursor()
        st.success("You are now connected to the database!")
    except:
        st.write("Conection dont stabilished, verify the information, database is running?")

#TABLE CREATION
tablename = st.text_input("Enter Table Name to create")
if st.button('Create Table'):
	st.write('Table Created Successfully')
	testDF = """CREATE TABLE IF NOT EXISTS {} (    name VARCHAR(255),	email VARCHAR(255),	address VARCHAR(255),	phone_number VARCHAR(16),	city VARCHAR(255),	state VARCHAR(255),	zip_code VARCHAR(16),	job VARCHAR(255),	card_number VARCHAR(64),	card_ssn VARCHAR(32),	score SMALLINT,	transaction_date DATETIME,	bank_name VARCHAR(64))""".format(tablename)
	connection = mysql.connector.connect(host=host, database=database, user=user, password=password, connection_timeout=180)
	cursor=connection.cursor()
	cursor.execute(testDF)
	connection.commit()

#DF TO SQL
def sql_df_upload(df):
    connection = mysql.connector.connect(host=host, database=database, user=user, password=password, connection_timeout=180)
    cursor=connection.cursor()     
    for index, row in df.iterrows():
        sql = "INSERT INTO {} (id_post, Fecha, Hora, Canal, Formato, Imagen, Alcance, Interacciones, Reproducciones, Duracion_video, DM, Retencion, Visitas_perfil, Link_bio, Visitas_producto, Carrito, Compras, Valor_compra, Contacto, Inversion, ROI, Engagement, CPC) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" .format(tablename)
        cursor.execute(sql, tuple(row))
        connection.commit()
    connection.close()
    print("Upload complete")

#BUTTON TO PUSH TO SQL
st.text("Push ur Data to the Table on the db")
if st.button("Push to DB"):
    sql_df_upload(df)
    st.success('Upload to DB complete!')

#Prueba
