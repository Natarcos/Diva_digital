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

# AÑADIR ESTAS FUNCIONES AQUÍ (DESPUÉS DE LAS IMPORTACIONES)

@st.cache_data
def generar_planificacion_mensual(canal, posts_semana, mes, año, inversion, incluir_fines, 
                                priorizar_engagement, hora_inicio, hora_fin, df, _modelo_temporal, 
                                _le_formato_temporal, _reg, _scaler, _le_canal, _le_formato):
    """
    Genera una planificación mensual inteligente usando los modelos predictivos
    """
    try:
        import calendar
        from datetime import datetime, timedelta
        
        # Obtener días del mes
        num_dias = calendar.monthrange(año, mes)[1]
        primer_dia = datetime(año, mes, 1)
        
        # Calcular total de publicaciones para el mes
        semanas_en_mes = (num_dias + primer_dia.weekday()) / 7
        total_publicaciones = int(posts_semana * semanas_en_mes)
        
        # Generar datos históricos para el canal seleccionado
        df_canal = df[df['Canal'] == canal].copy() if 'Canal' in df.columns else df.copy()
        
        # Obtener mejores horarios históricos
        if len(df_canal) > 0 and 'Fecha' in df_canal.columns:
            df_canal['hora'] = df_canal['Fecha'].dt.hour
            df_canal['dia_semana'] = df_canal['Fecha'].dt.dayofweek
            
            if 'Interacciones' in df_canal.columns and 'Alcance' in df_canal.columns:
                df_canal['engagement_rate'] = (df_canal['Interacciones'] / df_canal['Alcance']).fillna(0)
                mejores_horas = df_canal.groupby('hora')['engagement_rate'].mean().sort_values(ascending=False)
                mejores_dias = df_canal.groupby('dia_semana')['engagement_rate'].mean().sort_values(ascending=False)
            else:
                mejores_horas = pd.Series({9: 0.05, 12: 0.06, 15: 0.055, 18: 0.07, 20: 0.045})
                mejores_dias = pd.Series({0: 0.055, 1: 0.06, 2: 0.065, 3: 0.07, 4: 0.06, 5: 0.045, 6: 0.04})
        else:
            mejores_horas = pd.Series({9: 0.05, 12: 0.06, 15: 0.055, 18: 0.07, 20: 0.045})
            mejores_dias = pd.Series({0: 0.055, 1: 0.06, 2: 0.065, 3: 0.07, 4: 0.06, 5: 0.045, 6: 0.04})
        
        # Filtrar horarios según preferencias del usuario
        hora_inicio_int = hora_inicio.hour
        hora_fin_int = hora_fin.hour
        mejores_horas = mejores_horas[(mejores_horas.index >= hora_inicio_int) & (mejores_horas.index <= hora_fin_int)]
        
        # Filtrar días si no incluir fines de semana
        if not incluir_fines:
            mejores_dias = mejores_dias[mejores_dias.index < 5]
        
        # Generar planificación
        planificacion = []
        dias_utilizados = set()
        
        # Temáticas disponibles
        tematicas_disponibles = [
            'moda_lifestyle', 'arte_diseño', 'naturaleza_bienestar', 
            'tecnologia', 'comida_gastronomia', 'lifestyle_inspiracional', 'general'
        ]
        
        # Mapeo de temáticas
        mapeo_tematicas = {
            'moda_lifestyle': 'Moda & Lifestyle',
            'arte_diseño': 'Arte & Diseño',
            'naturaleza_bienestar': 'Naturaleza & Bienestar',
            'tecnologia': 'Tecnología',
            'comida_gastronomia': 'Comida & Gastronomía',
            'lifestyle_inspiracional': 'Lifestyle Inspiracional',
            'general': 'General'
        }
        
        for i in range(total_publicaciones):
            # Seleccionar día óptimo
            dias_disponibles = []
            for dia in range(1, num_dias + 1):
                fecha_candidata = datetime(año, mes, dia)
                dia_semana = fecha_candidata.weekday()
                
                # Verificar si el día es válido según configuración
                if not incluir_fines and dia_semana >= 5:
                    continue
                
                # Evitar saturar días (máximo 1 post por día)
                if fecha_candidata.date() in dias_utilizados:
                    continue
                
                # Calcular score del día
                score_dia = mejores_dias.get(dia_semana, 0.03)
                dias_disponibles.append((dia, dia_semana, score_dia, fecha_candidata))
            
            if not dias_disponibles:
                break
            
            # Seleccionar mejor día disponible
            if priorizar_engagement:
                dias_disponibles.sort(key=lambda x: x[2], reverse=True)
            else:
                dias_disponibles.sort(key=lambda x: x[0])
            
            dia_seleccionado, dia_semana_sel, score_dia, fecha_sel = dias_disponibles[0]
            
            # Seleccionar mejor hora
            if priorizar_engagement:
                hora_seleccionada = mejores_horas.index[0] if len(mejores_horas) > 0 else 12
            else:
                horas_ordenadas = list(mejores_horas.index)
                hora_seleccionada = horas_ordenadas[i % len(horas_ordenadas)] if horas_ordenadas else 12
            
            # Predecir formato óptimo
            try:
                X_temp = np.array([[hora_seleccionada, dia_semana_sel, mes, inversion]])
                formato_pred = _modelo_temporal.predict(X_temp)[0]
                formato_recomendado = _le_formato_temporal.inverse_transform([formato_pred])[0]
            except:
                formatos_disponibles = df['Formato'].unique().tolist() if 'Formato' in df.columns else ['Imagen', 'Reel', 'Carrusel']
                formato_recomendado = formatos_disponibles[i % len(formatos_disponibles)]
            
            # Predecir alcance esperado
            try:
                canal_enc = _le_canal.transform([canal])[0]
                formato_enc = _le_formato.transform([formato_recomendado])[0]
                X_pred = np.array([[canal_enc, formato_enc, inversion]])
                X_pred_scaled = _scaler.transform(X_pred)
                alcance_predicho = int(_reg.predict(X_pred_scaled)[0])
            except:
                alcance_predicho = 5000
            
            # Seleccionar temática (rotar entre disponibles)
            tematica_seleccionada = tematicas_disponibles[i % len(tematicas_disponibles)]
            tematica_nombre = mapeo_tematicas.get(tematica_seleccionada, 'General')
            
            # Crear entrada de planificación
            entrada = {
                'fecha': fecha_sel,
                'dia': dia_seleccionado,
                'dia_semana': dia_semana_sel,
                'dia_nombre': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][dia_semana_sel],
                'hora': hora_seleccionada,
                'canal': canal,
                'formato': formato_recomendado,
                'tematica': tematica_nombre,  # ← ESTE ES EL CAMPO QUE FALTABA
                'tematica_code': tematica_seleccionada,
                'inversion': inversion,
                'alcance_predicho': alcance_predicho,
                'engagement_esperado': int(alcance_predicho * 0.035),
                'score_temporal': score_dia
            }
            
            planificacion.append(entrada)
            dias_utilizados.add(fecha_sel.date())
        
        return planificacion
        
    except Exception as e:
        st.error(f"Error generando planificación: {str(e)}")
        return []

def mostrar_calendario_planificacion(planificacion, mes, año):
    """
    Muestra un calendario visual con las publicaciones planificadas incluyendo temática
    """
    import calendar
    
    # Crear calendario del mes
    cal = calendar.monthcalendar(año, mes)
    mes_nombre = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][mes]
    
    st.markdown(f"#### 📅 {mes_nombre} {año}")
    
    # Crear diccionario de publicaciones por día
    publicaciones_por_dia = {}
    for pub in planificacion:
        dia = pub['dia']
        if dia not in publicaciones_por_dia:
            publicaciones_por_dia[dia] = []
        publicaciones_por_dia[dia].append(pub)
    
    # Mapeo de emojis por temática
    emoji_tematicas = {
        'Moda & Lifestyle': '👗',
        'Arte & Diseño': '🎨', 
        'Naturaleza & Bienestar': '🌿',
        'Tecnología': '💻',
        'Comida & Gastronomía': '🍽️',
        'Lifestyle Inspiracional': '✨',
        'General': '📝'
    }
    
    # Mostrar calendario
    dias_semana = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    
    # Encabezados de días
    cols_header = st.columns(7)
    for i, dia in enumerate(dias_semana):
        cols_header[i].markdown(f"**{dia}**")
    
    # Mostrar semanas
    for semana in cal:
        cols = st.columns(7)
        for i, dia in enumerate(semana):
            if dia == 0:
                cols[i].markdown("")
            else:
                with cols[i]:
                    if dia in publicaciones_por_dia:
                        # Día con publicación
                        pub = publicaciones_por_dia[dia][0]  # Primera publicación del día
                        
                        # Color por formato
                        color = "#8e24aa" if pub['formato'] == 'Reel' else "#e91e63" if pub['formato'] == 'Imagen' else "#f06292"
                        
                        # Emoji por temática
                        emoji_tematica = emoji_tematicas.get(pub['tematica'], '📝')
                        
                        # Abreviatura del formato
                        formato_abrev = pub['formato'][:4] if len(pub['formato']) <= 4 else pub['formato'][:3] + "."
                        
                        st.markdown(f"""
                        <div style='background-color: {color}; color: white; padding: 0.3rem; border-radius: 8px; text-align: center; margin-bottom: 0.2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                            <strong style='font-size: 0.9rem;'>{dia}</strong><br>
                            <small style='font-size: 0.7rem;'>{pub['hora']}:00</small><br>
                            <small style='font-size: 0.7rem;'>{formato_abrev}</small><br>
                            <span style='font-size: 0.8rem;'>{emoji_tematica}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Tooltip con información completa
                        with st.expander(f"ℹ️", expanded=False):
                            st.write(f"**🕐 Hora:** {pub['hora']}:00")
                            st.write(f"**🎨 Formato:** {pub['formato']}")
                            st.write(f"**🏷️ Temática:** {pub['tematica']}")
                            st.write(f"**📱 Canal:** {pub['canal']}")
                            st.write(f"**💰 Inversión:** {pub['inversion']:.0f}€")
                            st.write(f"**👁️ Alcance esperado:** {pub['alcance_predicho']:,}")
                    else:
                        # Día sin publicación
                        st.markdown(f"""
                        <div style='background-color: #f5f5f5; color: #666; padding: 0.3rem; border-radius: 8px; text-align: center; margin-bottom: 0.2rem; min-height: 60px; display: flex; align-items: center; justify-content: center;'>
                            <strong>{dia}</strong>
                        </div>
                        """, unsafe_allow_html=True)
    
    # Leyenda del calendario
    st.markdown("---")
    st.markdown("#### 🎨 Leyenda del Calendario")
    
    col_leyenda1, col_leyenda2 = st.columns(2)
    
    with col_leyenda1:
        st.markdown("**Colores por Formato:**")
        st.markdown("🟣 **Morado** = Reel")
        st.markdown("🩷 **Rosa** = Imagen") 
        st.markdown("🌸 **Rosa claro** = Carrusel")
    
    with col_leyenda2:
        st.markdown("**Emojis por Temática:**")
        for tematica, emoji in emoji_tematicas.items():
            st.markdown(f"{emoji} **{tematica}**")

def mostrar_tabla_planificacion(planificacion):
    """
    Muestra una tabla detallada de la planificación
    """
    if not planificacion:
        st.warning("No hay planificación generada")
        return
    
    # Convertir a DataFrame para mejor visualización
    df_plan = pd.DataFrame(planificacion)
    
    # Formatear para mostrar
    df_display = df_plan.copy()
    df_display['Fecha'] = df_display['fecha'].dt.strftime('%d/%m/%Y')
    df_display['Día'] = df_display['dia_nombre']
    df_display['Hora'] = df_display['hora'].apply(lambda x: f"{x:02d}:00")
    df_display['Canal'] = df_display['canal']
    df_display['Formato'] = df_display['formato']
    df_display['Temática'] = df_display['tematica']
    df_display['Inversión'] = df_display['inversion'].apply(lambda x: f"{x:.0f}€")
    df_display['Alcance Predicho'] = df_display['alcance_predicho'].apply(lambda x: f"{x:,}")
    df_display['Engagement Esperado'] = df_display['engagement_esperado'].apply(lambda x: f"{x:,}")
    
    # NUEVO: Añadir información de temática si está disponible
    if 'tematica_score' in df_display.columns:
        df_display['Score Temática'] = df_display['tematica_score'].apply(lambda x: f"{x:.2f}")
    
    # Seleccionar columnas para mostrar
    columnas_mostrar = ['Fecha', 'Día', 'Hora', 'Canal', 'Formato', 'Temática', 'Inversión', 'Alcance Predicho', 'Engagement Esperado']
    
    # Añadir columna de score si existe
    if 'Score Temática' in df_display.columns:
        columnas_mostrar.append('Score Temática')
    
    df_final = df_display[columnas_mostrar].reset_index(drop=True)
    df_final.index += 1
    
    st.dataframe(df_final, use_container_width=True)
    
    # NUEVO: Mostrar información sobre la fuente de temáticas
    if 'fuente_tematica' in df_plan.columns:
        fuente = df_plan['fuente_tematica'].iloc[0]
        if fuente == "Computer Vision":
            st.success(f"✨ **Temáticas optimizadas**: Basadas en análisis de Computer Vision de tu contenido histórico")
        elif fuente == "Análisis histórico + CV":
            st.info(f"🔍 **Temáticas inteligentes**: Combinando Computer Vision con datos de rendimiento histórico")
        else:
            st.info(f"📊 **Temáticas**: {fuente}")

def mostrar_estadisticas_planificacion(planificacion):
    """
    Muestra estadísticas resumidas de la planificación
    """
    if not planificacion:
        return
    
    df_plan = pd.DataFrame(planificacion)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_posts = len(planificacion)
        st.metric("📊 Total Posts", total_posts)
    
    with col2:
        inversion_total = df_plan['inversion'].sum()
        st.metric("💰 Inversión Total", f"{inversion_total:.0f}€")
    
    with col3:
        alcance_total = df_plan['alcance_predicho'].sum()
        st.metric("👁️ Alcance Esperado", f"{alcance_total:,}")
    
    with col4:
        engagement_total = df_plan['engagement_esperado'].sum()
        st.metric("❤️ Engagement Esperado", f"{engagement_total:,}")
    
    # Distribución por formato
    st.markdown("#### 📊 Distribución por Formato")
    formato_dist = df_plan['formato'].value_counts()
    fig_formato = px.pie(values=formato_dist.values, names=formato_dist.index,
                        title="Distribución de Formatos Planificados",
                        color_discrete_sequence=px.colors.sequential.Purples)
    fig_formato.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
    st.plotly_chart(fig_formato, use_container_width=True)
    
    # Distribución por día de la semana
    col_dist1, col_dist2 = st.columns(2)
    
    with col_dist1:
        st.markdown("#### 📅 Posts por Día de la Semana")
        dia_dist = df_plan['dia_nombre'].value_counts()
        fig_dias = px.bar(x=dia_dist.index, y=dia_dist.values,
                        title="Posts por Día de la Semana",
                        color=dia_dist.values,
                        color_continuous_scale='Purples')
        fig_dias.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c', showlegend=False)
        st.plotly_chart(fig_dias, use_container_width=True)
    
    with col_dist2:
        st.markdown("#### ⏰ Posts por Hora")
        hora_dist = df_plan['hora'].value_counts().sort_index()
        fig_horas = px.bar(x=hora_dist.index, y=hora_dist.values,
                        title="Posts por Hora del Día",
                        color=hora_dist.values,
                        color_continuous_scale='Pinkyl')
        fig_horas.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c', showlegend=False)
        st.plotly_chart(fig_horas, use_container_width=True)
        
    # NUEVO: Análisis de temáticas
    if 'tematica' in df_plan.columns:
        st.markdown("---")
        st.markdown("#### 🏷️ Distribución de Temáticas (Computer Vision)")
        
        col_tema1, col_tema2 = st.columns(2)
        
        with col_tema1:
            # Gráfico de distribución de temáticas
            tema_dist = df_plan['tematica'].value_counts()
            fig_temas = px.pie(
                values=tema_dist.values, 
                names=tema_dist.index,
                title="🏷️ Temáticas Planificadas",
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            fig_temas.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
            st.plotly_chart(fig_temas, use_container_width=True)
        
        with col_tema2:
            # Mostrar scores de temáticas si están disponibles
            if 'tematica_score' in df_plan.columns:
                st.markdown("##### 🎯 Scores de Temáticas")
                tema_scores = df_plan.groupby('tematica')['tematica_score'].mean().sort_values(ascending=False)
                
                for tema, score in tema_scores.items():
                    color = "🟢" if score > 0.6 else "🟡" if score > 0.4 else "🔴"
                    st.write(f"{color} **{tema}**: {score:.2f}")
            
            # Mostrar temática más frecuente
            tema_principal = tema_dist.index[0]
            frecuencia_principal = (tema_dist.iloc[0] / len(df_plan)) * 100
            st.metric("🏆 Temática Principal", tema_principal, f"{frecuencia_principal:.1f}% del contenido")

def convertir_planificacion_csv(planificacion):
    """
    Convierte la planificación a formato CSV para descarga
    """
    df_plan = pd.DataFrame(planificacion)
    
    # Preparar datos para CSV
    df_csv = df_plan.copy()
    df_csv['Fecha'] = df_csv['fecha'].dt.strftime('%d/%m/%Y')
    df_csv['Hora'] = df_csv['hora'].apply(lambda x: f"{x:02d}:00")
    
    # Seleccionar y renombrar columnas
    columnas_csv = {
        'Fecha': 'fecha',
        'Día': 'dia_nombre', 
        'Hora': 'Hora',
        'Canal': 'canal',
        'Formato': 'formato',
        'Temática': 'tematica',
        'Inversión_€': 'inversion',
        'Alcance_Predicho': 'alcance_predicho',
        'Engagement_Esperado': 'engagement_esperado'
    }
    
    df_export = pd.DataFrame()
    for col_nueva, col_original in columnas_csv.items():
        if col_original in df_csv.columns:
            df_export[col_nueva] = df_csv[col_original]
    
    return df_export.to_csv(index=False)

def mostrar_insights_historicos(df, canal):
    """
    Muestra insights históricos para ayudar en la planificación
    """
    if len(df) == 0:
        return
    
    # Filtrar por canal si está disponible
    df_canal = df[df['Canal'] == canal].copy() if 'Canal' in df.columns and canal in df['Canal'].values else df.copy()
    
    if len(df_canal) == 0:
        return
    
    col_insight1, col_insight2 = st.columns(2)
    
    with col_insight1:
        if 'Fecha' in df_canal.columns:
            df_canal['hora'] = df_canal['Fecha'].dt.hour
            df_canal['dia_semana'] = df_canal['Fecha'].dt.dayofweek
            
            # Mejor hora histórica
            if 'Interacciones' in df_canal.columns and 'Alcance' in df_canal.columns:
                df_canal['engagement_rate'] = (df_canal['Interacciones'] / df_canal['Alcance']).fillna(0)
                mejor_hora = df_canal.groupby('hora')['engagement_rate'].mean().idxmax()
                mejor_engagement = df_canal.groupby('hora')['engagement_rate'].mean().max()
                
                st.info(f"🕐 **Mejor hora histórica**: {mejor_hora}:00 (Engagement: {mejor_engagement:.3f})")
            
            # Mejor día histórico
            if 'engagement_rate' in df_canal.columns:
                dias_nombres = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
                mejor_dia_num = df_canal.groupby('dia_semana')['engagement_rate'].mean().idxmax()
                mejor_dia_nombre = dias_nombres[mejor_dia_num]
                
                st.info(f"📅 **Mejor día histórico**: {mejor_dia_nombre}")
    
    with col_insight2:
        if 'Formato' in df_canal.columns:
            formato_mas_usado = df_canal['Formato'].mode().iloc[0] if not df_canal['Formato'].mode().empty else "N/A"
            st.info(f"🎨 **Formato más utilizado**: {formato_mas_usado}")
        
        if 'Alcance' in df_canal.columns:
            alcance_promedio = df_canal['Alcance'].mean()
            st.info(f"👁️ **Alcance promedio histórico**: {alcance_promedio:,.0f}")

# Configuración de la página
st.set_page_config(
    page_title="oráculo - Análisis de Redes Sociales",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Definir variables de colores y rutas
PRIMARY_COLOR = "#8e24aa"
LOGO_PATH = "/Users/n.arcos89/Documents/GitHub/Diva_digital/App/Logo-oraculo.png"

# --- ESTILOS PERSONALIZADOS MEJORADOS ---
page_bg = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --accent-color: #ec4899;
    --background-primary: #fafbfc;
    --background-secondary: #ffffff;
    --text-primary: #1f2937;
    --text-secondary: #6b7280;
    --border-color: #e5e7eb;
    --shadow-light: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    --shadow-medium: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-large: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    --gradient-accent: linear-gradient(135deg, #ec4899 0%, #f97316 100%);
}

/* CONFIGURACIÓN GENERAL */
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--background-primary);
    color: var(--text-primary);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* CONTENEDOR PRINCIPAL */
[data-testid="stAppViewContainer"] > .main {
    background: var(--background-primary);
    padding: 0;
}

[data-testid="stAppViewContainer"] {
    background: var(--background-primary);
}

/* SIDEBAR PROFESIONAL */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    border-right: 1px solid var(--border-color);
}

section[data-testid="stSidebar"] > div {
    background: transparent;
    padding-top: 2rem;
}

/* Texto del sidebar */
section[data-testid="stSidebar"] .markdown-text-container,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label {
    color: #f1f5f9 !important;
    font-weight: 500;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-weight: 700;
}

/* HEADER CON LOGO */
.header-container {
    background: var(--background-secondary);
    padding: 2rem 3rem;
    margin: -1rem -1rem 2rem -1rem;
    border-bottom: 1px solid var(--border-color);
    box-shadow: var(--shadow-light);
}

.logo-section {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
}

.brand-title {
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0;
}

.brand-subtitle {
    color: var(--text-secondary);
    font-size: 1.25rem;
    font-weight: 500;
    text-align: center;
    margin: 0.5rem 0 0 0;
}

/* TIPOGRAFÍA MODERNA */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.025em;
    line-height: 1.2;
}

h1 { font-size: 2.5rem !important; }
h2 { font-size: 2rem !important; }
h3 { font-size: 1.5rem !important; }
h4 { font-size: 1.25rem !important; }

.main p {
    color: var(--text-secondary) !important;
    font-size: 0.95rem;
    line-height: 1.7;
}

/* TARJETAS DE MÉTRICAS MODERNAS */
[data-testid="metric-container"] {
    background: var(--background-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    box-shadow: var(--shadow-light) !important;
    transition: all 0.2s ease !important;
    position: relative;
    overflow: hidden;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-medium) !important;
    border-color: var(--primary-color) !important;
}

[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--gradient-primary);
}

[data-testid="metric-container"] [data-testid="metric-value"] {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="metric-container"] [data-testid="metric-label"] {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* BOTONES PROFESIONALES */
.stButton > button {
    background: var(--gradient-primary) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.2s ease !important;
    box-shadow: var(--shadow-light) !important;
    letter-spacing: 0.025em;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-medium) !important;
    background: linear-gradient(135deg, #5855f7 0%, #7c3aed 100%) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* PESTAÑAS ELEGANTES */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: var(--background-secondary);
    padding: 0.5rem;
    border-radius: 12px;
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-light);
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.2s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(99, 102, 241, 0.1) !important;
    color: var(--primary-color) !important;
}

.stTabs [aria-selected="true"] {
    background: var(--gradient-primary) !important;
    color: white !important;
    box-shadow: var(--shadow-light) !important;
}

/* ALERTAS Y NOTIFICACIONES */
.stSuccess {
    background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%) !important;
    border: 1px solid #22c55e !important;
    border-radius: 8px !important;
    color: #15803d !important;
}

.stInfo {
    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
    border: 1px solid #3b82f6 !important;
    border-radius: 8px !important;
    color: #1d4ed8 !important;
}

.stWarning {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%) !important;
    border: 1px solid #f59e0b !important;
    border-radius: 8px !important;
    color: #d97706 !important;
}

.stError {
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%) !important;
    border: 1px solid #ef4444 !important;
    border-radius: 8px !important;
    color: #dc2626 !important;
}

/* CONTENEDORES DE CONTENIDO */
.content-card {
    background: var(--background-secondary);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: var(--shadow-light);
    transition: all 0.2s ease;
}

.content-card:hover {
    box-shadow: var(--shadow-medium);
}

/* FORMULARIOS ELEGANTES */
.stSelectbox > div > div,
.stMultiSelect > div > div,
.stDateInput > div > div,
.stNumberInput > div > div,
.stTextInput > div > div {
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    background: var(--background-secondary) !important;
    transition: all 0.2s ease !important;
}

.stSelectbox > div > div:focus-within,
.stMultiSelect > div > div:focus-within,
.stDateInput > div > div:focus-within,
.stNumberInput > div > div:focus-within,
.stTextInput > div > div:focus-within {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
}

/* SLIDERS MODERNOS */
.stSlider > div > div > div > div {
    background: var(--gradient-primary) !important;
}

/* DATAFRAMES PROFESIONALES */
.dataframe {
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-light) !important;
}

/* GRÁFICOS PLOTLY */
.js-plotly-plot {
    border-radius: 8px !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-light) !important;
}

/* EXPANDIBLES */
.streamlit-expanderHeader {
    background: var(--background-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}

/* SEPARADORES */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--border-color), transparent) !important;
    margin: 2rem 0 !important;
}

/* EFECTOS DE HOVER GLOBALES */
.element-container:hover .content-card {
    transform: translateY(-1px);
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .brand-title {
        font-size: 2rem;
    }
    
    .header-container {
        padding: 1rem;
        margin: -1rem -1rem 1rem -1rem;
    }
    
    [data-testid="metric-container"] {
        padding: 1rem !important;
    }
}

/* LOADING STATES */
.stSpinner > div {
    border-color: var(--primary-color) !important;
}

/* SCROLLBARS */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: var(--background-primary);
}

::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-secondary);
}

/* ANIMACIONES SUTILES */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.main > div {
    animation: fadeIn 0.3s ease-out;
}
</style>
"""

# Aplicar estilos
st.markdown(page_bg, unsafe_allow_html=True)

# --- CABECERA PROFESIONAL ---
st.markdown("""
<div class="header-container">
    <div class="logo-section">
""", unsafe_allow_html=True)

if os.path.exists(LOGO_PATH):
    col_logo_left, col_logo_center, col_logo_right = st.columns([1, 2, 1])
    with col_logo_center:
        st.image(LOGO_PATH, width=400)
else:
    st.markdown("""
        <h1 class="brand-title">🔮 ORÁCULO</h1>
        <p class="brand-subtitle"> Predice tu estrategia digital con datos inteligentes</p>
    """, unsafe_allow_html=True)

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)

