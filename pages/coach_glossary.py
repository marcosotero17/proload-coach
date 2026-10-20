# pages/coach_glossary.py
"""
Glosario completo de métricas y conceptos de ProLoad Coach
Explicaciones científicas y prácticas para el preparador físico
"""

import streamlit as st
from config import GLOSSARY

def show_glossary_header():
    """Header del glosario"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 15px; color: white; text-align: center;">
        <h1>📚 Glosario Científico - ProLoad Coach</h1>
        <p>Explicaciones completas de todas las métricas y conceptos utilizados en el sistema</p>
    </div>
    """, unsafe_allow_html=True)

def show_rpe_section():
    """Sección detallada sobre RPE"""
    with st.expander("📌 RPE (Rate of Perceived Exertion)", expanded=True):
        st.markdown("""
        ### Definición
        **RPE (Rate of Perceived Exertion)** es una escala subjetiva de 0-10 que mide la intensidad 
        percibida por el atleta durante el ejercicio. Es una herramienta simple pero poderosa para 
        monitorear la carga de entrenamiento.
        
        ### Fundamento Científico
        El RPE se basa en la percepción multisensorial del esfuerzo del atleta, incluyendo:
        
        - **Fatiga muscular:** Sensación de quemazón y fatiga muscular
        - **Demanda cardiovascular:** Ritmo cardíaco, respiración
        - **Demanda mental:** Concentración, dificultad táctica
        - **Demanda metabólica:** Acumulación de lactato, depletación de glucógeno
        
        ### Escala de 0-10
        
        | RPE | Descripción | Intensidad | Ejemplos Prácticos |
        |-----|-------------|-----------|-------------------|
        | 0-1 | Muy suave | Recuperación | Movilidad, estiramientos, paseos |
        | 2-3 | Suave | Baja | Calentamiento ligero, técnica sin contacto |
        | 4-5 | Moderado | Moderada | Entrenamiento técnico, trabajo táctico |
        | 6-7 | Moderado-Intenso | SubMaximal | Sesión completa, cambios de ritmo |
        | 8-9 | Intenso | Muy Alto | Sprints, entrenamientos competitivos |
        | 10 | Máximo | Máximo Esfuerzo | Competición oficial, pruebas físicas máximas |
        
        ### Ventajas del RPE
        
        ✅ **Fácil de usar:** Requiere solo un número del 0 al 10
        
        ✅ **Aplicable a cualquier contexto:** Funciona en campo, gimnasio, en grupo o individual
        
        ✅ **Refleja adaptación individual:** Cada jugador percibe la intensidad de forma diferente
        
        ✅ **Combina múltiples factores:** Integra factores físicos, mentales y emocionales
        
        ✅ **Rápido de registrar:** Toma solo segundos después de la sesión
        
        ### Desventajas del RPE
        
        ❌ **Subjetividad:** Depende de la percepción del atleta
        
        ❌ **Variabilidad:** El mismo esfuerzo puede percibirse diferente según el día
        
        ❌ **Necesita calibración:** Requiere educación y experiencia del jugador
        
        ❌ **Influenciable:** Puede ser afectado por estado emocional, fatiga general, etc.
        
        ### Recomendaciones Prácticas
        
        1. **Registrar DESPUÉS de la sesión:** Cuando aún recuerda bien la sensación
        
        2. **Usar la misma escala:** Establecer referentes comunes con el equipo
        
        3. **Educar a los jugadores:** Asegurar que comprenden la escala correctamente
        
        4. **Revisiones periódicas:** Comprobar que no haya "drift" en la calibración
        
        5. **Considerar contexto:** Ajustes por calor, humedad, estrés, etc.
        
        ### Correlación con otras métricas
        
        El RPE correlaciona bien con:
        - **Frecuencia cardíaca:** r = 0.8-0.9
        - **Lactato sanguíneo:** r = 0.75-0.85
        - **Consumo de oxígeno:** r = 0.80-0.90
        """)

