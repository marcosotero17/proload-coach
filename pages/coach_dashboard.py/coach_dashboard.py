# pages/coach_dashboard.py
"""
Dashboard principal del preparador físico
Monitoreo en tiempo real de carga de entrenamiento, ACWR y recomendaciones
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

from database import Database
from utils import LoadCalculator, MetricsAnalyzer, format_date

def initialize_coach_session():
    """Inicializa variables de sesión del coach"""
    if "coach_db" not in st.session_state:
        st.session_state.coach_db = Database()
    
    if "coach_team_id" not in st.session_state:
        st.session_state.coach_team_id = None

def show_coach_welcome():
    """Pantalla de bienvenida del coach"""
    st.markdown("""
    <div class="title-section" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 15px; color: white; text-align: center;">
        <h1>🏋️ ProLoad Coach Dashboard</h1>
        <p style="font-size: 18px;">Panel de Control Inteligente de Carga de Entrenamiento</p>
        <p style="font-size: 12px; opacity: 0.8;">Sistema Automático de Monitoreo ACWR y Gestión de Equipos</p>
    </div>
    """, unsafe_allow_html=True)

def coach_login(db):
    """Interfaz de login del coach"""
    st.markdown("### 🔐 Acceso Preparador Físico")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("")
        
        tab1, tab2 = st.tabs(["🔑 Iniciar Sesión", "➕ Crear Nuevo Equipo"])
        
        with tab1:
            st.write("#### Accede a tu equipo")
            
            teams = db.get_all_teams()
            
            if not teams:
                st.warning("⚠️ No hay equipos disponibles aún. Crea uno nuevo para comenzar.")
            else:
                team_names = [t["name"] for t in teams]
                selected_team_name = st.selectbox(
                    "Selecciona tu equipo:",
                    team_names,
                    key="coach_team_select"
                )
                
                selected_team = next(t for t in teams if t["name"] == selected_team_name)
                
                password = st.text_input(
                    "Contraseña:",
                    type="password",
                    key="coach_login_password"
                )
                
                if st.button("🔓 Iniciar Sesión", use_container_width=True, key="coach_login_btn"):
                    if password == selected_team["coach_password"]:
                        st.session_state.coach_team_id = selected_team["id"]
                        st.success("✅ Sesión iniciada correctamente")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Contraseña incorrecta")
        
        with tab2:
            st.write("#### Crea un nuevo equipo")
            
            team_name = st.text_input(
                "Nombre del equipo:",
                placeholder="Ej. SD Sarriana, Real Madrid, Barcelona",
                key="new_team_name"
            )
            
            coach_name = st.text_input(
                "Tu nombre (Preparador Físico):",
                placeholder="Ej. Juan García López",
                key="new_coach_name"
            )
            
            coach_password = st.text_input(
                "Crea una contraseña segura:",
                type="password",
                key="new_coach_password"
            )
            
            coach_password_confirm = st.text_input(
                "Confirma la contraseña:",
                type="password",
                key="confirm_coach_password"
            )
            
            if st.button("➕ Crear Equipo", use_container_width=True, key="create_team_btn"):
                if not team_name or not coach_name or not coach_password:
                    st.error("❌ Por favor completa todos los campos")
                elif coach_password != coach_password_confirm:
                    st.error("❌ Las contraseñas no coinciden")
                elif len(coach_password) < 6:
                    st.error("❌ La contraseña debe tener al menos 6 caracteres")
                else:
                    team_id, unique_code = db.create_team(team_name, coach_name, coach_password)
                    st.session_state.coach_team_id = team_id
                    st.success(f"✅ Equipo '{team_name}' creado correctamente")
                    st.info(f"📌 Código único: `{unique_code}`")
                    st.balloons()
                    st.rerun()

def show_team_overview(db, team):
    """Resumen general del equipo"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white;">
        <h2>📊 {team['name']}</h2>
        <p>Coach: <strong>{team['coach_name']}</strong> | Código: <code>{team['unique_code']}</code></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Estadísticas generales
    active_players = [p for p in team["players"] if p["active"]]
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("👥 Jugadores Activos", len(active_players))
    
    with col2:
        st.metric("📅 Total Sesiones", len(team["sessions"]))
    
    with col3:
        total_days_active = (datetime.now() - datetime.fromisoformat(team["created_date"])).days + 1
        st.metric("📆 Días Activo", total_days_active)
    
    with col4:
        if team["sessions"]:
            avg_sessions_per_player = len(team["sessions"]) / len(active_players) if active_players else 0
            st.metric("📊 Sesiones/Jugador", f"{avg_sessions_per_player:.1f}")
        else:
            st.metric("📊 Sesiones/Jugador", "0")
    
    with col5:
        last_session = max(team["sessions"], key=lambda x: x["date"])["date"] if team["sessions"] else "—"
        st.metric("🕐 Última Sesión", format_date(last_session)[:10] if last_session != "—" else "—")
    
    st.markdown("---")