# --- DESCRIPCIÓN PRINCIPAL MODERNA ---
st.markdown("""
<div class="content-card">
    <h2 style="margin-bottom: 1rem; color: var(--primary-color);">
        🚀 Revoluciona tu estrategia en redes sociales
    </h2>
    <p style="font-size: 1.1rem; margin-bottom: 0;">
        Oráculo combina <strong>inteligencia artificial</strong>, <strong>análisis predictivo</strong> y 
        <strong>computer vision</strong> para optimizar tu presencia digital. Toma decisiones basadas en datos 
        y maximiza el impacto de cada publicación.
    </p>
</div>
""", unsafe_allow_html=True)

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
        if 'Fecha' not in df.columns or 'Formato' not in df.columns:
            return None, None
        
        # Preparar datos temporales
        df_modelo = df.copy()
        df_modelo['hora'] = df_modelo['Fecha'].dt.hour
        df_modelo['dia_semana'] = df_modelo['Fecha'].dt.dayofweek
        df_modelo['mes'] = df_modelo['Fecha'].dt.month
        
        # FORZAR la inclusión de todos los formatos
        formatos_requeridos = ['Imagen', 'Reel', 'Carrusel']
        formatos_disponibles = df_modelo['Formato'].unique()
        
        # Crear datos sintéticos para TODOS los formatos faltantes
        datos_sinteticos = []
        base_size = len(df_modelo)
        
        for formato_requerido in formatos_requeridos:
            if formato_requerido not in formatos_disponibles:
                
                
                # Crear 30 registros sintéticos para cada formato faltante
                for i in range(30):
                    fila_base = df_modelo.iloc[i % len(df_modelo)].copy()
                    fila_base['Formato'] = formato_requerido
                    
                    # Ajustar métricas según el tipo de formato
                    if formato_requerido == 'Reel':
                        if 'Alcance' in fila_base:
                            fila_base['Alcance'] = fila_base['Alcance'] * 1.4
                        if 'Interacciones' in fila_base:
                            fila_base['Interacciones'] = fila_base['Interacciones'] * 1.6
                    elif formato_requerido == 'Carrusel':
                        if 'Alcance' in fila_base:
                            fila_base['Alcance'] = fila_base['Alcance'] * 1.2
                        if 'Interacciones' in fila_base:
                            fila_base['Interacciones'] = fila_base['Interacciones'] * 1.3
                    
                    # Variar horas para los Reels (mejor en tardes/noches)
                    if formato_requerido == 'Reel':
                        fila_base['hora'] = np.random.choice([14, 15, 16, 17, 18, 19, 20, 21])
                    elif formato_requerido == 'Carrusel':
                        fila_base['hora'] = np.random.choice([10, 11, 12, 13, 14, 15, 16])
                    
                    datos_sinteticos.append(fila_base)
        
        # Añadir datos sintéticos
        if datos_sinteticos:
            df_sintetico = pd.DataFrame(datos_sinteticos)
            df_modelo = pd.concat([df_modelo, df_sintetico], ignore_index=True)
            
        
        # Verificar que tenemos todos los formatos
        formatos_finales = df_modelo['Formato'].unique()
        
        
        # Crear engagement sintético si no existe
        if 'Alcance' in df_modelo.columns and 'Interacciones' in df_modelo.columns:
            df_modelo['engagement_rate'] = df_modelo['Interacciones'] / df_modelo['Alcance']
            df_modelo['engagement_rate'] = df_modelo['engagement_rate'].fillna(0)
        else:
            # Crear engagement sintético más realista por formato
            np.random.seed(42)
            engagement_base = []
            
            for _, row in df_modelo.iterrows():
                if row['Formato'] == 'Reel':
                    eng = np.random.normal(0.06, 0.02)  # Reels tienen mejor engagement
                elif row['Formato'] == 'Carrusel':
                    eng = np.random.normal(0.045, 0.015)  # Carruseles nivel medio
                else:  # Imagen
                    eng = np.random.normal(0.035, 0.01)  # Imágenes baseline
                
                engagement_base.append(max(0, min(eng, 0.15)))  # Entre 0% y 15%
            
            df_modelo['engagement_rate'] = engagement_base
        
        # Preparar features
        features = ['hora', 'dia_semana', 'mes']
        if 'Inversion' in df_modelo.columns:
            features.append('Inversion')
        else:
            np.random.seed(42)
            df_modelo['Inversion'] = np.random.uniform(50, 200, len(df_modelo))
            features.append('Inversion')
        
        # Encodificar formatos
        le_formato = LabelEncoder()
        df_modelo['formato_enc'] = le_formato.fit_transform(df_modelo['Formato'])
        
        # Verificar distribución de formatos
        distribucion_formatos = df_modelo['Formato'].value_counts()
        
        
        X = df_modelo[features]
        y = df_modelo['formato_enc']
        
        # Entrenar modelo balanceado
        modelo_temporal = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=8,
            min_samples_split=3,
            class_weight='balanced_subsample'  # Balanceado dinámico
        )
        modelo_temporal.fit(X, y)
        
        # Verificar predicciones de prueba
        y_pred_test = modelo_temporal.predict(X)
        predicciones_formatos = le_formato.inverse_transform(y_pred_test)
        distribucion_pred = pd.Series(predicciones_formatos).value_counts()
        
        
        return modelo_temporal, le_formato
        
    except Exception as e:
        st.error(f"Error creando modelo temporal: {e}")
        return None, None

# --- CABECERA SIMPLE CON LOGO CENTRADO ---
col_logo_left, col_logo_center, col_logo_right = st.columns([1, 2, 1])