def show_session_load_section():
    """Sección sobre Carga de Sesión"""
    with st.expander("📌 Carga de Sesión (Session Load)", expanded=False):
        st.markdown("""
        ### Definición
        **Carga de Sesión = RPE × Duración (minutos)**
        
        Es el producto del RPE y la duración de la sesión. Representa la demanda fisiológica 
        acumulada durante todo el entrenamiento.
        
        ### Fundamento Científico
        La carga de sesión integra dos dimensiones fundamentales del entrenamiento:
        
        1. **Intensidad (RPE):** Cuán demandante es la sesión
        2. **Volumen (Duración):** Cuánto tiempo dura la sesión
        
        Una sesión de alta intensidad pero corta puede tener una carga similar a una de 
        baja intensidad pero larga.
        
        ### Ejemplos de Cálculo
        
        **Ejemplo 1:**
        - RPE = 7/10
        - Duración = 60 minutos
        - Carga Sesión = 7 × 60 = **420 UA**
        
        **Ejemplo 2:**
        - RPE = 9/10
        - Duración = 40 minutos
        - Carga Sesión = 9 × 40 = **360 UA**
        
        **Ejemplo 3:**
        - RPE = 5/10
        - Duración = 75 minutos
        - Carga Sesión = 5 × 75 = **375 UA**
        
        ### Interpretación
        
        - **Baja carga (< 250 UA):** Sesiones de recuperación o técnica ligera
        - **Carga moderada (250-450 UA):** Entrenamientos normales
        - **Carga alta (> 450 UA):** Sesiones intensas o de larga duración
        
        ### Aplicación Práctica
        
        La carga de sesión permite:
        
        ✅ Cuantificar objetivamente el entrenamiento
        
        ✅ Comparar sesiones diferentes
        
        ✅ Identificar patrones de trabajo
        
        ✅ Detectar cambios en la estructura de entrenamiento
        
        ### Limitaciones
        
        ❌ No diferencia entre tipos de carga (fuerza, potencia, resistencia)
        
        ❌ No incluye impacto biomecánico
        
        ❌ Simplifica la complejidad del entrenamiento
        """)

def show_acute_chronic_section():
    """Sección sobre Carga Aguda y Crónica"""
    with st.expander("📌 Carga Aguda vs Carga Crónica", expanded=False):
        st.markdown("""
        ### Carga Aguda (Acute Workload)
        
        **Definición:** Media móvil de los últimos **7 días**
        
        **Fórmula:** Suma de cargas últimos 7 días / 7
        
        **Significado:** Refleja la carga de entrenamiento **reciente** del jugador
        
        **Rango típico:** 100-600 UA
        
        **Interpretación:**
        - Indica el estrés actual sobre el jugador
        - Cambios rápidos significan cambios en la estructura de entrenamiento
        - Aumentos súbitos pueden indicar peligro de lesión
        
        ---
        
        ### Carga Crónica (Chronic Workload)
        
        **Definición:** Media móvil de los últimos **28 días**
        
        **Fórmula:** Suma de cargas últimos 28 días / 28
        
        **Significado:** Refleja la capacidad de entrenamiento **histórica** del jugador
        
        **Rango típico:** 150-500 UA
        
        **Interpretación:**
        - Indica la adaptación general del jugador
        - Cambios lentos reflejan adaptación fisiológica
        - Base para comparar la carga aguda
        
        ---
        
        ### Relación Aguda-Crónica
        
        | Situación | Carga Aguda | Carga Crónica | Significado |
        |-----------|------------|---------------|------------|
        | Jugador bien adaptado | 300 | 300 | Equilibrio perfecto |
        | Período de sobrecarga | 500 | 300 | Adaptación en progreso |
        | Período de recuperación | 200 | 300 | Descenso controlado |
        | Insuficiencia de estímulo | 150 | 300 | Carga demasiado baja |
        | Sobrecarga extrema | 600+ | 300 | RIESGO ALTO |
        
        ### Ejemplos Prácticos
        
        **Ejemplo 1: Pretemporada**
        ```
        Semana 1: Aguda = 250, Crónica = 250 (primer día)
        Semana 2: Aguda = 350, Crónica = 280 (incremento planificado)
        Semana 3: Aguda = 420, Crónica = 310 (adaptación progresiva)
        ```
        
        **Ejemplo 2: Rehabilitación**
        ```
        Lesión: Aguda = 100, Crónica = 300 (reducción importante)
        1 semana: Aguda = 150, Crónica = 280 (reintroducción lenta)
        2 semanas: Aguda = 220, Crónica = 260 (progresión controlada)
        ```
        
        ### Utilidad Clínica
        
        ✅ **Tomar decisiones:** Aumentar, mantener o reducir carga
        
        ✅ **Detectar cambios:** Variaciones en el programa de entrenamiento
        
        ✅ **Predicción:** Anticipar riesgo de lesión basado en tendencias
        
        ✅ **Seguimiento:** Monitoreo objetivo de la capacidad del jugador
        """)