def show_team_metrics_table(db, team):
    """Tabla con métricas de todos los jugadores"""
    st.markdown("### 🎯 Métricas de Carga - Todos los Jugadores")
    
    active_players = [p for p in team["players"] if p["active"]]
    
    if not active_players:
        st.info("📭 No hay jugadores activos en el equipo")
        return
    
    metrics_data = []
    
    for player in active_players:
        sessions = db.get_player_sessions(team["id"], player["id"], days=28)
        
        if sessions:
            acute = LoadCalculator.calculate_acute_load(sessions, days=7)
            chronic = LoadCalculator.calculate_chronic_load(sessions, days=28)
            acwr = LoadCalculator.calculate_acwr(acute, chronic)
            acwr_status, acwr_color = LoadCalculator.get_acwr_status(acwr)
            variation = LoadCalculator.calculate_weekly_variation(sessions)
            var_status, var_color = LoadCalculator.get_variation_status(variation)
            
            # Mapeo de estados a emojis
            status_emoji_map = {
                "óptimo": "🟢",
                "vigilancia": "🟠",
                "peligro": "🔴",
                "sin_datos": "⚪"
            }
            
            metrics_data.append({
                "👤 Jugador": player["name"],
                "📊 Sesiones (28d)": len(sessions),
                "⚡ Carga Aguda (7d)": round(acute, 0),
                "💪 Carga Crónica (28d)": round(chronic, 0),
                "⚖️ ACWR": f"{acwr:.2f}" if acwr > 0 else "—",
                "🎯 Estado ACWR": f"{status_emoji_map.get(acwr_status, '⚪')} {acwr_status}",
                "📈 Variación (%)": f"{variation:+.1f}%" if variation != 0 else "—",
                "🚨 Riesgo Lesión": f"{status_emoji_map.get(var_status, '⚪')} {var_status}"
            })
        else:
            metrics_data.append({
                "👤 Jugador": player["name"],
                "📊 Sesiones (28d)": 0,
                "⚡ Carga Aguda (7d)": "—",
                "💪 Carga Crónica (28d)": "—",
                "⚖️ ACWR": "—",
                "🎯 Estado ACWR": "⚪ sin_datos",
                "📈 Variación (%)": "—",
                "🚨 Riesgo Lesión": "⚪ sin_datos"
            })
    
    df_metrics = pd.DataFrame(metrics_data)
    
    # Mostrar tabla con colores
    st.dataframe(
        df_metrics,
        use_container_width=True,
        hide_index=True,
        height=len(metrics_data) * 35 + 35
    )
    
    st.markdown("---")

