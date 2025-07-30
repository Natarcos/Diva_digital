import streamlit as st
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import os

import plotly.express as px

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="Diva Digital", layout="wide", page_icon=":sparkles:")

# --- CARGA Y PREPARACIÓN DE DATOS ---
@st.cache_data
def load_data():
    # Directorio de datos
    data_dir = "../Data"
    
    if not os.path.exists(data_dir):
        st.error(f"No existe el directorio: {data_dir}")
        return pd.DataFrame()
    
    # Listar todos los archivos CSV disponibles
    try:
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        st.write("📁 Archivos CSV disponibles:", csv_files)
    except Exception as e:
        st.error(f"Error listando archivos: {e}")
        return pd.DataFrame()
    
    # Buscar archivo de datos principales
    data_file = None
    possible_data_files = [
        'data_demo_ok.csv',
        'data_demo.csv', 
        'datos_sinteticos.csv',
        'data_sintetica.csv',
        'publicaciones_sinteticas.csv'
    ]
    
    for file in possible_data_files:
        if file in csv_files:
            data_file = os.path.join(data_dir, file)
            st.info(f"✅ Encontrado archivo de datos: {file}")
            break
    
    if data_file is None:
        st.error("❌ No se encontró ningún archivo de datos principales")
        return pd.DataFrame()
    
    try:
        # IMPORTANTE: Usar separador punto y coma (;)
        data_demo = pd.read_csv(data_file, sep=';')
        st.success(f"📊 Datos principales cargados: {len(data_demo)} filas")
        st.write("Columnas en datos principales:", list(data_demo.columns))
        
        # Buscar archivo de publicaciones si existe
        pub_file = None
        possible_pub_files = [
            'publicaciones_pixabay_ok.csv',
            'publicaciones_pixabay.csv',
            'publicaciones_pixabay_con_rutas.csv',
            'publicaciones_pixabay_modificado.csv'
        ]
        
        for file in possible_pub_files:
            if file in csv_files:
                pub_file = os.path.join(data_dir, file)
                st.info(f"✅ Encontrado archivo de publicaciones: {file}")
                break
        
        # Si hay archivo de publicaciones, hacer merge
        if pub_file:
            try:
                publicaciones = pd.read_csv(pub_file, sep=';')
                st.success(f"🖼️ Datos de publicaciones cargados: {len(publicaciones)} filas")
                
                # Hacer merge si ambos tienen id_post
                if 'id_post' in data_demo.columns and 'id_post' in publicaciones.columns:
                    df = pd.merge(data_demo, publicaciones, on='id_post', how='left')
                    st.success(f"🔗 Merge completado: {len(df)} filas")
                else:
                    st.warning("No se puede hacer merge - usando solo datos principales")
                    df = data_demo
            except:
                st.warning("Error al cargar publicaciones - usando solo datos principales")
                df = data_demo
        else:
            df = data_demo
        
        # Convertir fechas
        if 'Fecha' in df.columns:
            try:
                df['Fecha'] = pd.to_datetime(df['Fecha'])
                st.info("📅 Columna de fecha convertida")
            except:
                st.warning("No se pudo convertir la columna Fecha")
        
        st.success(f"✅ Datos finales cargados: {len(df)} filas, {len(df.columns)} columnas")
        return df
        
    except Exception as e:
        st.error(f"❌ Error al cargar los datos: {str(e)}")
        return pd.DataFrame()

# --- FUNCIONES AUXILIARES ---
def resumen_metrics(df):
    # Calcular métricas usando TODOS los datos (sin filtrar "Sin datos")
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
            engagement = (df['Interacciones'].sum() / df['Alcance'].sum()) * 100
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