with col_logo_center:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=400, use_container_width=False)
    else:
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h1 style="font-size: 3.5rem; color: #4a148c; margin: 0;">🔮 ORÁCULO</h1>
            <p style="font-size: 1.3rem; color: #6a1b9a; margin: 0.5rem 0;" Predice tu estrategia digital</p>
        </div>
        """, unsafe_allow_html=True)

# --- DESCRIPCIÓN INICIAL ---
st.markdown("""
<div style='background:rgba(255,255,255,0.9);padding:1.2em 2em;border-radius:18px;margin-bottom:1.5em;box-shadow:0 4px 15px rgba(142,36,170,0.1);border-left: 4px solid #e91e63;'>
    <span style='font-size:1.2em;color:#e91e63;'><b>¿Quieres impulsar tu marca en redes sociales?</b></span><br>
    <span style='color:#4a148c;'>Oráculo te ayuda a <b>analizar, visualizar y predecir</b> el rendimiento de tus publicaciones en Instagram, Facebook y TikTok.<br>
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
    Carga el CSV con los datos de las imágenes de Pixabay (versión limpia)
    """
    try:
        csv_path = "/Users/n.arcos89/Desktop/Bootcamp_Data/DIVA_DIGITAL_Proyecto Final/Data/publicaciones_pixabay_ok.csv"
        
        # Verificar si el archivo CSV existe
        if not os.path.exists(csv_path):
            return pd.DataFrame()
        
        # Cargar CSV
        df_imagenes = pd.read_csv(csv_path)
        
        # Convertir fecha si existe
        fecha_col = None
        if 'Fecha' in df_imagenes.columns:
            fecha_col = 'Fecha'
        elif 'fecha' in df_imagenes.columns:
            fecha_col = 'fecha'
        else:
            return pd.DataFrame()
        
        # Convertir fechas
        df_imagenes[fecha_col] = pd.to_datetime(df_imagenes[fecha_col], errors='coerce')
        df_imagenes['Fecha'] = df_imagenes[fecha_col]  # Estandarizar nombre
        
        # Verificar si hay fechas válidas
        fechas_validas = df_imagenes['Fecha'].notna().sum()
        if fechas_validas == 0:
            return pd.DataFrame()
        
        # Verificar columna Imagen
        if 'Imagen' not in df_imagenes.columns:
            return pd.DataFrame()
        
        # Definir la ruta donde están las imágenes
        ruta_base_imagenes = "/Users/n.arcos89/Desktop/Bootcamp_Data/DIVA_DIGITAL_Proyecto Final/Imagenes/imagenes_descargadas"
        
        if not os.path.exists(ruta_base_imagenes):
            return pd.DataFrame()
        
        # Obtener lista de archivos reales en el directorio
        try:
            archivos_reales = [f for f in os.listdir(ruta_base_imagenes) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
            archivos_reales.sort()
        except Exception as e:
            return pd.DataFrame()
        
        if len(archivos_reales) == 0:
            return pd.DataFrame()
        
        # Construir rutas
        def construir_ruta(nombre_imagen):
            if nombre_imagen and not pd.isna(nombre_imagen):
                return os.path.join(ruta_base_imagenes, nombre_imagen)
            return None
        
        df_imagenes['Ruta'] = df_imagenes['Imagen'].apply(construir_ruta)
        
        # Verificar qué imágenes existen realmente
        df_imagenes['imagen_existe'] = df_imagenes['Ruta'].apply(
            lambda x: os.path.exists(x) if x is not None else False
        )
        
        # Filtrar solo las imágenes que existen
        df_imagenes_validas = df_imagenes[df_imagenes['imagen_existe']].copy()
        df_imagenes_validas = df_imagenes_validas.dropna(subset=['Imagen', 'Ruta', 'Fecha'])
        
        return df_imagenes_validas
        
    except Exception as e:
        return pd.DataFrame()

# Cargar datos de imágenes SIN mensajes de diagnóstico
df_imagenes = cargar_datos_imagenes()

# --- SIDEBAR: LOGO, FILTROS Y RESUMEN ---
# Logo en el sidebar
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, width=150, use_container_width=False)
else:
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 1rem; background: rgba(255, 255, 255, 0.1); border-radius: 15px; margin-bottom: 1rem;'>
        <h2 style='margin: 0; color: #fff; font-size: 1.5rem;'>🔮 ORÁCULO</h2>
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
        
# Mostrar información básica (simplificada)
if not df.empty and 'Fecha' in df.columns and not df['Fecha'].isna().all():
    try:
        fecha_min = df['Fecha'].min().strftime('%Y-%m-%d')
        fecha_max = df['Fecha'].max().strftime('%Y-%m-%d')
        st.sidebar.info(f"📊 **{len(df)} publicaciones**\n📅 {fecha_min} a {fecha_max}")
    except:
        st.sidebar.info(f"📊 **{len(df)} publicaciones** disponibles")

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

# Mostrar resumen simple
st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Resumen")
if len(df_filtrado) < len(df):
    st.sidebar.success(f"**{len(df_filtrado)} de {len(df)}** publicaciones")
else:
    st.sidebar.success(f"**{len(df_filtrado)}** publicaciones")

# Mostrar tipo de datos usado
if tipo_datos == "principal":
    st.sidebar.info("📊 Dataset principal")
elif tipo_datos == "demo":
    st.sidebar.info("📊 Datos demo")

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
st.title("✨ Oráculo: Análisis de Redes Sociales para Marcas")

tab1, tab2, tab3 = st.tabs(["📊 Informe", "🔮 Modelo Predictivo", "🚀 Next Steps"])

# --- TAB 1: INFORME ---
with tab1:
    st.header("📊 Informe Interanual")
    if df_filtrado.empty:
        st.error("No hay datos para mostrar el informe")
    else:
        subtab1, subtab2, subtab3, subtab4, subtab5, subtab6, subtab7 = st.tabs([
            "📈 Resumen", "🖼️ Imágenes", "👁️ Visibilidad", "❤️ Interacción", "▶️ Reproducciones", "🛒 Conversión", "💰 Retorno"
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
            st.subheader("🖼️ Análisis de Imágenes")
    
            if df_imagenes.empty:
                st.warning("⚠️ No hay imágenes disponibles para analizar")
                st.info("💡 Verifica que el archivo de imágenes esté correctamente cargado en el sistema")
            else:
                # Filtrar imágenes según los filtros aplicados
                df_imagenes_filtrado = df_imagenes.copy()
        
                # Aplicar filtros de fecha si están disponibles
                if fecha_inicio and fecha_fin:
                    df_imagenes_filtrado = df_imagenes_filtrado[
                        (df_imagenes_filtrado['Fecha'].dt.date >= fecha_inicio) & 
                        (df_imagenes_filtrado['Fecha'].dt.date <= fecha_fin)
                    ]
        
                if len(df_imagenes_filtrado) == 0:
                    st.warning("⚠️ No hay imágenes en el período seleccionado")
                else:
                    st.info(f"📊 Analizando {len(df_imagenes_filtrado)} imágenes en el período seleccionado")
            
            # CONECTAR CON DATOS DE RENDIMIENTO
            @st.cache_data
            def conectar_datos_rendimiento(df_imgs, df_principal):
                """Conecta datos de imágenes con métricas de rendimiento"""
                
                # Crear una clave de unión basada en la fecha y el nombre de imagen
                df_principal_copy = df_principal.copy()
                df_imgs_copy = df_imgs.copy()
                
                # Intentar diferentes estrategias de unión
                resultados_unidos = []
                
                for _, img_row in df_imgs_copy.iterrows():
                    # Estrategia 1: Buscar por fecha exacta
                    fecha_img = img_row['Fecha'].date()
                    matching_rows = df_principal_copy[df_principal_copy['Fecha'].dt.date == fecha_img]
                    
                    if len(matching_rows) > 0:
                        # Si hay múltiples coincidencias en la misma fecha, tomar la primera
                        best_match = matching_rows.iloc[0]
                        
                        resultado = {
                            'Imagen': img_row['Imagen'],
                            'Fecha': img_row['Fecha'],
                            'Ruta': img_row['Ruta'],
                            'Alcance': best_match.get('Alcance', 0),
                            'Interacciones': best_match.get('Interacciones', 0),
                            'Compras': best_match.get('Compras', 0),
                            'Valor_compra': best_match.get('Valor_compra', 0.0),
                            'Canal': best_match.get('Canal', 'Unknown'),
                            'Formato': best_match.get('Formato', 'Imagen')
                        }
                        resultados_unidos.append(resultado)
                
                return pd.DataFrame(resultados_unidos)
            
            # Conectar datos
            df_imagenes_con_metricas = conectar_datos_rendimiento(df_imagenes_filtrado, df_filtrado)
            
            if df_imagenes_con_metricas.empty:
                st.warning("⚠️ No se pudieron conectar las imágenes con los datos de rendimiento")
                st.info("💡 Esto puede deberse a que las fechas en ambos datasets no coinciden exactamente")
                
                # Mostrar información de diagnóstico
                st.markdown("### 🔍 Diagnóstico de Datos")
                col_diag1, col_diag2 = st.columns(2)
                
                with col_diag1:
                    st.markdown("**📅 Fechas en Imágenes:**")
                    fechas_imgs = df_imagenes_filtrado['Fecha'].dt.date.unique()[:5]
                    for fecha in fechas_imgs:
                        st.write(f"• {fecha}")
                
                with col_diag2:
                    st.markdown("**📅 Fechas en Datos Principales:**")
                    fechas_principal = df_filtrado['Fecha'].dt.date.unique()[:5]
                    for fecha in fechas_principal:
                        st.write(f"• {fecha}")
                
                # Análisis básico sin métricas de rendimiento
                st.markdown("### 🎨 Análisis Visual Básico")
                
                @st.cache_data
                def analizar_imagenes_basico(df_imgs):
                    """Análisis básico solo con Computer Vision"""
                    resultados = []
                    
                    for idx, row in df_imgs.iterrows():
                        try:
                            if os.path.exists(row['Ruta']):
                                analisis = analizar_imagen_completo(row['Ruta'])
                                if analisis['exito']:
                                    resultado = {
                                        'Imagen': row['Imagen'],
                                        'Fecha': row['Fecha'],
                                        'Ruta': row['Ruta'],
                                        'tematica': analisis['tematica_predicha'],
                                        'engagement_score': analisis['engagement_score'],
                                        'colores_dominantes': analisis['colores_dominantes'],
                                        'caracteristicas': analisis['caracteristicas']
                                    }
                                    resultados.append(resultado)
                        except Exception as e:
                            continue
                    
                    return pd.DataFrame(resultados)
                
                with st.spinner("🔍 Analizando imágenes con Computer Vision..."):
                    df_analisis_basico = analizar_imagenes_basico(df_imagenes_filtrado)
                
                if not df_analisis_basico.empty:
                    # Mostrar análisis de temáticas y colores
                    st.markdown("#### 🏷️ Análisis de Temáticas")
                    tematicas_count = df_analisis_basico['tematica'].value_counts()
                    
                    mapeo_tematicas = {
                        'moda_lifestyle': 'Moda & Lifestyle',
                        'arte_diseño': 'Arte & Diseño',
                        'naturaleza_bienestar': 'Naturaleza & Bienestar',
                        'tecnologia': 'Tecnología',
                        'comida_gastronomia': 'Comida & Gastronomía',
                        'lifestyle_inspiracional': 'Lifestyle Inspiracional',
                        'general': 'General'
                    }
                    
                    tematicas_amigables = [mapeo_tematicas.get(tema, tema) for tema in tematicas_count.index]
                    
                    fig_tematicas = px.pie(
                        values=tematicas_count.values,
                        names=tematicas_amigables,
                        title="🏷️ Distribución de Temáticas",
                        color_discrete_sequence=px.colors.sequential.Purples
                    )
                    fig_tematicas.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                    st.plotly_chart(fig_tematicas, use_container_width=True)
            
            else:
                st.success(f"✅ {len(df_imagenes_con_metricas)} imágenes conectadas con datos de rendimiento")
                
                # FUNCIÓN PARA ANALIZAR MÚLTIPLES IMÁGENES CON MÉTRICAS
                @st.cache_data
                def analizar_imagenes_completo(df_imgs_metricas):
                    """Analiza todas las imágenes y extrae características + métricas"""
                    resultados = []
                    
                    for idx, row in df_imgs_metricas.iterrows():
                        try:
                            if os.path.exists(row['Ruta']):
                                analisis = analizar_imagen_completo(row['Ruta'])
                                if analisis['exito']:
                                    resultado = {
                                        'Imagen': row['Imagen'],
                                        'Fecha': row['Fecha'],
                                        'Ruta': row['Ruta'],
                                        'tematica': analisis['tematica_predicha'],
                                        'engagement_score': analisis['engagement_score'],
                                        'colores_dominantes': analisis['colores_dominantes'],
                                        'caracteristicas': analisis['caracteristicas'],
                                        # Métricas de rendimiento
                                        'Alcance': row['Alcance'],
                                        'Interacciones': row['Interacciones'],
                                        'Compras': row['Compras'],
                                        'Valor_compra': row['Valor_compra'],
                                        'Canal': row['Canal'],
                                        'Formato': row['Formato']
                                    }
                                    resultados.append(resultado)
                        except Exception as e:
                            continue
                    
                    return pd.DataFrame(resultados)
                
                # Analizar todas las imágenes
                with st.spinner("🔍 Analizando imágenes con Computer Vision..."):
                    df_analisis = analizar_imagenes_completo(df_imagenes_con_metricas)
                
                if df_analisis.empty:
                    st.error("❌ No se pudieron analizar las imágenes")
                else:
                    st.success(f"✅ {len(df_analisis)} imágenes analizadas correctamente")
                    
                    # ANÁLISIS GENERAL DE TEMÁTICAS Y COLORES
                    st.markdown("### 🎨 Análisis General del Contenido Visual")
                    
                    col_tema1, col_tema2 = st.columns(2)
                    
                    with col_tema1:
                        # Temáticas más frecuentes
                        tematicas_count = df_analisis['tematica'].value_counts()
                        
                        # Mapeo de nombres técnicos a nombres amigables
                        mapeo_tematicas = {
                            'moda_lifestyle': 'Moda & Lifestyle',
                            'arte_diseño': 'Arte & Diseño',
                            'naturaleza_bienestar': 'Naturaleza & Bienestar',
                            'tecnologia': 'Tecnología',
                            'comida_gastronomia': 'Comida & Gastronomía',
                            'lifestyle_inspiracional': 'Lifestyle Inspiracional',
                            'general': 'General'
                        }
                        
                        tematicas_amigables = [mapeo_tematicas.get(tema, tema) for tema in tematicas_count.index]
                        
                        fig_tematicas = px.pie(
                            values=tematicas_count.values,
                            names=tematicas_amigables,
                            title="🏷️ Temáticas Más Habituales",
                            color_discrete_sequence=px.colors.sequential.Purples
                        )
                        fig_tematicas.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                        st.plotly_chart(fig_tematicas, use_container_width=True)
                        
                        # Mostrar estadística principal
                        tematica_principal = mapeo_tematicas.get(tematicas_count.index[0], tematicas_count.index[0])
                        porcentaje_principal = (tematicas_count.iloc[0] / len(df_analisis)) * 100
                        st.metric("🎯 Temática Dominante", 
                                f"{tematica_principal}", 
                                f"{porcentaje_principal:.1f}% del contenido")
                    
                    with col_tema2:
                        # Análisis de colores dominantes
                        todos_colores = []
                        for _, row in df_analisis.iterrows():
                            if row['colores_dominantes']:
                                for color in row['colores_dominantes'][:3]:  # Top 3 colores por imagen
                                    todos_colores.append({
                                        'color': color['nombre'],
                                        'hex': color['hex'],
                                        'peso': color['porcentaje']
                                    })
                        
                        if todos_colores:
                            df_colores = pd.DataFrame(todos_colores)
                            colores_frecuentes = df_colores.groupby(['color', 'hex']).agg({
                                'peso': ['count', 'mean']
                            }).reset_index()
                            colores_frecuentes.columns = ['Color', 'Hex', 'Frecuencia', 'Peso_Promedio']
                            colores_frecuentes = colores_frecuentes.sort_values('Frecuencia', ascending=False).head(8)
                            
                            fig_colores = px.bar(
                                colores_frecuentes, 
                                x='Color', 
                                y='Frecuencia',
                                title="🎨 Paleta de Colores Más Habitual",
                                color='Color',
                                color_discrete_map={row['Color']: row['Hex'] for _, row in colores_frecuentes.iterrows()}
                            )
                            fig_colores.update_layout(
                                paper_bgcolor='rgba(255,255,255,0.9)', 
                                font_color='#4a148c',
                                showlegend=False
                            )
                            st.plotly_chart(fig_colores, use_container_width=True)
                            
                            # Mostrar paleta visual
                            st.markdown("#### 🎨 Paleta Visual Dominante")
                            cols_paleta = st.columns(len(colores_frecuentes))
                            for i, (_, color_info) in enumerate(colores_frecuentes.iterrows()):
                                with cols_paleta[i]:
                                    st.markdown(f"""
                                    <div style='background-color: {color_info["Hex"]}; 
                                                width: 50px; height: 50px; 
                                                border-radius: 50%; margin: auto;
                                                border: 2px solid #ccc;'></div>
                                    <p style='text-align: center; font-size: 10px; margin-top: 5px;'>
                                        {color_info["Color"]}<br>{color_info["Frecuencia"]} usos
                                    </p>
                                    """, unsafe_allow_html=True)
                    
                    # RANKINGS DE IMÁGENES - CORREGIDO
                    st.markdown("---")
                    st.markdown("### 🏆 Rankings de Mejores Imágenes")
                    
                    # Verificar qué métricas están disponibles
                    metricas_disponibles = []
                    if 'Alcance' in df_analisis.columns and df_analisis['Alcance'].sum() > 0:
                        metricas_disponibles.append('Alcance')
                    if 'Interacciones' in df_analisis.columns and df_analisis['Interacciones'].sum() > 0:
                        metricas_disponibles.append('Interacciones')
                    if 'Valor_compra' in df_analisis.columns and df_analisis['Valor_compra'].sum() > 0:
                        metricas_disponibles.append('Valor_compra')
                    
                    if not metricas_disponibles:
                        st.warning("⚠️ No se encontraron métricas de rendimiento válidas para crear rankings")
                        st.info("💡 Las métricas pueden estar vacías o en cero en el período seleccionado")
                    else:
                        # Crear pestañas para cada métrica disponible
                        tabs_nombres = []
                        if 'Alcance' in metricas_disponibles:
                            tabs_nombres.append("👁️ Top Visibilidad")
                        if 'Interacciones' in metricas_disponibles:
                            tabs_nombres.append("❤️ Top Interacción")
                        if 'Valor_compra' in metricas_disponibles:
                            tabs_nombres.append("🛒 Top Ventas")
                        
                        tabs_metricas = st.tabs(tabs_nombres)
                        
                        # Función para crear tabla de ranking
                        def crear_ranking_tabla(df, metrica, titulo, emoji):
                            df_sorted = df.nlargest(10, metrica)
                            
                            st.markdown(f"#### {emoji} {titulo}")
                            
                            # Mostrar las imágenes en grid
                            for i in range(0, min(10, len(df_sorted)), 5):
                                cols = st.columns(5)
                                for j, (idx, row) in enumerate(df_sorted.iloc[i:i+5].iterrows()):
                                    with cols[j]:
                                        try:
                                            # Mostrar imagen
                                            st.image(row['Ruta'], 
                                                    caption=f"#{i+j+1} - {row['Imagen']}", 
                                                    use_container_width=True)
                                            
                                            # Mostrar métricas
                                            if metrica == 'Valor_compra':
                                                st.metric(f"{metrica}", f"{row[metrica]:,.2f}€")
                                            else:
                                                st.metric(f"{metrica}", f"{row[metrica]:,.0f}")
                                            
                                            # Mostrar temática
                                            tematica_amigable = mapeo_tematicas.get(row['tematica'], row['tematica'])
                                            st.caption(f"🏷️ {tematica_amigable}")
                                            
                                            # Mostrar score de engagement
                                            st.caption(f"🎯 Score: {row['engagement_score']:.2f}")
                                            
                                        except Exception as e:
                                            st.error(f"Error cargando imagen: {row['Imagen']}")
                            
                            # Tabla detallada
                            st.markdown("##### 📋 Tabla Detallada")
                            tabla_display = df_sorted[['Imagen', metrica, 'tematica', 'engagement_score', 'Fecha']].copy()
                            tabla_display['tematica'] = tabla_display['tematica'].map(mapeo_tematicas).fillna(tabla_display['tematica'])
                            tabla_display['Fecha'] = tabla_display['Fecha'].dt.strftime('%Y-%m-%d')
                            tabla_display.columns = ['Imagen', metrica, 'Temática', 'Score CV', 'Fecha']
                            
                            if metrica == 'Valor_compra':
                                tabla_display[metrica] = tabla_display[metrica].apply(lambda x: f"{x:,.2f}€")
                            else:
                                tabla_display[metrica] = tabla_display[metrica].apply(lambda x: f"{x:,.0f}")
                            
                            tabla_display['Score CV'] = tabla_display['Score CV'].apply(lambda x: f"{x:.3f}")
                            
                            st.dataframe(tabla_display, use_container_width=True, hide_index=True)
                        
                        # Crear rankings para cada métrica disponible
                        tab_index = 0
                        
                        if 'Alcance' in metricas_disponibles:
                            with tabs_metricas[tab_index]:
                                crear_ranking_tabla(df_analisis, 'Alcance', "Imágenes con Mayor Visibilidad", "👁️")
                            tab_index += 1
                        
                        if 'Interacciones' in metricas_disponibles:
                            with tabs_metricas[tab_index]:
                                crear_ranking_tabla(df_analisis, 'Interacciones', "Imágenes con Mayor Interacción", "❤️")
                            tab_index += 1
                        
                        if 'Valor_compra' in metricas_disponibles:
                            with tabs_metricas[tab_index]:
                                crear_ranking_tabla(df_analisis, 'Valor_compra', "Imágenes que Más Ventas Generaron", "🛒")
                    
                    # INSIGHTS ADICIONALES
                    st.markdown("---")
                    st.markdown("### 💡 Insights de Computer Vision")
                    
                    col_insight1, col_insight2, col_insight3 = st.columns(3)
                    
                    with col_insight1:
                        # Score promedio de engagement visual
                        score_promedio = df_analisis['engagement_score'].mean()
                        score_maximo = df_analisis['engagement_score'].max()
                        st.metric("🎯 Score Promedio CV", f"{score_promedio:.3f}", f"Máximo: {score_maximo:.3f}")
                    
                    with col_insight2:
                        # Diversidad de temáticas
                        num_tematicas = df_analisis['tematica'].nunique()
                        st.metric("🏷️ Diversidad Temática", f"{num_tematicas} temáticas", "diferentes encontradas")
                    
                    with col_insight3:
                        # Diversidad de colores
                        if todos_colores:
                            num_colores = len(df_colores['color'].unique())
                            st.metric("🎨 Diversidad Cromática", f"{num_colores} colores", "únicos identificados")
                    
                    # Correlación entre Score CV y métricas de rendimiento
                    if metricas_disponibles:
                        st.markdown("### 📊 Correlación: Computer Vision vs Rendimiento")
                        
                        correlaciones = []
                        for metrica in metricas_disponibles:
                            corr = df_analisis['engagement_score'].corr(df_analisis[metrica])
                            correlaciones.append({
                                'Métrica': metrica,
                                'Correlación': corr,
                                'Interpretación': 'Fuerte' if abs(corr) > 0.7 else 'Moderada' if abs(corr) > 0.3 else 'Débil'
                            })
                        
                        df_correlaciones = pd.DataFrame(correlaciones)
                        
                        fig_corr = px.bar(
                            df_correlaciones, 
                            x='Métrica', 
                            y='Correlación',
                            title="🔍 Correlación entre Score de Computer Vision y Métricas de Rendimiento",
                            color='Correlación',
                            color_continuous_scale='RdBu_r',
                            color_continuous_midpoint=0
                        )
                        fig_corr.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                        st.plotly_chart(fig_corr, use_container_width=True)
                        
                        # Mostrar interpretación
                        st.markdown("**💡 Interpretación:**")
                        for _, row in df_correlaciones.iterrows():
                            color = "🟢" if row['Interpretación'] == 'Fuerte' else "🟡" if row['Interpretación'] == 'Moderada' else "🔴"
                            st.write(f"{color} **{row['Métrica']}**: Correlación {row['Interpretación'].lower()} ({row['Correlación']:.3f})")
                                
        with subtab3:
            st.subheader("👁️ Visibilidad")
            
            if 'Alcance' in df_filtrado.columns:
                # Métricas principales 
                col1, col2, col3 = st.columns(3)
                col1.metric("Alcance Total", f"{df_filtrado['Alcance'].sum():,.0f}")
                col2.metric("Alcance Promedio", f"{df_filtrado['Alcance'].mean():.0f}")
                col3.metric("Total de posts", f"{len(df_filtrado)}")
                
                # GRÁFICO EXISTENTE: Alcance por Canal 
                if 'Canal' in df_filtrado.columns:
                    alcance_canal = df_filtrado.groupby('Canal')['Alcance'].mean().reset_index()
                    fig = px.bar(alcance_canal, x='Canal', y='Alcance',
                            title="📊 Alcance promedio por Canal",
                            color='Alcance', color_continuous_scale='Purples')
                    fig.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                    st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                
                # ANÁLISIS DETALLADO
                st.markdown("### 📈 Análisis Detallado de Visibilidad")
                
                # NUEVA GRÁFICA 1: Alcance por Formato
                col_graf1, col_graf2 = st.columns(2)
                
                with col_graf1:
                    if 'Formato' in df_filtrado.columns:
                        st.markdown("#### 🎨 Alcance por Formato de Contenido")
                        alcance_formato = df_filtrado.groupby('Formato')['Alcance'].agg(['sum', 'mean', 'count']).reset_index()
                        alcance_formato.columns = ['Formato', 'Alcance_Total', 'Alcance_Promedio', 'Num_Posts']
                        
                        # Gráfico de barras con alcance total por formato
                        fig1 = px.bar(
                            alcance_formato, 
                            x='Formato', 
                            y='Alcance_Total',
                            title="📊 Alcance Total por Formato",
                            color='Alcance_Total',
                            color_continuous_scale='Purples',
                            text='Alcance_Total'
                        )
                        
                        fig1.update_traces(
                            texttemplate='%{text:,.0f}', 
                            textposition='outside',
                            marker_line_color='rgba(74, 20, 140, 0.8)',
                            marker_line_width=1.5
                        )
                        
                        fig1.update_layout(
                            paper_bgcolor='rgba(255,255,255,0.9)', 
                            plot_bgcolor='rgba(255,255,255,0.9)',
                            font_color='#4a148c',
                            title_font_size=14,
                            title_font_color='#4a148c',
                            xaxis_title="Formato",
                            yaxis_title="Alcance Total",
                            showlegend=False,
                            height=350
                        )
                        
                        st.plotly_chart(fig1, use_container_width=True)
                
                with col_graf2:
                    # NUEVA GRÁFICA 2: Evolución del Alcance por Fechas
                    if 'Fecha' in df_filtrado.columns:
                        st.markdown("#### 📈 Evolución Temporal del Alcance")
                        # Crear serie temporal
                        df_temp = df_filtrado.copy()
                        df_temp['Fecha'] = pd.to_datetime(df_temp['Fecha'])
                        df_temp = df_temp.sort_values('Fecha')
                        
                        # Agrupar por semana para mejor visualización
                        df_temp['Semana'] = df_temp['Fecha'].dt.to_period('W').dt.start_time
                        alcance_tiempo = df_temp.groupby('Semana')['Alcance'].sum().reset_index()
                        
                        # Gráfico de línea temporal
                        fig2 = px.line(
                            alcance_tiempo, 
                            x='Semana', 
                            y='Alcance',
                            title="📈 Evolución Semanal del Alcance",
                            markers=True,
                            color_discrete_sequence=['#8e24aa']
                        )
                        
                        # Añadir área bajo la curva
                        fig2.add_scatter(
                            x=alcance_tiempo['Semana'], 
                            y=alcance_tiempo['Alcance'],
                            fill='tonexty', 
                            mode='none',
                            fillcolor='rgba(142, 36, 170, 0.2)',
                            name='',
                            showlegend=False
                        )
                        
                        fig2.update_layout(
                            paper_bgcolor='rgba(255,255,255,0.9)', 
                            plot_bgcolor='rgba(255,255,255,0.9)',
                            font_color='#4a148c',
                            title_font_size=14,
                            title_font_color='#4a148c',
                            xaxis_title="Fecha",
                            yaxis_title="Alcance Total",
                            hovermode='x unified',
                            height=350,
                            showlegend=False
                        )
                        
                        fig2.update_traces(
                            hovertemplate='<b>Semana:</b> %{x}<br><b>Alcance:</b> %{y:,.0f}<extra></extra>',
                            line=dict(width=3)
                        )
                        
                        st.plotly_chart(fig2, use_container_width=True)
                
                # NUEVA GRÁFICA 3: Top 10 Posts con Mayor Alcance
                st.markdown("---")
                st.markdown("### 🏆 Top 10 Posts con Mayor Alcance")
                
                if len(df_filtrado) > 0:
                    # Crear identificador único para cada post
                    df_top = df_filtrado.copy()
                    
                    # Si existe columna de contenido o descripción, usarla; si no, crear identificador
                    if 'Contenido' in df_top.columns:
                        df_top['Post_ID'] = df_top['Contenido'].apply(lambda x: str(x)[:40] + "..." if len(str(x)) > 40 else str(x))
                    elif 'Descripcion' in df_top.columns:
                        df_top['Post_ID'] = df_top['Descripcion'].apply(lambda x: str(x)[:40] + "..." if len(str(x)) > 40 else str(x))
                    else:
                        df_top['Post_ID'] = df_top.apply(lambda row: f"Post {row.name + 1} - {row['Fecha'].strftime('%d/%m/%Y') if 'Fecha' in df_top.columns else 'Sin fecha'}", axis=1)
                    
                    # Obtener top 10
                    top_10_posts = df_top.nlargest(10, 'Alcance')[['Post_ID', 'Alcance', 'Fecha', 'Canal', 'Formato']].reset_index(drop=True)
                    
                    # Gráfico de barras horizontales
                    fig3 = px.bar(
                        top_10_posts.iloc[::-1],  # Invertir para mostrar el mayor arriba
                        x='Alcance', 
                        y='Post_ID',
                        title="🏆 Posts con Mayor Alcance",
                        orientation='h',
                        color='Alcance',
                        color_continuous_scale='Purples',
                        text='Alcance'
                    )
                    
                    fig3.update_traces(
                        texttemplate='%{text:,.0f}', 
                        textposition='outside',
                        marker_line_color='rgba(74, 20, 140, 0.8)',
                        marker_line_width=1.5
                    )
                    
                    fig3.update_layout(
                        paper_bgcolor='rgba(255,255,255,0.9)', 
                        plot_bgcolor='rgba(255,255,255,0.9)',
                        font_color='#4a148c',
                        title_font_size=16,
                        title_font_color='#4a148c',
                        xaxis_title="Alcance",
                        yaxis_title="Posts",
                        height=400,
                        showlegend=False,
                        margin=dict(l=20, r=20, t=60, b=20)
                    )
                    
                    fig3.update_yaxes(tickfont=dict(size=10))
                    st.plotly_chart(fig3, use_container_width=True)
                    
                    # Tabla del Top 5 (versión compacta)
                    st.markdown("##### 📋 Top 5 Detallado")
                    tabla_top5 = top_10_posts.head(5).copy()
                    tabla_top5['Ranking'] = range(1, len(tabla_top5) + 1)
                    tabla_top5['Alcance_Formateado'] = tabla_top5['Alcance'].apply(lambda x: f"{x:,.0f}")
                    tabla_top5['Fecha_Formateada'] = tabla_top5['Fecha'].dt.strftime('%d/%m/%Y') if 'Fecha' in tabla_top5.columns else 'N/A'
                    
                    tabla_display = tabla_top5[['Ranking', 'Post_ID', 'Alcance_Formateado', 'Fecha_Formateada', 'Canal', 'Formato']].copy()
                    tabla_display.columns = ['🏅', '📝 Post', '👁️ Alcance', '📅 Fecha', '📱 Canal', '🎨 Formato']
                    
                    st.dataframe(tabla_display, use_container_width=True, hide_index=True)
                    
                    # Insights del mejor post
                    col_insight1, col_insight2, col_insight3 = st.columns(3)
                    
                    with col_insight1:
                        mejor_post_alcance = top_10_posts.iloc[0]['Alcance']
                        st.metric("🥇 Mejor Post", f"{mejor_post_alcance:,.0f}", "alcance")
                    
                    with col_insight2:
                        if 'Canal' in top_10_posts.columns:
                            canal_dominante = top_10_posts['Canal'].mode().iloc[0] if not top_10_posts['Canal'].mode().empty else "N/A"
                            st.metric("📱 Canal Top", canal_dominante)
                    
                    with col_insight3:
                        if 'Formato' in top_10_posts.columns:
                            formato_dominante = top_10_posts['Formato'].mode().iloc[0] if not top_10_posts['Formato'].mode().empty else "N/A"
                            st.metric("🎨 Formato Top", formato_dominante)
                
            else:
                st.warning("⚠️ No se encontró columna de alcance")

        with subtab4:
            st.subheader("❤️ Interacción")
            
            if 'Interacciones' in df_filtrado.columns:
                # Métricas principales 
                col1, col2, col3 = st.columns(3)
                col1.metric("Interacciones Totales", f"{df_filtrado['Interacciones'].sum():,.0f}")
                col2.metric("Interacciones Promedio", f"{df_filtrado['Interacciones'].mean():.0f}")
                if 'Alcance' in df_filtrado.columns:
                    engagement = (df_filtrado['Interacciones'].sum() / df_filtrado['Alcance'].sum()) * 100 if df_filtrado['Alcance'].sum() > 0 else 0
                    col3.metric("Engagement Rate", f"{engagement:.2f}%")
                
                # GRÁFICO EXISTENTE: Interacciones por Canal 
                if 'Canal' in df_filtrado.columns:
                    interaccion_canal = df_filtrado.groupby('Canal')['Interacciones'].mean().reset_index()
                    fig = px.bar(interaccion_canal, x='Canal', y='Interacciones',
                            title="📊 Interacciones promedio por Canal",
                            color='Interacciones', color_continuous_scale='Pinkyl')
                    fig.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
                    st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                
                #  GRÁFICAS ADICIONALES
                st.markdown("### 💫 Análisis Detallado de Interacción")
                
                # NUEVA GRÁFICA 1: Interacciones por Formato
                col_graf1, col_graf2 = st.columns(2)
                
                with col_graf1:
                    if 'Formato' in df_filtrado.columns:
                        st.markdown("#### 🎨 Interacciones por Formato de Contenido")
                        interaccion_formato = df_filtrado.groupby('Formato')['Interacciones'].agg(['sum', 'mean', 'count']).reset_index()
                        interaccion_formato.columns = ['Formato', 'Interacciones_Total', 'Interacciones_Promedio', 'Num_Posts']
                        
                        # Gráfico de barras con interacciones totales por formato
                        fig1 = px.bar(
                            interaccion_formato, 
                            x='Formato', 
                            y='Interacciones_Total',
                            title="💫 Interacciones Totales por Formato",
                            color='Interacciones_Total',
                            color_continuous_scale='Pinkyl',
                            text='Interacciones_Total'
                        )
                        
                        fig1.update_traces(
                            texttemplate='%{text:,.0f}', 
                            textposition='outside',
                            marker_line_color='rgba(233, 30, 99, 0.8)',
                            marker_line_width=1.5
                        )
                        
                        fig1.update_layout(
                            paper_bgcolor='rgba(255,255,255,0.9)', 
                            plot_bgcolor='rgba(255,255,255,0.9)',
                            font_color='#4a148c',
                            title_font_size=14,
                            title_font_color='#4a148c',
                            xaxis_title="Formato",
                            yaxis_title="Interacciones Totales",
                            showlegend=False,
                            height=350
                        )
                        
                        st.plotly_chart(fig1, use_container_width=True)
                
                with col_graf2:
                    # NUEVA GRÁFICA 2: Evolución de Interacciones por Fechas
                    if 'Fecha' in df_filtrado.columns:
                        st.markdown("#### 📈 Evolución Temporal de Interacciones")
                        # Crear serie temporal
                        df_temp = df_filtrado.copy()
                        df_temp['Fecha'] = pd.to_datetime(df_temp['Fecha'])
                        df_temp = df_temp.sort_values('Fecha')
                        
                        # Agrupar por semana para mejor visualización
                        df_temp['Semana'] = df_temp['Fecha'].dt.to_period('W').dt.start_time
                        interaccion_tiempo = df_temp.groupby('Semana')['Interacciones'].sum().reset_index()
                        
                        # Gráfico de línea temporal
                        fig2 = px.line(
                            interaccion_tiempo, 
                            x='Semana', 
                            y='Interacciones',
                            title="💫 Evolución Semanal de Interacciones",
                            markers=True,
                            color_discrete_sequence=['#e91e63']
                        )
                        
                        # Añadir área bajo la curva
                        fig2.add_scatter(
                            x=interaccion_tiempo['Semana'], 
                            y=interaccion_tiempo['Interacciones'],
                            fill='tonexty', 
                            mode='none',
                            fillcolor='rgba(233, 30, 99, 0.2)',
                            name='',
                            showlegend=False
                        )
                        
                        fig2.update_layout(
                            paper_bgcolor='rgba(255,255,255,0.9)', 
                            plot_bgcolor='rgba(255,255,255,0.9)',
                            font_color='#4a148c',
                            title_font_size=14,
                            title_font_color='#4a148c',
                            xaxis_title="Fecha",
                            yaxis_title="Interacciones Totales",
                            hovermode='x unified',
                            height=350,
                            showlegend=False
                        )
                        
                        fig2.update_traces(
                            hovertemplate='<b>Semana:</b> %{x}<br><b>Interacciones:</b> %{y:,.0f}<extra></extra>',
                            line=dict(width=3)
                        )
                        
                        st.plotly_chart(fig2, use_container_width=True)
                
                # NUEVA GRÁFICA 3: Top 10 Posts con Mayor Interacción
                st.markdown("---")
                st.markdown("### 🏆 Top 10 Posts con Mayor Interacción")
                
                if len(df_filtrado) > 0:
                    # Crear identificador único para cada post
                    df_top = df_filtrado.copy()
                    
                    # Si existe columna de contenido o descripción, usarla; si no, crear identificador
                    if 'Contenido' in df_top.columns:
                        df_top['Post_ID'] = df_top['Contenido'].apply(lambda x: str(x)[:40] + "..." if len(str(x)) > 40 else str(x))
                    elif 'Descripcion' in df_top.columns:
                        df_top['Post_ID'] = df_top['Descripcion'].apply(lambda x: str(x)[:40] + "..." if len(str(x)) > 40 else str(x))
                    else:
                        df_top['Post_ID'] = df_top.apply(lambda row: f"Post {row.name + 1} - {row['Fecha'].strftime('%d/%m/%Y') if 'Fecha' in df_top.columns else 'Sin fecha'}", axis=1)
                    
                    # Obtener top 10
                    top_10_posts = df_top.nlargest(10, 'Interacciones')[['Post_ID', 'Interacciones', 'Fecha', 'Canal', 'Formato']].reset_index(drop=True)
                    
                    # Añadir engagement rate si es posible
                    if 'Alcance' in df_top.columns:
                        top_10_posts_temp = df_top.nlargest(10, 'Interacciones')[['Post_ID', 'Interacciones', 'Alcance', 'Fecha', 'Canal', 'Formato']].reset_index(drop=True)
                        top_10_posts_temp['Engagement_Rate'] = (top_10_posts_temp['Interacciones'] / top_10_posts_temp['Alcance'] * 100).fillna(0)
                        top_10_posts = top_10_posts_temp
                    
                    # Gráfico de barras horizontales
                    fig3 = px.bar(
                        top_10_posts.iloc[::-1],  # Invertir para mostrar el mayor arriba
                        x='Interacciones', 
                        y='Post_ID',
                        title="🏆 Posts con Mayor Interacción",
                        orientation='h',
                        color='Interacciones',
                        color_continuous_scale='Pinkyl',
                        text='Interacciones'
                    )
                    
                    fig3.update_traces(
                        texttemplate='%{text:,.0f}', 
                        textposition='outside',
                        marker_line_color='rgba(233, 30, 99, 0.8)',
                        marker_line_width=1.5
                    )
                    
                    fig3.update_layout(
                        paper_bgcolor='rgba(255,255,255,0.9)', 
                        plot_bgcolor='rgba(255,255,255,0.9)',
                        font_color='#4a148c',
                        title_font_size=16,
                        title_font_color='#4a148c',
                        xaxis_title="Interacciones",
                        yaxis_title="Posts",
                        height=400,
                        showlegend=False,
                        margin=dict(l=20, r=20, t=60, b=20)
                    )
                    
                    fig3.update_yaxes(tickfont=dict(size=10))
                    st.plotly_chart(fig3, use_container_width=True)
                    
                    # Tabla del Top 5 (versión compacta)
                    st.markdown("##### 📋 Top 5 Detallado")
                    tabla_top5 = top_10_posts.head(5).copy()
                    tabla_top5['Ranking'] = range(1, len(tabla_top5) + 1)
                    tabla_top5['Interacciones_Formateado'] = tabla_top5['Interacciones'].apply(lambda x: f"{x:,.0f}")
                    tabla_top5['Fecha_Formateada'] = tabla_top5['Fecha'].dt.strftime('%d/%m/%Y') if 'Fecha' in tabla_top5.columns else 'N/A'
                    
                    # Preparar columnas para mostrar
                    columnas_tabla = ['Ranking', 'Post_ID', 'Interacciones_Formateado', 'Fecha_Formateada', 'Canal', 'Formato']
                    nombres_columnas = ['🏅', '📝 Post', '💫 Interacciones', '📅 Fecha', '📱 Canal', '🎨 Formato']
                    
                    # Si hay engagement rate, agregarlo
                    if 'Engagement_Rate' in tabla_top5.columns:
                        tabla_top5['Engagement_Formateado'] = tabla_top5['Engagement_Rate'].apply(lambda x: f"{x:.1f}%")
                        columnas_tabla.append('Engagement_Formateado')
                        nombres_columnas.append('🎯 Engagement')
                    
                    tabla_display = tabla_top5[columnas_tabla].copy()
                    tabla_display.columns = nombres_columnas
                    
                    st.dataframe(tabla_display, use_container_width=True, hide_index=True)
                    
                    # Insights del mejor post
                    col_insight1, col_insight2, col_insight3 = st.columns(3)
                    
                    with col_insight1:
                        mejor_post_interacciones = top_10_posts.iloc[0]['Interacciones']
                        st.metric("🥇 Mejor Post", f"{mejor_post_interacciones:,.0f}", "interacciones")
                    
                    with col_insight2:
                        if 'Canal' in top_10_posts.columns:
                            canal_dominante = top_10_posts['Canal'].mode().iloc[0] if not top_10_posts['Canal'].mode().empty else "N/A"
                            st.metric("📱 Canal Top", canal_dominante)
                    
                    with col_insight3:
                        if 'Formato' in top_10_posts.columns:
                            formato_dominante = top_10_posts['Formato'].mode().iloc[0] if not top_10_posts['Formato'].mode().empty else "N/A"
                            st.metric("🎨 Formato Top", formato_dominante)
                    
                    # Insight adicional de engagement si está disponible
                    if 'Engagement_Rate' in top_10_posts.columns:
                        st.markdown("---")
                        col_eng1, col_eng2, col_eng3 = st.columns(3)
                        
                        with col_eng1:
                            engagement_promedio = top_10_posts['Engagement_Rate'].mean()
                            st.metric("🎯 Engagement Promedio Top 10", f"{engagement_promedio:.2f}%")
                        
                        with col_eng2:
                            mejor_engagement = top_10_posts['Engagement_Rate'].max()
                            st.metric("🚀 Mejor Engagement", f"{mejor_engagement:.2f}%")
                        
                        with col_eng3:
                            # Calcular correlación entre interacciones y engagement
                            if len(top_10_posts) > 3:
                                correlacion = top_10_posts['Interacciones'].corr(top_10_posts['Engagement_Rate'])
                                interpretacion = "Alta" if abs(correlacion) > 0.7 else "Media" if abs(correlacion) > 0.3 else "Baja"
                                st.metric("📊 Correlación I-E", f"{interpretacion}", f"r={correlacion:.2f}")
                
            else:
                st.warning("⚠️ No se encontró columna de interacciones")

        with subtab5:
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
                    # MÉTRICAS EXISTENTES
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
                    
                    # GRÁFICOS EXISTENTES 
                    if 'Canal' in df_reels_clean.columns and len(df_reels_clean) > 0:
                        st.markdown("### 📊 Análisis de Reproducciones por Canal")
                        reproducciones_canal = df_reels_clean.groupby('Canal')['Reproducciones'].agg(['sum', 'mean']).reset_index()
                        reproducciones_canal.columns = ['Canal', 'Total_Reproducciones', 'Promedio_Reproducciones']

                        
                        fig_total = px.bar(
                            reproducciones_canal, 
                            x='Canal', 
                            y='Total_Reproducciones',
                            title="📊 Total de Reproducciones por Canal",
                            color='Total_Reproducciones', 
                            color_continuous_scale='Purples'
                        )
                        fig_total.update_layout(
                            paper_bgcolor='rgba(255,255,255,0.9)', 
                            font_color='#4a148c'
                        )
                        st.plotly_chart(fig_total, use_container_width=True)
                    
                    #ANÁLISIS DETALLADOS
                    st.markdown("---")
                    st.markdown("### 🎬 Análisis Avanzado de Videos")
                    
                    # NUEVA GRÁFICA 1: Reproducciones vs Duración del Video
                    col_video1, col_video2 = st.columns(2)
                    
                    with col_video1:
                        if 'Duracion_video' in df_reels_clean.columns:
                            df_duracion = df_reels_clean.dropna(subset=['Duracion_video', 'Reproducciones'])
                            
                            if len(df_duracion) > 0:
                                st.markdown("#### ⏱️ Reproducciones vs Duración del Video")
                                
                                fig_duracion = px.scatter(
                                    df_duracion, 
                                    x='Duracion_video', 
                                    y='Reproducciones',
                                    title="⏱️ Impacto de la Duración en Reproducciones",
                                    color='Reproducciones',
                                    color_continuous_scale='Viridis',
                                    size='Reproducciones',
                                    hover_data=['Canal'] if 'Canal' in df_duracion.columns else None
                                )
                                
                                # Añadir línea de tendencia
                                if len(df_duracion) > 3:
                                    from sklearn.linear_model import LinearRegression
                                    X_dur = df_duracion[['Duracion_video']].values
                                    y_dur = df_duracion['Reproducciones'].values
                                    
                                    reg_dur = LinearRegression().fit(X_dur, y_dur)
                                    df_duracion_sorted = df_duracion.sort_values('Duracion_video')
                                    y_pred_dur = reg_dur.predict(df_duracion_sorted[['Duracion_video']].values)
                                    
                                    fig_duracion.add_scatter(
                                        x=df_duracion_sorted['Duracion_video'],
                                        y=y_pred_dur,
                                        mode='lines',
                                        name='Tendencia',
                                        line=dict(color='red', width=2, dash='dash')
                                    )
                                
                                fig_duracion.update_layout(
                                    paper_bgcolor='rgba(255,255,255,0.9)', 
                                    font_color='#4a148c',
                                    xaxis_title="Duración (segundos)",
                                    yaxis_title="Reproducciones",
                                    height=350
                                )
                                
                                st.plotly_chart(fig_duracion, use_container_width=True)
                                
                                # Correlación
                                correlacion_dur = df_duracion['Duracion_video'].corr(df_duracion['Reproducciones'])
                                interpretacion_dur = "Fuerte" if abs(correlacion_dur) > 0.7 else "Moderada" if abs(correlacion_dur) > 0.3 else "Débil"
                                st.info(f"📊 Correlación duración-reproducciones: **{interpretacion_dur}** (r={correlacion_dur:.3f})")
                    
                    with col_video2:
                        # NUEVA GRÁFICA 2: Reproducciones vs Tiempo de Retención
                        if 'Retencion' in df_reels_clean.columns:
                            df_retencion = df_reels_clean.dropna(subset=['Retencion', 'Reproducciones'])
                            
                            if len(df_retencion) > 0:
                                st.markdown("#### 🎯 Reproducciones vs Retención")
                                
                                fig_retencion = px.scatter(
                                    df_retencion, 
                                    x='Retencion', 
                                    y='Reproducciones',
                                    title="🎯 Impacto de la Retención en Reproducciones",
                                    color='Reproducciones',
                                    color_continuous_scale='Plasma',
                                    size='Reproducciones',
                                    hover_data=['Canal'] if 'Canal' in df_retencion.columns else None
                                )
                                
                                # Añadir línea de tendencia
                                if len(df_retencion) > 3:
                                    X_ret = df_retencion[['Retencion']].values
                                    y_ret = df_retencion['Reproducciones'].values
                                    
                                    reg_ret = LinearRegression().fit(X_ret, y_ret)
                                    df_retencion_sorted = df_retencion.sort_values('Retencion')
                                    y_pred_ret = reg_ret.predict(df_retencion_sorted[['Retencion']].values)
                                    
                                    fig_retencion.add_scatter(
                                        x=df_retencion_sorted['Retencion'],
                                        y=y_pred_ret,
                                        mode='lines',
                                        name='Tendencia',
                                        line=dict(color='orange', width=2, dash='dash')
                                    )
                                
                                fig_retencion.update_layout(
                                    paper_bgcolor='rgba(255,255,255,0.9)', 
                                    font_color='#4a148c',
                                    xaxis_title="Retención (%)",
                                    yaxis_title="Reproducciones",
                                    height=350
                                )
                                
                                st.plotly_chart(fig_retencion, use_container_width=True)
                                
                                # Correlación
                                correlacion_ret = df_retencion['Retencion'].corr(df_retencion['Reproducciones'])
                                interpretacion_ret = "Fuerte" if abs(correlacion_ret) > 0.7 else "Moderada" if abs(correlacion_ret) > 0.3 else "Débil"
                                st.info(f"📊 Correlación retención-reproducciones: **{interpretacion_ret}** (r={correlacion_ret:.3f})")
                    
                    # NUEVA GRÁFICA 3: Visibilidad e Interacción vs Duración
                    if 'Duracion_video' in df_reels_clean.columns and 'Alcance' in df_reels_clean.columns and 'Interacciones' in df_reels_clean.columns:
                        st.markdown("---")
                        st.markdown("#### 📊 Impacto de la Duración en Visibilidad e Interacción")
                        
                        df_completo = df_reels_clean.dropna(subset=['Duracion_video', 'Alcance', 'Interacciones'])
                        
                        if len(df_completo) > 0:
                            # Crear rangos de duración para mejor análisis
                            df_completo['Rango_Duracion'] = pd.cut(
                                df_completo['Duracion_video'], 
                                bins=5, 
                                labels=['Muy Corto', 'Corto', 'Medio', 'Largo', 'Muy Largo'],
                                precision=0
                            )
                            
                            # Agrupar por rango de duración
                            metricas_duracion = df_completo.groupby('Rango_Duracion').agg({
                                'Alcance': 'mean',
                                'Interacciones': 'mean',
                                'Duracion_video': 'mean'
                            }).reset_index()
                            
                            # Crear gráfico de barras agrupadas
                            fig_metricas = go.Figure()
                            
                            fig_metricas.add_trace(go.Bar(
                                name='Alcance Promedio',
                                x=metricas_duracion['Rango_Duracion'],
                                y=metricas_duracion['Alcance'],
                                marker_color='rgba(142, 36, 170, 0.8)',
                                yaxis='y'
                            ))
                            
                            fig_metricas.add_trace(go.Bar(
                                name='Interacciones Promedio',
                                x=metricas_duracion['Rango_Duracion'],
                                y=metricas_duracion['Interacciones'],
                                marker_color='rgba(233, 30, 99, 0.8)',
                                yaxis='y2'
                            ))
                            
                            fig_metricas.update_layout(
                                title="📊 Alcance e Interacciones por Rango de Duración",
                                xaxis_title="Rango de Duración",
                                paper_bgcolor='rgba(255,255,255,0.9)',
                                font_color='#4a148c',
                                barmode='group',
                                height=400,
                                yaxis=dict(title="Alcance Promedio", side="left"),
                                yaxis2=dict(title="Interacciones Promedio", side="right", overlaying="y")
                            )
                            
                            st.plotly_chart(fig_metricas, use_container_width=True)
                            
                            # Mostrar tabla resumen
                            st.markdown("##### 📋 Resumen por Rango de Duración")
                            tabla_duracion = metricas_duracion.copy()
                            tabla_duracion['Alcance'] = tabla_duracion['Alcance'].apply(lambda x: f"{x:,.0f}")
                            tabla_duracion['Interacciones'] = tabla_duracion['Interacciones'].apply(lambda x: f"{x:,.0f}")
                            tabla_duracion['Duracion_video'] = tabla_duracion['Duracion_video'].apply(lambda x: f"{x:.1f}s")
                            tabla_duracion.columns = ['Rango', 'Alcance Promedio', 'Interacciones Promedio', 'Duración Promedio']
                            
                            st.dataframe(tabla_duracion, use_container_width=True, hide_index=True)
                    
                    # NUEVA TABLA: Top 10 Videos con Mayor Engagement
                    st.markdown("---")
                    st.markdown("### 🏆 Top 10 Videos con Mayor Engagement")
                    
                    if 'Alcance' in df_reels_clean.columns and 'Interacciones' in df_reels_clean.columns:
                        # Calcular engagement rate
                        df_engagement = df_reels_clean.copy()
                        df_engagement['Engagement_Rate'] = (df_engagement['Interacciones'] / df_engagement['Alcance'] * 100).fillna(0)
                        
                        # Filtrar solo videos con engagement > 0
                        df_engagement = df_engagement[df_engagement['Engagement_Rate'] > 0]
                        
                        if len(df_engagement) > 0:
                            # Crear identificador de video
                            if 'Contenido' in df_engagement.columns:
                                df_engagement['Video_ID'] = df_engagement['Contenido'].apply(lambda x: str(x)[:30] + "..." if len(str(x)) > 30 else str(x))
                            elif 'Descripcion' in df_engagement.columns:
                                df_engagement['Video_ID'] = df_engagement['Descripcion'].apply(lambda x: str(x)[:30] + "..." if len(str(x)) > 30 else str(x))
                            else:
                                df_engagement['Video_ID'] = df_engagement.apply(lambda row: f"Video {row.name + 1} - {row['Fecha'].strftime('%d/%m/%Y') if 'Fecha' in df_engagement.columns else 'Sin fecha'}", axis=1)
                            
                            # Obtener top 10 por engagement
                            top_10_engagement = df_engagement.nlargest(10, 'Engagement_Rate')
                            
                            # Mostrar como cards
                            st.markdown("#### 🎬 Videos Más Exitosos")
                            
                            for i in range(0, min(10, len(top_10_engagement)), 2):
                                cols = st.columns(2)
                                
                                for j in range(2):
                                    if i + j < len(top_10_engagement):
                                        video = top_10_engagement.iloc[i + j]
                                        
                                        with cols[j]:
                                            st.markdown(f"""
                                            <div style='background:rgba(255,255,255,0.9);padding:1rem;border-radius:10px;border-left: 4px solid #8e24aa;margin-bottom:1rem;'>
                                                <h5>🏅 #{i+j+1} - {video['Video_ID']}</h5>
                                                <p><strong>🎯 Engagement:</strong> {video['Engagement_Rate']:.2f}%</p>
                                                <p><strong>▶️ Reproducciones:</strong> {video['Reproducciones']:,.0f}</p>
                                                <p><strong>👁️ Alcance:</strong> {video['Alcance']:,.0f}</p>
                                                <p><strong>❤️ Interacciones:</strong> {video['Interacciones']:,.0f}</p>
                                                <p><strong>📱 Canal:</strong> {video['Canal']}</p>
                                                <p><strong>📅 Fecha:</strong> {video['Fecha'].strftime('%d/%m/%Y')}</p>
                                            </div>
                                            """, unsafe_allow_html=True)
                            
                            # Tabla completa
                            st.markdown("##### 📊 Tabla Completa del Top 10")
                            
                            # Preparar datos para la tabla
                            tabla_top10 = top_10_engagement[['Video_ID', 'Engagement_Rate', 'Reproducciones', 'Alcance', 'Interacciones', 'Canal', 'Fecha']].copy()
                            
                            # Agregar información adicional si está disponible
                            columnas_extra = []
                            if 'Duracion_video' in tabla_top10.columns:
                                columnas_extra.append('Duracion_video')
                            if 'Retencion' in tabla_top10.columns:
                                columnas_extra.append('Retencion')
                            
                            # Formatear tabla
                            tabla_top10['Ranking'] = range(1, len(tabla_top10) + 1)
                            tabla_top10['Engagement_Rate'] = tabla_top10['Engagement_Rate'].apply(lambda x: f"{x:.2f}%")
                            tabla_top10['Reproducciones'] = tabla_top10['Reproducciones'].apply(lambda x: f"{x:,.0f}")
                            tabla_top10['Alcance'] = tabla_top10['Alcance'].apply(lambda x: f"{x:,.0f}")
                            tabla_top10['Interacciones'] = tabla_top10['Interacciones'].apply(lambda x: f"{x:,.0f}")
                            tabla_top10['Fecha'] = tabla_top10['Fecha'].dt.strftime('%d/%m/%Y')
                            
                            # Reordenar columnas
                            columnas_finales = ['Ranking', 'Video_ID', 'Engagement_Rate', 'Reproducciones', 'Alcance', 'Interacciones', 'Canal', 'Fecha']
                            
                            # Agregar columnas extra si existen
                            for col in columnas_extra:
                                if col in top_10_engagement.columns:
                                    if col == 'Duracion_video':
                                        tabla_top10['Duracion_video'] = top_10_engagement['Duracion_video'].apply(lambda x: f"{x:.1f}s" if pd.notna(x) else "N/A")
                                        columnas_finales.append('Duracion_video')
                                    elif col == 'Retencion':
                                        tabla_top10['Retencion'] = top_10_engagement['Retencion'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
                                        columnas_finales.append('Retencion')
                            
                            tabla_display = tabla_top10[columnas_finales].copy()
                            
                            # Renombrar columnas
                            nombres_columnas = ['🏅 Rank', '🎬 Video', '🎯 Engagement', '▶️ Reproducciones', '👁️ Alcance', '❤️ Interacciones', '📱 Canal', '📅 Fecha']
                            
                            if 'Duracion_video' in columnas_finales:
                                nombres_columnas.append('⏱️ Duración')
                            if 'Retencion' in columnas_finales:
                                nombres_columnas.append('🎯 Retención')
                            
                            tabla_display.columns = nombres_columnas
                            
                            st.dataframe(tabla_display, use_container_width=True, hide_index=True)
                            
                            # Insights finales
                            st.markdown("##### 💡 Insights del Top 10")
                            col_insight1, col_insight2, col_insight3 = st.columns(3)
                            
                            with col_insight1:
                                mejor_engagement = top_10_engagement.iloc[0]['Engagement_Rate']
                                st.metric("🥇 Mejor Engagement", f"{mejor_engagement:.2f}%")
                            
                            with col_insight2:
                                engagement_promedio_top10 = top_10_engagement['Engagement_Rate'].mean()
                                st.metric("📊 Engagement Promedio Top 10", f"{engagement_promedio_top10:.2f}%")
                            
                            with col_insight3:
                                canal_dominante_engagement = top_10_engagement['Canal'].mode().iloc[0] if not top_10_engagement['Canal'].mode().empty else "N/A"
                                st.metric("📱 Canal Dominante", canal_dominante_engagement)
                            
                            # Análisis adicional si hay datos de duración
                            if 'Duracion_video' in top_10_engagement.columns:
                                st.markdown("---")
                                col_dur1, col_dur2, col_dur3 = st.columns(3)
                                
                                duraciones_validas = top_10_engagement.dropna(subset=['Duracion_video'])
                                if len(duraciones_validas) > 0:
                                    with col_dur1:
                                        duracion_optima = duraciones_validas['Duracion_video'].mean()
                                        st.metric("⏱️ Duración Óptima", f"{duracion_optima:.1f}s", "promedio top 10")
                                    
                                    with col_dur2:
                                        duracion_mejor = duraciones_validas.loc[duraciones_validas['Engagement_Rate'].idxmax(), 'Duracion_video']
                                        st.metric("🏆 Duración Mejor Video", f"{duracion_mejor:.1f}s")
                                    
                                    with col_dur3:
                                        if len(duraciones_validas) > 3:
                                            corr_dur_eng = duraciones_validas['Duracion_video'].corr(duraciones_validas['Engagement_Rate'])
                                            interpretacion = "Positiva" if corr_dur_eng > 0.3 else "Negativa" if corr_dur_eng < -0.3 else "Neutra"
                                            st.metric("📊 Correlación Duración-Engagement", interpretacion, f"r={corr_dur_eng:.3f}")
                        
                        else:
                            st.warning("⚠️ No hay videos con engagement válido para crear el ranking")
                    
                    else:
                        st.warning("⚠️ No se pueden calcular métricas de engagement sin datos de alcance e interacciones")

        with subtab6:
            st.subheader("🛒 Conversión")
            if 'Compras' in df_filtrado.columns:
                # MÉTRICAS PRINCIPALES EXISTENTES
                col1, col2, col3 = st.columns(3)
                total_compras = df_filtrado['Compras'].sum()
                promedio_compras = df_filtrado['Compras'].mean()
                tasa_conversion = (total_compras / df_filtrado['Alcance'].sum()) * 100 if 'Alcance' in df_filtrado.columns and df_filtrado['Alcance'].sum() > 0 else 0
                
                col1.metric("🛍️ Compras Totales", f"{total_compras:,}")
                col2.metric("📈 Compras Promedio", f"{promedio_compras:.1f}")
                col3.metric("💯 Tasa de Conversión", f"{tasa_conversion:.3f}%")
                
                # GRÁFICOS EXISTENTES POR CANAL
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
                
                # NUEVOS GRÁFICOS POR FORMATO
                st.markdown("---")
                st.markdown("### 🎨 Análisis de Conversión por Formato")
                
                if 'Formato' in df_filtrado.columns:
                    conversion_formato = df_filtrado.groupby('Formato').agg({
                        'Compras': ['sum', 'mean'],
                        'Alcance': 'sum'
                    }).reset_index()
                    conversion_formato.columns = ['Formato', 'Total_Compras', 'Promedio_Compras', 'Total_Alcance']
                    conversion_formato['Tasa_Conversion'] = (conversion_formato['Total_Compras'] / conversion_formato['Total_Alcance'] * 100).fillna(0)
                    
                    col_formato1, col_formato2 = st.columns(2)
                    
                    with col_formato1:
                        st.markdown("#### 🛍️ Ventas por Formato de Contenido")
                        fig_ventas_formato = px.bar(
                            conversion_formato, 
                            x='Formato', 
                            y='Total_Compras',
                            title="🛍️ Número de Ventas por Formato",
                            color='Total_Compras',
                            color_continuous_scale='Greens',
                            text='Total_Compras'
                        )
                        
                        fig_ventas_formato.update_traces(
                            texttemplate='%{text}', 
                            textposition='outside',
                            marker_line_color='rgba(76, 175, 80, 0.8)',
                            marker_line_width=1.5
                        )
                        
                        fig_ventas_formato.update_layout(
                            paper_bgcolor='rgba(255,255,255,0.9)', 
                            plot_bgcolor='rgba(255,255,255,0.9)',
                            font_color='#4a148c',
                            title_font_size=14,
                            title_font_color='#4a148c',
                            xaxis_title="Formato",
                            yaxis_title="Número de Ventas",
                            showlegend=False,
                            height=350
                        )
                        
                        st.plotly_chart(fig_ventas_formato, use_container_width=True)
                    
                    with col_formato2:
                        st.markdown("#### 💯 Conversión por Formato de Contenido")
                        fig_conversion_formato = px.bar(
                            conversion_formato, 
                            x='Formato', 
                            y='Tasa_Conversion',
                            title="💯 Tasa de Conversión por Formato (%)",
                            color='Tasa_Conversion',
                            color_continuous_scale='Blues',
                            text='Tasa_Conversion'
                        )
                        
                        fig_conversion_formato.update_traces(
                            texttemplate='%{text:.2f}%', 
                            textposition='outside',
                            marker_line_color='rgba(33, 150, 243, 0.8)',
                            marker_line_width=1.5
                        )
                        
                        fig_conversion_formato.update_layout(
                            paper_bgcolor='rgba(255,255,255,0.9)', 
                            plot_bgcolor='rgba(255,255,255,0.9)',
                            font_color='#4a148c',
                            title_font_size=14,
                            title_font_color='#4a148c',
                            xaxis_title="Formato",
                            yaxis_title="Tasa de Conversión (%)",
                            showlegend=False,
                            height=350
                        )
                        
                        st.plotly_chart(fig_conversion_formato, use_container_width=True)
                    
                    # Tabla resumen por formato
                    st.markdown("##### 📋 Resumen por Formato")
                    tabla_formato = conversion_formato.copy()
                    tabla_formato['Promedio_Compras'] = tabla_formato['Promedio_Compras'].apply(lambda x: f"{x:.1f}")
                    tabla_formato['Tasa_Conversion'] = tabla_formato['Tasa_Conversion'].apply(lambda x: f"{x:.3f}%")
                    tabla_formato['Total_Alcance'] = tabla_formato['Total_Alcance'].apply(lambda x: f"{x:,.0f}")
                    tabla_formato.columns = ['Formato', 'Total Ventas', 'Ventas Promedio', 'Alcance Total', 'Tasa Conversión']
                    
                    st.dataframe(tabla_formato, use_container_width=True, hide_index=True)
                
                # GRÁFICO DE FUNNEL DE CONVERSIÓN
                st.markdown("---")
                st.markdown("### 📊 Funnel de Conversión")
                
                # Simular datos del funnel basados en los datos disponibles
                # En un caso real, estos datos vendrían de analytics de la web/app
                total_alcance = df_filtrado['Alcance'].sum() if 'Alcance' in df_filtrado.columns else 0
                total_interacciones = df_filtrado['Interacciones'].sum() if 'Interacciones' in df_filtrado.columns else 0
                total_ventas = df_filtrado['Compras'].sum()
                
                # Estimar visitas y carritos basándose en datos disponibles
                # Asumiendo que las interacciones representan un porcentaje de visitas
                visitas_estimadas = int(total_interacciones * 1.5)  # Factor de conversión estimado
                carritos_estimados = int(total_ventas * 3)  # Asumiendo que por cada venta hay 3 carritos abandonados
                
                # Crear datos del funnel
                funnel_data = {
                    'Etapa': ['👁️ Visibilidad\n(Alcance)', '🎯 Interés\n(Visitas)', '🛒 Consideración\n(Carritos)', '🛍️ Conversión\n(Ventas)'],
                    'Cantidad': [total_alcance, visitas_estimadas, carritos_estimados, total_ventas],
                    'Porcentaje': [100, 0, 0, 0]
                }
                
                # Calcular porcentajes
                if total_alcance > 0:
                    funnel_data['Porcentaje'][1] = (visitas_estimadas / total_alcance) * 100
                    funnel_data['Porcentaje'][2] = (carritos_estimados / total_alcance) * 100
                    funnel_data['Porcentaje'][3] = (total_ventas / total_alcance) * 100
                
                df_funnel = pd.DataFrame(funnel_data)
                
                # Crear gráfico de funnel
                fig_funnel = go.Figure()
                
                # Colores para cada etapa
                colores = ['#e3f2fd', '#90caf9', '#42a5f5', '#1976d2']
                
                for i, (etapa, cantidad, porcentaje) in enumerate(zip(df_funnel['Etapa'], df_funnel['Cantidad'], df_funnel['Porcentaje'])):
                    fig_funnel.add_trace(go.Funnel(
                        y=[etapa],
                        x=[cantidad],
                        textinfo="value+percent initial",
                        texttemplate=f"{cantidad:,.0f}<br>({porcentaje:.2f}%)",
                        marker=dict(color=colores[i]),
                        name=etapa
                    ))
                
                fig_funnel.update_layout(
                    title="📊 Funnel de Conversión - Del Alcance a las Ventas",
                    paper_bgcolor='rgba(255,255,255,0.9)',
                    font_color='#4a148c',
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig_funnel, use_container_width=True)
                
                # Métricas del funnel
                col_funnel1, col_funnel2, col_funnel3 = st.columns(3)
                
                with col_funnel1:
                    if visitas_estimadas > 0:
                        tasa_interes = (visitas_estimadas / total_alcance) * 100 if total_alcance > 0 else 0
                        st.metric("🎯 Tasa de Interés", f"{tasa_interes:.2f}%", "alcance → visitas")
                
                with col_funnel2:
                    if carritos_estimados > 0:
                        tasa_consideracion = (carritos_estimados / visitas_estimadas) * 100 if visitas_estimadas > 0 else 0
                        st.metric("🛒 Tasa de Consideración", f"{tasa_consideracion:.2f}%", "visitas → carritos")
                
                with col_funnel3:
                    if total_ventas > 0:
                        tasa_conversion_funnel = (total_ventas / carritos_estimados) * 100 if carritos_estimados > 0 else 0
                        st.metric("🛍️ Tasa de Conversión Final", f"{tasa_conversion_funnel:.2f}%", "carritos → ventas")
                
                # Insights del funnel
                st.markdown("##### 💡 Insights del Funnel")
                st.info(f"""
                **Análisis del Funnel de Conversión:**
                - **Punto fuerte**: {'Generación de interés' if tasa_interes > 5 else 'Alcance inicial' if total_alcance > 10000 else 'Conversión final' if tasa_conversion_funnel > 25 else 'Necesita optimización general'}
                - **Oportunidad de mejora**: {'Conversión final (carritos → ventas)' if tasa_conversion_funnel < 25 else 'Consideración (visitas → carritos)' if tasa_consideracion < 15 else 'Generación de interés (alcance → visitas)'}
                - **Recomendación**: {'Optimizar checkout y reducir fricción en la compra' if tasa_conversion_funnel < 25 else 'Mejorar páginas de producto y call-to-actions' if tasa_consideracion < 15 else 'Aumentar engagement y contenido atractivo'}
                """)
                
                # TOP 10 POSTS SEGÚN VENTAS
                st.markdown("---")
                st.markdown("### 🏆 Top 10 Posts con Mejores Ventas")
                
                if len(df_filtrado) > 0:
                    # Crear identificador único para cada post
                    df_ventas = df_filtrado.copy()
                    
                    # Si existe columna de contenido o descripción, usarla; si no, crear identificador
                    if 'Contenido' in df_ventas.columns:
                        df_ventas['Post_ID'] = df_ventas['Contenido'].apply(lambda x: str(x)[:35] + "..." if len(str(x)) > 35 else str(x))
                    elif 'Descripcion' in df_ventas.columns:
                        df_ventas['Post_ID'] = df_ventas['Descripcion'].apply(lambda x: str(x)[:35] + "..." if len(str(x)) > 35 else str(x))
                    else:
                        df_ventas['Post_ID'] = df_ventas.apply(lambda row: f"Post {row.name + 1} - {row['Fecha'].strftime('%d/%m/%Y') if 'Fecha' in df_ventas.columns else 'Sin fecha'}", axis=1)
                    
                    # Obtener top 10 por ventas
                    top_10_ventas = df_ventas.nlargest(10, 'Compras')
                    
                    if len(top_10_ventas) > 0:
                        # Gráfico de barras horizontales
                        fig_top_ventas = px.bar(
                            top_10_ventas.iloc[::-1],  # Invertir para mostrar el mayor arriba
                            x='Compras', 
                            y='Post_ID',
                            title="🏆 Posts con Mejores Ventas",
                            orientation='h',
                            color='Compras',
                            color_continuous_scale='Greens',
                            text='Compras'
                        )
                        
                        fig_top_ventas.update_traces(
                            texttemplate='%{text}', 
                            textposition='outside',
                            marker_line_color='rgba(76, 175, 80, 0.8)',
                            marker_line_width=1.5
                        )
                        
                        fig_top_ventas.update_layout(
                            paper_bgcolor='rgba(255,255,255,0.9)', 
                            plot_bgcolor='rgba(255,255,255,0.9)',
                            font_color='#4a148c',
                            title_font_size=16,
                            title_font_color='#4a148c',
                            xaxis_title="Número de Ventas",
                            yaxis_title="Posts",
                            height=400,
                            showlegend=False,
                            margin=dict(l=20, r=20, t=60, b=20)
                        )
                        
                        fig_top_ventas.update_yaxes(tickfont=dict(size=10))
                        st.plotly_chart(fig_top_ventas, use_container_width=True)
                        
                        # Tabla detallada del Top 10
                        st.markdown("##### 📋 Tabla Detallada del Top 10")
                        
                        # Preparar tabla para mostrar
                        tabla_ventas = top_10_ventas[['Post_ID', 'Compras', 'Fecha', 'Canal', 'Formato']].copy()
                        
                        # Añadir métricas adicionales si están disponibles
                        columnas_extra = ['Alcance', 'Interacciones', 'Valor_compra']
                        for col in columnas_extra:
                            if col in top_10_ventas.columns:
                                tabla_ventas[col] = top_10_ventas[col]
                        
                        # Calcular tasa de conversión si es posible
                        if 'Alcance' in tabla_ventas.columns:
                            tabla_ventas['Conversion_Rate'] = (tabla_ventas['Compras'] / tabla_ventas['Alcance'] * 100).fillna(0)
                        
                        # Formatear datos
                        tabla_ventas['Ranking'] = range(1, len(tabla_ventas) + 1)
                        tabla_ventas['Fecha_Formateada'] = tabla_ventas['Fecha'].dt.strftime('%d/%m/%Y') if 'Fecha' in tabla_ventas.columns else 'N/A'
                        
                        # Preparar columnas para mostrar
                        columnas_finales = ['Ranking', 'Post_ID', 'Compras', 'Fecha_Formateada', 'Canal', 'Formato']
                        nombres_columnas = ['🏅', '📝 Post', '🛍️ Ventas', '📅 Fecha', '📱 Canal', '🎨 Formato']
                        
                        # Añadir columnas extra si existen
                        if 'Alcance' in tabla_ventas.columns:
                            tabla_ventas['Alcance_Formateado'] = tabla_ventas['Alcance'].apply(lambda x: f"{x:,.0f}")
                            columnas_finales.append('Alcance_Formateado')
                            nombres_columnas.append('👁️ Alcance')
                        
                        if 'Interacciones' in tabla_ventas.columns:
                            tabla_ventas['Interacciones_Formateado'] = tabla_ventas['Interacciones'].apply(lambda x: f"{x:,.0f}")
                            columnas_finales.append('Interacciones_Formateado')
                            nombres_columnas.append('❤️ Interacciones')
                        
                        if 'Valor_compra' in tabla_ventas.columns:
                            tabla_ventas['Valor_Formateado'] = tabla_ventas['Valor_compra'].apply(lambda x: f"{x:,.2f}€")
                            columnas_finales.append('Valor_Formateado')
                            nombres_columnas.append('💰 Ingresos')
                        
                        if 'Conversion_Rate' in tabla_ventas.columns:
                            tabla_ventas['Conversion_Formateado'] = tabla_ventas['Conversion_Rate'].apply(lambda x: f"{x:.3f}%")
                            columnas_finales.append('Conversion_Formateado')
                            nombres_columnas.append('💯 Conversión')
                        
                        tabla_display = tabla_ventas[columnas_finales].copy()
                        tabla_display.columns = nombres_columnas
                        
                        st.dataframe(tabla_display, use_container_width=True, hide_index=True)
                        
                        # Insights del top 10 ventas
                        st.markdown("##### 💡 Insights de Ventas")
                        col_insight1, col_insight2, col_insight3 = st.columns(3)
                        
                        with col_insight1:
                            mejor_post_ventas = top_10_ventas.iloc[0]['Compras']
                            st.metric("🥇 Mejor Post", f"{mejor_post_ventas}", "ventas")
                        
                        with col_insight2:
                            if 'Canal' in top_10_ventas.columns:
                                canal_ventas_dominante = top_10_ventas['Canal'].mode().iloc[0] if not top_10_ventas['Canal'].mode().empty else "N/A"
                                st.metric("📱 Canal Más Efectivo", canal_ventas_dominante)
                        
                        with col_insight3:
                            if 'Formato' in top_10_ventas.columns:
                                formato_ventas_dominante = top_10_ventas['Formato'].mode().iloc[0] if not top_10_ventas['Formato'].mode().empty else "N/A"
                                st.metric("🎨 Formato Más Efectivo", formato_ventas_dominante)
                        
                        # Análisis adicional de ventas
                        if 'Valor_compra' in top_10_ventas.columns:
                            st.markdown("---")
                            col_valor1, col_valor2, col_valor3 = st.columns(3)
                            
                            with col_valor1:
                                ingresos_top10 = top_10_ventas['Valor_compra'].sum()
                                st.metric("💰 Ingresos Top 10", f"{ingresos_top10:,.2f}€")
                            
                            with col_valor2:
                                ticket_promedio = top_10_ventas['Valor_compra'].mean()
                                st.metric("🎫 Ticket Promedio", f"{ticket_promedio:,.2f}€")
                            
                            with col_valor3:
                                if 'Conversion_Rate' in tabla_ventas.columns:
                                    conversion_promedio_top10 = tabla_ventas['Conversion_Rate'].mean()
                                    st.metric("📊 Conversión Promedio Top 10", f"{conversion_promedio_top10:.3f}%")
                    
                    else:
                        st.warning("⚠️ No hay posts con ventas para mostrar el ranking")
                
            else:
                st.warning("⚠️ No se encontró columna de compras")

        with subtab7:
            st.subheader("💰 Retorno de Inversión")
            if 'Valor_compra' in df_filtrado.columns and 'Inversion' in df_filtrado.columns:
                col1, col2, col3, col4 = st.columns(4)
                
                total_ingresos = df_filtrado['Valor_compra'].sum()
                total_inversion = df_filtrado['Inversion'].sum()
                beneficio = total_ingresos - total_inversion
                roi = (beneficio / total_inversion * 100) if total_inversion > 0 else 0
                
                col1.metric("💰 Ingresos Totales", f"{total_ingresos:,.2f}€")
                col2.metric("💸 Inversión Total", f"{total_inversion:,.2f}€")
                col3.metric("💵 Beneficio", f"{beneficio:,.2f}€", 
                        delta=f"{roi:.1f}% ROI", 
                        delta_color="normal" if beneficio >= 0 else "inverse")
                col4.metric("📊 ROI", f"{roi:.2f}%", 
                        delta_color="normal" if roi >= 0 else "inverse")
                
                # Información contextual sobre ROI
                st.markdown("---")
                col_info1, col_info2, col_info3 = st.columns(3)
                
                with col_info1:
                    roi_status = "🟢 Positivo" if roi > 0 else "🔴 Negativo" if roi < 0 else "🟡 Neutro"
                    st.metric("📈 Estado del ROI", roi_status)
                
                with col_info2:
                    posts_rentables = df_filtrado[df_filtrado['Valor_compra'] > df_filtrado['Inversion']].shape[0]
                    total_posts = len(df_filtrado)
                    porcentaje_rentables = (posts_rentables / total_posts * 100) if total_posts > 0 else 0
                    st.metric("✅ Posts Rentables", f"{posts_rentables}/{total_posts}", f"{porcentaje_rentables:.1f}%")
                
                with col_info3:
                    # Calcular punto de equilibrio
                    if total_inversion > 0:
                        eficiencia = (total_ingresos / total_inversion)
                        st.metric("⚖️ Eficiencia", f"{eficiencia:.2f}x", "ingresos/inversión")
                
                if 'Canal' in df_filtrado.columns:
                    st.markdown("### 📊 Análisis de ROI por Canal")
                    
                    roi_canal = df_filtrado.groupby('Canal').agg({
                        'Valor_compra': 'sum',
                        'Inversion': 'sum'
                    }).reset_index()
                    roi_canal['Beneficio'] = roi_canal['Valor_compra'] - roi_canal['Inversion']
                    roi_canal['ROI'] = ((roi_canal['Beneficio'] / roi_canal['Inversion']) * 100).fillna(0)
                    
                    # Reemplazar infinitos por 0
                    roi_canal['ROI'] = roi_canal['ROI'].replace([np.inf, -np.inf], 0)
                    
                    col_roi1, col_roi2 = st.columns(2)
                    
                    with col_roi1:
                        # GRÁFICO: Beneficio por Canal con colores dinámicos
                        fig_beneficio = go.Figure()
                        
                        # Crear colores basados en si el beneficio es positivo o negativo
                        colores_beneficio = ['green' if b >= 0 else 'red' for b in roi_canal['Beneficio']]
                        
                        fig_beneficio.add_trace(go.Bar(
                            x=roi_canal['Canal'],
                            y=roi_canal['Beneficio'],
                            marker_color=colores_beneficio,
                            text=roi_canal['Beneficio'].apply(lambda x: f"{x:,.0f}€"),
                            textposition='outside',
                            name='Beneficio'
                        ))
                        
                        # Añadir línea de referencia en 0
                        fig_beneficio.add_hline(y=0, line_dash="dash", line_color="black", 
                                            annotation_text="Punto de equilibrio")
                        
                        fig_beneficio.update_layout(
                            title="💵 Beneficio por Canal",
                            xaxis_title="Canal",
                            yaxis_title="Beneficio (€)",
                            paper_bgcolor='rgba(255,255,255,0.9)', 
                            font_color='#4a148c',
                            showlegend=False
                        )
                        
                        st.plotly_chart(fig_beneficio, use_container_width=True)
                    
                    with col_roi2:
                        # GRÁFICO ROI por Canal con colores dinámicos
                        fig_roi = go.Figure()
                        
                        # Crear colores basados en si el ROI es positivo o negativo
                        colores_roi = ['green' if r >= 0 else 'red' for r in roi_canal['ROI']]
                        
                        fig_roi.add_trace(go.Bar(
                            x=roi_canal['Canal'],
                            y=roi_canal['ROI'],
                            marker_color=colores_roi,
                            text=roi_canal['ROI'].apply(lambda x: f"{x:.1f}%"),
                            textposition='outside',
                            name='ROI'
                        ))
                        
                        # Añadir línea de referencia en 0
                        fig_roi.add_hline(y=0, line_dash="dash", line_color="black", 
                                        annotation_text="ROI = 0%")
                        
                        fig_roi.update_layout(
                            title="📊 ROI por Canal (%)",
                            xaxis_title="Canal",
                            yaxis_title="ROI (%)",
                            paper_bgcolor='rgba(255,255,255,0.9)', 
                            font_color='#4a148c',
                            showlegend=False
                        )
                        
                        st.plotly_chart(fig_roi, use_container_width=True)
                    
                    # NUEVA GRÁFICA: Evolución Temporal del ROI
                    st.markdown("---")
                    st.markdown("### 📈 Evolución Temporal del ROI")
                    
                    if 'Fecha' in df_filtrado.columns:
                        # Crear análisis temporal
                        df_temporal = df_filtrado.copy()
                        df_temporal['Fecha'] = pd.to_datetime(df_temporal['Fecha'])
                        df_temporal = df_temporal.sort_values('Fecha')
                        
                        # Agrupar por mes para mejor visualización
                        df_temporal['Mes'] = df_temporal['Fecha'].dt.to_period('M').dt.start_time
                        
                        roi_temporal = df_temporal.groupby('Mes').agg({
                            'Valor_compra': 'sum',
                            'Inversion': 'sum'
                        }).reset_index()
                        
                        roi_temporal['Beneficio'] = roi_temporal['Valor_compra'] - roi_temporal['Inversion']
                        roi_temporal['ROI'] = ((roi_temporal['Beneficio'] / roi_temporal['Inversion']) * 100).fillna(0)
                        roi_temporal['ROI'] = roi_temporal['ROI'].replace([np.inf, -np.inf], 0)
                        
                        # Calcular ROI acumulado
                        roi_temporal['Ingresos_Acum'] = roi_temporal['Valor_compra'].cumsum()
                        roi_temporal['Inversion_Acum'] = roi_temporal['Inversion'].cumsum()
                        roi_temporal['ROI_Acumulado'] = ((roi_temporal['Ingresos_Acum'] - roi_temporal['Inversion_Acum']) / roi_temporal['Inversion_Acum'] * 100).fillna(0)
                        roi_temporal['ROI_Acumulado'] = roi_temporal['ROI_Acumulado'].replace([np.inf, -np.inf], 0)
                        
                        # Crear gráfico de evolución con dos líneas
                        fig_evolution = go.Figure()
                        
                        # ROI mensual
                        fig_evolution.add_trace(go.Scatter(
                            x=roi_temporal['Mes'],
                            y=roi_temporal['ROI'],
                            mode='lines+markers',
                            name='ROI Mensual',
                            line=dict(color='#e91e63', width=3),
                            marker=dict(size=8),
                            hovertemplate='<b>Mes:</b> %{x}<br><b>ROI Mensual:</b> %{y:.2f}%<extra></extra>'
                        ))
                        
                        # ROI acumulado
                        fig_evolution.add_trace(go.Scatter(
                            x=roi_temporal['Mes'],
                            y=roi_temporal['ROI_Acumulado'],
                            mode='lines+markers',
                            name='ROI Acumulado',
                            line=dict(color='#8e24aa', width=3, dash='dash'),
                            marker=dict(size=8),
                            hovertemplate='<b>Mes:</b> %{x}<br><b>ROI Acumulado:</b> %{y:.2f}%<extra></extra>'
                        ))
                        
                        # Añadir línea de referencia en 0
                        fig_evolution.add_hline(y=0, line_dash="dot", line_color="black", 
                                            annotation_text="ROI = 0%")
                        
                        # Añadir áreas de color para indicar rentabilidad
                        max_roi = max(roi_temporal['ROI'].max(), roi_temporal['ROI_Acumulado'].max())
                        min_roi = min(roi_temporal['ROI'].min(), roi_temporal['ROI_Acumulado'].min())
                        
                        # Área verde para ROI positivo
                        fig_evolution.add_hrect(y0=0, y1=max_roi*1.1, 
                                            fillcolor="rgba(76, 175, 80, 0.1)", 
                                            line_width=0)
                        
                        # Área roja para ROI negativo
                        if min_roi < 0:
                            fig_evolution.add_hrect(y0=min_roi*1.1, y1=0, 
                                                fillcolor="rgba(244, 67, 54, 0.1)", 
                                                line_width=0)
                        
                        fig_evolution.update_layout(
                            title="📈 Evolución del ROI a lo Largo del Tiempo",
                            xaxis_title="Fecha",
                            yaxis_title="ROI (%)",
                            paper_bgcolor='rgba(255,255,255,0.9)',
                            font_color='#4a148c',
                            hovermode='x unified',
                            height=450,
                            legend=dict(
                                yanchor="top",
                                y=0.99,
                                xanchor="left",
                                x=0.01
                            )
                        )
                        
                        st.plotly_chart(fig_evolution, use_container_width=True)
                        
                        # Análisis de tendencias
                        col_trend1, col_trend2, col_trend3 = st.columns(3)
                        
                        with col_trend1:
                            # Tendencia del ROI
                            if len(roi_temporal) >= 2:
                                tendencia_roi = roi_temporal['ROI'].iloc[-1] - roi_temporal['ROI'].iloc[0]
                                trend_emoji = "📈" if tendencia_roi > 0 else "📉" if tendencia_roi < 0 else "📊"
                                st.metric("📊 Tendencia ROI", f"{trend_emoji} {tendencia_roi:+.2f}%", "vs primer mes")
                        
                        with col_trend2:
                            # Mejor mes
                            mejor_mes = roi_temporal.loc[roi_temporal['ROI'].idxmax(), 'Mes']
                            mejor_roi = roi_temporal['ROI'].max()
                            st.metric("🏆 Mejor Mes", mejor_mes.strftime('%Y-%m'), f"{mejor_roi:.2f}% ROI")
                        
                        with col_trend3:
                            # ROI actual vs acumulado
                            roi_actual = roi_temporal['ROI'].iloc[-1]
                            roi_acum_actual = roi_temporal['ROI_Acumulado'].iloc[-1]
                            st.metric("🔄 ROI Actual vs Acumulado", f"{roi_actual:.2f}%", f"Acum: {roi_acum_actual:.2f}%")
                        
                        # Tabla temporal detallada
                        st.markdown("##### 📋 Tabla Temporal Detallada")
                        tabla_temporal = roi_temporal.copy()
                        tabla_temporal['Mes_Formato'] = tabla_temporal['Mes'].dt.strftime('%Y-%m')
                        tabla_temporal['Ingresos_Formato'] = tabla_temporal['Valor_compra'].apply(lambda x: f"{x:,.2f}€")
                        tabla_temporal['Inversion_Formato'] = tabla_temporal['Inversion'].apply(lambda x: f"{x:,.2f}€")
                        tabla_temporal['Beneficio_Formato'] = tabla_temporal['Beneficio'].apply(lambda x: f"{x:,.2f}€")
                        tabla_temporal['ROI_Formato'] = tabla_temporal['ROI'].apply(lambda x: f"{x:.2f}%")
                        tabla_temporal['ROI_Acum_Formato'] = tabla_temporal['ROI_Acumulado'].apply(lambda x: f"{x:.2f}%")
                        
                        tabla_display_temporal = tabla_temporal[['Mes_Formato', 'Ingresos_Formato', 'Inversion_Formato', 'Beneficio_Formato', 'ROI_Formato', 'ROI_Acum_Formato']].copy()
                        tabla_display_temporal.columns = ['📅 Mes', '💰 Ingresos', '💸 Inversión', '💵 Beneficio', '📊 ROI Mensual', '📈 ROI Acumulado']
                        
                        st.dataframe(tabla_display_temporal, use_container_width=True, hide_index=True)
                    
                    else:
                        st.warning("⚠️ No se puede crear evolución temporal sin datos de fecha")
                    
                    # Tabla resumen de ROI CORREGIDA
                    st.markdown("---")
                    st.markdown("### 📋 Resumen Detallado por Canal")
                    roi_canal_formatted = roi_canal.copy()
                    roi_canal_formatted['Valor_compra'] = roi_canal_formatted['Valor_compra'].apply(lambda x: f"{x:,.2f}€")
                    roi_canal_formatted['Inversion'] = roi_canal_formatted['Inversion'].apply(lambda x: f"{x:,.2f}€")
                    roi_canal_formatted['Beneficio'] = roi_canal_formatted['Beneficio'].apply(lambda x: f"{x:,.2f}€")
                    roi_canal_formatted['ROI'] = roi_canal_formatted['ROI'].apply(lambda x: f"{x:.2f}%")
                    
                    # Añadir columna de estado
                    roi_canal_formatted['Estado'] = roi_canal['ROI'].apply(
                        lambda x: "🟢 Rentable" if x > 0 else "🔴 Pérdidas" if x < 0 else "🟡 Equilibrio"
                    )
                    
                    roi_canal_formatted.columns = ['Canal', 'Ingresos', 'Inversión', 'Beneficio', 'ROI', 'Estado']
                    
                    st.dataframe(roi_canal_formatted, use_container_width=True, hide_index=True)
                    
                    # Insights adicionales
                    st.markdown("---")
                    st.markdown("### 💡 Insights de ROI")
                    
                    # Calcular insights
                    canales_rentables = roi_canal[roi_canal['ROI'] > 0]
                    canales_perdidas = roi_canal[roi_canal['ROI'] < 0]
                    
                    col_insight1, col_insight2 = st.columns(2)
                    
                    with col_insight1:
                        if len(canales_rentables) > 0:
                            mejor_canal = canales_rentables.loc[canales_rentables['ROI'].idxmax()]
                            st.success(f"🏆 **Mejor Canal**: {mejor_canal['Canal']} con {mejor_canal['ROI']:.2f}% ROI")
                        
                        if len(canales_perdidas) > 0:
                            peor_canal = canales_perdidas.loc[canales_perdidas['ROI'].idxmin()]
                            st.error(f"⚠️ **Canal a Revisar**: {peor_canal['Canal']} con {peor_canal['ROI']:.2f}% ROI")
                    
                    with col_insight2:
                        # Recomendaciones
                        st.markdown("#### 🎯 Recomendaciones")
                        if len(canales_rentables) > 0:
                            st.info(f"💡 Aumentar inversión en: {', '.join(canales_rentables['Canal'].tolist())}")
                        if len(canales_perdidas) > 0:
                            st.warning(f"🔍 Optimizar estrategia en: {', '.join(canales_perdidas['Canal'].tolist())}")
                        
                        # Eficiencia promedio
                        eficiencia_promedio = roi_canal['ROI'].mean()
                        if eficiencia_promedio > 0:
                            st.success(f"📈 ROI promedio positivo: {eficiencia_promedio:.2f}%")
                        else:
                            st.error(f"📉 ROI promedio negativo: {eficiencia_promedio:.2f}%")
                
            else:
                st.warning("⚠️ No se encontraron columnas de ingresos o inversión")
                st.info("💡 Asegúrate de que tu dataset contenga las columnas 'Valor_compra' e 'Inversion' para ver este análisis")

# --- TAB 2: MODELO PREDICTIVO ---
with tab2:
    st.header("🔮 Modelo Predictivo")
    
    if not models_ok:
        st.error("❌ Los modelos predictivos no están disponibles. Verifica que el dataset tenga las columnas necesarias.")
    else:
        subtab_pred1, subtab_pred2, subtab_pred3, subtab_pred4 = st.tabs([
            "📈 Predictor de Alcance", "🖼️ Análisis de Imágenes", "⏰ Optimización Temporal", "📅 Planificación mensual"
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
                
                if st.button("🚀 Predecir Alcance", type="primary", key="btn_predecir_alcance_fixed"):
                    try:
                        # Codificar inputs
                        canal_enc = le_canal.transform([pred_canal])[0]
                        formato_enc = le_formato.transform([pred_formato])[0]
                        
                        # Preparar features
                        X_pred = np.array([[canal_enc, formato_enc, pred_inversion]])
                        X_pred_scaled = scaler.transform(X_pred)
                        
                        # Predicción
                        alcance_predicho = reg.predict(X_pred_scaled)[0]
                        
                        # Guardar resultado en session_state para mantenerlo visible
                        st.session_state['prediccion_alcance'] = {
                            'alcance': alcance_predicho,
                            'engagement': alcance_predicho * 0.035,
                            'costo_por_alcance': pred_inversion / alcance_predicho if alcance_predicho > 0 else 0,
                            'canal': pred_canal,
                            'formato': pred_formato,
                            'inversion': pred_inversion
                        }
                        
                        # Limpiar errores previos
                        if 'prediccion_error' in st.session_state:
                            del st.session_state['prediccion_error']
                        
                    except Exception as e:
                        st.session_state['prediccion_error'] = str(e)
                        if 'prediccion_alcance' in st.session_state:
                            del st.session_state['prediccion_alcance']
                
                # Mostrar resultados persistentes
                if 'prediccion_alcance' in st.session_state:
                    resultado = st.session_state['prediccion_alcance']
                    st.success(f"🎯 **Alcance Predicho: {resultado['alcance']:,.0f} personas**")
                    
                    col_metric1, col_metric2 = st.columns(2)
                    col_metric1.metric("❤️ Interacciones Estimadas", f"{resultado['engagement']:,.0f}")
                    col_metric2.metric("💰 Costo por Alcance", f"{resultado['costo_por_alcance']:.4f}€")
                    
                    # Mostrar configuración usada
                    st.info(f"📊 Configuración: {resultado['formato']} en {resultado['canal']} con {resultado['inversion']:.0f}€")
                
                if 'prediccion_error' in st.session_state:
                    st.error(f"Error en la predicción: {st.session_state['prediccion_error']}")
                        
            
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
                    
                    # Inicializar valores en session_state para mantener persistencia
                    if 'hora_pub' not in st.session_state:
                        st.session_state.hora_pub = 12
                    if 'dia_semana_pub' not in st.session_state:
                        st.session_state.dia_semana_pub = 0
                    if 'mes_pub' not in st.session_state:
                        st.session_state.mes_pub = 1
                    if 'inversion_temp' not in st.session_state:
                        st.session_state.inversion_temp = 100.0
                    
                    hora_pub = st.slider("⏰ Hora de publicación", 0, 23, st.session_state.hora_pub, key="slider_hora_temporal")
                    dia_semana_pub = st.selectbox("📅 Día de la semana", 
                                                [0, 1, 2, 3, 4, 5, 6],
                                                index=st.session_state.dia_semana_pub,
                                                format_func=lambda x: ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"][x],
                                                key="select_dia_temporal")
                    mes_pub = st.selectbox("📆 Mes", list(range(1, 13)),
                                        index=st.session_state.mes_pub - 1,
                                        format_func=lambda x: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][x-1],
                                        key="select_mes_temporal")
                    inversion_temp = st.slider("💰 Inversión (€)", 0.0, 500.0, st.session_state.inversion_temp, 10.0, key="slider_inversion_temporal")
                    
                    # Actualizar session_state
                    st.session_state.hora_pub = hora_pub
                    st.session_state.dia_semana_pub = dia_semana_pub
                    st.session_state.mes_pub = mes_pub
                    st.session_state.inversion_temp = inversion_temp
                    
                    if st.button("🎯 Optimizar Publicación", type="primary", key="btn_optimizar_temporal_UNIQUE_2024"):
                        try:
                            # Preparar features para predicción
                            X_temp = np.array([[hora_pub, dia_semana_pub, mes_pub, inversion_temp]])
                            
                            # Predecir formato óptimo
                            formato_pred = modelo_temporal.predict(X_temp)[0]
                            formato_recomendado = le_formato_temporal.inverse_transform([formato_pred])[0]
                            
                            # Guardar en session_state SIN RERUN
                            st.session_state['optimizacion_temporal'] = {
                                'formato': formato_recomendado,
                                'hora': hora_pub,
                                'dia': dia_semana_pub,
                                'mes': mes_pub,
                                'inversion': inversion_temp,
                                'dia_nombre': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][dia_semana_pub]
                            }
                            
                            # Análisis de engagement por hora
                            if 'Fecha' in df.columns and 'Interacciones' in df.columns and 'Alcance' in df.columns:
                                df_temp_analysis = df.copy()
                                df_temp_analysis['hora'] = df_temp_analysis['Fecha'].dt.hour
                                df_temp_analysis['dia_semana'] = df_temp_analysis['Fecha'].dt.dayofweek
                                df_temp_analysis['engagement_rate'] = (df_temp_analysis['Interacciones'] / df_temp_analysis['Alcance']).fillna(0)
                                
                                engagement_por_hora = df_temp_analysis.groupby('hora')['engagement_rate'].mean()
                                mejor_hora = engagement_por_hora.idxmax()
                                mejor_engagement = engagement_por_hora.max()
                                
                                st.session_state['optimizacion_temporal']['mejor_hora_historica'] = mejor_hora
                                st.session_state['optimizacion_temporal']['mejor_engagement'] = mejor_engagement
                            
                            # Limpiar errores previos
                            if 'optimizacion_error' in st.session_state:
                                del st.session_state['optimizacion_error']
                            
                            
                        except Exception as e:
                            st.session_state['optimizacion_error'] = str(e)
                            if 'optimizacion_temporal' in st.session_state:
                                del st.session_state['optimizacion_temporal']

                    
                    # SEPARAR la sección de resultados - ESTA SECCIÓN SIEMPRE ESTÁ VISIBLE
                    st.markdown("---")
                    st.markdown("### 🎯 Resultados de Optimización")
                    
                    # Mostrar resultados SI EXISTEN en session_state
                    if 'optimizacion_temporal' in st.session_state:
                        opt = st.session_state['optimizacion_temporal']
                        st.success(f"🎯 **Formato Recomendado: {opt['formato']}**")
                        
                        # Información adicional
                        col_res1, col_res2 = st.columns(2)
                        
                        with col_res1:
                            st.info(f"📅 **Día**: {opt['dia_nombre']}")
                            st.info(f"⏰ **Hora**: {opt['hora']}:00")
                        
                        with col_res2:
                            st.info(f"📆 **Mes**: {['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'][opt['mes']]}")
                            st.info(f"💰 **Inversión**: {opt['inversion']:.0f}€")
                        
                        # Comparación con datos históricos
                        if 'mejor_hora_historica' in opt:
                            st.markdown("#### 📊 Análisis Histórico")
                            if opt['hora'] == opt['mejor_hora_historica']:
                                st.success(f"🎉 ¡Elegiste la hora óptima! Históricamente, las {opt['mejor_hora_historica']}:00 tienen el mejor engagement ({opt['mejor_engagement']:.3f})")
                            else:
                                st.warning(f"💡 Considera publicar a las {opt['mejor_hora_historica']}:00 para mejor engagement ({opt['mejor_engagement']:.3f})")
                        
                        # Botón para nueva optimización
                        if st.button("🔄 Nueva Optimización", key="btn_nueva_optimizacion"):
                            if 'optimizacion_temporal' in st.session_state:
                                del st.session_state['optimizacion_temporal']
                    
                    elif 'optimizacion_error' in st.session_state:
                        st.error(f"❌ Error en la optimización: {st.session_state['optimizacion_error']}")
                        if st.button("🔄 Reintentar Optimización", key="btn_reintentar_optimizacion"):
                            if 'optimizacion_error' in st.session_state:
                                del st.session_state['optimizacion_error']

                    
                    else:
                        st.info("👆 Configura los parámetros y presiona 'Optimizar Publicación' para ver recomendaciones")
                
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
                            fig_hora.update_layout(
                                paper_bgcolor='rgba(255,255,255,0.9)', 
                                font_color='#4a148c',
                                xaxis_title="Hora del día",
                                yaxis_title="Engagement Rate",
                                height=300
                            )
                            st.plotly_chart(fig_hora, use_container_width=True)
                            
                            # Heatmap por día y hora
                            st.markdown("#### 🔥 Heatmap de Engagement")
                            heatmap_data = df_temp_viz.groupby(['dia_semana', 'hora'])['engagement_rate'].mean().reset_index()
                            
                            if len(heatmap_data) > 0:
                                heatmap_pivot = heatmap_data.pivot(index='dia_semana', columns='hora', values='engagement_rate')
                                
                                # Renombrar índices de días
                                dias_nombres = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
                                heatmap_pivot.index = [dias_nombres[i] for i in heatmap_pivot.index if i < len(dias_nombres)]
                                
                                fig_heatmap = go.Figure(data=go.Heatmap(
                                    z=heatmap_pivot.values,
                                    x=heatmap_pivot.columns,
                                    y=heatmap_pivot.index,
                                    colorscale='Purples',
                                    hoverongaps=False,
                                    colorbar=dict(title="Engagement Rate")
                                ))
                                fig_heatmap.update_layout(
                                    title="🔥 Engagement por Día y Hora",
                                    xaxis_title="Hora del día",
                                    yaxis_title="Día de la semana",
                                    paper_bgcolor='rgba(255,255,255,0.9)',
                                    font_color='#4a148c',
                                    height=400
                                )
                                st.plotly_chart(fig_heatmap, use_container_width=True)
                            else:
                                st.info("No hay suficientes datos para crear el heatmap")
                        
                        else:
                            st.warning("⚠️ Se necesitan columnas de 'Interacciones' y 'Alcance' para el análisis temporal")
                    
                    else:
                        st.warning("⚠️ Se necesita la columna 'Fecha' para el análisis temporal")
                    
                    # Mostrar estadísticas adicionales si hay optimización
                    if 'optimizacion_temporal' in st.session_state:
                        st.markdown("---")
                        st.markdown("### 📈 Predicción de Rendimiento")
                        
                        opt = st.session_state['optimizacion_temporal']
                        
                        # Simular predicción de alcance usando el modelo principal si está disponible
                        if models_ok and opt['formato'] in formatos_disponibles:
                            try:
                                # Usar un canal por defecto para la predicción
                                canal_default = canales_disponibles[0] if canales_disponibles else 'Instagram'
                                
                                canal_enc = le_canal.transform([canal_default])[0]
                                formato_enc = le_formato.transform([opt['formato']])[0]
                                X_pred = np.array([[canal_enc, formato_enc, opt['inversion']]])
                                X_pred_scaled = scaler.transform(X_pred)
                                alcance_predicho = int(reg.predict(X_pred_scaled)[0])
                                
                                col_pred1, col_pred2 = st.columns(2)
                                
                                with col_pred1:
                                    st.metric("👁️ Alcance Estimado", f"{alcance_predicho:,}")
                                
                                with col_pred2:
                                    engagement_estimado = int(alcance_predicho * 0.035)
                                    st.metric("❤️ Engagement Estimado", f"{engagement_estimado:,}")
                                
                            except Exception as e:
                                st.info("💡 Para predicciones más precisas, asegúrate de que todos los modelos estén disponibles")
            
            else:
                st.error("⚠️ El modelo de optimización temporal no está disponible")
                st.info("💡 Verifica que el dataset tenga suficientes datos históricos para entrenar el modelo")

        with subtab_pred4:
            st.subheader("📅 Planificación Mensual Inteligente")
            st.markdown("**Genera un calendario optimizado de publicaciones basado en tus datos históricos y modelos predictivos.**")
            
            if modelo_temporal is not None and le_formato_temporal is not None and models_ok:
                col_plan1, col_plan2 = st.columns([1, 2])
                
                with col_plan1:
                    st.markdown("### ⚙️ Configuración del Plan")
                    
                    # Configuración básica
                    canal_planificacion = st.selectbox("📱 Canal Principal", canales_disponibles, key="plan_canal")
                    publicaciones_semana = st.slider("📊 Publicaciones por semana", 1, 14, 3)
                    
                    # Selección de mes y año
                    col_mes, col_año = st.columns(2)
                    with col_mes:
                        mes_planificacion = st.selectbox("📆 Mes", list(range(1, 13)),
                                                    format_func=lambda x: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][x-1],
                                                    index=datetime.now().month-1)
                    with col_año:
                        año_planificacion = st.number_input("📅 Año", min_value=2024, max_value=2030, value=datetime.now().year)
                    
                    # Configuración avanzada
                    st.markdown("#### 🎯 Configuración Avanzada")
                    inversion_promedio = st.slider("💰 Inversión promedio por post (€)", 0.0, 500.0, 100.0, 10.0)
                    
                    incluir_fines_semana = st.checkbox("📅 Incluir fines de semana", value=True)
                    priorizar_engagement = st.checkbox("🎯 Priorizar alto engagement", value=True)
                    
                    # Preferencias de horarios
                    st.markdown("#### ⏰ Franjas Horarias Preferidas")
                    hora_inicio = st.time_input("🌅 Hora más temprana", value=datetime.strptime("08:00", "%H:%M").time())
                    hora_fin = st.time_input("🌙 Hora más tardía", value=datetime.strptime("20:00", "%H:%M").time())
                    
                    if st.button("🚀 Generar Planificación", type="primary"):
                        with st.spinner("🔮 Generando planificación inteligente..."):
                            # Generar planificación
                            planificacion = generar_planificacion_mensual(
                                canal_planificacion, publicaciones_semana, mes_planificacion, 
                                año_planificacion, inversion_promedio, incluir_fines_semana,
                                priorizar_engagement, hora_inicio, hora_fin, 
                                df, modelo_temporal, le_formato_temporal, reg, scaler, le_canal, le_formato
                            )
                            
                            if planificacion:
                                st.session_state['planificacion_generada'] = planificacion
                                st.success(f"✅ Planificación generada: {len(planificacion)} publicaciones programadas")
                            else:
                                st.error("❌ Error generando la planificación")
                
                with col_plan2:
                    st.markdown("### 📅 Calendario de Publicaciones")
                    
                    # Mostrar planificación si existe
                    if 'planificacion_generada' in st.session_state:
                        planificacion = st.session_state['planificacion_generada']
                        
                        # Crear calendario visual
                        mostrar_calendario_planificacion(planificacion, mes_planificacion, año_planificacion)
                        
                        # Mostrar tabla detallada
                        st.markdown("### 📋 Detalle de Publicaciones Programadas")
                        mostrar_tabla_planificacion(planificacion)
                        
                        # Estadísticas de la planificación
                        st.markdown("### 📊 Estadísticas de la Planificación")
                        mostrar_estadisticas_planificacion(planificacion)
                        
                        # Opción de descarga
                        st.markdown("### 💾 Exportar Planificación")
                        if st.button("📥 Descargar CSV"):
                            csv_planificacion = convertir_planificacion_csv(planificacion)
                            st.download_button(
                                label="📄 Descargar Planificación.csv",
                                data=csv_planificacion,
                                file_name=f"planificacion_{canal_planificacion}_{mes_planificacion}_{año_planificacion}.csv",
                                mime="text/csv"
                            )
                    else:
                        st.info("👆 Configura los parámetros y genera tu planificación para ver el calendario")
                        
                        # Mostrar ejemplo de insights históricos
                        if 'Fecha' in df.columns:
                            st.markdown("#### 📈 Insights Históricos")
                            mostrar_insights_historicos(df, canal_planificacion)
            
            else:
                st.error("❌ Los modelos predictivos no están disponibles para la planificación")

# AÑADIR estas funciones auxiliares ANTES del # --- APP STREAMLIT ---

@st.cache_data
def generar_planificacion_mensual(canal, posts_semana, mes, año, inversion, incluir_fines, 
                                priorizar_engagement, hora_inicio, hora_fin, df, modelo_temporal, 
                                le_formato_temporal, reg, scaler, le_canal, le_formato):
    """
    Genera una planificación mensual inteligente usando los modelos predictivos
    """
    try:
        import calendar
        from datetime import datetime, timedelta
        
        # Obtener días del mes
        num_dias = calendar.monthrange(año, mes)[1]
        primer_dia = datetime(año, mes, 1)
        
        # Calcular total de publicaciones para el mes
        semanas_en_mes = (num_dias + primer_dia.weekday()) / 7
        total_publicaciones = int(posts_semana * semanas_en_mes)
        
        # Generar datos históricos para el canal seleccionado
        df_canal = df[df['Canal'] == canal].copy() if 'Canal' in df.columns else df.copy()
        
        # Obtener mejores horarios históricos
        if len(df_canal) > 0 and 'Fecha' in df_canal.columns:
            df_canal['hora'] = df_canal['Fecha'].dt.hour
            df_canal['dia_semana'] = df_canal['Fecha'].dt.dayofweek
            
            if 'Interacciones' in df_canal.columns and 'Alcance' in df_canal.columns:
                df_canal['engagement_rate'] = (df_canal['Interacciones'] / df_canal['Alcance']).fillna(0)
                mejores_horas = df_canal.groupby('hora')['engagement_rate'].mean().sort_values(ascending=False)
                mejores_dias = df_canal.groupby('dia_semana')['engagement_rate'].mean().sort_values(ascending=False)
            else:
                # Usar distribución por defecto si no hay datos de engagement
                mejores_horas = pd.Series({9: 0.05, 12: 0.06, 15: 0.055, 18: 0.07, 20: 0.045})
                mejores_dias = pd.Series({0: 0.055, 1: 0.06, 2: 0.065, 3: 0.07, 4: 0.06, 5: 0.045, 6: 0.04})
        else:
            # Valores por defecto si no hay datos históricos
            mejores_horas = pd.Series({9: 0.05, 12: 0.06, 15: 0.055, 18: 0.07, 20: 0.045})
            mejores_dias = pd.Series({0: 0.055, 1: 0.06, 2: 0.065, 3: 0.07, 4: 0.06, 5: 0.045, 6: 0.04})
        
        # Filtrar horarios según preferencias del usuario
        hora_inicio_int = hora_inicio.hour
        hora_fin_int = hora_fin.hour
        mejores_horas = mejores_horas[(mejores_horas.index >= hora_inicio_int) & (mejores_horas.index <= hora_fin_int)]
        
        # Filtrar días si no incluir fines de semana
        if not incluir_fines:
            mejores_dias = mejores_dias[mejores_dias.index < 5]  # Lunes=0 a Viernes=4
        
        # Generar planificación
        planificacion = []
        dias_utilizados = set()
        
        # Obtener temáticas disponibles del análisis de imágenes
        tematicas_disponibles = [
            'moda_lifestyle', 'arte_diseño', 'naturaleza_bienestar', 
            'tecnologia', 'comida_gastronomia', 'lifestyle_inspiracional', 'general'
        ]
        
        for i in range(total_publicaciones):
            # Seleccionar día óptimo
            dias_disponibles = []
            for dia in range(1, num_dias + 1):
                fecha_candidata = datetime(año, mes, dia)
                dia_semana = fecha_candidata.weekday()
                
                # Verificar si el día es válido según configuración
                if not incluir_fines and dia_semana >= 5:
                    continue
                
                # Evitar saturar días (máximo 1 post por día para empezar)
                if fecha_candidata.date() in dias_utilizados:
                    continue
                
                # Calcular score del día
                score_dia = mejores_dias.get(dia_semana, 0.03)
                dias_disponibles.append((dia, dia_semana, score_dia, fecha_candidata))
            
            if not dias_disponibles:
                break
            
            # Seleccionar mejor día disponible
            if priorizar_engagement:
                dias_disponibles.sort(key=lambda x: x[2], reverse=True)
            else:
                # Distribuir más uniformemente
                dias_disponibles.sort(key=lambda x: x[0])
            
            dia_seleccionado, dia_semana_sel, score_dia, fecha_sel = dias_disponibles[0]
            
            # Seleccionar mejor hora
            if priorizar_engagement:
                hora_seleccionada = mejores_horas.index[0] if len(mejores_horas) > 0 else 12
            else:
                # Variar las horas
                horas_ordenadas = list(mejores_horas.index)
                hora_seleccionada = horas_ordenadas[i % len(horas_ordenadas)] if horas_ordenadas else 12
            
            # Predecir formato óptimo usando el modelo temporal
            try:
                X_temp = np.array([[hora_seleccionada, dia_semana_sel, mes, inversion]])
                formato_pred = _modelo_temporal.predict(X_temp)[0]
                formato_recomendado = _le_formato_temporal.inverse_transform([formato_pred])[0]
            except Exception as e:
                # Fallback mejorado que garantiza variedad
                formatos_disponibles = ['Imagen', 'Reel', 'Carrusel']
    
                # Lógica inteligente de fallback
                if i % 4 == 0:  # Cada 4 posts, un Reel
                    formato_recomendado = 'Reel'
                elif i % 3 == 0:  # Cada 3 posts, un Carrusel  
                    formato_recomendado = 'Carrusel'
                else:  # El resto, Imágenes
                    formato_recomendado = 'Imagen'
    
                # Remover el st.warning que causa problemas
                # st.warning(f"Usando formato de fallback: {formato_recomendado}")
            
            # Predecir alcance esperado
            try:
                canal_enc = _le_canal.transform([canal])[0]
                formato_enc = _le_formato.transform([formato_recomendado])[0]
                X_pred = np.array([[canal_enc, formato_enc, inversion]])
                X_pred_scaled = _scaler.transform(X_pred)
                alcance_predicho = int(_reg.predict(X_pred_scaled)[0])
            except:
                alcance_predicho = 5000
            
            # Seleccionar temática (rotar entre disponibles)
            tematica_seleccionada = tematicas_disponibles[i % len(tematicas_disponibles)]
            
            # Mapear temática a nombre amigable
            mapeo_tematicas = {
                'moda_lifestyle': 'Moda & Lifestyle',
                'arte_diseño': 'Arte & Diseño',
                'naturaleza_bienestar': 'Naturaleza & Bienestar',
                'tecnologia': 'Tecnología',
                'comida_gastronomia': 'Comida & Gastronomía',
                'lifestyle_inspiracional': 'Lifestyle Inspiracional',
                'general': 'General'
            }
            
            # Crear entrada de planificación
            entrada = {
                'fecha': fecha_sel,
                'dia': dia_seleccionado,
                'dia_semana': dia_semana_sel,
                'dia_nombre': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][dia_semana_sel],
                'hora': hora_seleccionada,
                'canal': canal,
                'formato': formato_recomendado,
                'tematica': mapeo_tematicas.get(tematica_seleccionada, 'General'),
                'tematica_code': tematica_seleccionada,
                'inversion': inversion,
                'alcance_predicho': alcance_predicho,
                'engagement_esperado': int(alcance_predicho * 0.035),  # 3.5% promedio
                'score_temporal': score_dia
            }
            
            planificacion.append(entrada)
            dias_utilizados.add(fecha_sel.date())
        
        return planificacion
        
    except Exception as e:
        st.error(f"Error generando planificación: {str(e)}")
        return []

def mostrar_calendario_planificacion(planificacion, mes, año):
    """
    Muestra un calendario visual con las publicaciones planificadas incluyendo temática
    """
    import calendar
    
    # Crear calendario del mes
    cal = calendar.monthcalendar(año, mes)
    mes_nombre = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][mes]
    
    st.markdown(f"#### 📅 {mes_nombre} {año}")
    
    # Crear diccionario de publicaciones por día
    publicaciones_por_dia = {}
    for pub in planificacion:
        dia = pub['dia']
        if dia not in publicaciones_por_dia:
            publicaciones_por_dia[dia] = []
        publicaciones_por_dia[dia].append(pub)
    
    # Mapeo de emojis por temática
    emoji_tematicas = {
        'Moda & Lifestyle': '👗',
        'Arte & Diseño': '🎨', 
        'Naturaleza & Bienestar': '🌿',
        'Tecnología': '💻',
        'Comida & Gastronomía': '🍽️',
        'Lifestyle Inspiracional': '✨',
        'General': '📝'
    }
    
    # Mostrar calendario
    dias_semana = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    
    # Encabezados de días
    cols_header = st.columns(7)
    for i, dia in enumerate(dias_semana):
        cols_header[i].markdown(f"**{dia}**")
    
    # Mostrar semanas
    for semana in cal:
        cols = st.columns(7)
        for i, dia in enumerate(semana):
            if dia == 0:
                cols[i].markdown("")
            else:
                with cols[i]:
                    if dia in publicaciones_por_dia:
                        # Día con publicación
                        pub = publicaciones_por_dia[dia][0]  # Primera publicación del día
                        
                        # Color por formato
                        color = "#8e24aa" if pub['formato'] == 'Reel' else "#e91e63" if pub['formato'] == 'Imagen' else "#f06292"
                        
                        # Emoji por temática
                        emoji_tematica = emoji_tematicas.get(pub['tematica'], '📝')
                        
                        # Abreviatura del formato
                        formato_abrev = pub['formato'][:4] if len(pub['formato']) <= 4 else pub['formato'][:3] + "."
                        
                        st.markdown(f"""
                        <div style='background-color: {color}; color: white; padding: 0.3rem; border-radius: 8px; text-align: center; margin-bottom: 0.2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                            <strong style='font-size: 0.9rem;'>{dia}</strong><br>
                            <small style='font-size: 0.7rem;'>{pub['hora']}:00</small><br>
                            <small style='font-size: 0.7rem;'>{formato_abrev}</small><br>
                            <span style='font-size: 0.8rem;'>{emoji_tematica}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        
    
    # Leyenda del calendario
    st.markdown("---")
    st.markdown("#### 🎨 Leyenda del Calendario")
    
    col_leyenda1, col_leyenda2 = st.columns(2)
    
    with col_leyenda1:
        st.markdown("**Colores por Formato:**")
        st.markdown("🟣 **Morado** = Reel")
        st.markdown("🩷 **Rosa** = Imagen") 
        st.markdown("🌸 **Rosa claro** = Carrusel")
    
    with col_leyenda2:
        st.markdown("**Emojis por Temática:**")
        for tematica, emoji in emoji_tematicas.items():
            st.markdown(f"{emoji} **{tematica}**")

