"""
Simulador del Movimiento de un Carrito sobre un Plano Inclinado
────────────────────────────────────────────────────────────────
Laboratorio virtual de Física: compara los resultados experimentales
(cronometrados en el laboratorio) con las predicciones teóricas del
modelo de plano inclinado con fricción cinética.

Ejecución local:
    streamlit run app.py
"""

from __future__ import annotations

import math
from pathlib import Path

import streamlit as st

from charts.plots import (grafico_aceleracion_angulo, grafico_comparacion,
                          grafico_velocidad_tiempo, indicador_error)
from components.cards import pasos_detallados, titulo_zona, zona_resultados
from components.free_body_diagram import render_dcl
from components.simulation import render_simulacion
from components.surface_selector import selector_superficie
from physics.calculations import calcular_experimental, calcular_teorico, comparar
from physics.constants import (ANGULO_DEFECTO, ANGULO_MAX, ANGULO_MIN,
                               GRAVEDAD, LONGITUD_M, MASA_KG)
from utils.observations import generar_observaciones

# ══════════════════════════════════════════════════════════════
#  Configuración de página y estilos
# ══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Simulador · Plano Inclinado",
    page_icon="🛗",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"<style>{Path('styles/custom.css').read_text(encoding='utf-8')}</style>",
    unsafe_allow_html=True,
)


def color_angulo(angulo: int) -> str:
    """Color del indicador según el ángulo (heredado del diseño original)."""
    if angulo <= 33:
        return "#38BDF8"   # Azul
    if angulo <= 36:
        return "#34D399"   # Verde
    if angulo <= 38:
        return "#FB923C"   # Naranja
    return "#F87171"       # Rojo


