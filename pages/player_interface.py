# pages/player_interface.py
"""
Interfaz exclusiva del jugador
Pantalla minimalista para registro de RPE y duración de sesión
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from database import Database
from utils import LoadCalculator, format_date

def initialize_player_session():
    """Inicializa variables de sesión del jugador"""
    if "player_db" not in st.session_state:
        st.session_state.player_db = Database()
    
    if "player_team_id" not in st.session_state:
        st.session_state.player_team_id = None
    
    if "player_id" not in st.session_state:
        st.session_state.player_id = None

def show_player_welcome():
    """Pantalla de bienvenida del jugador"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 15px; color: white; text-align: center;">
        <h1>⚽ ProLoad Player</h1>
        <p style="font-size: 18px;">Registra tu entrenamiento de hoy</p>
        <p style="font-size: 12px; opacity: 0.8;">Aplicación de Monitoreo de Carga de Entrenamiento</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info("💡 **¿Cómo funciona?**\n\n1. Introduce tu código de equipo\n2. Selecciona tu nombre\n3. Registra tu RPE y duración\n4. ¡Listo! Tus datos se envían automáticamente")

def access_player_area(db):
    """Interfaz de acceso para jugadores"""
    st.markdown("### 🔓 Acceder a mi Equipo")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        unique_code = st.text_input(
            "Código Único del Equipo:",
            placeholder="Ej. a1b2c3d4e5f6",
            key="player_code_input",
            help="Pide este código a tu preparador físico"
        )
        
        st.write("")
        
        if st.button("✅ Acceder al Equipo", use_container_width=True, key="player_access"):
            if not unique_code.strip():
                st.error("❌ Por favor introduce un código")
            else:
                team = db.get_team_by_code(unique_code.strip())
                
                if team:
                    st.session_state.player_team_id = team["id"]
                    st.session_state.current_team = team
                    st.success(f"✅ Acceso concedido al equipo '{team['name']}'")
                    st.rerun()
                else:
                    st.error("❌ Código no válido. Verifica e intenta de nuevo.")