def show_acwr_visualization(db, team):
    """Visualizaciones de ACWR"""
    st.markdown("### 📊 Análisis Visual del ACWR")
    
    active_players = [p for p in team["players"] if p["active"]]
    
    if not active_players:
        st.info("No hay jugadores activos")
        return
    
    # Preparar datos
    acwr_data = []
    
    for player in active_players:
        sessions = db.get_player_sessions(team["id"], player["id"], days=28)
        
        if sessions:
            acute = LoadCalculator.calculate_acute_load(sessions, days=7)
            chronic = LoadCalculator.calculate_chronic_load(sessions, days=28)
            acwr = LoadCalculator.calculate_acwr(acute, chronic)
            
            if acwr > 0:
                acwr_status = LoadCalculator.get_acwr_status(acwr)[0]
                
                acwr_data.append({
                    "Jugador": player["name"],
                    "ACWR": acwr,
                    "Estado": "Óptimo" if acwr_status == "óptimo" else
                              "Vigilancia" if acwr_status == "vigilancia" else "Peligro"
                })
    
    if acwr_data:
        df_acwr = pd.DataFrame(acwr_data)
        
        # Gráfico de barras
        fig_bars = px.bar(
            df_acwr,
            x="Jugador",
            y="ACWR",
            color="Estado",
            color_discrete_map={"Óptimo": "#00CC00", "Vigilancia": "#FFA500", "Peligro": "#FF0000"},
            title="ACWR por Jugador (Carga Aguda vs Crónica)",
            labels={"ACWR": "Ratio ACWR", "Jugador": "Nombre del Jugador"},
            height=400
        )
        
        # Agregar líneas de referencia
        fig_bars.add_hline(
            y=0.8,
            line_dash="dash",
            line_color="green",
            annotation_text="Mín. Óptimo (0.8)",
            annotation_position="right"
        )
        fig_bars.add_hline(
            y=1.3,
            line_dash="dash",
            line_color="orange",
            annotation_text="Máx. Óptimo (1.3)",
            annotation_position="right"
        )
        fig_bars.add_hline(
            y=1.5,
            line_dash="dash",
            line_color="red",
            annotation_text="Zona Peligro (1.5)",
            annotation_position="right"
        )
        
        fig_bars.update_yaxis(range=[0, max(2.0, df_acwr["ACWR"].max() * 1.1)])
        
        st.plotly_chart(fig_bars, use_container_width=True)
        
        # Gráfico radar
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter plot ACWR vs Variación
            variation_data = []
            
            for player in active_players:
                sessions = db.get_player_sessions(team["id"], player["id"], days=28)
                
                if sessions:
                    acute = LoadCalculator.calculate_acute_load(sessions, days=7)
                    chronic = LoadCalculator.calculate_chronic_load(sessions, days=28)
                    acwr = LoadCalculator.calculate_acwr(acute, chronic)
                    variation = LoadCalculator.calculate_weekly_variation(sessions)
                    
                    if acwr > 0:
                        variation_data.append({
                            "Jugador": player["name"],
                            "ACWR": acwr,
                            "Variación (%)": variation
                        })
            
            if variation_data:
                df_variation = pd.DataFrame(variation_data)
                
                fig_scatter = px.scatter(
                    df_variation,
                    x="ACWR",
                    y="Variación (%)",
                    text="Jugador",
                    title="ACWR vs Variación Semanal",
                    height=400,
                    size_max=50
                )
                
                fig_scatter.update_traces(textposition='top center')
                fig_scatter.add_vline(x=0.8, line_dash="dash", line_color="green", opacity=0.5)
                fig_scatter.add_vline(x=1.3, line_dash="dash", line_color="orange", opacity=0.5)
                fig_scatter.add_vline(x=1.5, line_dash="dash", line_color="red", opacity=0.5)
                fig_scatter.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.3)
                
                st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            # Estadísticas de ACWR
            st.markdown("#### 📊 Estadísticas ACWR")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.metric("ACWR Promedio", f"{df_acwr['ACWR'].mean():.2f}")
                st.metric("ACWR Máximo", f"{df_acwr['ACWR'].max():.2f}")
            
            with col_b:
                st.metric("ACWR Mínimo", f"{df_acwr['ACWR'].min():.2f}")
                st.metric("Jugadores Críticos", len(df_acwr[df_acwr["Estado"] == "Peligro"]))
    else:
        st.info("No hay datos suficientes para mostrar ACWR")
    
    st.markdown("---")

