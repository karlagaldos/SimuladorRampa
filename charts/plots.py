"""
Gráficos interactivos del simulador (Plotly).

Incluye:
    · Velocidad vs tiempo (experimental y teórica)
    · Aceleración vs ángulo (curva teórica + puntos actuales)
    · Comparación experimental vs teórica (barras)
    · Indicador de error porcentual (gauge)

Identidad de color coherente con el resto de la app:
cian = experimental, violeta = teórico.
"""

from __future__ import annotations

import math

import numpy as np
import plotly.graph_objects as go

from physics.calculations import Comparacion, Resultados
from physics.constants import ANGULO_MAX, ANGULO_MIN, GRAVEDAD, Superficie

COLOR_EXP = "#38BDF8"
COLOR_TEO = "#A78BFA"
_PLANTILLA = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(19,28,46,.6)",
    font=dict(family="Space Grotesk, sans-serif", size=13),
    margin=dict(l=40, r=20, t=50, b=40),
    hovermode="x unified",
)


def grafico_velocidad_tiempo(exp: Resultados, teo: Resultados, t_exp: float) -> go.Figure:
    """v(t) = a·t para ambos ensayos, desde el reposo hasta el final de la pista."""
    fig = go.Figure()

    a_exp = exp.get("a").valor
    t = np.linspace(0, t_exp, 60)
    fig.add_trace(go.Scatter(
        x=t, y=a_exp * t, name="Experimental",
        line=dict(color=COLOR_EXP, width=3),
        hovertemplate="t = %{x:.2f} s<br>v = %{y:.3f} m/s",
    ))

    a_teo, t_teo = teo.get("a").valor, teo.get("t").valor
    if math.isfinite(t_teo) and a_teo > 0:
        tt = np.linspace(0, t_teo, 60)
        fig.add_trace(go.Scatter(
            x=tt, y=a_teo * tt, name="Teórico",
            line=dict(color=COLOR_TEO, width=3, dash="dash"),
            hovertemplate="t = %{x:.2f} s<br>v = %{y:.3f} m/s",
        ))

    fig.update_layout(
        title="Velocidad vs tiempo", xaxis_title="Tiempo (s)",
        yaxis_title="Velocidad (m/s)", **_PLANTILLA,
    )
    return fig


def grafico_aceleracion_angulo(superficie: Superficie, angulo_actual: float,
                               a_exp: float) -> go.Figure:
    """Curva teórica a(θ) en 30–40° con los puntos actuales marcados."""
    ang = np.linspace(ANGULO_MIN, ANGULO_MAX, 100)
    rad = np.radians(ang)
    a = GRAVEDAD * (np.sin(rad) - superficie.mu * np.cos(rad))
    a = np.clip(a, 0, None)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ang, y=a, name=f"Teórica (μ = {superficie.mu})",
        line=dict(color=COLOR_TEO, width=3),
        hovertemplate="θ = %{x:.1f}°<br>a = %{y:.3f} m/s²",
    ))
    theta = math.radians(angulo_actual)
    a_teo_actual = max(0.0, GRAVEDAD * (math.sin(theta) - superficie.mu * math.cos(theta)))
    fig.add_trace(go.Scatter(
        x=[angulo_actual], y=[a_teo_actual], name="Punto teórico actual",
        mode="markers", marker=dict(color=COLOR_TEO, size=13, symbol="diamond"),
    ))
    fig.add_trace(go.Scatter(
        x=[angulo_actual], y=[a_exp], name="Punto experimental",
        mode="markers", marker=dict(color=COLOR_EXP, size=13,
                                    line=dict(color="white", width=1.5)),
    ))
    fig.update_layout(
        title="Aceleración vs ángulo de inclinación",
        xaxis_title="Ángulo θ (grados)", yaxis_title="Aceleración (m/s²)",
        **_PLANTILLA,
    )
    return fig


def grafico_comparacion(exp: Resultados, teo: Resultados, t_exp: float) -> go.Figure:
    """Barras agrupadas: aceleración, velocidad final y tiempo de bajada."""
    categorias = ["Aceleración (m/s²)", "Velocidad final (m/s)", "Tiempo (s)"]
    t_teo = teo.get("t").valor
    val_exp = [exp.get("a").valor, exp.get("v").valor, t_exp]
    val_teo = [teo.get("a").valor, teo.get("v").valor,
               t_teo if math.isfinite(t_teo) else 0]

    fig = go.Figure(data=[
        go.Bar(name="Experimental", x=categorias, y=val_exp,
               marker_color=COLOR_EXP, text=[f"{v:.3f}" for v in val_exp],
               textposition="outside"),
        go.Bar(name="Teórico", x=categorias, y=val_teo,
               marker_color=COLOR_TEO, text=[f"{v:.3f}" for v in val_teo],
               textposition="outside"),
    ])
    fig.update_layout(
        title="Comparación experimental vs teórica",
        barmode="group", **_PLANTILLA,
    )
    return fig


def indicador_error(comp: Comparacion) -> go.Figure:
    """Gauge del error porcentual en la aceleración."""
    err = comp.error_aceleracion
    err_mostrar = min(err, 100) if math.isfinite(err) else 100
    color = "#34D399" if err <= 10 else "#FBBF24" if err <= 25 else "#F87171"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=err_mostrar,
        number={"suffix": " %", "font": {"family": "JetBrains Mono"}},
        title={"text": "Error porcentual (aceleración)"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "bgcolor": "rgba(19,28,46,.6)",
            "steps": [
                {"range": [0, 10], "color": "rgba(52,211,153,.15)"},
                {"range": [10, 25], "color": "rgba(251,191,36,.15)"},
                {"range": [25, 100], "color": "rgba(248,113,113,.15)"},
            ],
        },
    ))
    fig.update_layout(height=280, **{k: v for k, v in _PLANTILLA.items()
                                     if k not in ("hovermode",)})
    return fig
