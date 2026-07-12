"""
Constantes físicas del experimento.

Los datos constantes provienen del ensayo de laboratorio:
carrito de 32 g sobre una pista de 37 cm.
"""

from dataclasses import dataclass

# ── Datos constantes del ensayo ────────────────────────────────
MASA_KG: float = 0.032        # Masa del carrito [kg]  (32 g)
LONGITUD_M: float = 0.37      # Longitud de la pista [m]  (37 cm)
GRAVEDAD: float = 9.81        # Aceleración de la gravedad [m/s²]

# ── Rango del ángulo de inclinación ────────────────────────────
ANGULO_MIN: int = 30          # [grados]
ANGULO_MAX: int = 40          # [grados]
ANGULO_DEFECTO: int = 35      # [grados]


@dataclass(frozen=True)
class Superficie:
    """Superficie de contacto de la pista y su coeficiente de fricción cinética."""
    id: str
    nombre: str
    mu: float                 # Coeficiente de fricción cinética (valor de referencia)
    descripcion: str
    icono: str
    color: str                # Color de identidad de la tarjeta
    textura_css: str          # Gradiente CSS que simula la textura


# Coeficientes de referencia tomados de tablas de fricción cinética
# (valores aproximados; pueden ajustarse tras calibrar con el ensayo real).
SUPERFICIES: dict[str, Superficie] = {
    "mica": Superficie(
        id="mica",
        nombre="Mica lisa de anillado",
        mu=0.12,
        descripcion="Plástico liso · fricción baja",
        icono="🪞",
        color="#38BDF8",
        textura_css="linear-gradient(135deg,#1e3a5f 0%,#3b6ea5 45%,#9fd3f0 50%,#3b6ea5 55%,#1e3a5f 100%)",
    ),
    "arena": Superficie(
        id="arena",
        nombre="Arena",
        mu=0.45,
        descripcion="Granular · fricción alta",
        icono="🏜️",
        color="#FBBF24",
        textura_css="repeating-radial-gradient(circle at 30% 40%,#8a6d3b 0 2px,#a8874e 2px 4px,#6e5530 4px 6px)",
    ),
    "madera": Superficie(
        id="madera",
        nombre="Madera tipo canaleta",
        mu=0.30,
        descripcion="Madera · fricción media",
        icono="🪵",
        color="#F97316",
        textura_css="repeating-linear-gradient(95deg,#5c3a21 0 6px,#7a4f2d 6px 12px,#6b442a 12px 18px)",
    ),
}