def mostrar_tabla_planificacion(planificacion):
    """
    Muestra una tabla detallada de la planificación
    """
    if not planificacion:
        st.warning("No hay planificación generada")
        return
    
    # Convertir a DataFrame para mejor visualización
    df_plan = pd.DataFrame(planificacion)
    
    # Formatear para mostrar
    df_display = df_plan.copy()
    df_display['Fecha'] = df_display['fecha'].dt.strftime('%d/%m/%Y')
    df_display['Día'] = df_display['dia_nombre']
    df_display['Hora'] = df_display['hora'].apply(lambda x: f"{x:02d}:00")
    df_display['Canal'] = df_display['canal']
    df_display['Formato'] = df_display['formato']
    df_display['Temática'] = df_display['tematica']
    df_display['Inversión'] = df_display['inversion'].apply(lambda x: f"{x:.0f}€")
    df_display['Alcance Predicho'] = df_display['alcance_predicho'].apply(lambda x: f"{x:,}")
    df_display['Engagement Esperado'] = df_display['engagement_esperado'].apply(lambda x: f"{x:,}")
    
    # Seleccionar columnas para mostrar
    columnas_mostrar = ['Fecha', 'Día', 'Hora', 'Canal', 'Formato', 'Temática', 'Inversión', 'Alcance Predicho', 'Engagement Esperado']
    df_final = df_display[columnas_mostrar].reset_index(drop=True)
    df_final.index += 1
    
    st.dataframe(df_final, use_container_width=True)

