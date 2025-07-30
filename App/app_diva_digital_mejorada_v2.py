import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Nuevas importaciones para análisis de imágenes
from PIL import Image
import colorsys
from sklearn.cluster import KMeans
import requests
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="Diva Digital - Análisis de Redes Sociales",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Definir variables de colores y rutas
PRIMARY_COLOR = "#8e24aa"
LOGO_PATH = "/Users/n.arcos89/Desktop/Bootcamp_Data/DIVA_DIGITAL_Proyecto Final/App/logo_diva_digital.png"

# --- ESTILOS PERSONALIZADOS MEJORADOS ---
page_bg = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary-purple: #6a1b9a;
    --secondary-purple: #8e24aa;
    --accent-pink: #e91e63;
    --light-pink: #f06292;
    --very-light-pink: #fce4ec;
    --dark-bg: #1a1626;
    --card-bg: rgba(26, 22, 38, 0.95);
    --text-primary: #ffffff;
    --text-secondary: #f8bbd0;
    --text-dark: #4a148c;
    --gradient-main: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 25%, #f48fb1 75%, #f06292 100%);
    --gradient-card: linear-gradient(145deg, rgba(142, 36, 170, 0.15) 0%, rgba(233, 30, 99, 0.08) 100%);
    --shadow-glow: 0 8px 32px rgba(142, 36, 170, 0.3);
    --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.1);
}

body {
    background: var(--very-light-pink);
    font-family: 'Poppins', sans-serif;
}

/* SIDEBAR CON FONDO ROSA */
.css-1d391kg {
    background: #f06292 !important;
}

/* Alternativa para versiones más recientes de Streamlit */
section[data-testid="stSidebar"] {
    background: #f06292 !important;
}

section[data-testid="stSidebar"] > div {
    background: #f06292 !important;
}

/* Texto del sidebar en blanco */
.css-1d391kg .markdown-text-container {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] .markdown-text-container {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] label {
    color: #ffffff !important;
    font-weight: 600;
}

section[data-testid="stSidebar"] .stSelectbox label {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] .stMultiSelect label {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] .stDateInput label {
    color: #ffffff !important;
}

/* ÁREA PRINCIPAL CON FONDO ROSA CLARO */
[data-testid="stAppViewContainer"] > .main {
    background: var(--gradient-main) !important;
    background-size: 400% 400%;
    animation: gradientShift 12s ease infinite;
    color: var(--text-dark);
    padding: 1rem;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Tipografía mejorada con colores oscuros para el fondo rosa */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Poppins', sans-serif !important;
    color: var(--text-dark) !important;
    font-weight: 700;
    letter-spacing: 0.5px;
}