def show_acwr_section():
    """Sección detallada sobre ACWR"""
    with st.expander("📌 ACWR (Acute:Chronic Workload Ratio) - LA MÉTRICA CENTRAL", expanded=False):
        st.markdown("""
        ### Definición
        
        **ACWR = Carga Aguda / Carga Crónica**
        
        Es el ratio entre la carga de entrenamiento reciente (7 días) y la histórica (28 días).
        
        **Es la métrica más importante en ProLoad Coach para predicción de lesiones.**
        
        ---
        
        ### Fundamento Científico
        
        El ACWR se basa en el concepto de **Síndrome de Adaptación General (GAS)** de Selye y 
        la **Teoría de Estrés-Recuperación** del entrenamiento deportivo:
        
        1. **Fase de Alarma:** Cuerpo responde a nuevo estrés (entrenamiento)
        2. **Fase de Adaptación:** Cuerpo se adapta al estrés (ganancia)
        3. **Fase de Agotamiento:** Si el estrés persiste sin recuperación → LESIÓN
        
        El ACWR identifica si el jugador está en la fase 2 (óptima) o 3 (peligro).
        
        ### Cálculo Paso a Paso
        
        ```
        Día 1: RPE 5 × 60 min = 300 UA
        Día 2: RPE 6 × 45 min = 270 UA
        Día 3: RPE 7 × 60 min = 420 UA
        Día 4: RPE 5 × 50 min = 250 UA
        Día 5: RPE 8 × 40 min = 320 UA
        Día 6: Descanso = 0 UA
        Día 7: RPE 6 × 55 min = 330 UA
        
        CARGA AGUDA (7 días) = (300+270+420+250+320+0+330)/7 = 1890/7 = 270 UA
        
        CARGA CRÓNICA (28 días) = 7500/28 = 267.9 UA (aproximado)
        
        ACWR = 270 / 267.9 = 1.01
        ```
        
        ### Zonas de Riesgo
        
        #### 🟢 ZONA VERDE (0.8 - 1.3): ÓPTIMO
        
        - **Rango ideal:** ACWR entre 0.8 y 1.3
        - **Riesgo de lesión:** Bajo (2-5%)
        - **Interpretación:** El jugador está bien adaptado
        - **Acción:** Mantener programa actual
        
        **Ejemplos:**
        - ACWR 0.9: Carga reciente ligeramente reducida (recuperación controlada)
        - ACWR 1.0: Carga reciente igual a histórica (mantenimiento)
        - ACWR 1.2: Carga reciente ligeramente elevada (ligero aumento)
        
        ---
        
        #### 🟠 ZONA NARANJA (1.3 - 1.5): VIGILANCIA
        
        - **Rango de alerta:** ACWR entre 1.3 y 1.5
        - **Riesgo de lesión:** Moderado (5-20%)
        - **Interpretación:** Sobrecarga moderada, adaptación en proceso
        - **Acción:** Monitorear con frecuencia, considerar ajuste
        
        **Ejemplos:**
        - ACWR 1.35: Carga reciente 35% arriba de lo histórico
        - ACWR 1.45: Carga reciente 45% arriba de lo histórico
        
        **Recomendaciones:**
        - Revisar sesiones últimos 7 días
        - Considerar aumentar recuperación
        - Comunicar al jugador que reduzca volumen volitivamente
        - Revisar en 2-3 días
        
        ---
        
        #### 🔴 ZONA ROJA (> 1.5): PELIGRO CRÍTICO
        
        - **Rango crítico:** ACWR > 1.5
        - **Riesgo de lesión:** Alto (20-50%)
        - **Interpretación:** Sobrecarga severa, muy alto riesgo
        - **Acción:** Intervención inmediata
        
        **Ejemplos:**
        - ACWR 1.6: Carga reciente 60% arriba de lo histórico (CRÍTICO)
        - ACWR 2.0: Carga reciente 100% arriba de lo histórico (EXTREMO)
        
        **Acciones Recomendadas:**
        1. **Reunión inmediata** con jugador
        2. **Revisar en profundidad** los últimos 7 días
        3. **Reducir carga** de forma significativa (30-50%)
        4. **Aumentar recuperación:** Más descanso, masaje, crioterapia
        5. **Vigilancia diaria** de síntomas de lesión
        6. **Evaluaciones físicas** más frecuentes
        7. **Comunicar al equipo médico** de forma inmediata
        
        ---
        
        ### Ejemplos de Intervención
        
        **Caso 1: ACWR Óptimo (0.95)**
        ```
        Semana anterior: 280 UA
        Semana actual: 266 UA
        ACWR = 0.95
        
        ✅ ACCIÓN: Continuar programa normal
        Hipótesis: Semana más ligera (descanso extra, recuperación)
        ```
        
        **Caso 2: ACWR Vigilancia (1.4)**
        ```
        Semana anterior: 300 UA
        Semana actual: 420 UA
        ACWR = 1.4
        
        ⚠️ ACCIÓN: Revisar sesiones, considerar reducción
        Hipótesis: Dos sesiones de alta intensidad seguidas
        Plan: Reducir próxima sesión a RPE 4-5, más descanso
        ```
        
        **Caso 3: ACWR Crítico (1.65)**
        ```
        Semana anterior: 280 UA
        Semana actual: 462 UA
        ACWR = 1.65
        
        🔴 ACCIÓN: Intervención inmediata
        Hipótesis: Entrenamiento no planificado + competición + recuperación insuficiente
        Plan: 
        - Reducción del 40-50% en próxima sesión
        - Implementar protocolo de recuperación intensivo
        - Comunicar al médico del equipo
        - Reevaluar en 48 horas
        ```
        
        ### Factores que Afectan al ACWR
        
        **Aumentan ACWR (lo elevan):**
        - ⬆️ Aumento repentino de intensidad
        - ⬆️ Aumento repentino de volumen
        - ⬆️ Acumulación de competiciones
        - ⬆️ Estrés adicional (académico, personal, profesional)
        - ⬆️ Sueño insuficiente
        - ⬆️ Nutrición pobre
        
        **Reducen ACWR (lo bajan):**
        - ⬇️ Reducción deliberada de carga
        - ⬇️ Períodos de recuperación/descanso
        - ⬇️ Estabilización de carga
        - ⬇️ Mejoría de sueño/recuperación
        - ⬇️ Recuperación pasiva (no entrenar)
        
        ### Limitaciones del ACWR
        
        ❌ No diferencia tipos de carga (fuerza vs. resistencia)
        
        ❌ No considera impacto biomecánico del deporte
        
        ❌ No incluye factores de recuperación (sueño, nutrición)
        
        ❌ Puede enmascarar problemas agudos por lesión
        
        ❌ ACWR bajo no garantiza ausencia de lesión
        
        ### Investigación Reciente
        
        Estudios recientes de Gabbett et al. (2016) y Hulin et al. (2016) demuestran:
        
        - ACWR > 1.5 aumenta riesgo de lesión 4-6 veces
        - ACWR < 0.8 puede indicar insuficiencia de estimulo
        - La combinación de ACWR + síntomas es más predictiva que ACWR solo
        - Grandes cambios semana a semana (>10%) son riesgosos incluso si ACWR es bajo
        """)