def mostrar_estadisticas_planificacion(planificacion):
    """
    Muestra estadísticas resumidas de la planificación
    """
    if not planificacion:
        return
    
    df_plan = pd.DataFrame(planificacion)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_posts = len(planificacion)
        st.metric("📊 Total Posts", total_posts)
    
    with col2:
        inversion_total = df_plan['inversion'].sum()
        st.metric("💰 Inversión Total", f"{inversion_total:.0f}€")
    
    with col3:
        alcance_total = df_plan['alcance_predicho'].sum()
        st.metric("👁️ Alcance Esperado", f"{alcance_total:,}")
    
    with col4:
        engagement_total = df_plan['engagement_esperado'].sum()
        st.metric("❤️ Engagement Esperado", f"{engagement_total:,}")
    
    # Distribución por formato
    st.markdown("#### 📊 Distribución por Formato")
    formato_dist = df_plan['formato'].value_counts()
    fig_formato = px.pie(values=formato_dist.values, names=formato_dist.index,
                        title="Distribución de Formatos Planificados",
                        color_discrete_sequence=px.colors.sequential.Purples)
    fig_formato.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c')
    st.plotly_chart(fig_formato, use_container_width=True)
    
    # Distribución por día de la semana
    col_dist1, col_dist2 = st.columns(2)
    
    with col_dist1:
        st.markdown("#### 📅 Posts por Día de la Semana")
        dia_dist = df_plan['dia_nombre'].value_counts()
        fig_dias = px.bar(x=dia_dist.index, y=dia_dist.values,
                        title="Posts por Día de la Semana",
                        color=dia_dist.values,
                        color_continuous_scale='Purples')
        fig_dias.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c', showlegend=False)
        st.plotly_chart(fig_dias, use_container_width=True)
    
    with col_dist2:
        st.markdown("#### ⏰ Posts por Hora")
        hora_dist = df_plan['hora'].value_counts().sort_index()
        fig_horas = px.bar(x=hora_dist.index, y=hora_dist.values,
                        title="Posts por Hora del Día",
                        color=hora_dist.values,
                        color_continuous_scale='Pinkyl')
        fig_horas.update_layout(paper_bgcolor='rgba(255,255,255,0.9)', font_color='#4a148c', showlegend=False)
        st.plotly_chart(fig_horas, use_container_width=True)

