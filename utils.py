# utils.py
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from config import ACWR_OPTIMAL, ACWR_WARNING, ACWR_DANGER, VARIATION_WARNING, VARIATION_DANGER

class LoadCalculator:
    """Calcula métricas de carga de entrenamiento"""
    
    @staticmethod
    def calculate_acute_load(sessions, days=7):
        """Calcula la carga aguda (media móvil 7 días)"""
        if not sessions:
            return 0
        
        cutoff = datetime.now() - timedelta(days=days)
        recent_sessions = [
            s for s in sessions 
            if datetime.fromisoformat(s["date"]) >= cutoff
        ]
        
        if not recent_sessions:
            return 0
        
        total_load = sum(s["session_load"] for s in recent_sessions)
        return round(total_load / days, 2)
    
    @staticmethod
    def calculate_chronic_load(sessions, days=28):
        """Calcula la carga crónica (media móvil 28 días)"""
        if not sessions:
            return 0
        
        cutoff = datetime.now() - timedelta(days=days)
        relevant_sessions = [
            s for s in sessions 
            if datetime.fromisoformat(s["date"]) >= cutoff
        ]
        
        if not relevant_sessions:
            return 0
        
        total_load = sum(s["session_load"] for s in relevant_sessions)
        return round(total_load / days, 2)
    
    @staticmethod
    def calculate_acwr(acute_load, chronic_load):
        """Calcula el ACWR (Acute:Chronic Workload Ratio)"""
        if chronic_load == 0:
            return 0
        return round(acute_load / chronic_load, 2)
    
    @staticmethod
    def get_acwr_status(acwr):
        """Determina el estado basado en ACWR"""
        if acwr == 0:
            return "sin_datos", "#808080"  # Gris
        elif ACWR_OPTIMAL[0] <= acwr <= ACWR_OPTIMAL[1]:
            return "óptimo", "#00CC00"  # Verde
        elif ACWR_WARNING[0] < acwr <= ACWR_WARNING[1]:
            return "vigilancia", "#FFA500"  # Naranja
        else:
            return "peligro", "#FF0000"  # Rojo
    
    @staticmethod
    def calculate_weekly_variation(sessions):
        """Calcula variación semanal (%)"""
        if len(sessions) < 14:
            return 0
        
        today = datetime.now()
        one_week_ago = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)
        
        current_week = [
            s for s in sessions
            if datetime.fromisoformat(s["date"]) >= one_week_ago
        ]
        
        previous_week = [
            s for s in sessions
            if two_weeks_ago <= datetime.fromisoformat(s["date"]) < one_week_ago
        ]
        
        current_total = sum(s["session_load"] for s in current_week)
        previous_total = sum(s["session_load"] for s in previous_week)
        
        if previous_total == 0:
            return 0
        
        variation = ((current_total - previous_total) / previous_total) * 100
        return round(variation, 2)
    
    @staticmethod
    def get_variation_status(variation):
        """Determina el estado basado en variación semanal"""
        variation_abs = abs(variation)
        
        if variation_abs <= VARIATION_WARNING:
            return "óptimo", "#00CC00"
        elif variation_abs <= VARIATION_DANGER:
            return "vigilancia", "#FFA500"
        else:
            return "peligro", "#FF0000"

class MetricsAnalyzer:
    """Analiza datos para toma de decisiones"""
    
    @staticmethod
    def get_recommendations(acwr, variation, player_name):
        """Genera recomendaciones basadas en métricas"""
        recommendations = []
        
        # Basadas en ACWR
        if acwr > 1.5:
            recommendations.append(f"⚠️ {player_name}: ACWR crítico ({acwr}). Reducir carga inmediatamente.")
        elif acwr > 1.3:
            recommendations.append(f"⚡ {player_name}: ACWR elevado ({acwr}). Vigilar y considerar reducción.")
        elif acwr < 0.8 and acwr > 0:
            recommendations.append(f"📈 {player_name}: ACWR bajo ({acwr}). Puede tolerar más carga de entrenamiento.")
        
        # Basadas en variación
        if abs(variation) > VARIATION_DANGER:
            recommendations.append(f"🔥 {player_name}: Variación crítica ({variation:.1f}%). Progresión demasiado rápida o lenta.")
        elif abs(variation) > VARIATION_WARNING:
            recommendations.append(f"⚠️ {player_name}: Variación importante ({variation:.1f}%). Ajustar progresivamente.")
        
        return recommendations

def format_date(iso_string):
    """Formatea fecha ISO a formato legible"""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return iso_string

def generate_qr_code(unique_code, team_name):
    """Genera código QR para el enlace del jugador"""
    import qrcode
    from io import BytesIO
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(unique_code)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    return img