def show_variation_section():
    """Sección sobre Variación Semanal"""
    with st.expander("📌 Variación Semanal (% Variation)", expanded=False):
        st.markdown("""
        ### Definición
        
        **Variación % = ((Carga Semana Actual - Carga Semana Anterior) / Carga Semana Anterior) × 100**
        
        Mide el cambio porcentual en la carga de entrenamiento de una semana a otra.
        
        ### Significado
        
        Indica **cuán rápido cambia** la carga de entrenamiento. Cambios muy rápidos (positivos 
        o negativos) son factores de riesgo independientes.
        
        ### Zonas de Variación
        
        #### 🟢 ÓPTIMO (0% - 10%)
        - Cambio apropiado week-to-week
        - Progresión gradual y segura
        - Permite adaptación fisiológica
        
        #### 🟠 VIGILANCIA (10% - 20%)
        - Cambio importante pero tolerable
        - Requiere monitoreo
        - Puede ser planificado (deload, tapering)
        
        #### 🔴 PELIGRO (> 20%)
        - Cambio muy rápido
        - Alto riesgo de lesión
        - Requiere intervención inmediata
        
        ### Ejemplos
        
        **Ejemplo 1: Variación Positiva Óptima**
        ```
        Semana anterior: 2000 UA
        Semana actual: 2150 UA
        Variación = ((2150 - 2000) / 2000) × 100 = +7.5%
        
        ✅ Aumento progresivo y controlado
        ```
        
        **Ejemplo 2: Variación Negativa Excesiva**
        ```
        Semana anterior: 2000 UA
        Semana actual: 1500 UA
        Variación = ((1500 - 2000) / 2000) × 100 = -25%
        
        🔴 Reducción demasiado rápida (por lesión, enfermedad, etc.)
        ```
        
        ### Recomendaciones Prácticas
        
        **Para aumentar carga:**
        - Máximo 10% de aumento semanal
        - Máximo 15% en períodos de adaptación planificada
        
        **Para reducir carga:**
        - Máximo 15% de reducción controlada
        - Reducciones mayores solo si es necesario (lesión, enfermedad)
        
        ### Relación con ACWR
        
        La variación semanal es complementaria al ACWR:
        
        - **ACWR:** Mide la carga reciente vs histórica (últimos 7 vs 28 días)
        - **Variación:** Mide cambio semana a semana (7 días vs 7 días anteriores)
        
        Un ACWR alto + variación alta = RIESGO MÁS CRÍTICO
        """)