def convertir_planificacion_csv(planificacion):
    """
    Convierte la planificación a formato CSV para descarga
    """
    df_plan = pd.DataFrame(planificacion)
    
    # Preparar datos para CSV
    df_csv = df_plan.copy()
    df_csv['Fecha'] = df_csv['fecha'].dt.strftime('%d/%m/%Y')
    df_csv['Hora'] = df_csv['hora'].apply(lambda x: f"{x:02d}:00")
    
    # Seleccionar y renombrar columnas
    columnas_csv = {
        'Fecha': 'fecha',
        'Día': 'dia_nombre', 
        'Hora': 'Hora',
        'Canal': 'canal',
        'Formato': 'formato',
        'Temática': 'tematica',
        'Inversión_€': 'inversion',
        'Alcance_Predicho': 'alcance_predicho',
        'Engagement_Esperado': 'engagement_esperado'
    }
    
    df_export = pd.DataFrame()
    for col_nueva, col_original in columnas_csv.items():
        if col_original in df_csv.columns:
            df_export[col_nueva] = df_csv[col_original]
    
    return df_export.to_csv(index=False)

def mostrar_insights_historicos(df, canal):
    """
    Muestra insights históricos para ayudar en la planificación
    """
    if len(df) == 0:
        return
    
    # Filtrar por canal si está disponible
    df_canal = df[df['Canal'] == canal].copy() if 'Canal' in df.columns and canal in df['Canal'].values else df.copy()
    
    if len(df_canal) == 0:
        return
    
    col_insight1, col_insight2 = st.columns(2)
    
    with col_insight1:
        if 'Fecha' in df_canal.columns:
            df_canal['hora'] = df_canal['Fecha'].dt.hour
            df_canal['dia_semana'] = df_canal['Fecha'].dt.dayofweek
            
            # Mejor hora histórica
            if 'Interacciones' in df_canal.columns and 'Alcance' in df_canal.columns:
                df_canal['engagement_rate'] = (df_canal['Interacciones'] / df_canal['Alcance']).fillna(0)
                mejor_hora = df_canal.groupby('hora')['engagement_rate'].mean().idxmax()
                mejor_engagement = df_canal.groupby('hora')['engagement_rate'].mean().max()
                
                st.info(f"🕐 **Mejor hora histórica**: {mejor_hora}:00 (Engagement: {mejor_engagement:.3f})")
            
            # Mejor día histórico
            if 'engagement_rate' in df_canal.columns:
                dias_nombres = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
                mejor_dia_num = df_canal.groupby('dia_semana')['engagement_rate'].mean().idxmax()
                mejor_dia_nombre = dias_nombres[mejor_dia_num]
                
                st.info(f"📅 **Mejor día histórico**: {mejor_dia_nombre}")
    
    with col_insight2:
        if 'Formato' in df_canal.columns:
            formato_mas_usado = df_canal['Formato'].mode().iloc[0] if not df_canal['Formato'].mode().empty else "N/A"
            st.info(f"🎨 **Formato más utilizado**: {formato_mas_usado}")
        
        if 'Alcance' in df_canal.columns:
            alcance_promedio = df_canal['Alcance'].mean()
            st.info(f"👁️ **Alcance promedio histórico**: {alcance_promedio:,.0f}")
            
