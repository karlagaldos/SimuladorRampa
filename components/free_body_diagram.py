"""
Diagrama de cuerpo libre (DCL) del carrito.

Muestra únicamente las tres fuerzas del enunciado:
    · Peso (W = m·g)               → vertical hacia abajo
    · Normal (N = m·g·cosθ)        → perpendicular al plano
    · Fricción (f = μ·N)           → paralela al plano, hacia arriba

Las longitudes de las flechas se escalan con la magnitud real de cada
fuerza, de modo que el diagrama se actualiza automáticamente al cambiar
el ángulo o la superficie.
"""

from __future__ import annotations

import math

import streamlit.components.v1 as components

from physics.constants import GRAVEDAD, MASA_KG, Superficie

W, H = 460, 260
CX, CY = W // 2, H // 2 + 8   # Centro del cuerpo


def _flecha(x1: float, y1: float, x2: float, y2: float,
            color: str, etiqueta: str, valor_n: float,
            desplaz_txt=(8, 0)) -> str:
    """Genera una flecha SVG con etiqueta y magnitud en newtons."""
    tx, ty = x2 + desplaz_txt[0], y2 + desplaz_txt[1]
    return f"""
        <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"
              stroke="{color}" stroke-width="3.5" marker-end="url(#punta-{color.strip('#')})"
              class="fuerza"/>
        <text x="{tx:.1f}" y="{ty:.1f}" fill="{color}" font-size="13" font-weight="bold">{etiqueta}</text>
        <text x="{tx:.1f}" y="{ty+14:.1f}" fill="{color}" font-size="10.5"
              font-family="monospace">{valor_n*1000:.1f} mN</text>
    """


def render_dcl(angulo_deg: float, superficie: Superficie, altura: int = H + 10) -> None:
    """Dibuja el DCL con Peso, Normal y Fricción (sin la componente paralela)."""
    theta = math.radians(angulo_deg)
    m, g, mu = MASA_KG, GRAVEDAD, superficie.mu

    peso = m * g
    normal = m * g * math.cos(theta)
    friccion = mu * normal

    # Escala: el peso (fuerza mayor) mide 95 px
    escala = 95 / peso
    l_peso, l_norm, l_fric = peso * escala, normal * escala, friccion * escala

    # Direcciones (el plano sube hacia la izquierda):
    #   normal → perpendicular al plano
    #   fricción → paralela al plano, hacia arriba (opuesta al movimiento)
    nx, ny = math.sin(theta), -math.cos(theta)
    fx, fy = -math.cos(theta), -math.sin(theta)

    colores = {"peso": "#F87171", "normal": "#38BDF8", "friccion": "#FBBF24"}
    puntas = "".join(
        f"""<marker id="punta-{c.strip('#')}" markerWidth="9" markerHeight="9"
                    refX="7" refY="3.5" orient="auto">
                <path d="M0,0 L8,3.5 L0,7 Z" fill="{c}"/>
            </marker>"""
        for c in colores.values()
    )

    html = f"""
    <style>
        .fuerza {{ transition: all .5s ease; }}
    </style>
    <svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg"
         style="font-family:'Space Grotesk',sans-serif;">
        <defs>{puntas}</defs>

        <!-- Línea del plano inclinado (misma orientación que la simulación:
             desciende de izquierda a derecha) -->
        <line x1="{CX-120*math.cos(theta):.1f}" y1="{CY-120*math.sin(theta):.1f}"
              x2="{CX+120*math.cos(theta):.1f}" y2="{CY+120*math.sin(theta):.1f}"
              stroke="#3B4A6E" stroke-width="2" stroke-dasharray="6 4"/>

        <!-- Cuerpo (carrito como partícula) -->
        <g transform="rotate({angulo_deg:.1f} {CX} {CY})">
            <rect x="{CX-22}" y="{CY-16}" width="44" height="16" rx="4"
                  fill="#EAF2FF" stroke="#38BDF8" stroke-width="2"/>
        </g>

        <!-- Peso: vertical hacia abajo -->
        {_flecha(CX, CY, CX, CY + l_peso, colores['peso'], "W = mg", peso, (10, -4))}

        <!-- Normal: perpendicular al plano -->
        {_flecha(CX, CY - 8, CX + l_norm * nx, CY - 8 + l_norm * ny,
                 colores['normal'], "N", normal, (8, -6))}

        <!-- Fricción: paralela al plano, hacia arriba -->
        {_flecha(CX, CY - 8, CX + l_fric * fx, CY - 8 + l_fric * fy,
                 colores['friccion'], "f = μN", friccion, (-70, -8))}

        <text x="14" y="22" fill="#8CA0C4" font-size="12">
            Diagrama de cuerpo libre · θ = {angulo_deg:.0f}° · μ = {mu}
        </text>
    </svg>
    """
    components.html(html, height=altura)