def show_injury_risk_section():
    """Sección sobre Riesgo de Lesión"""
    with st.expander("📌 Predicción de Riesgo de Lesión", expanded=False):
        st.markdown("""
        ### Modelo de Riesgo de Lesión en ProLoad Coach
        
        El sistema utiliza múltiples indicadores para estimar riesgo:
        
        ### Factor 1: ACWR (Peso: 50%)
        
        ```
        ACWR < 0.8     → Riesgo bajo (2-3%)
        ACWR 0.8-1.3   → Riesgo óptimo (2-5%)
        ACWR 1.3-1.5   → Riesgo moderado (5-15%)
        ACWR > 1.5     → Riesgo alto (20-50%)
        ```
        
        ### Factor 2: Variación Semanal (Peso: 30%)
        
        ```
        -10% a +10%    → Riesgo bajo
        -20% a -10% o +10% a +20% → Riesgo moderado
        > 20% o < -20% → Riesgo alto
        ```
        
        ### Factor 3: Carga Crónica Absoluta (Peso: 20%)
        
        ```
        < 100 UA       → Insuficiente estímulo
        100-200 UA     → Bajo (sedentario)
        200-400 UA     → Óptimo (entrenamiento normal)
        400-600 UA     → Alto (entrenamiento intenso)
        > 600 UA       → Muy alto (elite o riesgo de sobreentrenamiento)
        ```
        
        ### Matriz de Riesgo Integrada
        
        | ACWR | Variación | Riesgo General |
        |------|-----------|---|
        | Óptimo | Óptima | 🟢 BAJO (2-5%) |
        | Óptimo | Moderada | 🟡 BAJO-MODERADO (5-10%) |
        | Vigilancia | Óptima | 🟡 MODERADO (8-15%) |
        | Vigilancia | Moderada | 🟠 MODERADO-ALTO (15-25%) |
        | Vigilancia | Alta | 🔴 ALTO (25-40%) |
        | Crítico | Cualquiera | 🔴 MUY ALTO (>40%) |
        
        ### Protocolos de Intervención
        
        **Riesgo Bajo (2-5%)**
        - ✅ Continuar programa normal
        - ✅ Monitoreo rutinario
        
        **Riesgo Moderado (5-25%)**
        - ⚠️ Revisar carga de últimos 7 días
        - ⚠️ Aumentar frecuencia de check-ins
        - ⚠️ Preparar reducción controlada si es necesario
        - ⚠️ Evaluar factores de recuperación
        
        **Riesgo Alto (25-40%)**
        - 🔴 Intervención inmediata
        - 🔴 Reducción 30-40% de carga
        - 🔴 Protocolo intensivo de recuperación
        - 🔴 Comunicar al equipo médico
        - 🔴 Evaluación diaria de síntomas
        
        **Riesgo Muy Alto (>40%)**
        - 🔴 CRISIS: Reduce 50% o más
        - 🔴 Descanso completo si es posible
        - 🔴 Evaluación médica inmediata
        - 🔴 Monitoreo cada 12 horas
        """)