# --- MODELOS SIMPLIFICADOS ---
@st.cache_resource
def get_models(df):
    # Verificar columnas necesarias para modelos
    required_cols = ['Canal', 'Formato', 'Alcance', 'Inversion']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.error(f"No se pueden crear modelos. Faltan columnas: {missing_cols}")
        return None, None, None, None, None, None
    
    try:
        # Codificar variables categóricas
        le_canal = LabelEncoder()
        le_formato = LabelEncoder()
        df_copy = df.copy()
        
        df_copy['Canal_enc'] = le_canal.fit_transform(df_copy['Canal'])
        df_copy['Formato_enc'] = le_formato.fit_transform(df_copy['Formato'])
        
        # Modelo de regresión para alcance
        features = ['Canal_enc', 'Formato_enc', 'Inversion']
        X = df_copy[features]
        y = df_copy['Alcance']
        
        scaler = StandardScaler().fit(X)
        X_scaled = scaler.transform(X)
        
        reg = RandomForestRegressor(n_estimators=50, random_state=42).fit(X_scaled, y)
        clf_canal = RandomForestClassifier(n_estimators=50, random_state=42).fit(X_scaled, df_copy['Canal_enc'])
        clf_formato = RandomForestClassifier(n_estimators=50, random_state=42).fit(X_scaled, df_copy['Formato_enc'])
        
        st.success("✅ Modelos creados exitosamente")
        return reg, scaler, le_canal, le_formato, clf_canal, clf_formato
    
    except Exception as e:
        st.error(f"Error al crear modelos: {str(e)}")
        return None, None, None, None, None, None

# --- CARGAR DATOS ---
df = load_data()

# Verificar que los datos se cargaron correctamente
if df.empty:
    st.error("No se pudieron cargar los datos. La aplicación no puede continuar.")
    st.stop()

# --- OBTENER MODELOS ---
reg, scaler, le_canal, le_formato, clf_canal, clf_formato = get_models(df)

# Verificar que los modelos se crearon correctamente
models_ok = all(model is not None for model in [reg, scaler, le_canal, le_formato, clf_canal, clf_formato])

# --- APP STREAMLIT ---
st.title("✨ Diva Digital: Análisis de Redes Sociales para Marcas")

tab1, tab2, tab3 = st.tabs(["Informe Interanual", "Modelo Predictivo", "Next Steps"])