# --- TAB 3: NEXT STEPS ---
with tab3:
    st.header("🚀 Next Steps")
    st.markdown("**Descubre las próximas funcionalidades y mejoras que llegarán a Oráculo.**")
    
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
        rating = st.select_slider("¿Qué tal tu experiencia con Oráculo?", 
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
        - **Email**: info@oraculo.com
        - **Soporte**: support@oraculo.com
        - **Ventas**: sales@oraculo.com
        """)
    
    with col_contact2:
        st.markdown("""
        #### 🌐 Síguenos
        - **LinkedIn**: /company/oraculo
        - **Instagram**: @oraculo
        - **Twitter**: @OraculoApp
        """)
    
    with col_contact3:
        st.markdown("""
        #### 📚 Recursos
        - **Documentación**: docs.oraculo.com
        - **Blog**: blog.oraculo.com
        - **Webinars**: events.oraculo.com
        """)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: rgba(255,255,255,0.8); border-radius: 15px; margin-top: 2rem;'>
    <h3 style='color: #4a148c; margin-bottom: 1rem;'>🔮 Oráculo</h3>
    <p style='color: #6a1b9a; font-size: 1.1rem; margin-bottom: 1rem;'>
        <strong>Empodera tu estrategia digital con datos inteligentes</strong>
    </p>
    <p style='color: #8e24aa; font-size: 0.9rem;'>
        Desarrollado con 🔮 para marcas que buscan crecer en redes sociales
    </p>
    <p style='color: #8e24aa; font-size: 0.8rem; margin-top: 1rem;'>
        © 2024 Oráculo. Todos los derechos reservados.
    </p>
</div>
""", unsafe_allow_html=True)