def show_anthropometry_section():
    """Sección sobre Antropometría"""
    with st.expander("📌 Medidas Antropométricas", expanded=False):
        st.markdown("""
        ### Componentes Principales
        
        #### Peso (kg)
        - Medida: Báscula digital (preferiblemente digital)
        - Momento: Mañana, en ayunas, después de vaciar vejiga
        - Variación normal: ±0.5-1 kg día a día
        - Aplicación: Detectar cambios en masa corporal
        
        #### Talla/Altura (cm)
        - Medida: Tallímetro (no cinta métrica)
        - Momento: Mañana, sin calzado
        - Variación: Puede variar 0.5-1 cm diarios (deshidratación/compresión)
        - Aplicación: Base para índices (IMC, etc.)
        
        #### Pliegues de Grasa (mm)
        
        **Pliegues comunes:**
        - **Tríceps:** Atrás del brazo
        - **Bíceps:** Adelante del brazo
        - **Subescapular:** Bajo escápula
        - **Suprailíaco:** Por encima cadera
        - **Abdominal:** Al lado ombligo
        - **Muslo anterior:** Cuádriceps
        - **Pantorrilla medial:** Pantorrilla
        
        **Medición:**
        - Usar plicómetro calibrado
        - Realizar 2-3 mediciones por sitio
        - Usar promedio
        - Mismo evaluador (importante)
        - Mismo lado corporal
        
        **Ecuaciones de % Grasa:**
        
        Jackson & Pollock (7 pliegues):
        ```
        Hombres: Densidad = 1.112 - (0.00043499 × Σ7 pliegues) + (0.00000055 × Σ7²) - (0.00028826 × Edad)
        Mujeres: Densidad = 1.097 - (0.00046971 × Σ7 pliegues) + (0.00000056 × Σ7²) - (0.00012828 × Edad)
        % Grasa = (495 / Densidad) - 450
        ```
        
        ### Interpretación en Deportistas
        
        | Población | % Grasa Óptimo |
        |-----------|---|
        | Futbolistas | 8-12% |
        | Jugadores de Baloncesto | 7-14% |
        | Jugadores de Rugby | 10-16% |
        | Atletas de Resistencia | 6-10% |
        | Media Población | 15-25% |
        
        ### Cambios a Monitorear
        
        ✅ **Cambios positivos:**
        - Reducción de % grasa (15 → 12%) = mejor forma
        - Aumento de peso con mismo % grasa = ganancia muscular
        
        ❌ **Cambios de alerta:**
        - Aumento de % grasa rápido = posible sobrentrenamiento
        - Pérdida de peso rápida = deshidratación o pérdida muscular
        - Cambios erráticos = problemas de recuperación/nutrición
        """)

