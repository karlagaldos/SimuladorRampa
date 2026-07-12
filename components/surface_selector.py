"""
Selector de superficies mediante tarjetas seleccionables.

Cada tarjeta muestra una textura CSS distinta (mica, arena, madera).
La superficie activa se resalta con borde y brillo. Se evita el uso
de listas desplegables, según los requisitos de diseño.
"""

from __future__ import annotations

import streamlit as st

from physics.constants import SUPERFICIES, Superficie


def selector_superficie() -> Superficie:
    """Renderiza las tarjetas y devuelve la superficie seleccionada."""
    if "superficie" not in st.session_state:
        st.session_state.superficie = "mica"

    for clave, sup in SUPERFICIES.items():
        activa = "activa" if st.session_state.superficie == clave else ""
        st.markdown(
            f"""
            <div class="tarjeta-superficie {activa}">
                <div class="textura" style="background:{sup.textura_css}"></div>
                <div class="info">
                    <b>{sup.icono} {sup.nombre}</b><br>
                    <span>{sup.descripcion} · μ = {sup.mu}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "✓ Seleccionada" if activa else "Seleccionar",
            key=f"btn_{clave}",
            use_container_width=True,
            type="primary" if activa else "secondary",
            disabled=bool(activa),
        ):
            st.session_state.superficie = clave
            st.rerun()

    return SUPERFICIES[st.session_state.superficie]
