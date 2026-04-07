# � Oráculo - Predice tu Estrategia en Redes Sociales

<div align="center">
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
    <img src="https://img.shields.io/badge/Streamlit-1.28+-red.svg" alt="Streamlit">
    <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg" alt="ML">
    <img src="https://img.shields.io/badge/Computer%20Vision-PIL-green.svg" alt="CV">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</div>

---

## 🌟 ¿Qué es Oráculo?

**Oráculo** es una plataforma inteligente diseñada específicamente para **mujeres emprendedoras** que buscan maximizar el impacto de sus redes sociales. Utilizando **Machine Learning** y **Computer Vision**, transformamos datos en insights accionables para impulsar tu marca digital.

### 🎯 **¿Para quién es?**
- 👩‍💼 Emprendedoras digitales
- 🏢 Pequeñas y medianas empresas
- 📱 Community managers
- 🎨 Creadores de contenido
- 💼 Consultoras de marketing digital

Visíta la app: https://oraculo.streamlit.app/

---

## ✨ Características Principales

### 📊 **Análisis Inteligente de Datos**
- **Informe Interanual Completo**: Análisis detallado de visibilidad, interacción, reproducciones, conversión y ROI
- **Segmentación por Canal**: Instagram, Facebook, TikTok
- **Análisis Temporal**: Identifica patrones por día, hora y estacionalidad

### 🔮 **Modelos Predictivos Avanzados**
- **Predictor de Alcance**: Estima el rendimiento antes de publicar
- **Análisis de Imágenes con IA**: Computer Vision para optimizar contenido visual
- **Optimización Temporal**: Encuentra el momento perfecto para publicar

### 📅 **Planificación Estratégica**
- **Calendario Editorial Inteligente**: Planificación mensual automatizada
- **Recomendaciones de Formato**: Qué tipo de contenido funciona mejor
- **Sugerencias de Temática**: Basadas en tendencias y tu audiencia

---

## 🚀 Tecnologías Utilizadas

### 🧠 **Machine Learning**
```python
• RandomForest para predicción de alcance
• Clasificación de temáticas automática
• Análisis predictivo temporal
• Clustering de audiencias
```

### 👁️ **Computer Vision**
```python
• Análisis de colores dominantes
• Detección de características visuales
• Predicción de engagement visual
• Clasificación automática de contenido
```

### 🛠️ **Stack Tecnológico**
- **Frontend**: Streamlit con UI personalizada
- **Backend**: Python 3.8+
- **ML/AI**: Scikit-learn, PIL, OpenCV
- **Data**: Pandas, NumPy
- **Visualización**: Plotly, Matplotlib
- **Cloud**: Azure (para conexión con APIs)

---

## 📱 Funcionalidades Detalladas

### 📈 **1. Informe Interanual**

#### 👁️ **Análisis de Visibilidad**
- Métricas de alcance por canal y formato
- Evolución temporal del crecimiento
- Identificación de picos y valles de audiencia

#### 🔮 **Análisis de Interacción**
- Rate de engagement detallado
- Análisis de comentarios y shares
- Identificación de contenido viral

#### ▶️ **Métricas de Reproducciones**
- Análisis específico para video content
- Retención de audiencia
- Optimización de duración

#### 🛒 **Análisis de Conversión**
- Tracking de ventas desde redes sociales
- Embudo de conversión completo
- Identificación de mejores performing posts

#### 💰 **Retorno de Inversión (ROI)**
- Cálculo automático de ROI por campaña
- Análisis costo-beneficio
- Recomendaciones de presupuesto

### 🔮 **2. Modelo Predictivo**

#### 📊 **Predictor de Alcance**
```
Inputs: Canal, Formato, Inversión, Hora, Día
Output: Alcance estimado + Intervalo de confianza
```

#### 🖼️ **Análisis de Imágenes IA**
- **Análisis de colores**: Identifica paletas que generan más engagement
- **Detección de características visuales**: Brillo, contraste, saturación
- **Predicción de rendimiento**: Score de engagement visual
- **Recomendaciones automáticas**: Mejoras sugeridas para optimizar

#### ⏰ **Optimización Temporal**
- **Mejor hora para publicar**: Por canal y tipo de audiencia
- **Días de mayor engagement**: Análisis semanal y mensual
- **Planificación estacional**: Adaptación a épocas del año

### 📅 **3. Planificación Mensual**

#### 🗓️ **Calendario Editorial Inteligente**
- Generación automática de calendario mensual
- Sugerencias de contenido por día
- Distribución equilibrada de formatos

#### 🎯 **Recomendaciones Personalizadas**
- Temáticas trending para tu nicho
- Formatos que mejor funcionan con tu audiencia
- Horarios optimizados por zona geográfica

---

## 🎨 Interfaz y Experiencia de Usuario

### � **Diseño Centrado en la Usuaria**
- **Colores**: Paleta rosa-morado que refleja empoderamiento femenino
- **UX Intuitiva**: Navegación simple y clara
- **Responsive**: Adaptada a todos los dispositivos
- **Accesibilidad**: Diseño inclusivo y accesible