def show_load_evolution(db, team):
    """Evolución de carga en el tiempo"""
    st.markdown("### 📈 Evolución de Carga (últimos 28 días)")
    
    active_players = [p for p in team["players"] if p["active"]]
    
    if not active_players or not team["sessions"]:
        st.info("No hay datos suficientes")
        return
    
    # Datos por día
    days_data = {}
    cutoff = datetime.now() - timedelta(days=28)
    
    for session in team["sessions"]:
        session_date = datetime.fromisoformat(session["date"]).date()
        
        if session_date >= cutoff.date():
            if session_date not in days_data:
                days_data[session_date] = {"total_load": 0, "num_sessions": 0, "avg_rpe": 0, "total_rpe": 0}
            
            days_data[session_date]["total_load"] += session["session_load"]
            days_data[session_date]["num_sessions"] += 1
            days_data[session_date]["total_rpe"] += session["rpe"]
    
    # Calcular promedio RPE por día
    for day in days_data:
        if days_data[day]["num_sessions"] > 0:
            days_data[day]["avg_rpe"] = days_data[day]["total_rpe"] / days_data[day]["num_sessions"]
    
    # Convertir a DataFrame
    df_daily = pd.DataFrame([
        {
            "Fecha": day,
            "Carga Total": data["total_load"],
            "Sesiones": data["num_sessions"],
            "RPE Promedio": round(data["avg_rpe"], 1)
        }
        for day, data in sorted(days_data.items())
    ])
    
    if not df_daily.empty:
        # Gráfico de línea
        fig_evolution = go.Figure()
        
        fig_evolution.add_trace(go.Scatter(
            x=df_daily["Fecha"],
            y=df_daily["Carga Total"],
            name="Carga Total",
            mode="lines+markers",
            line=dict(color="#667eea", width=2),
            yaxis="y"
        ))
        
        fig_evolution.add_trace(go.Scatter(
            x=df_daily["Fecha"],
            y=df_daily["RPE Promedio"],
            name="RPE Promedio",
            mode="lines+markers",
            line=dict(color="#764ba2", width=2),
            yaxis="y2"
        ))
        
        fig_evolution.update_layout(
            title="Evolución de Carga y RPE",
            xaxis_title="Fecha",
            yaxis=dict(title="Carga Total (u.a.)", side="left"),
            yaxis2=dict(title="RPE Promedio", overlaying="y", side="right"),
            hovermode="x unified",
            height=400
        )
        
        st.plotly_chart(fig_evolution, use_container_width=True)
        
        # Tabla de evolución
        st.markdown("#### 📋 Datos Diarios")
        st.dataframe(df_daily, use_container_width=True, hide_index=True)
    
    st.markdown("---")

def show_automatic_recommendations(db, team):
    """Recomendaciones automáticas basadas en métricas"""
    st.markdown("### 💡 Recomendaciones Automáticas")
    
    active_players = [p for p in team["players"] if p["active"]]
    
    all_recommendations = []
    danger_count = 0
    warning_count = 0
    success_count = 0
    
    for player in active_players:
        sessions = db.get_player_sessions(team["id"], player["id"], days=28)
        
        if sessions:
            acute = LoadCalculator.calculate_acute_load(sessions, days=7)
            chronic = LoadCalculator.calculate_chronic_load(sessions, days=28)
            acwr = LoadCalculator.calculate_acwr(acute, chronic)
            variation = LoadCalculator.calculate_weekly_variation(sessions)
            
            recs = MetricsAnalyzer.get_recommendations(acwr, variation, player["name"])
            
            for rec in recs:
                if "ACWR crítico" in rec or "Variación crítica" in rec:
                    all_recommendations.append(("danger", rec))
                    danger_count += 1
                elif "ACWR elevado" in rec or "Variación importante" in rec:
                    all_recommendations.append(("warning", rec))
                    warning_count += 1
                else:
                    all_recommendations.append(("info", rec))
            
            # Si todo está bien
            if not recs:
                success_count += 1
    
    # Resumen
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔴 Críticos", danger_count)
    
    with col2:
        st.metric("🟠 Vigilancia", warning_count)
    
    with col3:
        st.metric("🟢 Óptimos", success_count)
    
    with col4:
        st.metric("👥 Total Jugadores", len(active_players))
    
    st.write("")
    
    # Mostrar recomendaciones
    if all_recommendations:
        for rec_type, rec_text in all_recommendations:
            if rec_type == "danger":
                st.error(rec_text)
            elif rec_type == "warning":
                st.warning(rec_text)
            else:
                st.info(rec_text)
    else:
        if len(active_players) > 0:
            st.success("✅ Todos los jugadores están en estado óptimo")
        else:
            st.info("📭 Añade jugadores al equipo para comenzar el monitoreo")
    
    st.markdown("---")

