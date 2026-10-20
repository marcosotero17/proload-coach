# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import qrcode
from io import BytesIO

from config import APP_NAME, APP_VERSION, GLOSSARY
from database import Database
from utils import LoadCalculator, MetricsAnalyzer, format_date, generate_qr_code

# Configuración de Streamlit
st.set_page_config(
    page_title=f"{APP_NAME} v{APP_VERSION}",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #1f77b4;
    }
    .danger-card {
        background-color: #ffe6e6;
        border-left-color: #ff0000;
    }
    .warning-card {
        background-color: #fff3cd;
        border-left-color: #FFA500;
    }
    .success-card {
        background-color: #d4edda;
        border-left-color: #00CC00;
    }
    .title-section {
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar sesión
if "db" not in st.session_state:
    st.session_state.db = Database()

if "current_team_id" not in st.session_state:
    st.session_state.current_team_id = None

if "user_role" not in st.session_state:
    st.session_state.user_role = None

db = st.session_state.db

# ============================================================================
# PÁGINA DE LOGIN/INICIO
# ============================================================================

def show_welcome_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="title-section">
            <h1>🏋️ ProLoad Coach</h1>
            <p style="font-size: 18px;">Gestión Inteligente de Carga de Entrenamiento</p>
            <p style="font-size: 12px;">v{}</p>
        </div>
        """.format(APP_VERSION), unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👨‍🏫 Preparador Físico")
        st.write("Accede al panel de control exclusivo para:")
        st.write("✅ Monitorear carga de todos tus jugadores")
        st.write("✅ Visualizar métricas ACWR en tiempo real")
        st.write("✅ Registrar datos antropométricos")
        st.write("✅ Analizar rendimiento físico")
        
        if st.button("🔐 Acceso Coach", key="coach_login", use_container_width=True):
            st.session_state.user_role = "coach"
            st.rerun()
    
    with col2:
        st.markdown("### ⚽ Jugador")
        st.write("Accede con tu código único para:")
        st.write("✅ Registrar tu RPE diario")
        st.write("✅ Registrar duración del entrenamiento")
        st.write("✅ Enviar datos privados")
        st.write("✅ Ver solo tu información")
        
        if st.button("🎮 Acceso Jugador", key="player_login", use_container_width=True):
            st.session_state.user_role = "player"
            st.rerun()

def show_coach_login():
    st.markdown("### 🔐 Acceso Coach - ProLoad Coach")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("")
        
        # Opciones
        tab1, tab2 = st.tabs(["🔑 Iniciar Sesión", "➕ Crear Nuevo Equipo"])
        
        with tab1:
            st.write("#### Accede a tu equipo existente")
            
            teams = db.get_all_teams()
            if not teams:
                st.warning("No hay equipos disponibles. Crea uno nuevo primero.")
            else:
                team_names = [t["name"] for t in teams]
                selected_team_name = st.selectbox("Selecciona tu equipo:", team_names, key="team_select")
                
                selected_team = next(t for t in teams if t["name"] == selected_team_name)
                
                password = st.text_input("Contraseña:", type="password", key="login_password")
                
                if st.button("Iniciar Sesión", use_container_width=True, key="login_btn"):
                    if password == selected_team["coach_password"]:
                        st.session_state.current_team_id = selected_team["id"]
                        st.session_state.user_role = "coach"
                        st.success("✅ Sesión iniciada correctamente")
                        st.rerun()
                    else:
                        st.error("❌ Contraseña incorrecta")
        
        with tab2:
            st.write("#### Crear un nuevo equipo")
            
            team_name = st.text_input("Nombre del equipo:", placeholder="Ej. SD Sarriana")
            coach_name = st.text_input("Tu nombre:", placeholder="Ej. Juan García")
            coach_password = st.text_input("Crea una contraseña:", type="password", key="new_password")
            coach_password_confirm = st.text_input("Confirma la contraseña:", type="password", key="confirm_password")
            
            if st.button("Crear Equipo", use_container_width=True, key="create_team_btn"):
                if not team_name or not coach_name or not coach_password:
                    st.error("Por favor completa todos los campos")
                elif coach_password != coach_password_confirm:
                    st.error("Las contraseñas no coinciden")
                elif len(coach_password) < 4:
                    st.error("La contraseña debe tener al menos 4 caracteres")
                else:
                    team_id, unique_code = db.create_team(team_name, coach_name, coach_password)
                    st.session_state.current_team_id = team_id
                    st.session_state.user_role = "coach"
                    st.success(f"✅ Equipo '{team_name}' creado correctamente")
                    st.balloons()
                    st.rerun()

def show_player_login():
    st.markdown("### ⚽ Acceso Jugador - ProLoad Coach")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("")
        st.info("💡 Pide a tu preparador físico el código único de tu equipo")
        
        unique_code = st.text_input("Código único del equipo:", placeholder="Ej. a1b2c3d4e5f6")
        
        if st.button("Acceder", use_container_width=True, key="player_access_btn"):
            team = db.get_team_by_code(unique_code)
            if team:
                st.session_state.current_team_id = team["id"]
                st.session_state.user_role = "player"
                st.success(f"✅ Acceso concedido al equipo '{team['name']}'")
                st.rerun()
            else:
                st.error("❌ Código no válido. Verifica e intenta de nuevo.")

# ============================================================================
# INTERFAZ DEL JUGADOR
# ============================================================================

def show_player_interface():
    team = db.get_team_by_id(st.session_state.current_team_id)
    
    if not team:
        st.error("Equipo no encontrado")
        return
    
    # Header minimalista
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white; text-align: center;">
        <h2>⚽ {team['name']}</h2>
        <p>Registra tu sesión de entrenamiento</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Formulario del jugador
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 👤 Tu Información")
        
        # Lista de jugadores activos
        active_players = [p for p in team["players"] if p["active"]]
        player_names = [p["name"] for p in active_players]
        
        if not player_names:
            st.warning("⚠️ No hay jugadores disponibles en este equipo.")
            st.write("Contacta con tu preparador físico.")
            return
        
        selected_player = st.selectbox("Selecciona tu nombre:", player_names, key="player_select")
        player_obj = next(p for p in active_players if p["name"] == selected_player)
    
    with col2:
        st.markdown("### 📊 Tu Sesión de Hoy")
        
        rpe = st.slider("RPE (Intensidad 0-10):", 0, 10, 5, step=1, 
                       help="0=Muy suave | 5=Moderado | 10=Máximo esfuerzo")
        
        duration = st.number_input("Duración (minutos):", min_value=0, max_value=180, value=60, step=5)
    
    st.write("")
    
    # Información de RPE
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("RPE Seleccionado", f"{rpe}/10")
    with col2:
        st.metric("Duración", f"{duration} min")
    with col3:
        session_load = rpe * duration
        st.metric("Carga de Sesión", session_load)
    
    st.markdown("---")
    
    # Botón de envío
    if st.button("✅ Enviar Sesión", use_container_width=True, key="submit_session"):
        if duration == 0:
            st.error("Por favor indica una duración mayor a 0 minutos")
        else:
            db.record_session(
                team_id=st.session_state.current_team_id,
                player_id=player_obj["id"],
                player_name=selected_player,
                rpe=rpe,
                duration_minutes=duration
            )
            st.success("✅ ¡Sesión registrada correctamente!")
            st.balloons()
    
    st.write("")
    st.markdown("---")
    
    if st.button("← Volver al inicio", key="player_back"):
        st.session_state.user_role = None
        st.rerun()

# ============================================================================
# DASHBOARD DEL COACH
# ============================================================================

def show_coach_dashboard():
    team = db.get_team_by_id(st.session_state.current_team_id)
    
    if not team:
        st.error("Equipo no encontrado")
        return
    
    # Header del dashboard
    st.markdown(f"""
    <div class="title-section">
        <h1>🏋️ Dashboard ProLoad Coach</h1>
        <p>Equipo: <strong>{team['name']}</strong> | Coach: <strong>{team['coach_name']}</strong></p>
        <p style="font-size: 12px;">Código único: <code>{team['unique_code']}</code></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar para navegación
    with st.sidebar:
        st.markdown("### 📋 Panel de Control")
        section = st.radio(
            "Selecciona una sección:",
            ["📊 Resumen General", "👥 Gestión de Jugadores", "📈 Análisis Detallado", "📋 Glosario", "⚙️ Configuración"]
        )
    
    if section == "📊 Resumen General":
        show_dashboard_overview(team)
    elif section == "👥 Gestión de Jugadores":
        show_player_management(team)
    elif section == "📈 Análisis Detallado":
        show_detailed_analysis(team)
    elif section == "📋 Glosario":
        show_glossary()
    elif section == "⚙️ Configuración":
        show_settings(team)

def show_dashboard_overview(team):
    """Resumen general del equipo"""
    st.markdown("### 📊 Resumen del Equipo")
    
    active_players = [p for p in team["players"] if p["active"]]
    
    # Estadísticas generales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Jugadores Activos", len(active_players))
    with col2:
        st.metric("📅 Sesiones Totales", len(team["sessions"]))
    with col3:
        last_update = team.get("last_updated", "N/A")
        st.metric("🕐 Última Actualización", format_date(last_update)[:10] if last_update != "N/A" else "N/A")
    with col4:
        st.metric("🔗 Código Único", team["unique_code"][:8])
    
    st.markdown("---")
    
    # Tabla de métricas por jugador
    st.markdown("### 🎯 Métricas Actuales por Jugador")
    
    metrics_data = []
    
    for player in active_players:
        sessions = db.get_player_sessions(team["id"], player["id"], days=28)
        
        if not sessions:
            metrics_data.append({
                "Jugador": player["name"],
                "Sesiones": 0,
                "Carga Aguda": 0,
                "Carga Crónica": 0,
                "ACWR": "—",
                "Estado": "Sin datos",
                "Variación %": "—"
            })
        else:
            acute = LoadCalculator.calculate_acute_load(sessions, days=7)
            chronic = LoadCalculator.calculate_chronic_load(sessions, days=28)
            acwr = LoadCalculator.calculate_acwr(acute, chronic)
            acwr_status, _ = LoadCalculator.get_acwr_status(acwr)
            variation = LoadCalculator.calculate_weekly_variation(sessions)
            
            status_map = {
                "óptimo": "✅ Óptimo",
                "vigilancia": "⚠️ Vigilancia",
                "peligro": "🔴 Peligro",
                "sin_datos": "—"
            }
            
            metrics_data.append({
                "Jugador": player["name"],
                "Sesiones": len(sessions),
                "Carga Aguda": round(acute, 0),
                "Carga Crónica": round(chronic, 0),
                "ACWR": f"{acwr:.2f}" if acwr > 0 else "—",
                "Estado": status_map.get(acwr_status, "—"),
                "Variación %": f"{variation:+.1f}%" if variation != 0 else "—"
            })
    
    df_metrics = pd.DataFrame(metrics_data)
    st.dataframe(df_metrics, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Gráfico de ACWR
    st.markdown("### 📊 Evolución del ACWR")
    
    acwr_data = []
    for player in active_players:
        sessions = db.get_player_sessions(team["id"], player["id"], days=28)
        if sessions:
            acute = LoadCalculator.calculate_acute_load(sessions, days=7)
            chronic = LoadCalculator.calculate_chronic_load(sessions, days=28)
            acwr = LoadCalculator.calculate_acwr(acute, chronic)
            
            if acwr > 0:
                acwr_data.append({
                    "Jugador": player["name"],
                    "ACWR": acwr,
                    "Zona": "Óptimo" if LoadCalculator.get_acwr_status(acwr)[0] == "óptimo" else 
                            "Vigilancia" if LoadCalculator.get_acwr_status(acwr)[0] == "vigilancia" else "Peligro"
                })
    
    if acwr_data:
        df_acwr = pd.DataFrame(acwr_data)
        fig = px.bar(df_acwr, x="Jugador", y="ACWR", color="Zona",
                    color_discrete_map={"Óptimo": "#00CC00", "Vigilancia": "#FFA500", "Peligro": "#FF0000"},
                    title="ACWR por Jugador (últimos 7 días vs 28 días)")
        
        # Añadir líneas de referencia
        fig.add_hline(y=0.8, line_dash="dash", line_color="green", annotation_text="Mín. Óptimo")
        fig.add_hline(y=1.3, line_dash="dash", line_color="orange", annotation_text="Máx. Óptimo")
        fig.add_hline(y=1.5, line_dash="dash", line_color="red", annotation_text="Peligro")
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar ACWR")
    
    st.markdown("---")
    
    # Recomendaciones automáticas
    st.markdown("### 💡 Recomendaciones Automáticas")
    
    recommendations = []
    for player in active_players:
        sessions = db.get_player_sessions(team["id"], player["id"], days=28)
        if sessions:
            acute = LoadCalculator.calculate_acute_load(sessions, days=7)
            chronic = LoadCalculator.calculate_chronic_load(sessions, days=28)
            acwr = LoadCalculator.calculate_acwr(acute, chronic)
            variation = LoadCalculator.calculate_weekly_variation(sessions)
            
            recs = MetricsAnalyzer.get_recommendations(acwr, variation, player["name"])
            recommendations.extend(recs)
    
    if recommendations:
        for rec in recommendations:
            if "ACWR crítico" in rec or "Variación crítica" in rec:
                st.error(rec)
            elif "ACWR elevado" in rec or "Variación importante" in rec:
                st.warning(rec)
            else:
                st.info(rec)
    else:
        st.success("✅ Todos los jugadores están en estado óptimo")

def show_player_management(team):
    """Gestión de jugadores"""
    st.markdown("### 👥 Gestión de Jugadores")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        new_player_name = st.text_input("Nombre del nuevo jugador:", key="new_player")
        
        if st.button("➕ Añadir Jugador", use_container_width=True):
            if new_player_name.strip():
                db.add_player_to_team(team["id"], new_player_name)
                st.success(f"✅ Jugador '{new_player_name}' añadido")
                st.rerun()
            else:
                st.error("Por favor introduce un nombre válido")
    
    with col2:
        st.write("")  # Espaciador
    
    st.markdown("---")
    
    # Lista de jugadores
    st.markdown("#### Lista de Jugadores")
    
    active_players = [p for p in team["players"] if p["active"]]
    inactive_players = [p for p in team["players"] if not p["active"]]
    
    tab1, tab2 = st.tabs([f"✅ Activos ({len(active_players)})", f"❌ Inactivos ({len(inactive_players)})"])
    
    with tab1:
        if active_players:
            for player in active_players:
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    sessions = db.get_player_sessions(team["id"], player["id"], days=7)
                    st.write(f"**{player['name']}** | Sesiones (7d): {len(sessions)}")
                
                with col2:
                    st.write("")  # Espaciador
                
                with col3:
                    if st.button("❌ Dar de baja", key=f"deactivate_{player['id']}", use_container_width=True):
                        db.remove_player_from_team(team["id"], player["id"])
                        st.success(f"'{player['name']}' marcado como inactivo")
                        st.rerun()
        else:
            st.info("No hay jugadores activos. Añade algunos para comenzar.")
    
    with tab2:
        if inactive_players:
            for player in inactive_players:
                st.write(f"• {player['name']} - Inactivo desde {format_date(player['added_date'])}")
        else:
            st.info("No hay jugadores inactivos")
    
    st.markdown("---")
    
    # Datos antropométricos
    st.markdown("#### 📏 Datos Antropométricos")
    
    if active_players:
        selected_player_name = st.selectbox("Selecciona un jugador:", [p["name"] for p in active_players], key="anthro_select")
        selected_player = next(p for p in active_players if p["name"] == selected_player_name)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            weight = st.number_input(f"Peso ({selected_player_name}) [kg]:", min_value=30.0, max_value=150.0, step=0.1)
        
        with col2:
            height = st.number_input(f"Altura ({selected_player_name}) [cm]:", min_value=150, max_value=220, step=1)
        
        with col3:
            st.write("")  # Espaciador
        
        notes = st.text_area("Notas (opcional):", height=80)
        
        if st.button("💾 Guardar Datos Antropométricos", use_container_width=True):
            db.add_anthropometry(team["id"], selected_player["id"], {
                "weight": weight,
                "height": height,
                "skinfolds": {},
                "notes": notes
            })
            st.success("✅ Datos guardados")
            st.rerun()

def show_detailed_analysis(team):
    """Análisis detallado por jugador"""
    st.markdown("### 📈 Análisis Detallado del Equipo")
    
    active_players = [p for p in team["players"] if p["active"]]
    
    if not active_players:
        st.warning("No hay jugadores activos")
        return
    
    selected_player_name = st.selectbox("Selecciona un jugador:", [p["name"] for p in active_players], key="analysis_select")
    selected_player = next(p for p in active_players if p["name"] == selected_player_name)
    
    sessions = db.get_player_sessions(team["id"], selected_player["id"], days=28)
    
    if not sessions:
        st.info(f"No hay sesiones registradas para {selected_player_name}")
        return
    
    st.markdown(f"#### 📊 Análisis de {selected_player_name}")
    
    # Métricas principales
    acute = LoadCalculator.calculate_acute_load(sessions, days=7)
    chronic = LoadCalculator.calculate_chronic_load(sessions, days=28)
    acwr = LoadCalculator.calculate_acwr(acute, chronic)
    acwr_status, acwr_color = LoadCalculator.get_acwr_status(acwr)
    variation = LoadCalculator.calculate_weekly_variation(sessions)
    var_status, var_color = LoadCalculator.get_variation_status(variation)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Carga Aguda (7d)", f"{acute:.0f}")
    with col2:
        st.metric("Carga Crónica (28d)", f"{chronic:.0f}")
    with col3:
        color_emoji = "🟢" if acwr_status == "óptimo" else "🟠" if acwr_status == "vigilancia" else "🔴" if acwr_status == "peligro" else "⚪"
        st.metric("ACWR", f"{acwr:.2f}" if acwr > 0 else "—", f"{color_emoji} {acwr_status}")
    with col4:
        st.metric("Variación Semanal", f"{variation:+.1f}%", f"🎯 {var_status}")
    with col5:
        st.metric("Total Sesiones", len(sessions))
    
    st.markdown("---")
    
    # Gráfico de carga diaria
    df_sessions = pd.DataFrame([
        {
            "Fecha": datetime.fromisoformat(s["date"]).date(),
            "Carga": s["session_load"],
            "RPE": s["rpe"],
            "Minutos": s["duration_minutes"]
        }
        for s in sessions
    ])
    
    fig_daily = px.bar(df_sessions, x="Fecha", y="Carga", title=f"Carga de Sesión Diaria - {selected_player_name}",
                      labels={"Carga": "RPE × Minutos", "Fecha": "Fecha"})
    st.plotly_chart(fig_daily, use_container_width=True)
    
    # Gráfico de evolución de carga aguda y crónica
    st.markdown("---")
    
    # Calcular evolución diaria
    dates = []
    acute_evolution = []
    chronic_evolution = []
    
    for i in range(len(sessions)):
        current_sessions = sessions[:i+1]
        dates.append(datetime.fromisoformat(sessions[i]["date"]).date())
        acute_evolution.append(LoadCalculator.calculate_acute_load(current_sessions, days=7))
        chronic_evolution.append(LoadCalculator.calculate_chronic_load(current_sessions, days=28))
    
    df_evolution = pd.DataFrame({
        "Fecha": dates,
        "Carga Aguda (7d)": acute_evolution,
        "Carga Crónica (28d)": chronic_evolution
    })
    
    fig_evolution = go.Figure()
    fig_evolution.add_trace(go.Scatter(x=df_evolution["Fecha"], y=df_evolution["Carga Aguda (7d)"], 
                                       name="Carga Aguda (7d)", mode="lines+markers", line=dict(color="blue")))
    fig_evolution.add_trace(go.Scatter(x=df_evolution["Fecha"], y=df_evolution["Carga Crónica (28d)"], 
                                       name="Carga Crónica (28d)", mode="lines+markers", line=dict(color="orange")))
    
    fig_evolution.update_layout(title=f"Evolución de Cargas - {selected_player_name}",
                               xaxis_title="Fecha", yaxis_title="Carga (u.a.)",
                               hovermode="x unified", height=400)
    
    st.plotly_chart(fig_evolution, use_container_width=True)

def show_glossary():
    """Glosario de métricas"""
    st.markdown("### 📚 Glosario de Métricas - ProLoad Coach")
    
    st.info("📖 Esta sección explica de forma científica todas las métricas utilizadas en ProLoad Coach")
    
    st.markdown("---")
    
    for metric_name, metric_info in GLOSSARY.items():
        with st.expander(f"📌 {metric_name}", expanded=False):
            st.write(f"**Definición:** {metric_info.get('definicion', 'N/A')}")
            
            if "formula" in metric_info:
                st.write(f"**Fórmula:** `{metric_info['formula']}`")
            
            if "rango" in metric_info:
                st.write(f"**Rango:** {metric_info['rango']}")
            
            if "periodo" in metric_info:
                st.write(f"**Período:** {metric_info['periodo']}")
            
            if "interpretacion" in metric_info:
                st.write(f"**Interpretación:** {metric_info['interpretacion']}")
            
            if "ejemplo" in metric_info:
                st.write(f"**Ejemplo:** {metric_info['ejemplo']}")
            
            if "zonas" in metric_info:
                st.write("**Zonas de Riesgo:**")
                for zone, description in metric_info["zonas"].items():
                    st.write(f"  - {zone}: {description}")
            
            if "recomendacion" in metric_info:
                st.write(f"✅ **Recomendación:** {metric_info['recomendacion']}")
            
            if "medida" in metric_info:
                st.write(f"**Unidad de Medida:** {metric_info['medida']}")
            
            if "aplicacion" in metric_info:
                st.write(f"**Aplicación Práctica:** {metric_info['aplicacion']}")

def show_settings(team):
    """Configuración del equipo"""
    st.markdown("### ⚙️ Configuración del Equipo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔗 Enlace de Acceso Jugadores")
        st.write(f"**Código Único:** `{team['unique_code']}`")
        
        # Generar URL (en producción sería la URL real)
        player_url = f"https://proload.coach/?code={team['unique_code']}"
        st.write(f"**URL de Acceso:** {player_url}")
        
        if st.button("📋 Copiar Código", key="copy_code"):
            st.info(f"Código copiado: {team['unique_code']}")
        
        st.markdown("---")
        st.markdown("#### 📱 Código QR para Jugadores")
        
        qr_img = generate_qr_code(team['unique_code'], team['name'])
        st.image(qr_img, width=300, caption="Escanea este código QR para acceder")
    
    with col2:
        st.markdown("#### ℹ️ Información del Equipo")
        st.write(f"**Nombre:** {team['name']}")
        st.write(f"**Coach:** {team['coach_name']}")
        st.write(f"**Creado:** {format_date(team['created_date'])}")
        st.write(f"**Total Jugadores:** {len([p for p in team['players'] if p['active']])}")
        st.write(f"**Total Sesiones:** {len(team['sessions'])}")
        
        st.markdown("---")
        
        if st.button("🚪 Cerrar Sesión", use_container_width=True, key="logout"):
            st.session_state.current_team_id = None
            st.session_state.user_role = None
            st.success("Sesión cerrada")
            st.rerun()

# ============================================================================
# FLUJO PRINCIPAL DE LA APLICACIÓN
# ============================================================================

def main():
    if st.session_state.user_role is None:
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏠 Inicio", use_container_width=True, key="home_btn"):
                st.session_state.user_role = None
        
        with col2:
            st.write("")
        
        st.write("")
        show_welcome_page()
    
    elif st.session_state.user_role == "coach":
        if st.session_state.current_team_id is None:
            show_coach_login()
        else:
            show_coach_dashboard()
    
    elif st.session_state.user_role == "player":
        if st.session_state.current_team_id is None:
            show_player_login()
        else:
            show_player_interface()

if __name__ == "__main__":
    main()