def show_performance_tests_section():
    """Sección sobre Tests de Rendimiento"""
    with st.expander("📌 Tests de Rendimiento Físico", expanded=False):
        st.markdown("""
        ### CMJ (Countermovement Jump)
        
        #### Descripción
        Salto vertical máximo desde una posición de pie, con movimiento previo de piernas.
        
        #### Protocolo
        1. De pie, pies separados a ancho de hombros
        2. Balanceo de brazos hacia atrás
        3. Descenso rápido (100-200ms) hasta flexión máxima
        4. Salto explosivo hacia arriba
        5. Medir altura máxima alcanzada
        
        #### Medidas
        - **Altura (cm):** Distancia en centímetros
        - **Potencia (watts):** Calculada a partir de altura y peso
        
        **Cálculo de Potencia:**
        ```
        Altura en metros = h
        Potencia (watts) = (20.4 × peso [kg] × √(altura [m])) + 51
        ```
        
        #### Interpretación
        
        **Futbolista profesional:**
        - Excelente: > 60 cm
        - Bueno: 50-60 cm
        - Medio: 40-50 cm
        - Bajo: < 40 cm
        
        #### Aplicación
        - Indicador de potencia explosiva
        - Muy sensible a fatiga
        - Buen predictor de capacidad neuromuscular
        - Cambios rápidos indican recuperación/fatiga
        
        #### Variabilidad
        - Día a día: ±5-8% variación normal
        - Fatiga acuda: -10-15%
        - Sobrentrenamiento crónico: -15-20%
        
        ---
        
        ### Test de Buchheit (30-15 IFT)
        
        #### Descripción
        Test de resistencia anaeróbica repetida. El jugador realiza esprints de 40 metros 
        con recuperaciones incompletas.
        
        #### Protocolo
        1. 6-8 sprints de 40 metros
        2. Inicio cada 45 segundos
        3. Velocidad aumenta cada sprint
        4. Se continúa hasta que no se puede mantener ritmo
        
        #### Medidas Principales
        - **Velocidad máxima (km/h):** Velocidad alcanzada en último sprint
        - **Decrement Index (%):** Ralentización progresiva
        
        **Cálculo de Decrement:**
        ```
        Decrement (%) = ((Tiempo promedio lento / Tiempo promedio rápido) - 1) × 100
        ```
        
        #### Interpretación
        
        **Capacidad de cambios de ritmo:**
        - Excelente: Velocidad máxima > 18 km/h
        - Bueno: 17-18 km/h
        - Medio: 16-17 km/h
        - Bajo: < 16 km/h
        
        **Tolerancia a la fatiga:**
        - Bueno: Decrement < 5%
        - Aceptable: 5-10%
        - Pobre: > 10%
        
        #### Aplicación
        - Evalúa potencia repetida
        - Detecta fatiga acumulativa
        - Predice rendimiento en competición
        - Muy relevante para deportes colectivos
        
        ---
        
        ### Test Yo-Yo (Intermittent Recovery Test)
        
        #### Descripción
        Test de resistencia aeróbica con recuperación activa. Carreras de 20 metros 
        intercaladas con períodos de recuperación caminando.
        
        #### Niveles
        - **Nivel 1 (Básico):** Velocidad baja, recuperación
        - **Nivel 2 (Intermedio):** Velocidad moderada-alta
        
        #### Medidas
        - **Distancia total:** Metros recorridos antes del agotamiento
        - **Velocidad final:** km/h en último shuttle
        
        #### Interpretación
        
        | Distancia | Capacidad Aeróbica |
        |-----------|---|
        | > 2800 m | Excelente |
        | 2400-2800 m | Muy Bueno |
        | 2000-2400 m | Bueno |
        | 1600-2000 m | Medio |
        | < 1600 m | Bajo |
        
        #### Aplicación
        - Capacidad aeróbica sostenida
        - Fatiga más acumulativa
        - Cambios lentos pero más estables
        - Mejor para seguimiento de forma general
        
        ### Comparación de Tests
        
        | Aspecto | CMJ | Buchheit | Yo-Yo |
        |--------|-----|---------|-------|
        | Rapidez de cambio | Muy rápida | Rápida | Lenta |
        | Sensibilidad a fatiga | Alta | Muy Alta | Media |
        | Facilidad de realizar | Muy fácil | Fácil | Difícil |
        | Especificidad fútbol | Alta | Muy Alta | Alta |
        | Necesidad de equipo | Mínima | Mínima | Pista 20m |
        """)

