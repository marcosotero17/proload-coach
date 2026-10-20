# config.py
import os
from datetime import datetime

# Configuración de la aplicación
APP_NAME = "ProLoad Coach"
APP_VERSION = "1.0.0"
SECRET_KEY = "proload_coach_secure_2024"

# Rutas
DATA_DIR = "data"
TEAMS_DATA_FILE = os.path.join(DATA_DIR, "teams_data.json")

# Asegurar que el directorio de datos existe
os.makedirs(DATA_DIR, exist_ok=True)

# Parámetros de métricas
ACWR_OPTIMAL = (0.8, 1.3)  # Verde
ACWR_WARNING = (1.3, 1.5)  # Naranja
ACWR_DANGER = (1.5, float('inf'))  # Rojo

# Umbrales de variación semanal
VARIATION_WARNING = 10  # %
VARIATION_DANGER = 20   # %

# Configuración de streamlit
STREAMLIT_CONFIG = {
    "page_icon": "🏋️",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Glosario de métricas
GLOSSARY = {
    "RPE (Rate of Perceived Exertion)": {
        "definicion": "Escala de 0-10 que mide la intensidad percibida del jugador durante la sesión de entrenamiento.",
        "rango": "0-10",
        "interpretacion": "0-3: Muy suave | 4-6: Moderado | 7-9: Intenso | 10: Máximo"
    },
    "Carga de Sesión": {
        "definicion": "Producto del RPE y la duración en minutos. Representa la demanda fisiológica total de una sesión.",
        "formula": "RPE × Minutos",
        "ejemplo": "RPE 7 × 60 min = Carga 420"
    },
    "Carga Aguda (Acute Workload)": {
        "definicion": "Media móvil de los últimos 7 días. Refleja la carga de entrenamiento reciente.",
        "periodo": "7 días",
        "interpretacion": "Cambios rápidos en el estado del jugador"
    },
    "Carga Crónica (Chronic Workload)": {
        "definicion": "Media móvil de los últimos 28 días. Refleja la capacidad de entrenamiento histórica del jugador.",
        "periodo": "28 días",
        "interpretacion": "Forma física y adaptación general"
    },
    "ACWR (Acute:Chronic Workload Ratio)": {
        "definicion": "Ratio entre carga aguda y carga crónica. Indica si el jugador está siendo sobrecargado o infracargado.",
        "formula": "Carga Aguda / Carga Crónica",
        "zonas": {
            "Verde (0.8-1.3)": "Zona óptima de entrenamiento",
            "Naranja (1.3-1.5)": "Vigilancia: posible sobrecarga",
            "Rojo (>1.5)": "ALERTA: Alto riesgo de lesión"
        }
    },
    "Variación Semanal (%)": {
        "definicion": "Cambio porcentual de la carga de esta semana respecto a la anterior.",
        "formula": "(Carga Semana Actual - Carga Semana Anterior) / Carga Semana Anterior × 100",
        "recomendacion": "No exceder el 10% de variación para minimizar lesiones"
    },
    "CMJ (Countermovement Jump)": {
        "definicion": "Test de potencia donde el jugador salta desde bipedestación. Indicador de capacidad neuromuscular.",
        "medida": "Centímetros o potencia (watts)",
        "aplicacion": "Control de fatiga y recuperación"
    },
    "Test de Buchheit": {
        "definicion": "Test de resistencia anaeróbica repetida (6-8 sprints de 30-40 metros con recuperación incompleta).",
        "medida": "Mejor sprint (ms), decrement index (%)",
        "aplicacion": "Evalúa capacidad de cambios de ritmo y resistencia a la fatiga"
    }
}