def show_detailed_player_analysis(db, team):
    """Análisis detallado de un jugador específico"""
    st.markdown("### 📊 Análisis Detallado por Jugador")
    
    active_players = [p for p in team["players"] if p["active"]]
    
    if not active_players:
        st.info("No hay jugadores activos")
        return
    
    selected_player_name = st.selectbox(
        "Selecciona un jugador:",
        [p["name"] for p in active_players],
        key="detailed_player_select"
    )
    
    selected_player = next(p for p in active_players if p["name"] == selected_player_name)
    sessions = db.get_player_sessions(team["id"], selected_player["id"], days=28)
    
    if not sessions:
        st.info(f"📭 No hay sesiones registradas para {selected_player_name}")
        return
    
    # Métricas principales
    acute = LoadCalculator.calculate_acute_load(sessions, days=7)
    chronic = LoadCalculator.calculate_chronic_load(sessions, days=28)
    acwr = LoadCalculator.calculate_acwr(acute, chronic)
    acwr_status, acwr_color = LoadCalculator.get_acwr_status(acwr)
    variation = LoadCalculator.calculate_weekly_variation(sessions)
    var_status, var_color = LoadCalculator.get_variation_status(variation)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("⚡ Carga Aguda (7d)", f"{acute:.0f}")
    
    with col2:
        st.metric("💪 Carga Crónica (28d)", f"{chronic:.0f}")
    
    with col3:
        emoji = "🟢" if acwr_status == "óptimo" else "🟠" if acwr_status == "vigilancia" else "🔴"
        st.metric("⚖️ ACWR", f"{acwr:.2f}", f"{emoji} {acwr_status}")
    
    with col4:
        st.metric("📈 Variación %", f"{variation:+.1f}%")
    
    with col5:
        st.metric("📊 Total Sesiones", len(sessions))
    
    st.markdown("---")
    
    # Gráfico de carga diaria
    col1, col2 = st.columns(2)
    
    with col1:
        df_sessions = pd.DataFrame([
            {
                "Fecha": datetime.fromisoformat(s["date"]).date(),
                "Carga": s["session_load"],
                "RPE": s["rpe"],
                "Minutos": s["duration_minutes"]
            }
            for s in sessions
        ])
        
        fig_daily = px.bar(
            df_sessions,
            x="Fecha",
            y="Carga",
            title=f"Carga Diaria - {selected_player_name}",
            labels={"Carga": "RPE × Minutos"},
            height=400
        )
        
        st.plotly_chart(fig_daily, use_container_width=True)
    
    with col2:
        # Tabla de sesiones
        df_table = pd.DataFrame([
            {
                "Fecha": format_date(s["date"])[:10],
                "Hora": format_date(s["date"])[11:16],
                "RPE": s["rpe"],
                "Duración": f"{s['duration_minutes']} min",
                "Carga": s["session_load"]
            }
            for s in sorted(sessions, key=lambda x: x["date"], reverse=True)[:10]
        ])
        
        st.markdown("#### Últimas 10 Sesiones")
        st.dataframe(df_table, use_container_width=True, hide_index=True)
    
    st.markdown("---")

