"""
Tarjetas modernas de resultados y desglose paso a paso.

Sustituyen a las tablas tradicionales: cada magnitud se presenta en una
tarjeta con ícono, nombre, fórmula, valor y unidad, y aparece con una
animación en cascada (ver styles/custom.css).
"""

from __future__ import annotations

import streamlit as st

from physics.calculations import Paso, Resultados


def tarjeta_resultado(paso: Paso, variante: str = "") -> None:
    """Renderiza una tarjeta individual. `variante`: '' | 'teorica' | 'comparacion'."""
    valor = "∞" if paso.valor == float("inf") else f"{paso.valor:.4g}"
    st.markdown(
        f"""
        <div class="tarjeta {variante}">
            <div class="encabezado">
                <span>{paso.icono} {paso.nombre}</span>
            </div>
            <div class="formula">{_latex_plano(paso.formula)}</div>
            <div><span class="valor">{valor}</span><span class="unidad">{paso.unidad}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def zona_resultados(resultados: Resultados, variante: str = "") -> None:
    """Renderiza el bloque completo de tarjetas de un ensayo."""
    for paso in resultados.pasos:
        tarjeta_resultado(paso, variante)


def pasos_detallados(resultados: Resultados) -> None:
    """Cálculos paso a paso: fórmula → sustitución → resultado → explicación."""
    for paso in resultados.pasos:
        with st.expander(f"{paso.icono} {paso.nombre} — {paso.resultado}"):
            c1, c2 = st.columns(2)
            with c1:
                st.caption("Fórmula")
                st.latex(paso.formula)
            with c2:
                st.caption("Sustitución")
                st.latex(paso.sustitucion)
            st.success(f"**Resultado:** {paso.resultado}")
            st.caption(f"💡 {paso.explicacion}")


def titulo_zona(texto: str, color: str) -> None:
    """Encabezado de zona con punto de color de identidad."""
    st.markdown(
        f"""<div class="zona-titulo">
              <span class="punto" style="background:{color}"></span>{texto}
            </div>""",
        unsafe_allow_html=True,
    )


def _latex_plano(formula: str) -> str:
    """Versión compacta de la fórmula para la tarjeta (sin renderizar LaTeX)."""
    reemplazos = {
        r"\dfrac": "", r"\sqrt": "√", r"\sin": "sin", r"\cos": "cos",
        r"\theta": "θ", r"\mu": "μ", r"\cdot": "·", r"\times": "×",
        r"\tfrac{1}{2}": "½", "{": "", "}": "", r"\,": " ", "^2": "²",
        r"\to \infty": "→ ∞", "_exp": "ₑₓₚ", "_teo": "ₜₑₒ", r"\": "",
    }
    for k, v in reemplazos.items():
        formula = formula.replace(k, v)
    return formula