def show_recommendations_section():
    """Sección sobre Recomendaciones"""
    with st.expander("📌 Recomendaciones de Intervención", expanded=False):
        st.markdown("""
        ### Protocolo de Decisión del Coach
        
        #### Paso 1: Revisar Métricas Actuales
        - ✅ ACWR (ratio actual)
        - ✅ Variación semanal (%)
        - ✅ Carga crónica (capacidad)
        - ✅ Tendencia (creciente/decreciente)
        
        #### Paso 2: Clasificar Riesgo
        ```
        ACWR < 0.8          → Riesgo BAJO (bajo estímulo)
        ACWR 0.8-1.3        → Riesgo ÓPTIMO (mantener)
        ACWR 1.3-1.5        → Riesgo MODERADO (vigilar)
        ACWR > 1.5          → Riesgo ALTO (intervenir)
        ```
        
        #### Paso 3: Tomar Acción
        
        **Si ACWR Óptimo (0.8-1.3):**
        - ✅ Mantener programa
        - ✅ Revisar en 1 semana
        - ✅ Continuar monitoreo rutinario
        
        **Si ACWR Moderado (1.3-1.5):**
        - ⚠️ Reunión con jugador
        - ⚠️ Revisar últimos 7 días
        - ⚠️ Planificar reducción 10-15%
        - ⚠️ Aumentar recuperación
        - ⚠️ Revisar en 2-3 días
        
        **Si ACWR Crítico (>1.5):**
        - 🔴 Acción inmediata
        - 🔴 Reducir carga 30-50%
        - 🔴 Protocolo de recuperación intensivo
        - 🔴 Comunicar al equipo médico
        - 🔴 Evaluación diaria
        - 🔴 Revisar en 24-48 horas
        
        ### Ejemplo de Plan de Acción
        
        **Escenario: Jugador con ACWR 1.65**
        
        **Día 1 (Identificación):**
        - Revisar datos, confirmar ACWR alto
        - Contactar con jugador
        - Evaluar síntomas (dolor, fatiga, rigidez)
        
        **Día 2-3 (Intervención):**
        - Reducir entrenamiento 40% (RPE más bajo)
        - Sesión de recuperación: movilidad + estiramientos
        - Aumentar sueño (9+ horas)
        - Masaje/tratamiento miofascial
        
        **Día 4-5 (Seguimiento):**
        - Nueva medición (si es posible)
        - Verificar síntomas desaparecen
        - Aumento gradual de carga (5-10% por día)
        
        **Día 7 (Evaluación):**
        - Calcular nuevo ACWR
        - Decidir si continuar progresión o mantener
        
        ### Factores Adicionales a Considerar
        
        Más allá de la carga cuantitativa:
        
        ✅ **Síntomas subjetivos:**
        - Dolor muscular
        - Fatiga generalizada
        - Cambios de humor
        - Calidad de sueño
        - Apetito
        
        ✅ **Factores de recuperación:**
        - Horas de sueño
        - Calidad del sueño
        - Nutrición (especialmente proteína y carbohidratos)
        - Hidratación
        - Estrés personal/académico
        
        ✅ **Historial de lesiones:**
        - Lesiones previas (aumentan riesgo)
        - Zonas débiles (monitor especial)
        - Tiempo desde última lesión
        
        ✅ **Contexto competitivo:**
        - Competiciones próximas
        - Períodos de temporada
        - Viajes/cambios de zona horaria
        """)

def main():
    """Función principal del glosario"""
    show_glossary_header()
    
    st.write("")
    st.markdown("---")
    st.write("")
    
    # Tabs para organizar
    tab1, tab2, tab3 = st.tabs(["📚 Conceptos Fundamentales", "📊 Métricas de Carga", "🎯 Aplicación Práctica"])
    
    with tab1:
        st.markdown("## Conceptos Clave")
        show_rpe_section()
        show_session_load_section()
        show_acute_chronic_section()
    
    with tab2:
        st.markdown("## Métricas Principales")
        show_acwr_section()
        show_variation_section()
        show_injury_risk_section()
    
    with tab3:
        st.markdown("## Evaluación y Tests")
        show_anthropometry_section()
        show_performance_tests_section()
        show_recommendations_section()
    
    st.write("")
    st.markdown("---")
    st.write("")
    
    # Footer
    st.markdown("""
    <div style="background: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center;">
        <p><strong>ProLoad Coach v1.0</strong></p>
        <p style="font-size: 12px;">Sistema inteligente de monitoreo de carga de entrenamiento basado en ciencia</p>
        <p style="font-size: 11px; color: #666;">
        Basado en investigación científica de Gabbett (2016), Hulin (2016), Soligard (2016) y Bourdon (2017)
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
