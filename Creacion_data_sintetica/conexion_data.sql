-- =====================================================
-- SCRIPT SQL PARA UNIR DATA_DEMO_OK.CSV Y PUBLICACIONES_PIXABAY_OK.CSV
-- Fecha: Julio 2025
-- Propósito: Crear base de datos unificada por id_post
-- Base de datos: SQLite/MySQL
-- =====================================================

-- =====================================================
-- CREAR TABLAS
-- =====================================================

-- Tabla para data_demo_ok.csv (métricas de rendimiento)
CREATE TABLE data_demo (
    id_post TEXT PRIMARY KEY,
    Hora TEXT,
    Canal TEXT,
    Formato TEXT,
    Alcance INTEGER,
    Interacciones INTEGER,
    Reproducciones TEXT,
    Duracion_video TEXT,
    DM INTEGER,
    Retencion TEXT,
    Visitas_perfil INTEGER,
    Link_bio INTEGER,
    Visitas_producto INTEGER,
    Carrito INTEGER,
    Compras INTEGER,
    Valor_compra REAL,
    Contacto INTEGER,
    Inversion REAL,
    ROI REAL,
    Engagement REAL,
    CPC REAL
);

-- Tabla para publicaciones_pixabay_ok.csv (información de imágenes)
CREATE TABLE publicaciones_pixabay (
    id_post TEXT PRIMARY KEY,
    Ruta TEXT,
    Fecha TEXT,
    Imagen TEXT
);

-- =====================================================
-- CARGAR DATOS (usando Python/Pandas es más fácil)
-- =====================================================

-- Ejemplo conceptual de INSERT (los datos reales se cargan con Python)
-- INSERT INTO data_demo VALUES ('POST_1', '12:00', 'Facebook', 'Imagen', 1000, 50, ...);
-- INSERT INTO publicaciones_pixabay VALUES ('POST_1', '/path/image.jpg', '2024-01-01', 'image.jpg');

-- =====================================================
-- QUERY PRINCIPAL: UNIR AMBAS TABLAS POR id_post
-- =====================================================

-- Vista unificada (equivalente a JOIN)
CREATE VIEW datos_unificados AS
SELECT 
    d.id_post,
    d.Hora,
    d.Canal,
    d.Formato,
    d.Alcance,
    d.Interacciones,
    d.Reproducciones,
    d.Duracion_video,
    d.DM,
    d.Retencion,
    d.Visitas_perfil,
    d.Link_bio,
    d.Visitas_producto,
    d.Carrito,
    d.Compras,
    d.Valor_compra,
    d.Contacto,
    d.Inversion,
    d.ROI,
    d.Engagement,
    d.CPC,
    p.Ruta,
    p.Fecha,
    p.Imagen
FROM data_demo d
INNER JOIN publicaciones_pixabay p ON d.id_post = p.id_post;

-- =====================================================
-- QUERY PARA EXPORTAR DATOS UNIFICADOS
-- =====================================================

-- Seleccionar todos los datos unidos
SELECT 
    d.id_post,
    d.Hora,
    d.Canal,
    d.Formato,
    d.Alcance,
    d.Interacciones,
    d.Reproducciones,
    d.Duracion_video,
    d.DM,
    d.Retencion,
    d.Visitas_perfil,
    d.Link_bio,
    d.Visitas_producto,
    d.Carrito,
    d.Compras,
    d.Valor_compra,
    d.Contacto,
    d.Inversion,
    d.ROI,
    d.Engagement,
    d.CPC,
    p.Ruta,
    p.Fecha,
    p.Imagen
FROM data_demo d
INNER JOIN publicaciones_pixabay p ON d.id_post = p.id_post
ORDER BY d.id_post;

-- =====================================================
-- QUERIES DE VERIFICACIÓN Y ANÁLISIS
-- =====================================================

-- Verificar número de registros en cada tabla
SELECT COUNT(*) as total_data_demo FROM data_demo;
SELECT COUNT(*) as total_publicaciones FROM publicaciones_pixabay;
SELECT COUNT(*) as total_unificados FROM datos_unificados;

-- Verificar que los id_post coinciden
SELECT COUNT(DISTINCT d.id_post) as ids_data_demo,
       COUNT(DISTINCT p.id_post) as ids_publicaciones
FROM data_demo d, publicaciones_pixabay p;

-- Mostrar muestra de datos unificados
SELECT * FROM datos_unificados LIMIT 5;

-- Análisis básico por canal
SELECT Canal, COUNT(*) as num_posts, AVG(Alcance) as alcance_promedio
FROM datos_unificados 
GROUP BY Canal 
ORDER BY alcance_promedio DESC;

-- =====================================================
-- PROCESO EQUIVALENTE EN PYTHON (más fácil para CSVs)
-- =====================================================

/*
# Python equivalente para unir los CSVs:

import pandas as pd

# Cargar los dos archivos CSV
data_demo = pd.read_csv('data_demo_ok.csv', sep=';')
publicaciones = pd.read_csv('publicaciones_pixabay_ok.csv', sep=';')

# Unir por id_post (INNER JOIN)
data_unificada = pd.merge(data_demo, publicaciones, on='id_post', how='inner')

# Guardar resultado
data_unificada.to_csv('data_unificada.csv', sep=';', index=False)

# Verificar resultado
print(f"Data demo: {len(data_demo)} filas")
print(f"Publicaciones: {len(publicaciones)} filas") 
print(f"Datos unificados: {len(data_unificada)} filas")
*/

-- =====================================================
-- NOTAS FINALES
-- =====================================================

/*
RESUMEN DEL PROCESO:

1. OBJETIVO: Unir data_demo_ok.csv + publicaciones_pixabay_ok.csv
2. CLAVE DE UNIÓN: id_post (debe existir en ambos archivos)
3. TIPO DE JOIN: INNER JOIN (solo registros que existen en ambos)
4. RESULTADO: Base de datos completa con métricas + información de imágenes

ESTRUCTURA FINAL:
- Columnas de data_demo_ok.csv: métricas de rendimiento de posts
- Columnas de publicaciones_pixabay_ok.csv: rutas de imágenes y fechas
- Total: ~25 columnas combinadas

USO POSTERIOR:
- Para análisis EDA en Jupyter notebooks
- Para aplicación Streamlit con imágenes
- Para modelos de predicción de engagement
*/