# --- TAB 1: INFORME INTERANUAL ---
with tab1:
    st.header("Informe Interanual")
    
    if df.empty:
        st.error("No hay datos para mostrar el informe")
    else:
        subtab1, subtab2, subtab3, subtab4, subtab5, subtab6 = st.tabs([
            "Resumen", "Visibilidad", "Interacción", "Reproducciones", "Conversión", "Retorno"
        ])

        with subtab1:
            st.subheader("Resumen")
            metrics = resumen_metrics(df)
            
            # Mostrar métricas principales
            if metrics:
                cols = st.columns(4)
                for i, (k, v) in enumerate(metrics.items()):
                    cols[i % 4].metric(k, v)
            
            st.markdown("**Resumen de los principales KPIs de la actividad en redes sociales.**")
            
            # AÑADIR GRÁFICOS AL RESUMEN
            st.markdown("---")
            
            # Fila 1: Gráficos principales
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de distribución por Canal
                if 'Canal' in df.columns:
                    posts_por_canal = df['Canal'].value_counts().reset_index()
                    posts_por_canal.columns = ['Canal', 'Número de Posts']
                    
                    fig1 = px.pie(posts_por_canal, values='Número de Posts', names='Canal',
                                title="📊 Distribución de Posts por Canal",
                                color_discrete_sequence=px.colors.qualitative.Pastel)
                    st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Gráfico de distribución por Formato
                if 'Formato' in df.columns:
                    posts_por_formato = df['Formato'].value_counts().reset_index()
                    posts_por_formato.columns = ['Formato', 'Número de Posts']
                    
                    fig2 = px.bar(posts_por_formato, x='Formato', y='Número de Posts',
                                title="📈 Posts por Formato",
                                color='Número de Posts',
                                color_continuous_scale='Blues')
                    st.plotly_chart(fig2, use_container_width=True)
            
            # Fila 2: Métricas de rendimiento
            col3, col4 = st.columns(2)
            
            with col3:
                # Gráfico de Alcance vs Interacciones por Canal
                if 'Alcance' in df.columns and 'Interacciones' in df.columns and 'Canal' in df.columns:
                    resumen_canal = df.groupby('Canal').agg({
                        'Alcance': 'sum',
                        'Interacciones': 'sum'
                    }).reset_index()
                    
                    fig3 = px.scatter(resumen_canal, x='Alcance', y='Interacciones',
                                    size='Alcance', color='Canal',
                                    title="🎯 Alcance vs Interacciones por Canal",
                                    labels={'Alcance': 'Alcance Total', 'Interacciones': 'Interacciones Totales'})
                    st.plotly_chart(fig3, use_container_width=True)
            
            with col4:
                # Gráfico de ROI por Canal
                if 'Inversion' in df.columns and 'Valor_compra' in df.columns and 'Canal' in df.columns:
                    roi_resumen = df.groupby('Canal').agg({
                        'Inversion': 'sum',
                        'Valor_compra': 'sum'
                    }).reset_index()
                    roi_resumen['ROI'] = ((roi_resumen['Valor_compra'] - roi_resumen['Inversion']) / roi_resumen['Inversion'] * 100).fillna(0)
                    
                    fig4 = px.bar(roi_resumen, x='Canal', y='ROI',
                                title="💰 ROI por Canal (%)",
                                color='ROI',
                                color_continuous_scale='RdYlGn')
                    # Añadir línea de referencia en ROI = 0
                    fig4.add_hline(y=0, line_dash="dash", line_color="red")
                    st.plotly_chart(fig4, use_container_width=True)
            
            # Fila 3: Tendencias temporales
            if 'Fecha' in df.columns:
                st.markdown("### 📅 Tendencias Temporales")
                
                col5, col6 = st.columns(2)
                
                with col5:
                    # Evolución de posts por mes
                    df_temp = df.copy()
                    df_temp['Mes'] = df_temp['Fecha'].dt.to_period('M').astype(str)
                    posts_por_mes = df_temp.groupby('Mes').size().reset_index()
                    posts_por_mes.columns = ['Mes', 'Número de Posts']
                    
                    fig5 = px.line(posts_por_mes, x='Mes', y='Número de Posts',
                                 title="📈 Evolución de Posts por Mes",
                                 markers=True)
                    st.plotly_chart(fig5, use_container_width=True)
                
                with col6:
                    # Evolución del engagement por mes
                    if 'Alcance' in df.columns and 'Interacciones' in df.columns:
                        engagement_mes = df_temp.groupby('Mes').agg({
                            'Alcance': 'sum',
                            'Interacciones': 'sum'
                        }).reset_index()
                        engagement_mes['Engagement'] = (engagement_mes['Interacciones'] / engagement_mes['Alcance'] * 100).fillna(0)
                        
                        fig6 = px.line(engagement_mes, x='Mes', y='Engagement',
                                     title="📊 Evolución del Engagement por Mes (%)",
                                     markers=True)
                        st.plotly_chart(fig6, use_container_width=True)
            
            # Fila 4: Top Performers
            st.markdown("### 🏆 Top Performers")
            
            col7, col8 = st.columns(2)
            
            with col7:
                # Top 5 posts por alcance
                if 'Alcance' in df.columns:
                    top_alcance = df.nlargest(5, 'Alcance')[['id_post', 'Canal', 'Formato', 'Alcance', 'Interacciones']]
                    st.markdown("**🎯 Top 5 Posts por Alcance**")
                    st.dataframe(top_alcance, use_container_width=True)
            
            with col8:
                # Top 5 posts por ROI
                if 'Inversion' in df.columns and 'Valor_compra' in df.columns:
                    df_roi_top = df.copy()
                    df_roi_top['ROI'] = ((df_roi_top['Valor_compra'] - df_roi_top['Inversion']) / df_roi_top['Inversion'] * 100).fillna(0)
                    top_roi = df_roi_top.nlargest(5, 'ROI')[['id_post', 'Canal', 'Formato', 'ROI', 'Valor_compra']]
                    st.markdown("**💰 Top 5 Posts por ROI**")
                    st.dataframe(top_roi, use_container_width=True)
            
            # Resumen ejecutivo
            st.markdown("---")
            st.markdown("### 📋 Resumen Ejecutivo")
            
            # Calcular insights automáticos
            if metrics:
                mejor_canal = df['Canal'].value_counts().index[0] if 'Canal' in df.columns else "N/A"
                mejor_formato = df['Formato'].value_counts().index[0] if 'Formato' in df.columns else "N/A"
                
                # ROI promedio
                if 'Inversion' in df.columns and 'Valor_compra' in df.columns:
                    roi_promedio = ((df['Valor_compra'].sum() - df['Inversion'].sum()) / df['Inversion'].sum() * 100) if df['Inversion'].sum() > 0 else 0
                else:
                    roi_promedio = 0
                
                # Engagement promedio
                if 'Alcance' in df.columns and 'Interacciones' in df.columns:
                    engagement_promedio = (df['Interacciones'].sum() / df['Alcance'].sum() * 100) if df['Alcance'].sum() > 0 else 0
                else:
                    engagement_promedio = 0
                
                st.info(f"""
                🎯 **Canal más activo:** {mejor_canal}  
                📱 **Formato predominante:** {mejor_formato}  
                💰 **ROI promedio:** {roi_promedio:.1f}%  
                ❤️ **Engagement promedio:** {engagement_promedio:.2f}%  
                📊 **Total de publicaciones:** {len(df)}
                """)

        with subtab2:
            st.subheader("Visibilidad")
            
            if 'Alcance' in df.columns:
                # Usar TODOS los datos (sin filtrar)
                if 'Canal' in df.columns:
                    # Gráfico de alcance por canal
                    alcance_canal = df.groupby('Canal')['Alcance'].mean().reset_index()
                    fig = px.bar(alcance_canal, x='Canal', y='Alcance',
                               title="Alcance promedio por Canal")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Métricas de visibilidad
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Alcance Total", f"{df['Alcance'].sum():,.0f}")
                    col2.metric("Alcance Promedio", f"{df['Alcance'].mean():.0f}")
                    col3.metric("Total de posts", f"{len(df)}")
                else:
                    st.warning("No hay datos válidos de alcance para mostrar")
            else:
                st.warning("No se encontró columna de alcance")

        with subtab3:
            st.subheader("Interacción")
            
            if 'Interacciones' in df.columns:
                # Usar TODOS los datos (sin filtrar)
                if 'Formato' in df.columns:
                    # Gráfico de interacciones por formato
                    fig = px.box(df, x='Formato', y='Interacciones',
                               title="Distribución de Interacciones por Formato")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Gráfico adicional: Interacciones por Canal
                    if 'Canal' in df.columns:
                        interac_canal = df.groupby('Canal')['Interacciones'].mean().reset_index()
                        fig2 = px.pie(interac_canal, values='Interacciones', names='Canal',
                                    title="Distribución de Interacciones por Canal")
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    # Métricas
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Interacciones Totales", f"{df['Interacciones'].sum():,.0f}")
                    col2.metric("Interacciones Promedio", f"{df['Interacciones'].mean():.0f}")
                    col3.metric("Total de posts", f"{len(df)}")
                else:
                    st.warning("No hay datos válidos de interacciones para mostrar")
            else:
                st.warning("No se encontró columna de interacciones")

        with subtab4:
            st.subheader("Reproducciones de Video")
            
            if 'Reproducciones' in df.columns:
                # AQUÍ SÍ filtramos: solo Reels con datos válidos
                df_video = df[df['Formato'] == 'Reel'].copy()
                df_video_con_datos = df_video[df_video['Reproducciones'] != 'Sin datos'].copy()
                
                if not df_video_con_datos.empty:
                    # Convertir a numérico
                    df_video_con_datos['Reproducciones'] = pd.to_numeric(df_video_con_datos['Reproducciones'], errors='coerce')
                    df_video_con_datos = df_video_con_datos.dropna(subset=['Reproducciones'])
                    
                    if not df_video_con_datos.empty:
                        # Gráfico de reproducciones por canal (solo Reels)
                        if 'Canal' in df_video_con_datos.columns:
                            repro_canal = df_video_con_datos.groupby('Canal')['Reproducciones'].mean().reset_index()
                            fig = px.bar(repro_canal, x='Canal', y='Reproducciones',
                                       title="Reproducciones promedio por Canal (solo Reels)")
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Análisis de duración vs reproducciones
                        if 'Duracion_video' in df_video_con_datos.columns:
                            df_duracion = df_video_con_datos[df_video_con_datos['Duracion_video'] != 'Sin datos'].copy()
                            if not df_duracion.empty:
                                df_duracion['Duracion_video'] = pd.to_numeric(df_duracion['Duracion_video'], errors='coerce')
                                df_duracion = df_duracion.dropna(subset=['Duracion_video'])
                                
                                if not df_duracion.empty:
                                    fig2 = px.scatter(df_duracion, x='Duracion_video', y='Reproducciones',
                                                    color='Canal', title="Duración vs Reproducciones (Reels)",
                                                    labels={'Duracion_video': 'Duración (segundos)', 'Reproducciones': 'Reproducciones'})
                                    st.plotly_chart(fig2, use_container_width=True)
                        
                        # Análisis de retención vs reproducciones
                        if 'Retencion' in df_video_con_datos.columns:
                            df_retencion = df_video_con_datos[df_video_con_datos['Retencion'] != 'Sin datos'].copy()
                            if not df_retencion.empty:
                                df_retencion['Retencion'] = pd.to_numeric(df_retencion['Retencion'], errors='coerce')
                                df_retencion = df_retencion.dropna(subset=['Retencion'])
                                
                                # Filtrar Duracion_video a valores numéricos válidos y no nulos
                                if 'Duracion_video' in df_retencion.columns:
                                    df_retencion = df_retencion[df_retencion['Duracion_video'] != 'Sin datos'].copy()
                                    df_retencion['Duracion_video'] = pd.to_numeric(df_retencion['Duracion_video'], errors='coerce')
                                    df_retencion = df_retencion.dropna(subset=['Duracion_video'])
                                
                                if not df_retencion.empty:
                                    fig3 = px.scatter(df_retencion, x='Retencion', y='Reproducciones',
                                                    color='Canal', size='Duracion_video',
                                                    title="Retención vs Reproducciones (Reels)",
                                                    labels={'Retencion': 'Retención (%)', 'Reproducciones': 'Reproducciones'})
                                    st.plotly_chart(fig3, use_container_width=True)
                        
                        # Métricas de video
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Reproducciones Totales", f"{df_video_con_datos['Reproducciones'].sum():,.0f}")
                        col2.metric("Reproducciones Promedio", f"{df_video_con_datos['Reproducciones'].mean():.0f}")
                        col3.metric("Reels con datos", f"{len(df_video_con_datos)}")
                        col4.metric("Total Reels", f"{len(df_video)}")
                        
                        # Tabla top performers
                        st.subheader("Top 5 Reels por Reproducciones")
                        top_reels = df_video_con_datos.nlargest(5, 'Reproducciones')[['id_post', 'Canal', 'Reproducciones', 'Retencion', 'Duracion_video']]
                        st.dataframe(top_reels, use_container_width=True)
                    else:
                        st.info("No hay datos numéricos válidos de reproducciones")
                else:
                    st.info("No hay Reels con datos de reproducciones disponibles")
            else:
                st.info("No hay datos de reproducciones disponibles")

        with subtab5:
            st.subheader("Conversión")
            
            if 'Compras' in df.columns:
                # Usar TODOS los datos (sin filtrar)
                if 'Canal' in df.columns:
                    # Gráfico de compras por canal
                    compras_canal = df.groupby('Canal')['Compras'].sum().reset_index()
                    fig = px.pie(compras_canal, values='Compras', names='Canal',
                               title="Distribución de Compras por Canal")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Embudo de conversión (usando todos los datos)
                if all(col in df.columns for col in ['Visitas_producto', 'Carrito', 'Compras']):
                    embudo_data = {
                        'Etapa': ['Visitas Producto', 'Añadido a Carrito', 'Compras'],
                        'Cantidad': [
                            df['Visitas_producto'].sum(),
                            df['Carrito'].sum(),
                            df['Compras'].sum()
                        ]
                    }
                    fig2 = px.funnel(pd.DataFrame(embudo_data), x='Cantidad', y='Etapa',
                                   title="Embudo de Conversión")
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Métricas
                col1, col2, col3 = st.columns(3)
                col1.metric("Compras Totales", f"{df['Compras'].sum():.0f}")
                col2.metric("Compras Promedio", f"{df['Compras'].mean():.1f}")
                col3.metric("Posts con ventas", f"{len(df[df['Compras'] > 0])}")
            else:
                st.info("No hay datos de compras disponibles")

        with subtab6:
            st.subheader("Retorno")
            
            # Usar TODOS los datos para ROI (sin filtrar)
            if 'Inversion' in df.columns and 'Valor_compra' in df.columns:
                # Calcular ROI por registro
                df_roi = df.copy()
                df_roi['ROI_calc'] = ((df_roi['Valor_compra'] - df_roi['Inversion']) / df_roi['Inversion'] * 100).fillna(0)
                
                # Gráfico de ROI por canal
                if 'Canal' in df_roi.columns:
                    roi_canal = df_roi.groupby('Canal').agg({
                        'Inversion': 'sum',
                        'Valor_compra': 'sum'
                    }).reset_index()
                    roi_canal['ROI'] = ((roi_canal['Valor_compra'] - roi_canal['Inversion']) / roi_canal['Inversion'] * 100).fillna(0)
                    
                    fig = px.bar(roi_canal, x='Canal', y='ROI',
                               title="ROI por Canal (%)",
                               color='ROI',
                               color_continuous_scale='RdYlGn')
                    st.plotly_chart(fig, use_container_width=True)
                
                # Gráfico de inversión vs ingresos (CORREGIDO)
                # Crear columna de tamaño absoluto para evitar valores negativos
                df_roi['ROI_size'] = abs(df_roi['ROI_calc']) + 1  # +1 para evitar tamaño 0
                
                fig2 = px.scatter(df_roi, x='Inversion', y='Valor_compra',
                                color='Canal', 
                                size='ROI_size',  # Usar valores absolutos
                                hover_data={'ROI_calc': ':.1f'},  # Mostrar ROI real en hover
                                title="Inversión vs Ingresos por Canal",
                                labels={'Inversion': 'Inversión (€)', 'Valor_compra': 'Ingresos (€)'})
                st.plotly_chart(fig2, use_container_width=True)
                
                # Gráfico adicional: ROI vs Alcance
                if 'Alcance' in df_roi.columns:
                    fig3 = px.scatter(df_roi, x='Alcance', y='ROI_calc',
                                    color='Canal', 
                                    title="Alcance vs ROI por Canal",
                                    labels={'Alcance': 'Alcance', 'ROI_calc': 'ROI (%)'})
                    # Añadir línea horizontal en ROI = 0
                    fig3.add_hline(y=0, line_dash="dash", line_color="red", 
                                  annotation_text="ROI = 0%")
                    st.plotly_chart(fig3, use_container_width=True)
                
                # Métricas
                total_inversion = df_roi['Inversion'].sum()
                total_ingresos = df_roi['Valor_compra'].sum()
                roi_total = ((total_ingresos - total_inversion) / total_inversion * 100) if total_inversion > 0 else 0
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Inversión Total", f"€{total_inversion:,.2f}")
                col2.metric("Ingresos Totales", f"€{total_ingresos:,.2f}")
                col3.metric("ROI Total", f"{roi_total:.1f}%")
                col4.metric("Posts rentables", f"{len(df_roi[df_roi['ROI_calc'] > 0])}")
                
                # Tabla de análisis de rentabilidad
                st.subheader("Análisis de Rentabilidad")
                
                # Crear categorías de ROI
                def categorizar_roi(roi):
                    if roi > 50:
                        return "Muy Rentable (>50%)"
                    elif roi > 0:
                        return "Rentable (0-50%)"
                    elif roi > -25:
                        return "Pérdida Moderada (-25% a 0%)"
                    else:
                        return "Pérdida Alta (<-25%)"
                
                df_roi['Categoria_ROI'] = df_roi['ROI_calc'].apply(categorizar_roi)
                
                # Resumen por categoría
                resumen_roi = df_roi.groupby('Categoria_ROI').agg({
                    'id_post': 'count',
                    'Inversion': 'sum',
                    'Valor_compra': 'sum',
                    'ROI_calc': 'mean'
                }).round(2)
                resumen_roi.columns = ['Número de Posts', 'Inversión Total', 'Ingresos Totales', 'ROI Promedio']
                
                st.dataframe(resumen_roi, use_container_width=True)
                
            else:
                st.info("No hay datos de ROI disponibles")