def main():
    """Función principal del dashboard del coach"""
    initialize_coach_session()
    
    db = st.session_state.coach_db
    
    show_coach_welcome()
    
    st.write("")
    
    # Verificar si hay sesión iniciada
    if st.session_state.coach_team_id is None:
        coach_login(db)
    else:
        # Obtener equipo
        team = db.get_team_by_id(st.session_state.coach_team_id)
        
        if not team:
            st.error("❌ Equipo no encontrado")
            if st.button("🔄 Volver al login", key="back_to_login"):
                st.session_state.coach_team_id = None
                st.rerun()
            return
        
        # Crear tabs para navegación
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📊 Resumen General", "👥 Gestión de Jugadores", "📈 Análisis Detallado", "⚙️ Configuración", "🚪 Salir"]
        )
        
        with tab1:
            show_team_overview(db, team)
            show_team_metrics_table(db, team)
            show_acwr_visualization(db, team)
            show_load_evolution(db, team)
            show_automatic_recommendations(db, team)
        
        with tab2:
            st.markdown("### 👥 Gestión de Jugadores")
            st.write("")
            
            # Añadir jugador
            col1, col2 = st.columns([3, 1])
            
            with col1:
                new_player_name = st.text_input(
                    "Nombre del nuevo jugador:",
                    key="new_player_coach",
                    placeholder="Ej. Juan Pérez"
                )
            
            with col2:
                st.write("")
                if st.button("➕ Añadir", use_container_width=True, key="add_player_btn"):
                    if new_player_name.strip():
                        db.add_player_to_team(team["id"], new_player_name)
                        st.success(f"✅ '{new_player_name}' añadido al equipo")
                        st.rerun()
                    else:
                        st.error("Por favor introduce un nombre válido")
            
            st.markdown("---")
            
            # Lista de jugadores
            active_players = [p for p in team["players"] if p["active"]]
            inactive_players = [p for p in team["players"] if not p["active"]]
            
            col_active, col_inactive = st.columns(2)
            
            with col_active:
                st.markdown(f"#### ✅ Jugadores Activos ({len(active_players)})")
                
                if active_players:
                    for player in active_players:
                        sessions = db.get_player_sessions(team["id"], player["id"], days=7)
                        
                        col_name, col_sessions, col_action = st.columns([2, 1, 1])
                        
                        with col_name:
                            st.write(f"**{player['name']}**")
                        
                        with col_sessions:
                            st.write(f"Sesiones (7d): {len(sessions)}")
                        
                        with col_action:
                            if st.button("❌ Desactivar", key=f"deactivate_{player['id']}", use_container_width=True):
                                db.remove_player_from_team(team["id"], player["id"])
                                st.success(f"'{player['name']}' desactivado")
                                st.rerun()
                else:
                    st.info("No hay jugadores activos")
            
            with col_inactive:
                st.markdown(f"#### ❌ Jugadores Inactivos ({len(inactive_players)})")
                
                if inactive_players:
                    for player in inactive_players:
                        st.write(f"• {player['name']}")
                else:
                    st.info("No hay jugadores inactivos")
        
        with tab3:
            show_detailed_player_analysis(db, team)
        
        with tab4:
            st.markdown("### ⚙️ Configuración del Equipo")
            st.write("")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🔗 Acceso de Jugadores")
                st.write(f"**Código Único:** `{team['unique_code']}`")
                
                player_url = f"https://proload.coach/?code={team['unique_code']}"
                st.write(f"**URL:** {player_url}")
                
                if st.button("📋 Copiar Código", key="copy_unique_code"):
                    st.info(f"Código: {team['unique_code']}")
                
                st.markdown("---")
                
                st.markdown("#### 📱 Código QR")
                from utils import generate_qr_code
                qr_img = generate_qr_code(team['unique_code'], team['name'])
                st.image(qr_img, width=250, caption="Escanea para acceder")
            
            with col2:
                st.markdown("#### ℹ️ Información del Equipo")
                st.write(f"**Nombre:** {team['name']}")
                st.write(f"**Coach:** {team['coach_name']}")
                st.write(f"**Creado:** {format_date(team['created_date'])}")
                st.write(f"**Jugadores Activos:** {len(active_players)}")
                st.write(f"**Total Sesiones:** {len(team['sessions'])}")
                
                # Exportar datos (JSON)
                st.markdown("---")
                
                if st.button("💾 Exportar Datos (JSON)", key="export_data"):
                    json_data = json.dumps(team, indent=2, ensure_ascii=False)
                    st.download_button(
                        label="📥 Descargar JSON",
                        data=json_data,
                        file_name=f"{team['name']}_data.json",
                        mime="application/json",
                        key="download_json"
                    )
        
        with tab5:
            st.markdown("### 🚪 Sesión")
            st.write("")
            
            if st.button("Cerrar Sesión", use_container_width=True, key="logout_coach"):
                st.session_state.coach_team_id = None
                st.success("Sesión cerrada")
                st.rerun()

if __name__ == "__main__":
    main()