h1 {
    font-size: 2.5rem !important;
    background: linear-gradient(45deg, #4a148c, #6a1b9a);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

h2 {
    font-size: 2rem !important;
    color: var(--primary-purple) !important;
}

h3, h4 {
    color: var(--text-dark) !important;
    font-weight: 600;
}

/* Métricas mejoradas con fondo blanco semitransparente */
[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.8) !important;
    border: 1px solid rgba(142, 36, 170, 0.3);
    border-radius: 15px;
    padding: 1.2rem;
    backdrop-filter: blur(15px);
    box-shadow: var(--shadow-card);
    transition: all 0.3s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(142, 36, 170, 0.2);
    border-color: rgba(142, 36, 170, 0.6);
    background: rgba(255, 255, 255, 0.95) !important;
}

[data-testid="metric-container"] [data-testid="metric-value"] {
    color: var(--text-dark) !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
    font-family: 'Poppins', sans-serif !important;
}

[data-testid="metric-container"] [data-testid="metric-label"] {
    color: var(--primary-purple) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Estilos para el logo en la cabecera */
.header-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
}

.logo-container {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    padding: 1rem;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(142, 36, 170, 0.3);
    box-shadow: 0 8px 25px rgba(142, 36, 170, 0.2);
}

/* Cajas de información y warnings con mejor contraste */
.stInfo {
    background-color: rgba(255, 255, 255, 0.9) !important;
    color: var(--text-dark) !important;
    border-left: 4px solid #2196F3 !important;
}

.stWarning {
    background-color: rgba(255, 255, 255, 0.9) !important;
    color: var(--text-dark) !important;
    border-left: 4px solid #FF9800 !important;
}

.stSuccess {
    background-color: rgba(255, 255, 255, 0.9) !important;
    color: var(--text-dark) !important;
    border-left: 4px solid #4CAF50 !important;
}

.stError {
    background-color: rgba(255, 255, 255, 0.9) !important;
    color: var(--text-dark) !important;
    border-left: 4px solid #F44336 !important;
}

/* Texto general de la aplicación */
.main .markdown-text-container {
    color: var(--text-dark) !important;
}

.main p {
    color: var(--text-dark) !important;
}

/* Botones con estilo personalizado */
.stButton > button {
    background: linear-gradient(45deg, #8e24aa, #ab47bc) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(45deg, #6a1b9a, #8e24aa) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(142, 36, 170, 0.3) !important;
}
</style>
"""

# Aplicar estilos
st.markdown(page_bg, unsafe_allow_html=True)

# --- FUNCIONES DE ANÁLISIS DE IMÁGENES ---
@st.cache_data
def analizar_imagen_completo(imagen_path_o_url):
    """
    Análisis completo de imagen usando PIL y Computer Vision
    """
    try:
        # Cargar imagen desde URL o archivo local
        if isinstance(imagen_path_o_url, str) and imagen_path_o_url.startswith('http'):
            response = requests.get(imagen_path_o_url, timeout=10)
            img = Image.open(BytesIO(response.content))
        elif hasattr(imagen_path_o_url, 'read'):
            # Es un archivo subido
            img = Image.open(imagen_path_o_url)
        else:
            # Es una ruta local
            img = Image.open(imagen_path_o_url)
        
        # Convertir a RGB si es necesario
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 1. ANÁLISIS DE COLORES DOMINANTES
        colores_dominantes = extraer_colores_dominantes(img)
        
        # 2. ANÁLISIS DE CARACTERÍSTICAS VISUALES
        caracteristicas = analizar_caracteristicas_visuales(img)
        
        # 3. CLASIFICACIÓN DE TEMÁTICA
        tematica_predicha = clasificar_tematica_imagen(caracteristicas, colores_dominantes)
        
        # 4. SCORE DE ENGAGEMENT PREDICHO
        engagement_score = predecir_engagement_visual(caracteristicas, colores_dominantes)
        
        return {
            'exito': True,
            'colores_dominantes': colores_dominantes,
            'caracteristicas': caracteristicas,
            'tematica_predicha': tematica_predicha,
            'engagement_score': engagement_score,
            'recomendaciones': generar_recomendaciones_visuales(caracteristicas, colores_dominantes)
        }
        
    except Exception as e:
        return {'exito': False, 'error': str(e)}

def extraer_colores_dominantes(img, n_colores=5):
    """
    Extrae los colores dominantes usando K-means
    """
    # Redimensionar para acelerar procesamiento
    img_small = img.resize((150, 150))
    
    # Convertir a array numpy
    img_array = np.array(img_small)
    pixels = img_array.reshape(-1, 3)
    
    # K-means clustering
    kmeans = KMeans(n_clusters=n_colores, random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    colores = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    counts = np.bincount(labels)
    percentages = counts / len(labels) * 100
    
    resultado_colores = []
    for i, (color, porcentaje) in enumerate(zip(colores, percentages)):
        r, g, b = color
        resultado_colores.append({
            'rgb': (int(r), int(g), int(b)),
            'hex': f'#{r:02x}{g:02x}{b:02x}',
            'porcentaje': float(porcentaje),
            'nombre': obtener_nombre_color(r, g, b)
        })
    
    # Ordenar por porcentaje
    resultado_colores.sort(key=lambda x: x['porcentaje'], reverse=True)
    return resultado_colores

def analizar_caracteristicas_visuales(img):
    """
    Analiza características visuales de la imagen
    """
    # Información básica
    ancho, alto = img.size
    
    # Color promedio
    img_1x1 = img.resize((1, 1))
    color_promedio = img_1x1.getpixel((0, 0))
    
    # Análisis de brillo
    brillo = sum(color_promedio) / (3 * 255)
    
    # Análisis de contraste (usando desviación estándar)
    img_gray = img.convert('L')
    img_array = np.array(img_gray)
    contraste = np.std(img_array) / 128.0
    
    # Análisis de saturación
    r, g, b = color_promedio
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    
    # Análisis de complejidad visual
    complejidad = calcular_complejidad_visual(img)
    
    return {
        'dimensiones': (ancho, alto),
        'aspecto_ratio': ancho / alto,
        'brillo': brillo,
        'contraste': contraste,
        'saturacion': s,
        'complejidad': complejidad,
        'color_dominante': determinar_color_dominante(r, g, b),
        'tipo_brillo': clasificar_brillo(brillo),
        'tipo_contraste': clasificar_contraste(contraste)
    }

def calcular_complejidad_visual(img):
    """
    Calcula la complejidad visual basada en bordes detectados
    """
    try:
        # Convertir a escala de grises y array numpy
        img_gray = img.convert('L')
        img_array = np.array(img_gray)
        
        # Detectar bordes usando gradiente
        grad_x = np.abs(np.diff(img_array, axis=1))
        grad_y = np.abs(np.diff(img_array, axis=0))
        
        # Calcular complejidad como densidad de bordes
        complejidad = (np.sum(grad_x) + np.sum(grad_y)) / (img_array.size)
        
        return min(complejidad / 50, 1.0)  # Normalizar entre 0-1
    except:
        return 0.5  # Valor por defecto

def obtener_nombre_color(r, g, b):
    """Determina el nombre del color basado en RGB"""
    colores = {
        'rojo': (r > 150 and g < 100 and b < 100),
        'verde': (g > 150 and r < 100 and b < 100),
        'azul': (b > 150 and r < 100 and g < 100),
        'amarillo': (r > 200 and g > 200 and b < 100),
        'naranja': (r > 200 and g > 100 and g < 200 and b < 100),
        'rosa': (r > 200 and g > 150 and b > 150),
        'morado': (r > 100 and g < 100 and b > 150),
        'blanco': (r > 200 and g > 200 and b > 200),
        'negro': (r < 50 and g < 50 and b < 50),
        'gris': (abs(r-g) < 30 and abs(g-b) < 30 and abs(r-b) < 30)
    }
    
    for nombre, condicion in colores.items():
        if condicion:
            return nombre
    return 'neutro'

def determinar_color_dominante(r, g, b):
    """Determina el color dominante principal"""
    if r > max(g, b) + 20:
        return 'rojizo'
    elif g > max(r, b) + 20:
        return 'verdoso'
    elif b > max(r, g) + 20:
        return 'azulado'
    else:
        return 'neutro'

def clasificar_brillo(brillo):
    """Clasifica el nivel de brillo"""
    if brillo > 0.8:
        return 'muy_claro'
    elif brillo > 0.6:
        return 'claro'
    elif brillo > 0.4:
        return 'medio'
    elif brillo > 0.2:
        return 'oscuro'
    else:
        return 'muy_oscuro'

def clasificar_contraste(contraste):
    """Clasifica el nivel de contraste"""
    if contraste > 0.7:
        return 'alto'
    elif contraste > 0.4:
        return 'medio'
    else:
        return 'bajo'

def clasificar_tematica_imagen(caracteristicas, colores):
    """
    Clasifica la temática de la imagen basada en características visuales
    """
    # Reglas de clasificación basadas en características
    brillo = caracteristicas['brillo']
    saturacion = caracteristicas['saturacion']
    complejidad = caracteristicas['complejidad']
    color_dominante = caracteristicas['color_dominante']
    
    # Colores predominantes
    colores_principales = [c['nombre'] for c in colores[:3]]
    
    # Lógica de clasificación
    if 'rosa' in colores_principales or 'morado' in colores_principales:
        if brillo > 0.6:
            return 'moda_lifestyle'
        else:
            return 'arte_diseño'
    
    elif 'verde' in colores_principales or 'azul' in colores_principales:
        if complejidad < 0.3:
            return 'naturaleza_bienestar'
        else:
            return 'tecnologia'
    
    elif 'amarillo' in colores_principales or 'naranja' in colores_principales:
        return 'comida_gastronomia'
    
    elif brillo > 0.7 and saturacion > 0.5:
        return 'lifestyle_inspiracional'
    
    elif complejidad > 0.6:
        return 'arte_diseño'
    
    else:
        return 'general'

def predecir_engagement_visual(caracteristicas, colores):
    """
    Predice el score de engagement basado en características visuales
    """
    score = 0.5  # Base score
    
    # Factores que aumentan engagement
    brillo = caracteristicas['brillo']
    saturacion = caracteristicas['saturacion']
    contraste = caracteristicas['contraste']
    complejidad = caracteristicas['complejidad']
    
    # Brillo óptimo (ni muy oscuro ni muy claro)
    if 0.3 <= brillo <= 0.8:
        score += 0.1
    
    # Saturación alta aumenta engagement
    if saturacion > 0.4:
        score += 0.15
    
    # Contraste medio-alto es mejor
    if contraste > 0.3:
        score += 0.1
    
    # Complejidad moderada es óptima
    if 0.2 <= complejidad <= 0.6:
        score += 0.1
    
    # Colores que funcionan bien en redes sociales
    colores_engagement = ['rosa', 'azul', 'verde', 'amarillo']
    if any(c['nombre'] in colores_engagement for c in colores[:2]):
        score += 0.15
    
    return min(score, 1.0)

def generar_recomendaciones_visuales(caracteristicas, colores):
    """
    Genera recomendaciones para mejorar el engagement visual
    """
    recomendaciones = []
    
    brillo = caracteristicas['brillo']
    saturacion = caracteristicas['saturacion']
    contraste = caracteristicas['contraste']
    
    if brillo < 0.3:
        recomendaciones.append("💡 Aumenta el brillo para mayor visibilidad")
    elif brillo > 0.8:
        recomendaciones.append("🌙 Reduce el brillo para evitar sobreexposición")
    
    if saturacion < 0.3:
        recomendaciones.append("🎨 Aumenta la saturación de colores para más impacto")
    
    if contraste < 0.2:
        recomendaciones.append("⚡ Mejora el contraste para destacar elementos")
    
    # Recomendaciones de colores
    color_principal = colores[0]['nombre'] if colores else 'neutro'
    if color_principal in ['gris', 'negro', 'neutro']:
        recomendaciones.append("🌈 Añade colores más vibrantes (rosa, azul, verde)")
    
    if not recomendaciones:
        recomendaciones.append("✅ La imagen tiene buenas características visuales")
    
    return recomendaciones

# --- MODELO PREDICTIVO TEMPORAL ---
@st.cache_resource
def crear_modelo_temporal_visual(df):
    """
    Crea un modelo que predice el mejor tipo de imagen según hora y día
    """
    try:
        if 'Fecha' not in df.columns:
            return None, None
        
        # Preparar datos temporales
        df_modelo = df.copy()
        df_modelo['hora'] = df_modelo['Fecha'].dt.hour
        df_modelo['dia_semana'] = df_modelo['Fecha'].dt.dayofweek
        df_modelo['mes'] = df_modelo['Fecha'].dt.month
        
        # Crear variables de engagement
        if 'Alcance' in df.columns and 'Interacciones' in df.columns:
            df_modelo['engagement_rate'] = df_modelo['Interacciones'] / df_modelo['Alcance']
            df_modelo['engagement_rate'] = df_modelo['engagement_rate'].fillna(0)
        else:
            return None, None
        
        # Preparar features
        features = ['hora', 'dia_semana', 'mes']
        if 'Inversion' in df.columns:
            features.append('Inversion')
        
        # Encodificar formatos
        le_formato = LabelEncoder()
        df_modelo['formato_enc'] = le_formato.fit_transform(df_modelo['Formato'])
        
        X = df_modelo[features]
        y = df_modelo['formato_enc']
        
        # Entrenar modelo
        modelo_temporal = RandomForestClassifier(n_estimators=100, random_state=42)
        modelo_temporal.fit(X, y)
        
        return modelo_temporal, le_formato
        
    except Exception as e:
        st.error(f"Error creando modelo temporal: {e}")
        return None, None

# --- CABECERA CON LOGO ---
# Crear columnas para centrar el logo en la cabecera
col_logo1, col_logo_center, col_logo3 = st.columns([1, 2, 1])

with col_logo_center:
    if os.path.exists(LOGO_PATH):
        st.markdown('<div class="header-logo">', unsafe_allow_html=True)
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.image(LOGO_PATH, width=200, use_container_width=False)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="header-logo">
            <div class="logo-container">
                <h1 style="text-align: center; margin: 0; font-size: 2rem; color: #4a148c;">💜 DIVA DIGITAL</h1>
                <p style="text-align: center; margin: 0; color: #6a1b9a;">Empodera tu estrategia digital</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- DESCRIPCIÓN INICIAL ---
st.markdown("""
<div style='background:rgba(255,255,255,0.9);padding:1.2em 2em;border-radius:18px;margin-bottom:1.5em;box-shadow:0 4px 15px rgba(142,36,170,0.1);border-left: 4px solid #e91e63;'>
    <span style='font-size:1.2em;color:#e91e63;'><b>¿Quieres impulsar tu marca en redes sociales?</b></span><br>
    <span style='color:#4a148c;'>Diva Digital te ayuda a <b>analizar, visualizar y predecir</b> el rendimiento de tus publicaciones en Instagram, Facebook y TikTok.<br>
    Descubre qué funciona mejor, optimiza tu inversión y toma decisiones basadas en datos, ¡todo en una interfaz atractiva y sencilla!</span>
</div>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def cargar_datos():
    """
    Carga el dataset principal con fallback a datos demo
    """
    try:
        # Intentar cargar el dataset principal
        df_principal = pd.read_csv("/Users/n.arcos89/Desktop/Bootcamp_Data/DIVA_DIGITAL_Proyecto Final/Data/data_unificada.csv", sep=';')
        
        # Convertir fechas
        if 'Fecha' in df_principal.columns:
            try:
                df_principal['Fecha'] = pd.to_datetime(df_principal['Fecha'])
            except:
                st.warning("No se pudo convertir la columna Fecha del dataset principal")
        
        return df_principal, "principal"
        
    except FileNotFoundError:
        st.warning("⚠️ Dataset principal no encontrado, cargando datos demo...")
        try:
            # Cargar datos demo como fallback
            df_demo = pd.read_csv("/Users/n.arcos89/Desktop/Bootcamp_Data/DIVA_DIGITAL_Proyecto Final/Data/data_demo_ok.csv")
            
            # Convertir fechas
            if 'Fecha' in df_demo.columns:
                try:
                    df_demo['Fecha'] = pd.to_datetime(df_demo['Fecha'])
                except:
                    st.warning("No se pudo convertir la columna Fecha del dataset demo")
            
            return df_demo, "demo"
            
        except FileNotFoundError:
            st.error("❌ No se encontró ningún archivo de datos. Verifique que existan los archivos CSV.")
            return pd.DataFrame(), "none"
            
    except Exception as e:
        st.error(f"❌ Error al cargar los datos: {str(e)}")
        return pd.DataFrame(), "error"

# Cargar datos
df, tipo_datos = cargar_datos()

# Carga de datos de imágenes
@st.cache_data
def cargar_datos_imagenes():
    """
    Carga el CSV con los datos de las imágenes de Pixabay y ajusta las rutas
    """
    try:
        csv_path = "/Users/n.arcos89/Desktop/Bootcamp_Data/DIVA_DIGITAL_Proyecto Final/Data/publicaciones_pixabay_ok.csv"
        
        # Verificar si el archivo CSV existe
        if not os.path.exists(csv_path):
            st.sidebar.error(f"❌ No se encontró el archivo CSV en: {csv_path}")
            return pd.DataFrame()
        
        # Cargar CSV
        df_imagenes = pd.read_csv(csv_path)
        st.sidebar.info(f"✅ CSV cargado: {len(df_imagenes)} filas")
        
        # Mostrar columnas disponibles para diagnóstico
        st.sidebar.write(f"📋 Columnas disponibles: {list(df_imagenes.columns)}")
        
        # Convertir fecha si existe
        fecha_col = None
        if 'Fecha' in df_imagenes.columns:
            fecha_col = 'Fecha'
        elif 'fecha' in df_imagenes.columns:
            fecha_col = 'fecha'
        else:
            st.sidebar.warning("⚠️ No se encontró columna de fecha (Fecha/fecha)")
            return pd.DataFrame()
        
        # Convertir fechas
        df_imagenes[fecha_col] = pd.to_datetime(df_imagenes[fecha_col], errors='coerce')
        df_imagenes['Fecha'] = df_imagenes[fecha_col]  # Estandarizar nombre
        
        # Verificar si hay fechas válidas
        fechas_validas = df_imagenes['Fecha'].notna().sum()
        st.sidebar.info(f"📅 Fechas válidas: {fechas_validas} de {len(df_imagenes)}")
        
        if fechas_validas == 0:
            st.sidebar.error("❌ No hay fechas válidas en el CSV")
            return pd.DataFrame()
        
        # Verificar columna Imagen
        if 'Imagen' not in df_imagenes.columns:
            st.sidebar.error("❌ No se encontró la columna 'Imagen' en el CSV")
            st.sidebar.write("🔍 Columnas disponibles:", list(df_imagenes.columns))
            return pd.DataFrame()
        
        # Mostrar algunas imágenes de ejemplo del CSV
        imagenes_ejemplo_csv = df_imagenes['Imagen'].dropna().head(3).tolist()
        st.sidebar.write(f"🖼️ Nombres en CSV: {imagenes_ejemplo_csv}")
        
        # Definir la ruta donde están las imágenes reales
        ruta_base_imagenes = "/Users/n.arcos89/Desktop/Bootcamp_Data/DIVA_DIGITAL_Proyecto Final/Imagenes/imagenes_pixabay"
        
        if not os.path.exists(ruta_base_imagenes):
            st.sidebar.error("❌ No se encontró el directorio de imágenes")
            st.sidebar.info("💡 Verifica que las imágenes estén extraídas en: imagenes_pixabay/")
            return pd.DataFrame()
        
        # Obtener lista de archivos reales en el directorio
        try:
            archivos_reales = [f for f in os.listdir(ruta_base_imagenes) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
            archivos_reales.sort()  # Ordenar para facilitar el mapeo
            st.sidebar.write(f"🖼️ Archivos reales encontrados: {len(archivos_reales)}")
            st.sidebar.write(f"🖼️ Primeros archivos reales: {archivos_reales[:3]}")
        except Exception as e:
            st.sidebar.error(f"❌ Error leyendo directorio: {str(e)}")
            return pd.DataFrame()
        
        if len(archivos_reales) == 0:
            st.sidebar.error("❌ No se encontraron archivos de imagen en el directorio")
            return pd.DataFrame()
        
        # FUNCIÓN PARA CONVERTIR POST_X.jpg a IMG_X.jpg
        def convertir_post_a_img(nombre_archivo):
            """
            Convierte nombres de POST_X.jpg a IMG_X.jpg
            """
            if nombre_archivo.startswith('POST_'):
                # Extraer el número: POST_47.jpg -> 47
                numero = nombre_archivo.replace('POST_', '').replace('.jpg', '').replace('.jpeg', '').replace('.png', '')
                # Obtener la extensión original
                extension = '.' + nombre_archivo.split('.')[-1]
                # Crear nuevo nombre: IMG_47.jpg
                nuevo_nombre = f"IMG_{numero}{extension}"
                return nuevo_nombre
            return nombre_archivo
        
        # MAPEAR ARCHIVOS REALES (POST_X) CON NOMBRES DEL CSV (IMG_X)
        # Crear mapeo: IMG_X.jpg (CSV) -> POST_X.jpg (archivo real)
        mapeo_imagenes = {}
        mapeo_invertido = {}  # Para mostrar el mapeo POST -> IMG
        
        for archivo_real in archivos_reales:
            if archivo_real.startswith('POST_'):
                # Convertir POST_47.jpg -> IMG_47.jpg
                nombre_img = convertir_post_a_img(archivo_real)
                mapeo_imagenes[nombre_img] = archivo_real
                mapeo_invertido[archivo_real] = nombre_img
        
        st.sidebar.write(f"🔗 Mapeo creado para {len(mapeo_imagenes)} imágenes")
        
        # Mostrar algunos ejemplos del mapeo
        if len(mapeo_invertido) > 0:
            ejemplos_mapeo = list(mapeo_invertido.items())[:3]
            st.sidebar.write("🔄 **Ejemplos de conversión:**")
            for archivo_real, nombre_img in ejemplos_mapeo:
                st.sidebar.write(f"  • {archivo_real} → {nombre_img}")
        
        # Aplicar mapeo y construir rutas
        def mapear_imagen(nombre_csv):
            if nombre_csv in mapeo_imagenes:
                archivo_real = mapeo_imagenes[nombre_csv]
                return os.path.join(ruta_base_imagenes, archivo_real)
            return None
        
        df_imagenes['Ruta'] = df_imagenes['Imagen'].apply(mapear_imagen)
        
        # Verificar cuántas imágenes se mapearon correctamente
        df_imagenes['imagen_existe'] = df_imagenes['Ruta'].apply(
            lambda x: os.path.exists(x) if x else False
        )
        
        # Mostrar estadísticas detalladas del mapeo
        imagenes_totales = len(df_imagenes)
        imagenes_mapeadas = df_imagenes['Ruta'].notna().sum()
        imagenes_encontradas = df_imagenes['imagen_existe'].sum()
        
        st.sidebar.info(f"""
        📸 **Estadísticas de Mapeo:**
        - Total en CSV: {imagenes_totales}
        - Archivos POST encontrados: {len([f for f in archivos_reales if f.startswith('POST_')])}
        - Mapeadas exitosamente: {imagenes_mapeadas}
        - Archivos verificados existentes: {imagenes_encontradas}
        - Éxito del mapeo: {(imagenes_encontradas/imagenes_totales)*100:.1f}%
        """)
        
        # Mostrar ejemplos de mapeo exitoso y verificación
        if imagenes_encontradas > 0:
            imagenes_exitosas = df_imagenes[df_imagenes['imagen_existe']].head(3)
            st.sidebar.success("✅ **Ejemplos de mapeo exitoso:**")
            for _, row in imagenes_exitosas.iterrows():
                archivo_real = os.path.basename(row['Ruta'])
                st.sidebar.write(f"  • {row['Imagen']} → {archivo_real}")
        
        # Filtrar solo las imágenes que existen
        df_imagenes_validas = df_imagenes[df_imagenes['imagen_existe']].copy()
        
        # Verificar columnas necesarias
        required_cols = ['Imagen', 'Ruta', 'Fecha']
        missing_cols = [col for col in required_cols if col not in df_imagenes_validas.columns]
        
        if missing_cols:
            st.sidebar.error(f"❌ Columnas faltantes: {missing_cols}")
            return pd.DataFrame()
        
        # Filtrar solo filas con datos válidos
        df_imagenes_validas = df_imagenes_validas.dropna(subset=['Imagen', 'Ruta', 'Fecha'])
        
        # Resultado final
        if len(df_imagenes_validas) > 0:
            st.sidebar.success(f"🎉 {len(df_imagenes_validas)} imágenes válidas cargadas")
            
            # Mostrar rango de fechas
            fecha_min = df_imagenes_validas['Fecha'].min().date()
            fecha_max = df_imagenes_validas['Fecha'].max().date()
            st.sidebar.info(f"📅 Fechas disponibles: {fecha_min} a {fecha_max}")
            
            # Mostrar algunos nombres de archivos mapeados
            archivos_mapeados = df_imagenes_validas.apply(
                lambda row: f"{row['Imagen']} → {os.path.basename(row['Ruta'])}", axis=1
            ).head(3).tolist()
            st.sidebar.write("🔗 **Mapeo final exitoso:**")
            for mapeo in archivos_mapeados:
                st.sidebar.write(f"  • {mapeo}")
        else:
            st.sidebar.error("❌ No se encontraron imágenes válidas después del mapeo")
        
        return df_imagenes_validas
        
    except FileNotFoundError:
        st.sidebar.error("❌ Archivo CSV de imágenes no encontrado")
        return pd.DataFrame()
    except Exception as e:
        st.sidebar.error(f"❌ Error cargando datos de imágenes: {str(e)}")
        st.sidebar.write(f"🔍 Detalles del error: {type(e).__name__}")
        return pd.DataFrame()

# Cargar datos de imágenes con diagnóstico
st.sidebar.markdown("---")
st.sidebar.markdown("### 🖼️ Estado de Imágenes")

try:
    df_imagenes = cargar_datos_imagenes()
    if df_imagenes.empty:
        st.sidebar.error("❌ No se pudieron cargar las imágenes")
    else:
        st.sidebar.success(f"✅ {len(df_imagenes)} imágenes cargadas correctamente")
except Exception as e:
    st.sidebar.error(f"❌ Error al cargar imágenes: {str(e)}")
    df_imagenes = pd.DataFrame()

# Mostrar qué tipo de datos se están usando
if tipo_datos == "principal":
    st.sidebar.success("📊 **Usando dataset principal**")
elif tipo_datos == "demo":
    st.sidebar.warning("📊 **Usando datos demo**")
elif tipo_datos == "none":
    st.error("No se pudieron cargar los datos. La aplicación no puede continuar.")
    st.stop()
elif tipo_datos == "error":
    st.error("Error en la carga de datos. La aplicación no puede continuar.")
    st.stop()

if df.empty:
    st.error("No se pudieron cargar los datos. La aplicación no puede continuar.")
    st.stop()

# --- SIDEBAR: LOGO, FILTROS Y RESUMEN ---
# Logo en el sidebar
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, width=150, use_container_width=False)
else:
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 1rem; background: rgba(255, 255, 255, 0.1); border-radius: 15px; margin-bottom: 1rem;'>
        <h2 style='margin: 0; color: #fff; font-size: 1.5rem;'>💜 DIVA DIGITAL</h2>
        <p style='margin: 0; color: #fff; font-size: 0.9rem;'>Analytics & Insights</p>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='color:#fff; text-align: center;'>📊 Panel de Control</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#fff; text-align: center;'>Empodera tu estrategia digital con datos 💫</p>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔎 Filtra tus datos")

# Mostrar información básica de los datos
fecha_info = "N/A"
if 'Fecha' in df.columns and not df['Fecha'].isna().all():
    try:
        fecha_min = df['Fecha'].min().strftime('%Y-%m-%d')
        fecha_max = df['Fecha'].max().strftime('%Y-%m-%d')
        fecha_info = f"{fecha_min} a {fecha_max}"
    except:
        fecha_info = "Formato de fecha inválido"

st.sidebar.info(f"📊 **Datos cargados:**\n- {len(df)} publicaciones\n- {len(df.columns)} columnas\n- Período: {fecha_info}")

# Filtros
canales_disponibles = df['Canal'].unique().tolist() if 'Canal' in df.columns else []
formatos_disponibles = df['Formato'].unique().tolist() if 'Formato' in df.columns else []

filtro_canal = st.sidebar.multiselect("📱 Canal", canales_disponibles, default=canales_disponibles)
filtro_formato = st.sidebar.multiselect("🎨 Formato", formatos_disponibles, default=formatos_disponibles)

if 'Fecha' in df.columns and not df['Fecha'].isna().all():
    try:
        fecha_min = df['Fecha'].min().date()
        fecha_max = df['Fecha'].max().date()
        filtro_fecha = st.sidebar.date_input("📅 Rango de fechas", [fecha_min, fecha_max])
        if len(filtro_fecha) == 2:
            fecha_inicio, fecha_fin = filtro_fecha
        else:
            fecha_inicio = fecha_fin = filtro_fecha[0]
    except:
        fecha_inicio = fecha_fin = None
        st.sidebar.warning("⚠️ Error en el formato de fechas")
else:
    fecha_inicio = fecha_fin = None

# Aplicar filtros
df_filtrado = df.copy()
if filtro_canal and 'Canal' in df.columns:
    df_filtrado = df_filtrado[df_filtrado['Canal'].isin(filtro_canal)]
if filtro_formato and 'Formato' in df.columns:
    df_filtrado = df_filtrado[df_filtrado['Formato'].isin(filtro_formato)]
if fecha_inicio and fecha_fin and 'Fecha' in df.columns:
    try:
        df_filtrado = df_filtrado[(df_filtrado['Fecha'].dt.date >= fecha_inicio) & 
                                 (df_filtrado['Fecha'].dt.date <= fecha_fin)]
    except:
        st.sidebar.warning("⚠️ Error aplicando filtro de fechas")

# Mostrar resumen de filtros aplicados
st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Resumen Filtrado")
st.sidebar.success(f"**{len(df_filtrado)}** publicaciones seleccionadas de **{len(df)}** totales")

if len(df_filtrado) < len(df):
    st.sidebar.markdown(f"""
    **Filtros activos:**
    - Canales: {', '.join(filtro_canal) if filtro_canal else 'Todos'}
    - Formatos: {', '.join(filtro_formato) if filtro_formato else 'Todos'}
    - Fechas: {fecha_inicio} a {fecha_fin if fecha_fin else fecha_inicio}
    """)

# --- FUNCIONES AUXILIARES ---
def resumen_metrics(df):
    metrics = {}
    try:
        if 'Canal' in df.columns:
            canal_counts = df['Canal'].value_counts()
            metrics["Canal más habitual"] = canal_counts.index[0]
        if 'Formato' in df.columns:
            formato_counts = df['Formato'].value_counts()
            metrics["Formato más utilizado"] = formato_counts.index[0]
        if 'Alcance' in df.columns:
            total_alcance = df['Alcance'].sum()
            media_alcance = df['Alcance'].mean()
            metrics["Total alcance"] = f"{total_alcance:,}"
            metrics["Media alcance/post"] = f"{media_alcance:,.0f}"
        if 'Interacciones' in df.columns:
            total_interacciones = df['Interacciones'].sum()
            media_interacciones = df['Interacciones'].mean()
            metrics["Total interacciones"] = f"{total_interacciones:,}"
            metrics["Media interacciones/post"] = f"{media_interacciones:,.0f}"
        if 'Alcance' in df.columns and 'Interacciones' in df.columns:
            engagement = (df['Interacciones'].sum() / df['Alcance'].sum()) * 100 if df['Alcance'].sum() > 0 else 0
            metrics["Engagement (%)"] = f"{engagement:.2f}%"
        if 'Inversion' in df.columns:
            inversion_total = df['Inversion'].sum()
            metrics["Inversión total (€)"] = f"{inversion_total:,.2f}"
        if 'Compras' in df.columns:
            compras_total = df['Compras'].sum()
            metrics["Compras totales"] = f"{compras_total:,}"
        if 'Valor_compra' in df.columns:
            ingresos_total = df['Valor_compra'].sum()
            metrics["Ingresos totales (€)"] = f"{ingresos_total:,.2f}"
            if 'Inversion' in df.columns:
                inversion_val = df['Inversion'].sum()
                if inversion_val > 0:
                    roi = ((ingresos_total - inversion_val) / inversion_val) * 100
                    metrics["ROI (%)"] = f"{roi:.2f}%"
    except Exception as e:
        st.error(f"Error calculando métricas: {e}")
    return metrics

@st.cache_resource
def get_models(df):
    required_cols = ['Canal', 'Formato', 'Alcance', 'Inversion']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"No se pueden crear modelos. Faltan columnas: {missing_cols}")
        return None, None, None, None, None, None
    try:
        le_canal = LabelEncoder()
        le_formato = LabelEncoder()
        df_copy = df.copy()
        df_copy['Canal_enc'] = le_canal.fit_transform(df_copy['Canal'])
        df_copy['Formato_enc'] = le_formato.fit_transform(df_copy['Formato'])
        features = ['Canal_enc', 'Formato_enc', 'Inversion']
        X = df_copy[features]
        y = df_copy['Alcance']
        scaler = StandardScaler().fit(X)
        X_scaled = scaler.transform(X)
        reg = RandomForestRegressor(n_estimators=50, random_state=42).fit(X_scaled, y)
        clf_canal = RandomForestClassifier(n_estimators=50, random_state=42).fit(X_scaled, df_copy['Canal_enc'])
        clf_formato = RandomForestClassifier(n_estimators=50, random_state=42).fit(X_scaled, df_copy['Formato_enc'])
        return reg, scaler, le_canal, le_formato, clf_canal, clf_formato
    except Exception as e:
        st.error(f"Error al crear modelos: {str(e)}")
        return None, None, None, None, None, None

reg, scaler, le_canal, le_formato, clf_canal, clf_formato = get_models(df)
models_ok = all(model is not None for model in [reg, scaler, le_canal, le_formato, clf_canal, clf_formato])

# Crear modelo temporal
modelo_temporal, le_formato_temporal = crear_modelo_temporal_visual(df)

# --- APP STREAMLIT ---
st.title("✨ Diva Digital: Análisis de Redes Sociales para Marcas")

tab1, tab2, tab3 = st.tabs(["📊 Informe Interanual", "🔮 Modelo Predictivo", "🚀 Next Steps"])

# --- TAB 1: INFORME INTERANUAL ---
with tab1:
    st.header("📊 Informe Interanual")
    if df_filtrado.empty:
        st.error("No hay datos para mostrar el informe")
    else:
        subtab1, subtab2, subtab3, subtab4, subtab5, subtab6 = st.tabs([
            "📈 Resumen", "👁️ Visibilidad", "❤️ Interacción", "▶️ Reproducciones", "🛒 Conversión", "💰 Retorno"
        ])
        
        with subtab1:
            st.subheader("📈 Resumen General")
            metrics = resumen_metrics(df_filtrado)
            if metrics:
                cols = st.columns(4)
                for i, (k, v) in enumerate(metrics.items()):
                    cols[i % 4].metric(k, v)
            
            st.markdown("**Resumen de los principales KPIs de la actividad en redes sociales.**")
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                if 'Canal' in df_filtrado.columns:
                    posts_por_canal = df_filtrado['Canal'].value_counts().reset_index()
                    posts_por_canal.columns = ['Canal', 'Número de Posts']
                    fig1 = px.pie(posts_por_canal, values='Número de Posts', names='Canal',
                                title="📊 Distribución de Posts por Canal",
                                color_discrete_sequence=px.colors.sequential.Purples)
                    fig1.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                    st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                if 'Formato' in df_filtrado.columns:
                    posts_por_formato = df_filtrado['Formato'].value_counts().reset_index()
                    posts_por_formato.columns = ['Formato', 'Número de Posts']
                    fig2 = px.bar(posts_por_formato, x='Formato', y='Número de Posts',
                                title="📈 Posts por Formato",
                                color='Número de Posts',
                                color_continuous_scale='Pinkyl')
                    fig2.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                    st.plotly_chart(fig2, use_container_width=True)
            
            if 'Fecha' in df_filtrado.columns:
                st.markdown("### 📅 Tendencias Temporales")
                col5, col6 = st.columns(2)
                with col5:
                    df_temp = df_filtrado.copy()
                    df_temp['Mes'] = df_temp['Fecha'].dt.to_period('M').astype(str)
                    posts_por_mes = df_temp.groupby('Mes').size().reset_index()
                    posts_por_mes.columns = ['Mes', 'Número de Posts']
                    fig5 = px.line(posts_por_mes, x='Mes', y='Número de Posts',
                                 title="📈 Evolución de Posts por Mes",
                                 markers=True, color_discrete_sequence=['#e91e63'])
                    fig5.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                    st.plotly_chart(fig5, use_container_width=True)
                
                with col6:
                    if 'Alcance' in df_filtrado.columns and 'Interacciones' in df_filtrado.columns:
                        engagement_mes = df_temp.groupby('Mes').agg({
                            'Alcance': 'sum',
                            'Interacciones': 'sum'
                        }).reset_index()
                        engagement_mes['Engagement'] = (engagement_mes['Interacciones'] / engagement_mes['Alcance'] * 100).fillna(0)
                        fig6 = px.line(engagement_mes, x='Mes', y='Engagement',
                                     title="📊 Evolución del Engagement por Mes (%)",
                                     markers=True, color_discrete_sequence=['#8e24aa'])
                        fig6.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                        st.plotly_chart(fig6, use_container_width=True)

        with subtab2:
            st.subheader("👁️ Visibilidad")
            if 'Alcance' in df_filtrado.columns:
                col1, col2, col3 = st.columns(3)
                col1.metric("Alcance Total", f"{df_filtrado['Alcance'].sum():,.0f}")
                col2.metric("Alcance Promedio", f"{df_filtrado['Alcance'].mean():.0f}")
                col3.metric("Total de posts", f"{len(df_filtrado)}")
                
                if 'Canal' in df_filtrado.columns:
                    alcance_canal = df_filtrado.groupby('Canal')['Alcance'].mean().reset_index()
                    fig = px.bar(alcance_canal, x='Canal', y='Alcance',
                               title="📊 Alcance promedio por Canal",
                               color='Alcance', color_continuous_scale='Purples')
                    fig.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No se encontró columna de alcance")

        with subtab3:
            st.subheader("❤️ Interacción")
            if 'Interacciones' in df_filtrado.columns:
                col1, col2, col3 = st.columns(3)
                col1.metric("Interacciones Totales", f"{df_filtrado['Interacciones'].sum():,.0f}")
                col2.metric("Interacciones Promedio", f"{df_filtrado['Interacciones'].mean():.0f}")
                if 'Alcance' in df_filtrado.columns:
                    engagement = (df_filtrado['Interacciones'].sum() / df_filtrado['Alcance'].sum()) * 100 if df_filtrado['Alcance'].sum() > 0 else 0
                    col3.metric("Engagement Rate", f"{engagement:.2f}%")
                
                if 'Canal' in df_filtrado.columns:
                    interaccion_canal = df_filtrado.groupby('Canal')['Interacciones'].mean().reset_index()
                    fig = px.bar(interaccion_canal, x='Canal', y='Interacciones',
                               title="📊 Interacciones promedio por Canal",
                               color='Interacciones', color_continuous_scale='Pinkyl')
                    fig.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No se encontró columna de interacciones")

        with subtab4:
            st.subheader("▶️ Reproducciones")
            
            # Filtrar solo Reels para métricas de video
            df_reels = df_filtrado[df_filtrado['Formato'] == 'Reel'].copy()
            
            if len(df_reels) == 0:
                st.info("📱 No hay Reels en los datos filtrados")
                st.markdown("""
                **💡 Nota:** Las métricas de reproducciones, duración y retención solo están disponibles para contenido en formato Reel.
                
                **Formatos disponibles en tu selección:**
                """)
                formatos_disponibles = df_filtrado['Formato'].value_counts()
                for formato, cantidad in formatos_disponibles.items():
                    st.write(f"- **{formato}**: {cantidad} publicaciones")
                    
            else:
                # Convertir 'Sin datos' a NaN y luego a numérico
                numeric_cols = ['Reproducciones', 'Duracion_video', 'Retencion']
                for col in numeric_cols:
                    if col in df_reels.columns:
                        df_reels[col] = pd.to_numeric(df_reels[col].replace('Sin datos', np.nan), errors='coerce')
                
                # Eliminar filas con valores NaN en Reproducciones
                df_reels_clean = df_reels.dropna(subset=['Reproducciones'])
                
                if len(df_reels_clean) == 0:
                    st.warning("⚠️ Los Reels seleccionados no tienen datos válidos de reproducciones")
                else:
                    col1, col2, col3 = st.columns(3)
                    
                    # Métricas básicas
                    total_reproducciones = df_reels_clean['Reproducciones'].sum()
                    promedio_reproducciones = df_reels_clean['Reproducciones'].mean()
                    
                    col1.metric("📊 Reels analizados", f"{len(df_reels_clean)}")
                    col2.metric("▶️ Reproducciones Totales", f"{total_reproducciones:,.0f}")
                    col3.metric("📈 Reproducciones Promedio", f"{promedio_reproducciones:,.0f}")
                    
                    # Segunda fila de métricas
                    col4, col5, col6 = st.columns(3)
                    
                    # Tasa de reproducción vs alcance
                    if 'Alcance' in df_reels_clean.columns:
                        tasa_reproduccion = (total_reproducciones / df_reels_clean['Alcance'].sum()) * 100 if df_reels_clean['Alcance'].sum() > 0 else 0
                        col4.metric("🎯 Tasa de Reproducción", f"{tasa_reproduccion:.1f}%")
                    
                    # Duración promedio (solo para reels)
                    if 'Duracion_video' in df_reels_clean.columns:
                        duracion_clean = df_reels_clean.dropna(subset=['Duracion_video'])
                        if len(duracion_clean) > 0:
                            duracion_promedio = duracion_clean['Duracion_video'].mean()
                            col5.metric("⏱️ Duración Promedio", f"{duracion_promedio:.1f}s")
                    
                    # Retención promedio
                    if 'Retencion' in df_reels_clean.columns:
                        retencion_clean = df_reels_clean.dropna(subset=['Retencion'])
                        if len(retencion_clean) > 0:
                            retencion_promedio = retencion_clean['Retencion'].mean()
                            col6.metric("🎯 Retención Promedio", f"{retencion_promedio:.1f}%")
                    
                    # Gráfico de reproducciones por canal (solo para Reels)
                    if 'Canal' in df_reels_clean.columns and len(df_reels_clean) > 0:
                        st.markdown("### 📊 Análisis de Reproducciones por Canal")
                        reproducciones_canal = df_reels_clean.groupby('Canal')['Reproducciones'].agg(['sum', 'mean']).reset_index()
                        reproducciones_canal.columns = ['Canal', 'Total_Reproducciones', 'Promedio_Reproducciones']
                        
                        col_chart1, col_chart2 = st.columns(2)
                        
                        with col_chart1:
                            fig_total = px.bar(reproducciones_canal, x='Canal', y='Total_Reproducciones',
                                             title="📊 Total de Reproducciones por Canal",
                                             color='Total_Reproducciones', color_continuous_scale='Purples')
                            fig_total.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                            st.plotly_chart(fig_total, use_container_width=True)
                        
                        with col_chart2:
                            fig_promedio = px.bar(reproducciones_canal, x='Canal', y='Promedio_Reproducciones',
                                                title="📈 Promedio de Reproducciones por Canal",
                                                color='Promedio_Reproducciones', color_continuous_scale='Pinkyl')
                            fig_promedio.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                            st.plotly_chart(fig_promedio, use_container_width=True)

        with subtab5:
            st.subheader("🛒 Conversión")
            if 'Compras' in df_filtrado.columns:
                col1, col2, col3 = st.columns(3)
                total_compras = df_filtrado['Compras'].sum()
                promedio_compras = df_filtrado['Compras'].mean()
                tasa_conversion = (total_compras / df_filtrado['Alcance'].sum()) * 100 if 'Alcance' in df_filtrado.columns and df_filtrado['Alcance'].sum() > 0 else 0
                
                col1.metric("🛍️ Compras Totales", f"{total_compras:,}")
                col2.metric("📈 Compras Promedio", f"{promedio_compras:.1f}")
                col3.metric("💯 Tasa de Conversión", f"{tasa_conversion:.3f}%")
                
                if 'Canal' in df_filtrado.columns:
                    st.markdown("### 📊 Análisis de Conversión por Canal")
                    
                    conversion_canal = df_filtrado.groupby('Canal').agg({
                        'Compras': ['sum', 'mean'],
                        'Alcance': 'sum'
                    }).reset_index()
                    conversion_canal.columns = ['Canal', 'Total_Compras', 'Promedio_Compras', 'Total_Alcance']
                    conversion_canal['Tasa_Conversion'] = (conversion_canal['Total_Compras'] / conversion_canal['Total_Alcance'] * 100).fillna(0)
                    
                    col_conv1, col_conv2 = st.columns(2)
                    
                    with col_conv1:
                        fig_compras = px.bar(conversion_canal, x='Canal', y='Total_Compras',
                                           title="🛍️ Compras Totales por Canal",
                                           color='Total_Compras', color_continuous_scale='Greens')
                        fig_compras.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                        st.plotly_chart(fig_compras, use_container_width=True)
                    
                    with col_conv2:
                        fig_tasa = px.bar(conversion_canal, x='Canal', y='Tasa_Conversion',
                                        title="💯 Tasa de Conversión por Canal (%)",
                                        color='Tasa_Conversion', color_continuous_scale='Blues')
                        fig_tasa.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                        st.plotly_chart(fig_tasa, use_container_width=True)
            else:
                st.warning("No se encontró columna de compras")

        with subtab6:
            st.subheader("💰 Retorno de Inversión")
            if 'Valor_compra' in df_filtrado.columns and 'Inversion' in df_filtrado.columns:
                col1, col2, col3, col4 = st.columns(4)
                
                total_ingresos = df_filtrado['Valor_compra'].sum()
                total_inversion = df_filtrado['Inversion'].sum()
                beneficio = total_ingresos - total_inversion
                roi = (beneficio / total_inversion * 100) if total_inversion > 0 else 0
                
                col1.metric("💰 Ingresos Totales", f"{total_ingresos:,.2f}€")
                col2.metric("💸 Inversión Total", f"{total_inversion:,.2f}€")
                col3.metric("💵 Beneficio", f"{beneficio:,.2f}€", delta=f"{roi:.1f}% ROI")
                col4.metric("📊 ROI", f"{roi:.2f}%")
                
                if 'Canal' in df_filtrado.columns:
                    st.markdown("### 📊 Análisis de ROI por Canal")
                    
                    roi_canal = df_filtrado.groupby('Canal').agg({
                        'Valor_compra': 'sum',
                        'Inversion': 'sum'
                    }).reset_index()
                    roi_canal['Beneficio'] = roi_canal['Valor_compra'] - roi_canal['Inversion']
                    roi_canal['ROI'] = ((roi_canal['Beneficio'] / roi_canal['Inversion']) * 100).fillna(0)
                    
                    col_roi1, col_roi2 = st.columns(2)
                    
                    with col_roi1:
                        fig_beneficio = px.bar(roi_canal, x='Canal', y='Beneficio',
                                             title="💵 Beneficio por Canal",
                                             color='Beneficio', 
                                             color_continuous_scale='RdYlGn',
                                             color_continuous_midpoint=0)
                        fig_beneficio.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                        st.plotly_chart(fig_beneficio, use_container_width=True)
                    
                    with col_roi2:
                        fig_roi = px.bar(roi_canal, x='Canal', y='ROI',
                                       title="📊 ROI por Canal (%)",
                                       color='ROI', 
                                       color_continuous_scale='RdYlGn',
                                       color_continuous_midpoint=0)
                        fig_roi.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                        st.plotly_chart(fig_roi, use_container_width=True)
                    
                    # Tabla resumen de ROI
                    st.markdown("### 📋 Resumen Detallado por Canal")
                    roi_canal_formatted = roi_canal.copy()
                    roi_canal_formatted['Valor_compra'] = roi_canal_formatted['Valor_compra'].apply(lambda x: f"{x:,.2f}€")
                    roi_canal_formatted['Inversion'] = roi_canal_formatted['Inversion'].apply(lambda x: f"{x:,.2f}€")
                    roi_canal_formatted['Beneficio'] = roi_canal_formatted['Beneficio'].apply(lambda x: f"{x:,.2f}€")
                    roi_canal_formatted['ROI'] = roi_canal_formatted['ROI'].apply(lambda x: f"{x:.2f}%")
                    
                    st.dataframe(roi_canal_formatted, use_container_width=True, hide_index=True)
            else:
                st.warning("No se encontraron columnas de ingresos o inversión")

# --- TAB 2: MODELO PREDICTIVO ---
with tab2:
    st.header("🔮 Modelo Predictivo")
    
    if not models_ok:
        st.error("❌ Los modelos predictivos no están disponibles. Verifica que el dataset tenga las columnas necesarias.")
    else:
        subtab_pred1, subtab_pred2, subtab_pred3 = st.tabs([
            "📈 Predictor de Alcance", "🖼️ Análisis de Imágenes", "⏰ Optimización Temporal"
        ])
        
        with subtab_pred1:
            st.subheader("📈 Predictor de Alcance")
            st.markdown("**Predice el alcance esperado de una publicación basándose en el canal, formato e inversión.**")
            
            col_pred1, col_pred2 = st.columns([1, 1])
            
            with col_pred1:
                st.markdown("### 🎯 Configuración de la Publicación")
                
                pred_canal = st.selectbox("📱 Canal", canales_disponibles)
                pred_formato = st.selectbox("🎨 Formato", formatos_disponibles)
                pred_inversion = st.slider("💰 Inversión (€)", 0.0, 1000.0, 100.0, 10.0)
                
                if st.button("🚀 Predecir Alcance", type="primary"):
                    try:
                        # Codificar inputs
                        canal_enc = le_canal.transform([pred_canal])[0]
                        formato_enc = le_formato.transform([pred_formato])[0]
                        
                        # Preparar features
                        X_pred = np.array([[canal_enc, formato_enc, pred_inversion]])
                        X_pred_scaled = scaler.transform(X_pred)
                        
                        # Predicción
                        alcance_predicho = reg.predict(X_pred_scaled)[0]
                        
                        # Mostrar resultado
                        st.success(f"🎯 **Alcance Predicho: {alcance_predicho:,.0f} personas**")
                        
                        # Calcular métricas adicionales
                        engagement_estimado = alcance_predicho * 0.035  # 3.5% promedio
                        costo_por_alcance = pred_inversion / alcance_predicho if alcance_predicho > 0 else 0
                        
                        col_metric1, col_metric2 = st.columns(2)
                        col_metric1.metric("❤️ Interacciones Estimadas", f"{engagement_estimado:,.0f}")
                        col_metric2.metric("💰 Costo por Alcance", f"{costo_por_alcance:.4f}€")
                        
                    except Exception as e:
                        st.error(f"Error en la predicción: {str(e)}")
            
            with col_pred2:
                st.markdown("### 📊 Análisis Comparativo")
                
                # Mostrar estadísticas históricas
                if pred_canal in df['Canal'].values and pred_formato in df['Formato'].values:
                    df_similar = df[(df['Canal'] == pred_canal) & (df['Formato'] == pred_formato)]
                    
                    if len(df_similar) > 0:
                        st.markdown(f"**📈 Datos históricos para {pred_formato} en {pred_canal}:**")
                        
                        alcance_promedio = df_similar['Alcance'].mean()
                        alcance_max = df_similar['Alcance'].max()
                        alcance_min = df_similar['Alcance'].min()
                        
                        st.metric("📊 Alcance Promedio Histórico", f"{alcance_promedio:,.0f}")
                        st.metric("🏆 Mejor Resultado", f"{alcance_max:,.0f}")
                        st.metric("📉 Resultado Mínimo", f"{alcance_min:,.0f}")
                        
                        # Gráfico de distribución
                        fig_dist = px.histogram(df_similar, x='Alcance', 
                                              title=f"Distribución de Alcance - {pred_formato} en {pred_canal}",
                                              color_discrete_sequence=['#8e24aa'])
                        fig_dist.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                        st.plotly_chart(fig_dist, use_container_width=True)
                    else:
                        st.info("No hay datos históricos para esta combinación canal-formato")

        with subtab_pred2:
            st.subheader("🖼️ Análisis de Imágenes con Computer Vision")
            st.markdown("**Analiza características visuales de imágenes para predecir su potencial de engagement.**")
            
            # Pestañas para diferentes fuentes de imágenes
            img_tab1, img_tab2, img_tab3 = st.tabs([
                "📤 Subir Imagen", "🖼️ Galería de Imágenes", "🔗 URL de Imagen"
            ])
            
            with img_tab1:
                st.markdown("### 📤 Sube tu imagen para análisis")
                uploaded_file = st.file_uploader("Selecciona una imagen", type=['png', 'jpg', 'jpeg'])
                
                if uploaded_file is not None:
                    col_img1, col_img2 = st.columns([1, 1])
                    
                    with col_img1:
                        st.image(uploaded_file, caption="Imagen cargada", use_container_width=True)
                    
                    with col_img2:
                        if st.button("🔍 Analizar Imagen", type="primary"):
                            with st.spinner("Analizando imagen..."):
                                resultado = analizar_imagen_completo(uploaded_file)
                                
                                if resultado['exito']:
                                    st.success("✅ Análisis completado")
                                    
                                    # Mostrar resultados
                                    col_r1, col_r2 = st.columns(2)
                                    
                                    with col_r1:
                                        st.metric("🎯 Score de Engagement", f"{resultado['engagement_score']:.2f}")
                                        st.metric("🏷️ Temática Predicha", resultado['tematica_predicha'])
                                    
                                    with col_r2:
                                        carac = resultado['caracteristicas']
                                        st.metric("💡 Brillo", f"{carac['brillo']:.2f}")
                                        st.metric("🎨 Saturación", f"{carac['saturacion']:.2f}")
                                    
                                    # Colores dominantes
                                    st.markdown("#### 🎨 Colores Dominantes")
                                    cols_color = st.columns(5)
                                    for i, color in enumerate(resultado['colores_dominantes'][:5]):
                                        with cols_color[i]:
                                            st.markdown(f"""
                                            <div style='background-color: {color["hex"]}; 
                                                        width: 60px; height: 60px; 
                                                        border-radius: 50%; margin: auto;
                                                        border: 2px solid #ccc;'></div>
                                            <p style='text-align: center; font-size: 12px; margin-top: 5px;'>
                                                {color["nombre"]}<br>{color["porcentaje"]:.1f}%
                                            </p>
                                            """, unsafe_allow_html=True)
                                    
                                    # Recomendaciones
                                    st.markdown("#### 💡 Recomendaciones")
                                    for rec in resultado['recomendaciones']:
                                        st.info(rec)
                                else:
                                    st.error(f"❌ Error en el análisis: {resultado['error']}")
            
            with img_tab2:
                st.markdown("### 🖼️ Galería de Imágenes Disponibles")
                
                if not df_imagenes.empty:
                    # Selector de fecha para filtrar imágenes
                    col_fecha1, col_fecha2 = st.columns(2)
                    
                    with col_fecha1:
                        fecha_min_img = df_imagenes['Fecha'].min().date()
                        fecha_max_img = df_imagenes['Fecha'].max().date()
                        fecha_seleccionada = st.date_input("📅 Selecciona una fecha", 
                                                         value=fecha_min_img,
                                                         min_value=fecha_min_img,
                                                         max_value=fecha_max_img)
                    
                    # Filtrar imágenes por fecha
                    imagenes_fecha = df_imagenes[df_imagenes['Fecha'].dt.date == fecha_seleccionada]
                    
                    if len(imagenes_fecha) > 0:
                        with col_fecha2:
                            imagen_seleccionada = st.selectbox("🖼️ Selecciona una imagen", 
                                                             imagenes_fecha['Imagen'].tolist())
                        
                        # Obtener la ruta de la imagen seleccionada
                        ruta_imagen = imagenes_fecha[imagenes_fecha['Imagen'] == imagen_seleccionada]['Ruta'].iloc[0]
                        
                        col_gal1, col_gal2 = st.columns([1, 1])
                        
                        with col_gal1:
                            try:
                                st.image(ruta_imagen, caption=f"Imagen: {imagen_seleccionada}", use_container_width=True)
                            except Exception as e:
                                st.error(f"Error cargando imagen: {str(e)}")
                        
                        with col_gal2:
                            if st.button("🔍 Analizar Imagen Seleccionada", type="primary"):
                                with st.spinner("Analizando imagen..."):
                                    try:
                                        resultado = analizar_imagen_completo(ruta_imagen)
                                        
                                        if resultado['exito']:
                                            st.success("✅ Análisis completado")
                                            
                                            # Mostrar resultados
                                            col_r1, col_r2 = st.columns(2)
                                            
                                            with col_r1:
                                                st.metric("🎯 Score de Engagement", f"{resultado['engagement_score']:.2f}")
                                                st.metric("🏷️ Temática Predicha", resultado['tematica_predicha'])
                                            
                                            with col_r2:
                                                carac = resultado['caracteristicas']
                                                st.metric("💡 Brillo", f"{carac['brillo']:.2f}")
                                                st.metric("🎨 Saturación", f"{carac['saturacion']:.2f}")
                                            
                                            # Colores dominantes
                                            st.markdown("#### 🎨 Colores Dominantes")
                                            cols_color = st.columns(5)
                                            for i, color in enumerate(resultado['colores_dominantes'][:5]):
                                                with cols_color[i]:
                                                    st.markdown(f"""
                                                    <div style='background-color: {color["hex"]}; 
                                                                width: 60px; height: 60px; 
                                                                border-radius: 50%; margin: auto;
                                                                border: 2px solid #ccc;'></div>
                                                    <p style='text-align: center; font-size: 12px; margin-top: 5px;'>
                                                        {color["nombre"]}<br>{color["porcentaje"]:.1f}%
                                                    </p>
                                                    """, unsafe_allow_html=True)
                                            
                                            # Recomendaciones
                                            st.markdown("#### 💡 Recomendaciones")
                                            for rec in resultado['recomendaciones']:
                                                st.info(rec)
                                        else:
                                            st.error(f"❌ Error en el análisis: {resultado['error']}")
                                    except Exception as e:
                                        st.error(f"❌ Error analizando imagen: {str(e)}")
                    else:
                        st.info(f"No hay imágenes disponibles para la fecha {fecha_seleccionada}")
                else:
                    st.warning("⚠️ No hay imágenes disponibles en la galería")
            
            with img_tab3:
                st.markdown("### 🔗 Analizar imagen desde URL")
                url_imagen = st.text_input("🔗 Ingresa la URL de la imagen")
                
                if url_imagen:
                    col_url1, col_url2 = st.columns([1, 1])
                    
                    with col_url1:
                        try:
                            st.image(url_imagen, caption="Imagen desde URL", use_container_width=True)
                        except Exception as e:
                            st.error("❌ Error cargando imagen desde URL")
                    
                    with col_url2:
                        if st.button("🔍 Analizar Imagen URL", type="primary"):
                            with st.spinner("Analizando imagen..."):
                                try:
                                    resultado = analizar_imagen_completo(url_imagen)
                                    
                                    if resultado['exito']:
                                        st.success("✅ Análisis completado")
                                        
                                        # Mostrar resultados
                                        col_r1, col_r2 = st.columns(2)
                                        
                                        with col_r1:
                                            st.metric("🎯 Score de Engagement", f"{resultado['engagement_score']:.2f}")
                                            st.metric("🏷️ Temática Predicha", resultado['tematica_predicha'])
                                        
                                        with col_r2:
                                            carac = resultado['caracteristicas']
                                            st.metric("💡 Brillo", f"{carac['brillo']:.2f}")
                                            st.metric("🎨 Saturación", f"{carac['saturacion']:.2f}")
                                        
                                        # Colores dominantes
                                        st.markdown("#### 🎨 Colores Dominantes")
                                        cols_color = st.columns(5)
                                        for i, color in enumerate(resultado['colores_dominantes'][:5]):
                                            with cols_color[i]:
                                                st.markdown(f"""
                                                <div style='background-color: {color["hex"]}; 
                                                            width: 60px; height: 60px; 
                                                            border-radius: 50%; margin: auto;
                                                            border: 2px solid #ccc;'></div>
                                                <p style='text-align: center; font-size: 12px; margin-top: 5px;'>
                                                    {color["nombre"]}<br>{color["porcentaje"]:.1f}%
                                                </p>
                                                """, unsafe_allow_html=True)
                                        
                                        # Recomendaciones
                                        st.markdown("#### 💡 Recomendaciones")
                                        for rec in resultado['recomendaciones']:
                                            st.info(rec)
                                    else:
                                        st.error(f"❌ Error en el análisis: {resultado['error']}")
                                except Exception as e:
                                    st.error(f"❌ Error analizando imagen: {str(e)}")

        with subtab_pred3:
            st.subheader("⏰ Optimización Temporal")
            st.markdown("**Encuentra el mejor momento y formato para publicar basándose en datos históricos.**")
            
            if modelo_temporal is not None and le_formato_temporal is not None:
                col_temp1, col_temp2 = st.columns([1, 1])
                
                with col_temp1:
                    st.markdown("### 🕐 Configuración Temporal")
                    
                    hora_pub = st.slider("⏰ Hora de publicación", 0, 23, 12)
                    dia_semana_pub = st.selectbox("📅 Día de la semana", 
                                                [0, 1, 2, 3, 4, 5, 6],
                                                format_func=lambda x: ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"][x])
                    mes_pub = st.selectbox("📆 Mes", list(range(1, 13)),
                                         format_func=lambda x: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                                                               "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][x-1])
                    inversion_temp = st.slider("💰 Inversión (€)", 0.0, 500.0, 100.0, 10.0)
                    
                    if st.button("🎯 Optimizar Publicación", type="primary"):
                        try:
                            # Preparar features para predicción
                            X_temp = np.array([[hora_pub, dia_semana_pub, mes_pub, inversion_temp]])
                            
                            # Predecir formato óptimo
                            formato_pred = modelo_temporal.predict(X_temp)[0]
                            formato_recomendado = le_formato_temporal.inverse_transform([formato_pred])[0]
                            
                            st.success(f"🎯 **Formato Recomendado: {formato_recomendado}**")
                            
                            # Análisis de engagement por hora
                            if 'Fecha' in df.columns and 'Interacciones' in df.columns and 'Alcance' in df.columns:
                                df_temp_analysis = df.copy()
                                df_temp_analysis['hora'] = df_temp_analysis['Fecha'].dt.hour
                                df_temp_analysis['dia_semana'] = df_temp_analysis['Fecha'].dt.dayofweek
                                df_temp_analysis['engagement_rate'] = (df_temp_analysis['Interacciones'] / df_temp_analysis['Alcance']).fillna(0)
                                
                                engagement_por_hora = df_temp_analysis.groupby('hora')['engagement_rate'].mean()
                                mejor_hora = engagement_por_hora.idxmax()
                                mejor_engagement = engagement_por_hora.max()
                                
                                st.info(f"💡 **Mejor hora histórica: {mejor_hora}:00 (Engagement: {mejor_engagement:.3f})**")
                        
                        except Exception as e:
                            st.error(f"Error en la optimización: {str(e)}")
                
                with col_temp2:
                    st.markdown("### 📊 Análisis Temporal Histórico")
                    
                    if 'Fecha' in df.columns:
                        # Análisis por hora
                        df_temp_viz = df.copy()
                        df_temp_viz['hora'] = df_temp_viz['Fecha'].dt.hour
                        df_temp_viz['dia_semana'] = df_temp_viz['Fecha'].dt.dayofweek
                        
                        if 'Interacciones' in df.columns and 'Alcance' in df.columns:
                            df_temp_viz['engagement_rate'] = (df_temp_viz['Interacciones'] / df_temp_viz['Alcance']).fillna(0)
                            
                            # Gráfico de engagement por hora
                            engagement_hora = df_temp_viz.groupby('hora')['engagement_rate'].mean().reset_index()
                            fig_hora = px.line(engagement_hora, x='hora', y='engagement_rate',
                                             title="📈 Engagement Promedio por Hora",
                                             markers=True, color_discrete_sequence=['#e91e63'])
                            fig_hora.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                            st.plotly_chart(fig_hora, use_container_width=True)
                            
                            # Heatmap por día y hora
                            heatmap_data = df_temp_viz.groupby(['dia_semana', 'hora'])['engagement_rate'].mean().reset_index()
                            heatmap_pivot = heatmap_data.pivot(index='dia_semana', columns='hora', values='engagement_rate')
                            
                            # Renombrar índices de días
                            dias_nombres = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
                            heatmap_pivot.index = [dias_nombres[i] for i in heatmap_pivot.index]
                            
                            fig_heatmap = go.Figure(data=go.Heatmap(
                                z=heatmap_pivot.values,
                                x=heatmap_pivot.columns,
                                y=heatmap_pivot.index,
                                colorscale='Purples',
                                hoverongaps=False
                            ))
                            fig_heatmap.update_layout(
                                title="🔥 Heatmap de Engagement por Día y Hora",
                                xaxis_title="Hora del día",
                                yaxis_title="Día de la semana",
                                paper_bgcolor='rgba(255,255,255,0.9)',
                                font_color='#4a148c'
                            )
                            st.plotly_chart(fig_heatmap, use_container_width=True)
            else:
                st.warning("⚠️ El modelo de optimización temporal no está disponible")

# --- TAB 3: NEXT STEPS ---
with tab3:
    st.header("🚀 Next Steps")
    st.markdown("**Descubre las próximas funcionalidades y mejoras que llegarán a Diva Digital.**")
    
    # Organizar en columnas para mejor presentación
    col_next1, col_next2 = st.columns(2)
    
    with col_next1:
        st.markdown("""
        ### 🎯 Próximas Funcionalidades
        
        #### 🤖 Inteligencia Artificial Avanzada
        - **Generador de Contenido IA**: Crear textos para publicaciones automáticamente
        - **Predicción de Tendencias**: Identificar temas que serán populares
        - **Optimización Automática**: Sugerencias de mejora en tiempo real
        
        #### 📊 Analytics Avanzados
        - **Análisis de Competencia**: Comparar rendimiento con otros perfiles
        - **Segmentación de Audiencia**: Análisis detallado de tu audiencia
        - **Tracking de Conversiones**: Seguimiento completo del customer journey
        
        #### 🛠️ Herramientas de Productividad
        - **Calendario Editorial**: Planificación y programación de contenido
        - **Colaboración en Equipo**: Gestión de múltiples usuarios
        - **Templates Personalizados**: Plantillas adaptadas a tu marca
        """)
    
    with col_next2:
        st.markdown("""
        ### 📈 Métricas Adicionales
        
        #### 💡 Nuevos KPIs
        - **Brand Awareness Score**: Medición del conocimiento de marca
        - **Engagement Quality**: Análisis cualitativo de interacciones
        - **Viral Potential**: Predicción de contenido viral
        
        #### 🔗 Integraciones
        - **APIs de Redes Sociales**: Conexión directa con plataformas
        - **CRM Integration**: Sincronización con sistemas de clientes
        - **E-commerce Platforms**: Integración con tiendas online
        
        #### 🎨 Características Visuales
        - **Editor de Imágenes IA**: Edición automática de fotos
        - **Generador de Hashtags**: Sugerencias inteligentes
        - **Video Analytics**: Análisis detallado de contenido audiovisual
        """)
    
    # Sección de roadmap
    st.markdown("---")
    st.markdown("### 🗓️ Roadmap de Desarrollo")
    
    roadmap_items = [
        {
            "trimestre": "Q1 2024",
            "titulo": "🤖 IA y Automatización",
            "descripcion": "Implementación de generación automática de contenido y optimización inteligente",
            "status": "En desarrollo"
        },
        {
            "trimestre": "Q2 2024", 
            "titulo": "📱 App Móvil",
            "descripcion": "Lanzamiento de aplicación móvil nativa para iOS y Android",
            "status": "Planificado"
        },
        {
            "trimestre": "Q3 2024",
            "titulo": "🔗 Integraciones API",
            "descripcion": "Conexiones directas con Instagram, Facebook, TikTok, LinkedIn",
            "status": "Planificado"
        },
        {
            "trimestre": "Q4 2024",
            "titulo": "🎯 Analytics Avanzados",
            "descripcion": "Dashboards personalizables y reportes automáticos",
            "status": "Planificado"
        }
    ]
    
    for item in roadmap_items:
        color = "🟢" if item["status"] == "En desarrollo" else "🔵"
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.9);padding:1em;border-radius:10px;margin:0.5em 0;border-left: 4px solid #8e24aa;'>
            <h4>{color} {item['trimestre']} - {item['titulo']}</h4>
            <p>{item['descripcion']}</p>
            <small><strong>Estado:</strong> {item['status']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Feedback section
    st.markdown("---")
    st.markdown("### 💬 Tu Opinión Nos Importa")
    
    col_feedback1, col_feedback2 = st.columns(2)
    
    with col_feedback1:
        st.markdown("#### 📝 Déjanos tu Feedback")
        feedback_tipo = st.selectbox("Tipo de feedback", [
            "Sugerencia de funcionalidad",
            "Reporte de bug",
            "Mejora de UX/UI",
            "Integración solicitada",
            "Otro"
        ])
        feedback_texto = st.text_area("Cuéntanos tu idea o experiencia", height=100)
        
        if st.button("📤 Enviar Feedback"):
            if feedback_texto:
                st.success("¡Gracias por tu feedback! Lo revisaremos pronto.")
            else:
                st.warning("Por favor, escribe tu feedback antes de enviar.")
    
    with col_feedback2:
        st.markdown("#### ⭐ Califica tu Experiencia")
        rating = st.select_slider("¿Qué tal tu experiencia con Diva Digital?", 
                                options=[1, 2, 3, 4, 5],
                                format_func=lambda x: "⭐" * x)
        
        st.markdown("#### 🎯 ¿Qué funcionalidad te gustaría ver primero?")
        feature_vote = st.radio("Vota por tu favorita:", [
            "🤖 Generador de contenido IA",
            "📱 App móvil",
            "🔗 Integraciones con redes sociales",
            "📊 Analytics más avanzados",
            "🎨 Editor de imágenes integrado"
        ])
        
        if st.button("🗳️ Votar"):
            st.success(f"¡Voto registrado! Prioridad: {feature_vote}")
    
    # Contacto y recursos
    st.markdown("---")
    st.markdown("### 📞 Mantente Conectado")
    
    col_contact1, col_contact2, col_contact3 = st.columns(3)
    
    with col_contact1:
        st.markdown("""
        #### 📧 Contacto
        - **Email**: info@divadigital.com
        - **Soporte**: support@divadigital.com
        - **Ventas**: sales@divadigital.com
        """)
    
    with col_contact2:
        st.markdown("""
        #### 🌐 Síguenos
        - **LinkedIn**: /company/diva-digital
        - **Instagram**: @divadigital_official
        - **Twitter**: @DivaDigitalApp
        """)
    
    with col_contact3:
        st.markdown("""
        #### 📚 Recursos
        - **Documentación**: docs.divadigital.com
        - **Blog**: blog.divadigital.com
        - **Webinars**: events.divadigital.com
        """)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: rgba(255,255,255,0.8); border-radius: 15px; margin-top: 2rem;'>
    <h3 style='color: #4a148c; margin-bottom: 1rem;'>💜 Diva Digital</h3>
    <p style='color: #6a1b9a; font-size: 1.1rem; margin-bottom: 1rem;'>
        <strong>Empodera tu estrategia digital con datos inteligentes</strong>
    </p>
    <p style='color: #8e24aa; font-size: 0.9rem;'>
        Desarrollado con ❤️ para marcas que buscan crecer en redes sociales
    </p>
    <p style='color: #8e24aa; font-size: 0.8rem; margin-top: 1rem;'>
        © 2024 Diva Digital. Todos los derechos reservados.
    </p>
</div>
""", unsafe_allow_html=True)