# ══════════════════════════════════════════════════════════════
#  Barra lateral: panel de control del ensayo
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🎛️ Panel de control")
    st.caption("Configura las condiciones del ensayo")

    # Datos constantes
    st.markdown("#### Datos constantes")
    c1, c2 = st.columns(2)
    c1.metric("Masa", f"{MASA_KG*1000:.0f} g")
    c2.metric("Pista", f"{LONGITUD_M*100:.0f} cm")
    st.metric("Gravedad", f"{GRAVEDAD} m/s²")

    st.divider()

    # Ángulo
    st.markdown("#### 📐 Ángulo de inclinación")
    angulo = st.slider("Ángulo (°)", ANGULO_MIN, ANGULO_MAX, ANGULO_DEFECTO,
                       step=1, label_visibility="collapsed",
                       help="Inclinación de la rampa entre 30° y 40°")
    st.markdown(
        f'<div class="valor-angulo" style="color:{color_angulo(angulo)}">{angulo}°</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    # Superficie (tarjetas seleccionables)
    st.markdown("#### 🧱 Superficie de la pista")
    superficie = selector_superficie()

    st.divider()

    # Tiempo experimental
    st.markdown("#### ⏱️ Tiempo experimental")
    t_exp = st.number_input(
        "Tiempo medido (s)", min_value=0.05, max_value=10.0,
        value=0.45, step=0.01, format="%.2f",
        help="Tiempo cronometrado en el laboratorio para recorrer los 37 cm",
    )

    calcular = st.button("▶️ Calcular y simular", type="primary",
                         use_container_width=True)
    if calcular:
        st.session_state.calculado = True

calculado: bool = st.session_state.get("calculado", False)

# ══════════════════════════════════════════════════════════════
#  Encabezado
# ══════════════════════════════════════════════════════════════

st.markdown(
    """
    <p class="titulo-app">🛗 Simulador · Carrito sobre Plano Inclinado</p>
    <p class="subtitulo-app">Laboratorio virtual de Física ·
    comparación entre resultados experimentales y teóricos</p>
    """,
    unsafe_allow_html=True,
)
st.write("")

# ══════════════════════════════════════════════════════════════
#  Cálculos
# ══════════════════════════════════════════════════════════════

exp = calcular_experimental(angulo, t_exp)
teo = calcular_teorico(angulo, superficie)
comp = comparar(exp, teo, superficie)

# ══════════════════════════════════════════════════════════════
#  Zonas principales: simulación | experimental | teórico
# ══════════════════════════════════════════════════════════════

zona_izq, zona_centro, zona_der = st.columns([1.35, 1, 1], gap="large")

with zona_izq:
    titulo_zona("🔬 Simulación", "#34D399")
    render_simulacion(angulo, superficie, animar=calcular, duracion_s=t_exp)
    if calcular:
        st.toast(f"Simulando bajada de {t_exp:.2f} s", icon="🚀")

    titulo_zona("🧭 Diagrama de cuerpo libre", "#F87171")
    render_dcl(angulo, superficie)
    st.caption("Las flechas se escalan con la magnitud real de cada fuerza "
               "y se actualizan al cambiar el ángulo o la superficie.")

with zona_centro:
    titulo_zona("🧪 Resultados experimentales", "#38BDF8")
    if calculado:
        zona_resultados(exp)
    else:
        st.info("Configura el ensayo y presiona **Calcular y simular** "
                "para obtener los resultados.", icon="👈")

with zona_der:
    titulo_zona("📘 Resultados teóricos", "#A78BFA")
    if calculado:
        zona_resultados(teo, variante="teorica")
    else:
        st.info("Los resultados teóricos usan el μ de referencia de la "
                "superficie seleccionada.", icon="📖")

# ══════════════════════════════════════════════════════════════
#  Comparación, gráficos, pasos y observaciones
# ══════════════════════════════════════════════════════════════

if calculado:
    st.divider()
    titulo_zona("⚖️ Comparación entre ensayos", "#FBBF24")

    m1, m2, m3, m4 = st.columns(4)
    err_a = comp.error_aceleracion
    m1.metric("Error en aceleración",
              f"{err_a:.1f} %" if math.isfinite(err_a) else "—",
              help="Error porcentual relativo respecto al valor teórico")
    m2.metric("Error en velocidad",
              f"{comp.error_velocidad:.1f} %" if math.isfinite(comp.error_velocidad) else "—")
    m3.metric("μ experimental vs teórico",
              f"{comp.mu_exp:.3f} / {comp.mu_teo:.2f}",
              delta=f"{comp.mu_exp - comp.mu_teo:+.3f}")
    m4.metric("Energía disipada",
              f"{comp.dif_energia*1000:.2f} mJ",
              help="Ep − Ec experimental: energía perdida por fricción")

    st.write("")
    tab_graf, tab_pasos, tab_obs = st.tabs(
        ["📊 Gráficos interactivos", "🧮 Cálculos paso a paso", "🔎 Observaciones"]
    )

    with tab_graf:
        g1, g2 = st.columns(2)
        with g1:
            st.plotly_chart(grafico_velocidad_tiempo(exp, teo, t_exp),
                            use_container_width=True)
            st.plotly_chart(grafico_comparacion(exp, teo, t_exp),
                            use_container_width=True)
        with g2:
            st.plotly_chart(
                grafico_aceleracion_angulo(superficie, angulo, exp.get("a").valor),
                use_container_width=True)
            st.plotly_chart(indicador_error(comp), use_container_width=True)

    with tab_pasos:
        p1, p2 = st.columns(2)
        with p1:
            st.markdown("##### 🧪 Ensayo experimental")
            pasos_detallados(exp)
        with p2:
            st.markdown("##### 📘 Ensayo teórico")
            pasos_detallados(teo)

    with tab_obs:
        st.markdown("##### Conclusiones automáticas del sistema")
        for o in generar_observaciones(comp, superficie, angulo):
            st.markdown(f'<span class="badge-obs badge-{o.nivel}">{o.texto}</span>',
                        unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  Pie de página
# ══════════════════════════════════════════════════════════════

st.divider()
st.caption(
    "Modelo: cinemática con fricción cinética, partiendo del reposo · "
    "a_exp = 2L/t² · a_teo = g(sinθ − μcosθ) · "
    "Los coeficientes μ son valores de referencia y pueden calibrarse en "
    "`physics/constants.py`."
)