def show_session_registration_form(db, team, player_name, player_obj):
    """Formulario de registro de sesión"""
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white;">
        <h2>⚽ {team['name']}</h2>
        <p>Hola <strong>{player_name}</strong>, registra tu sesión de hoy</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    # Layout de dos columnas
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 💪 Intensidad de tu Sesión")
        
        rpe = st.slider(
            "**RPE (Rate of Perceived Exertion)**",
            min_value=0,
            max_value=10,
            value=5,
            step=1,
            key="player_rpe_slider",
            help="Escala de 0-10 | 0=Muy suave | 5=Moderado | 10=Máximo esfuerzo"
        )
        
        # Descripción de RPE
        rpe_descriptions = {
            0: "🟢 Muy suave - Movilidad, calentamiento",
            1: "🟢 Muy suave - Calentamiento",
            2: "🟢 Suave - Recuperación activa",
            3: "🟡 Suave - Técnica, bajos intensidad",
            4: "🟡 Moderado - Trabajo técnico",
            5: "🟡 Moderado - Entrenamiento normal",
            6: "🟠 Moderado-intenso - Trabajo con demanda",
            7: "🟠 Intenso - Sesión exigente",
            8: "🔴 Muy intenso - Alta demanda",
            9: "🔴 Muy intenso - Casi máximo",
            10: "🔴 Máximo esfuerzo - Competición/Prueba"
        }
        
        st.write(f"**Tu selección:** {rpe_descriptions[rpe]}")
    
    with col2:
        st.markdown("### ⏱️ Duración de tu Sesión")
        
        duration = st.number_input(
            "**Duración (minutos)**",
            min_value=0,
            max_value=180,
            value=60,
            step=5,
            key="player_duration_input",
            help="Introduce la duración total del entrenamiento"
        )
        
        st.write(f"⏰ **Total:** {duration} minutos")
    
    st.write("")
    st.markdown("---")
    
    # Resumen de la sesión
    st.markdown("### 📊 Resumen de Tu Sesión")
    
    session_load = rpe * duration if duration > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "RPE",
            f"{rpe}/10",
            help="Intensidad percibida"
        )
    
    with col2:
        st.metric(
            "Duración",
            f"{duration} min",
            help="Tiempo total de entrenamiento"
        )
    
    with col3:
        st.metric(
            "Carga Sesión",
            f"{session_load}",
            help="RPE × Minutos = Carga de Sesión"
        )
    
    st.write("")
    st.markdown("---")
    st.write("")
    
    # Botón de envío
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button(
            "✅ REGISTRAR SESIÓN",
            use_container_width=True,
            key="submit_player_session",
            help="Envía tu datos de entrenamiento de forma segura"
        ):
            if duration == 0:
                st.error("❌ Por favor indica una duración mayor a 0 minutos")
            elif rpe == 0 and duration > 0:
                st.warning("⚠️ ¿Seguro que RPE fue 0? Verifica tu selección")
            else:
                # Registrar sesión en BD
                db.record_session(
                    team_id=st.session_state.player_team_id,
                    player_id=player_obj["id"],
                    player_name=player_name,
                    rpe=rpe,
                    duration_minutes=duration
                )
                
                # Mostrar confirmación
                st.success("✅ ¡Sesión registrada correctamente!")
                st.balloons()
                
                st.markdown(f"""
                <div style="background: #d4edda; padding: 15px; border-radius: 10px; border-left: 4px solid #00CC00;">
                    <h4>📝 Confirmación</h4>
                    <p><strong>Equipo:</strong> {team['name']}</p>
                    <p><strong>Jugador:</strong> {player_name}</p>
                    <p><strong>RPE:</strong> {rpe}/10 | <strong>Duración:</strong> {duration} min | <strong>Carga:</strong> {session_load}</p>
                    <p><strong>Hora:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                
                if st.button("📝 Registrar otra sesión", use_container_width=True, key="register_another"):
                    st.rerun()

def show_player_history(db, team_id, player_id, player_name):
    """Muestra el historial de sesiones del jugador"""
    st.markdown("---")
    st.markdown("### 📋 Tu Historial (últimos 7 días)")
    
    sessions = db.get_player_sessions(team_id, player_id, days=7)
    
    if not sessions:
        st.info("📭 No tienes sesiones registradas en los últimos 7 días")
    else:
        # Crear DataFrame
        history_data = []
        for session in sorted(sessions, key=lambda x: x["date"], reverse=True):
            session_date = datetime.fromisoformat(session["date"])
            history_data.append({
                "Fecha": session_date.strftime("%d/%m/%Y"),
                "Hora": session_date.strftime("%H:%M"),
                "RPE": session["rpe"],
                "Minutos": session["duration_minutes"],
                "Carga": session["session_load"]
            })
        
        df_history = pd.DataFrame(history_data)
        
        # Mostrar tabla
        st.dataframe(df_history, use_container_width=True, hide_index=True)
        
        # Estadísticas rápidas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Sesiones (7d)", len(sessions))
        
        with col2:
            total_minutes = sum(s["duration_minutes"] for s in sessions)
            st.metric("Total Minutos (7d)", total_minutes)
        
        with col3:
            avg_rpe = sum(s["rpe"] for s in sessions) / len(sessions)
            st.metric("RPE Promedio (7d)", f"{avg_rpe:.1f}")
        
        with col4:
            total_load = sum(s["session_load"] for s in sessions)
            st.metric("Carga Total (7d)", f"{total_load:.0f}")

def show_player_tips():
    """Consejos sobre RPE y carga de entrenamiento"""
    st.markdown("---")
    st.markdown("### 💡 ¿Cómo Evaluar tu RPE?")
    
    with st.expander("📚 Guía de RPE", expanded=False):
        st.markdown("""
        **RPE (Rate of Perceived Exertion)** es tu evaluación personal de la intensidad del entrenamiento.
        
        #### Escala de 0-10:
        
        | RPE | Descripción | Ejemplos |
        |-----|-------------|----------|
        | 0-1 | Muy suave | Movilidad, estiramientos, recuperación completa |
        | 2-3 | Suave | Calentamiento, técnica sin demanda |
        | 4-5 | Moderado | Entrenamiento técnico, trabajo táctico normal |
        | 6-7 | Moderado-Intenso | Sesión de entrenamiento completa, cambios de ritmo |
        | 8-9 | Intenso | Ejercicios de alta demanda, competición simulada |
        | 10 | Máximo | Competición real, pruebas físicas máximas |
        
        #### Tips para evaluar correctamente:
        
        ✅ Sé honesto contigo mismo - tu preparador depende de estos datos
        
        ✅ Considera:
        - Intensidad física (esfuerzo muscular)
        - Intensidad cardiovascular (respiración, ritmo cardíaco)
        - Demanda mental/táctica
        - Impacto emocional
        
        ✅ Registra DESPUÉS de la sesión, cuando aún recuerdes bien
        
        ❌ NO confundas:
        - RPE con duración (una sesión corta puede ser muy intensa)
        - RPE con número de ejercicios
        - Tu estado emocional con la intensidad real
        """)
    
    with st.expander("⏱️ Registrando la Duración", expanded=False):
        st.markdown("""
        La **duración** es el tiempo TOTAL de tu sesión de entrenamiento.
        
        #### ¿Qué incluir?
        
        ✅ Calentamiento específico
        
        ✅ Ejercicios principales
        
        ✅ Trabajo complementario
        
        ❌ NO incluir:
        - Descanso entre sesiones
        - Tiempo en vestuario/ducha
        - Viaje de ida/vuelta
        
        #### Ejemplo:
        
        - Calentamiento: 10 min
        - Trabajo técnico: 25 min
        - Ejercicios específicos: 20 min
        - Trabajo complementario: 10 min
        - **TOTAL: 65 minutos**
        """)

def show_player_dashboard(db, team, player_name, player_obj):
    """Dashboard resumido del jugador (SIN datos de compañeros)"""
    st.markdown("---")
    st.markdown("### 📊 Tu Seguimiento Personal")
    
    sessions = db.get_player_sessions(team["id"], player_obj["id"], days=28)
    
    if sessions:
        # Calcular métricas personales
        acute = LoadCalculator.calculate_acute_load(sessions, days=7)
        chronic = LoadCalculator.calculate_chronic_load(sessions, days=28)
        acwr = LoadCalculator.calculate_acwr(acute, chronic)
        
        acwr_status, acwr_color = LoadCalculator.get_acwr_status(acwr)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 4px solid #1f77b4;">
                <h4>📈 Carga Aguda (7d)</h4>
                <h2>{acute:.0f}</h2>
                <p style="font-size: 12px; color: #666;">Media móvil últimos 7 días</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 4px solid #ff9999;">
                <h4>📊 Carga Crónica (28d)</h4>
                <h2>{chronic:.0f}</h2>
                <p style="font-size: 12px; color: #666;">Media móvil últimos 28 días</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            status_emoji = "🟢" if acwr_status == "óptimo" else "🟠" if acwr_status == "vigilancia" else "🔴" if acwr_status == "peligro" else "⚪"
            status_text = "Óptimo" if acwr_status == "óptimo" else "Vigilancia" if acwr_status == "vigilancia" else "Peligro" if acwr_status == "peligro" else "Sin datos"
            
            st.markdown(f"""
            <div style="background: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 4px solid {acwr_color};">
                <h4>⚖️ Ratio ACWR</h4>
                <h2>{acwr:.2f}</h2>
                <p style="font-size: 12px; color: #666;">{status_emoji} {status_text}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Mensaje informativo sobre ACWR
        if acwr > 0:
            if acwr_status == "peligro":
                st.error("""
                🔴 **ALERTA:** Tu ratio ACWR está muy alto.
                
                Esto significa que estás siendo sobrecargado. 
                **Comunícate con tu preparador físico** para ajustar tu plan de entrenamiento.
                """)
            elif acwr_status == "vigilancia":
                st.warning("""
                🟠 **VIGILANCIA:** Tu ratio ACWR está elevado.
                
                Tu preparador está monitoreando tu carga. 
                Asegúrate de registrar correctamente tus sesiones.
                """)
            elif acwr_status == "óptimo":
                st.success("""
                🟢 **ÓPTIMO:** Tu carga de entrenamiento está correctamente balanceada.
                
                Continúa registrando tus sesiones de manera consistente.
                """)
    else:
        st.info("📭 Aún no tienes suficientes sesiones registradas para ver tu seguimiento.")
        st.info("Registra al menos una sesión para comenzar el monitoreo.")

def main():
    """Función principal de la interfaz del jugador"""
    initialize_player_session()
    
    db = st.session_state.player_db
    
    # Verificar si hay equipo seleccionado
    if "player_team_id" not in st.session_state or st.session_state.player_team_id is None:
        show_player_welcome()
        access_player_area(db)
    else:
        # Obtener equipo
        team = db.get_team_by_id(st.session_state.player_team_id)
        
        if not team:
            st.error("❌ Equipo no encontrado")
            if st.button("🔄 Volver al inicio", key="back_to_welcome"):
                st.session_state.player_team_id = None
                st.rerun()
            return
        
        # Verificar si el jugador está seleccionado
        if "player_id" not in st.session_state or st.session_state.player_id is None:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 30px; border-radius: 15px; color: white; text-align: center;">
                <h1>⚽ {team['name']}</h1>
                <p>Bienvenido, selecciona tu nombre</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            
            # Obtener jugadores activos
            active_players = [p for p in team["players"] if p["active"]]
            
            if not active_players:
                st.error("❌ No hay jugadores disponibles en este equipo")
                if st.button("🔄 Cambiar código", key="change_code"):
                    st.session_state.player_team_id = None
                    st.rerun()
            else:
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col2:
                    player_names = [p["name"] for p in active_players]
                    selected_player_name = st.selectbox(
                        "¿Cuál es tu nombre?",
                        player_names,
                        key="player_name_select",
                        help="Selecciona tu nombre de la lista"
                    )
                    
                    if st.button("✅ Continuar", use_container_width=True, key="select_player"):
                        selected_player = next(p for p in active_players if p["name"] == selected_player_name)
                        st.session_state.player_id = selected_player["id"]
                        st.session_state.player_name = selected_player_name
                        st.rerun()
        else:
            # Interfaz principal del jugador
            player_obj = next((p for p in team["players"] if p["id"] == st.session_state.player_id), None)
            
            if not player_obj:
                st.error("❌ Jugador no encontrado")
                if st.button("🔄 Seleccionar otro jugador", key="select_other_player"):
                    st.session_state.player_id = None
                    st.rerun()
            else:
                # Mostrar formulario de registro
                show_session_registration_form(db, team, st.session_state.player_name, player_obj)
                
                # Mostrar historial
                show_player_history(db, team["id"], player_obj["id"], st.session_state.player_name)
                
                # Mostrar dashboard personal
                show_player_dashboard(db, team, st.session_state.player_name, player_obj)
                
                # Mostrar tips
                show_player_tips()
                
                # Opción de cambiar jugador o equipo
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("👤 Cambiar de jugador", use_container_width=True, key="change_player"):
                        st.session_state.player_id = None
                        st.rerun()
                
                with col2:
                    if st.button("🔄 Cambiar equipo", use_container_width=True, key="change_team"):
                        st.session_state.player_team_id = None
                        st.session_state.player_id = None
                        st.rerun()
                
                with col3:
                    if st.button("🏠 Volver al inicio", use_container_width=True, key="back_to_home"):
                        st.session_state.player_team_id = None
                        st.session_state.player_id = None
                        st.rerun()

if __name__ == "__main__":
    main()