# --- TAB 2: MODELO PREDICTIVO ---
with tab2:
    st.header("Modelo Predictivo")
    
    if not models_ok:
        st.error("Los modelos predictivos no están disponibles debido a problemas con los datos.")
    else:
        st.markdown("Predice el rendimiento de tus publicaciones en redes sociales.")

        # Buscar las columnas correctas para los selectbox
        canal_col = None
        formato_col = None
        
        for col in ['Canal', 'canal', 'Channel']:
            if col in df.columns:
                canal_col = col
                break
        
        for col in ['Formato', 'formato', 'Format']:
            if col in df.columns:
                formato_col = col
                break

        if canal_col and formato_col:
            # Inputs usuario
            fecha = st.date_input("Fecha de publicación", value=datetime.now())
            hora = st.time_input("Hora de publicación", value=datetime.now().time())
            canal = st.selectbox("Canal", df[canal_col].unique())
            formato = st.selectbox("Formato", df[formato_col].unique())
            inversion = st.number_input("Inversión (€)", min_value=0.0, value=10.0, step=1.0)

            # Codificar inputs
            try:
                canal_enc = le_canal.transform([canal])[0]
                formato_enc = le_formato.transform([formato])[0]
                X_pred = scaler.transform([[canal_enc, formato_enc, inversion]])

                # Predicciones
                alcance_pred = reg.predict(X_pred)[0]
                canal_pred = le_canal.inverse_transform(clf_canal.predict(X_pred))[0]
                formato_pred = le_formato.inverse_transform(clf_formato.predict(X_pred))[0]

                st.subheader("Predicción de Resultados")
                col1, col2, col3 = st.columns(3)
                col1.metric("Alcance estimado", f"{int(alcance_pred):,}")
                col2.metric("Canal recomendado", canal_pred)
                col3.metric("Formato recomendado", formato_pred)
                
            except Exception as e:
                st.error(f"Error en las predicciones: {str(e)}")
        else:
            st.error("No se encontraron las columnas necesarias para hacer predicciones")

        # Computer Vision DEMO (simulado)
        st.subheader("Análisis de Imagen (DEMO)")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Temática detectada:** Moda")
            st.write("**Objetos detectados:** Persona, Ropa, Accesorios")
            st.write("**Paleta de colores:** Rosa, Blanco, Negro")
        with col2:
            st.image("https://cdn.pixabay.com/photo/2016/03/27/18/10/bear-1283347_1280.jpg", width=200)

        st.info("💡 **Nota:** El análisis de imágenes es una simulación. Para producción, integrar modelo de Computer Vision.")

