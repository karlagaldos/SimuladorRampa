"""
Simulación visual de la rampa y el carrito (SVG animado).

El SVG se genera dinámicamente en función del ángulo y la superficie.
Al presionar «Calcular», el carrito desciende por la rampa con una
animación CSS cuya duración coincide con el tiempo experimental medido,
de modo que la simulación es físicamente coherente con el ensayo.
"""

from __future__ import annotations

import math

import streamlit.components.v1 as components

from physics.constants import Superficie

# Dimensiones del lienzo SVG
W, H = 460, 300
MARGEN = 30
BASE_Y = H - 46          # Altura del piso
LARGO_PX = 340           # Longitud de la rampa en píxeles (representa 37 cm)


def _geometria(angulo_deg: float):
    """Coordenadas de la rampa: pie (derecha) y cima (izquierda)."""
    theta = math.radians(angulo_deg)
    pie = (MARGEN + LARGO_PX * math.cos(theta) + 40, BASE_Y)
    cima = (pie[0] - LARGO_PX * math.cos(theta), BASE_Y - LARGO_PX * math.sin(theta))
    return cima, pie, theta


def render_simulacion(
    angulo_deg: float,
    superficie: Superficie,
    animar: bool = False,
    duracion_s: float = 1.0,
    altura: int = H + 10,
) -> None:
    """Dibuja la rampa, el carrito y las fuerzas. Si `animar`, el carrito baja."""
    cima, pie, theta = _geometria(angulo_deg)
    ang = angulo_deg

    # El carrito se dibuja centrado en el origen y se posiciona/rota con transform,
    # lo que permite animar su desplazamiento a lo largo de la rampa con CSS.
    dx = (pie[0] - cima[0])
    dy = (pie[1] - cima[1])
    dur = max(0.6, min(duracion_s, 6.0))  # Duración acotada para que siempre se aprecie

    # La TRASLACIÓN se anima con CSS (independiente del origen de transformación)
    # y la ROTACIÓN se aplica como atributo SVG en un grupo interno, que rota de
    # forma fiable alrededor del origen local en todos los navegadores.
    animacion_css = f"""
        #carrito {{
            transform-box: view-box;
            transform-origin: 0 0;
            animation: bajar {dur:.2f}s cubic-bezier(.45,.03,.71,.61) forwards;
        }}
        @keyframes bajar {{
            from {{ transform: translate({cima[0]:.1f}px, {cima[1]:.1f}px); }}
            to   {{ transform: translate({(cima[0]+dx*0.93):.1f}px, {(cima[1]+dy*0.93):.1f}px); }}
        }}
    """ if animar else f"""
        #carrito {{
            transform-box: view-box;
            transform-origin: 0 0;
            transform: translate({cima[0]:.1f}px, {cima[1]:.1f}px);
            transition: transform .5s ease;
        }}
    """

    html = f"""
    <style>
        .lienzo {{ font-family: 'Space Grotesk', sans-serif; }}
        #rampa {{ transition: all .5s ease; }}
        {animacion_css}
        .etiqueta {{ font-size: 12px; fill: #8CA0C4; }}
        .medida  {{ font-size: 11px; fill: #64748B; font-family: monospace; }}
        @media (prefers-reduced-motion: reduce) {{
            #carrito {{ animation: none; }}
        }}
    </style>
    <svg class="lienzo" viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg">
        <!-- Piso -->
        <line x1="10" y1="{BASE_Y}" x2="{W-10}" y2="{BASE_Y}"
              stroke="#24304D" stroke-width="4" stroke-linecap="round"/>

        <!-- Rampa (la textura del gradiente cambia con la superficie) -->
        <defs>
            <linearGradient id="gradRampa" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0" stop-color="{superficie.color}" stop-opacity="0.85"/>
                <stop offset="1" stop-color="{superficie.color}" stop-opacity="0.35"/>
            </linearGradient>
        </defs>
        <polygon id="rampa"
                 points="{cima[0]:.1f},{cima[1]:.1f} {pie[0]:.1f},{pie[1]:.1f} {cima[0]:.1f},{pie[1]:.1f}"
                 fill="url(#gradRampa)" opacity="0.9"/>
        <line x1="{cima[0]:.1f}" y1="{cima[1]:.1f}" x2="{pie[0]:.1f}" y2="{pie[1]:.1f}"
              stroke="{superficie.color}" stroke-width="5" stroke-linecap="round"/>

        <!-- Arco y valor del ángulo -->
        <path d="M {pie[0]-52:.1f} {BASE_Y}
                 A 52 52 0 0 1 {pie[0]-52*math.cos(theta):.1f} {BASE_Y-52*math.sin(theta):.1f}"
              fill="none" stroke="#EAF2FF" stroke-width="1.6" stroke-dasharray="4 3"/>
        <text x="{pie[0]-86:.1f}" y="{BASE_Y-14:.1f}" class="etiqueta"
              fill="#EAF2FF" font-weight="bold">θ = {ang:.0f}°</text>

        <!-- Cotas: longitud y altura -->
        <text x="{(cima[0]+pie[0])/2-28:.1f}" y="{(cima[1]+pie[1])/2-14:.1f}"
              class="medida" transform="rotate({ang:.1f} {(cima[0]+pie[0])/2:.1f} {(cima[1]+pie[1])/2:.1f})">
              L = 37 cm</text>
        <line x1="{cima[0]-14:.1f}" y1="{cima[1]:.1f}" x2="{cima[0]-14:.1f}" y2="{BASE_Y}"
              stroke="#64748B" stroke-width="1" stroke-dasharray="3 3"/>
        <text x="{cima[0]-20:.1f}" y="{(cima[1]+BASE_Y)/2:.1f}" class="medida" text-anchor="middle"
              transform="rotate(-90 {cima[0]-20:.1f} {(cima[1]+BASE_Y)/2:.1f})">h = {0.37*math.sin(theta)*100:.1f} cm</text>

        <!-- Carrito: el grupo externo se traslada (CSS) y el interno rota (SVG)
             para que las llantas queden apoyadas sobre la superficie -->
        <g id="carrito">
          <g transform="rotate({ang:.1f})">
            <rect x="6" y="-28" width="46" height="18" rx="5"
                  fill="#EAF2FF" stroke="#38BDF8" stroke-width="2"/>
            <circle cx="17" cy="-8" r="6" fill="#0D1526" stroke="#38BDF8" stroke-width="2"/>
            <circle cx="41" cy="-8" r="6" fill="#0D1526" stroke="#38BDF8" stroke-width="2"/>
            <!-- Vector velocidad (indicativo, apunta pendiente abajo) -->
            <line x1="52" y1="-19" x2="76" y2="-19" stroke="#34D399" stroke-width="2.5"
                  marker-end="url(#flechaV)"/>
          </g>
        </g>
        <defs>
            <marker id="flechaV" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="9"
                    refX="8" refY="4" orient="auto">
                <path d="M0,0 L10,4 L0,8 Z" fill="#34D399"/>
            </marker>
        </defs>

        <!-- Leyenda de superficie -->
        <rect x="14" y="14" width="12" height="12" rx="3" fill="{superficie.color}"/>
        <text x="32" y="24" class="etiqueta">{superficie.icono} {superficie.nombre} · μ = {superficie.mu}</text>
    </svg>
    """
    components.html(html, height=altura)