### 📊 **Visualizaciones Interactivas**
- Gráficos dinámicos con Plotly
- Dashboards personalizables
- Exportación de reportes en PDF
- Métricas en tiempo real

---

## 🔧 Instalación y Configuración

### 📋 **Requisitos Previos**
```bash
Python 3.8+
pip 20.0+
```

### ⚡ **Instalación Rápida**
```bash
# Clonar el repositorio
git clone https://github.com/Natarcos/Diva_digital.git
cd Diva_digital

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run App/diva_digital.py
```

### 🗂️ **Estructura del Proyecto**
```
Diva_digital/
├── 📱 App/                          # Aplicación principal
│   ├── diva_digital.py              # Archivo principal de la app (actualizado)
│   ├── logo_diva_digital.png
│   └── ...
├── 📊 Data/                         # Datasets y bases de datos
│   ├── data_demo_ok.csv
│   ├── diva_digital.db
│   └── ...
├── 🔍 EDA/                          # Análisis exploratorio
│   └── eda.ipynb
├── 🤖 Modelos de predicción/        # Modelos entrenados
│   ├── model.pkl
│   ├── scaler.pkl
│   └── features.pkl
├── 🖼️ Computer Vision_Imagenes/     # Análisis de imágenes
│   ├── clasificacion.ipynb
│   └── CV_Images.ipynb
├── 🎲 Creacion_data_sintetica/      # Generación de datos
│   └── ...
└── 📝 README.md
```

---

## 📸 Screenshots y Demo

### 🏠 **Dashboard Principal**
*Vista general con métricas clave y navegación intuitiva*

### 📊 **Informe Interanual**
*Análisis completo con visualizaciones interactivas*

### 🔮 **Predictor de Alcance**
*Modelo predictivo con interfaz amigable*

### 🖼️ **Análisis de Imágenes**
*Computer Vision aplicado a optimización de contenido*

---

## 🛣️ Roadmap y Futuras Funcionalidades

### 🎯 **Q1 2024 - IA Avanzada**
- 🤖 Generador automático de captions
- 📝 Sugerencias de hashtags inteligentes
- 🎨 Editor de imágenes con IA

### 📱 **Q2 2024 - App Móvil**
- 📲 Aplicación nativa iOS/Android
- 📸 Carga directa desde móvil
- 🔔 Notificaciones push inteligentes

### 🔗 **Q3 2024 - Integraciones API**
- 📘 Conexión directa con Facebook Business
- 📷 Integración con Instagram Creator Studio
- 🎵 Sincronización con TikTok for Business
- 💼 Conexión con LinkedIn Business

### 📊 **Q4 2024 - Analytics Pro**
- 🏆 Análisis de competencia
- 👥 Segmentación avanzada de audiencia
- 🎯 Attribution modeling completo
- 📈 Forecasting a largo plazo

---

## 🤝 Contribuir al Proyecto

### 🌟 **¿Cómo Contribuir?**
1. 🍴 Fork el repositorio
2. 🌿 Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push a la rama (`git push origin feature/AmazingFeature`)
5. 🔄 Abre un Pull Request

### 🐛 **Reportar Bugs**
- Usa los GitHub Issues
- Describe el problema detalladamente
- Incluye screenshots si es necesario

### 💡 **Sugerir Funcionalidades**
- Abre un Issue con la etiqueta "enhancement"
- Explica el caso de uso
- Describe el comportamiento esperado

---

## 📞 Contacto y Soporte

### 👩‍💻 **Equipo de Desarrollo**
- **Lead Developer**: [@Natarcos](https://github.com/Natarcos)
- **Email**: contacto@oraculo.com
- **LinkedIn**: [Diva Digital](https://linkedin.com/company/diva-digital)

### 🆘 **Soporte**
- 📧 **Email**: soporte@oraculo.com
- 💬 **Discord**: [Comunidad Oráculo](https://discord.gg/oraculo)
- 📱 **WhatsApp Business**: +34 XXX XXX XXX

### 🌐 **Síguenos**
- 📷 [Instagram @oraculo](https://instagram.com/oraculo)
- 📘 [Facebook Oráculo](https://facebook.com/oraculo)
- 🎵 [TikTok @oraculo](https://tiktok.com/@oraculo)

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

### 💜 **Comunidad**
Gracias a todas las emprendedoras que han probado la beta y han aportado feedback valioso.

### 🛠️ **Tecnologías Open Source**
- [Streamlit](https://streamlit.io/) - Framework de aplicaciones
- [Scikit-learn](https://scikit-learn.org/) - Machine Learning
- [Plotly](https://plotly.com/) - Visualizaciones interactivas
- [PIL](https://pillow.readthedocs.io/) - Procesamiento de imágenes

---

<div align="center">
    <h3>� Hecho con 🔮 para emprendedoras que sueñan en grande</h3>
    <p><strong>Oráculo - Predice tu estrategia digital</strong></p>
    
    ⭐ **¡Si te gusta el proyecto, dale una estrella!** ⭐
</div>