# --- TAB 3: NEXT STEPS ---
with tab3:
    st.header("Next Steps")
    st.markdown("""
    ### 🎯 Conclusiones y Recomendaciones

    #### 📊 **Optimización de Canales**
    - **Canales más efectivos:** Priorizar los canales que han mostrado mayor alcance y engagement
    - **Diversificación:** Explorar nuevos canales con potencial de crecimiento
    - **Horarios óptimos:** Analizar patrones temporales para maximizar la visibilidad

    #### 💰 **Gestión de Inversión**
    - **ROI por canal:** Ajustar la inversión hacia los posts y formatos con mejor retorno
    - **Presupuesto dinámico:** Redistribuir recursos según performance histórica
    - **Optimización de costes:** Identificar oportunidades de ahorro sin perder efectividad

    #### 🎥 **Contenido Audiovisual**
    - **Retención en vídeos:** Analizar los vídeos con mayor retención y replicar características
    - **Formatos innovadores:** Experimentar con nuevos tipos de contenido
    - **Duración óptima:** Ajustar la duración según el comportamiento de la audiencia

    #### 🔄 **Conversión y Engagement**
    - **Call-to-actions:** Mejorar las llamadas a la acción en posts de alta visibilidad
    - **Interacción:** Fomentar la participación activa de la comunidad
    - **Seguimiento:** Implementar tracking avanzado para medir conversiones

    #### 🤖 **Tecnología e Innovación**
    - **Computer Vision:** Integrar análisis automático de imágenes para optimizar contenido visual
    - **Machine Learning:** Implementar modelos predictivos más sofisticados
    - **Automatización:** Desarrollar flujos de trabajo automatizados para eficiencia

    #### 📈 **Monitorización Continua**
    - **KPIs clave:** Revisar mensualmente métricas críticas
    - **Tendencias:** Adaptar estrategia según cambios en el comportamiento digital
    - **Benchmarking:** Comparar performance con competidores del sector

    ---
    
    ### 🌟 **Próximos Pasos Inmediatos**

    1. **Implementar recomendaciones de canales más efectivos**
    2. **Ajustar presupuesto según análisis de ROI**
    3. **Desarrollar calendario de contenidos optimizado**
    4. **Configurar alertas automáticas para KPIs críticos**
    5. **Planificar iteraciones mensuales del modelo predictivo**

    ---

    _💎 **Diva Digital** te ayuda a tomar decisiones basadas en datos para maximizar el impacto de tu marca en redes sociales._
    """)

# --- SIDEBAR ---
st.sidebar.image("https://cdn.pixabay.com/photo/2017/01/06/19/15/soap-bubble-1958650_1280.jpg", width=200)
st.sidebar.title("💎 Diva Digital")
st.sidebar.markdown("**App de análisis y predicción para redes sociales**")

# Información adicional en sidebar
if not df.empty:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Resumen de Datos")
    st.sidebar.metric("Total de registros", len(df))
    st.sidebar.metric("Columnas disponibles", len(df.columns))
    
    # Rango de fechas si existe columna de fecha
    for col in ['Fecha', 'fecha', 'Date']:
        if col in df.columns:
            try:
                fecha_min = df[col].min().strftime('%Y-%m-%d')
                fecha_max = df[col].max().strftime('%Y-%m-%d')
                st.sidebar.text(f"Periodo: {fecha_min} a {fecha_max}")
                break
            except:
                continue

st.sidebar.markdown("---")
st.sidebar.markdown("*Desarrollado con ❤️ para optimizar tu presencia digital*")