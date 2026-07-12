"""
Motor de cálculos físicos del plano inclinado.

Cada magnitud se calcula junto con su desglose paso a paso
(fórmula → sustitución → resultado → explicación) para que el
simulador funcione también como herramienta de aprendizaje.

Modelo físico (cinemática con fricción cinética, partiendo del reposo):

    Experimental:  a_exp = 2L / t²             (de  L = ½ a t²)
                   v_exp = a_exp · t
                   μ_exp = (g·sinθ − a_exp) / (g·cosθ)

    Teórico:       a_teo = g (sinθ − μ·cosθ)
                   t_teo = √(2L / a_teo)
                   v_teo = a_teo · t_teo

    Energías:      h  = L·sinθ
                   Ep = m·g·h          (en la parte superior)
                   Ec = ½·m·v²         (al final de la pista)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from physics.constants import GRAVEDAD, LONGITUD_M, MASA_KG, Superficie


# ══════════════════════════════════════════════════════════════
#  Estructuras de datos
# ══════════════════════════════════════════════════════════════

@dataclass
class Paso:
    """Un cálculo individual mostrado paso a paso."""
    nombre: str
    simbolo: str
    formula: str          # Fórmula en LaTeX
    sustitucion: str      # Sustitución numérica en LaTeX
    valor: float
    unidad: str
    explicacion: str
    icono: str = "📐"

    @property
    def resultado(self) -> str:
        return f"{self.valor:.4g} {self.unidad}"


@dataclass
class Resultados:
    """Conjunto de resultados de un ensayo (experimental o teórico)."""
    titulo: str
    pasos: list[Paso] = field(default_factory=list)

    def get(self, simbolo: str) -> Paso:
        """Devuelve un paso por su símbolo (p. ej. 'a', 'v', 'Ec')."""
        for p in self.pasos:
            if p.simbolo == simbolo:
                return p
        raise KeyError(simbolo)


# ══════════════════════════════════════════════════════════════
#  Ensayo experimental (a partir del tiempo medido)
# ══════════════════════════════════════════════════════════════

def calcular_experimental(angulo_deg: float, t_exp: float) -> Resultados:
    """Calcula las magnitudes experimentales a partir del tiempo cronometrado."""
    theta = math.radians(angulo_deg)
    L, m, g = LONGITUD_M, MASA_KG, GRAVEDAD

    a_exp = 2 * L / t_exp**2
    v_exp = a_exp * t_exp
    mu_exp = (g * math.sin(theta) - a_exp) / (g * math.cos(theta))
    h = L * math.sin(theta)
    ep = m * g * h
    ec = 0.5 * m * v_exp**2

    r = Resultados(titulo="Experimental")
    r.pasos = [
        Paso(
            "Aceleración experimental", "a",
            r"a_{exp} = \dfrac{2L}{t^2}",
            rf"a_{{exp}} = \dfrac{{2\,(0.37)}}{{({t_exp:.3g})^2}} = {a_exp:.4g}",
            a_exp, "m/s²",
            "Se despeja de L = ½·a·t², válida porque el carrito parte del reposo.",
            "🚀",
        ),
        Paso(
            "Velocidad final", "v",
            r"v_f = a_{exp}\cdot t",
            rf"v_f = {a_exp:.4g} \times {t_exp:.3g} = {v_exp:.4g}",
            v_exp, "m/s",
            "Velocidad con la que el carrito llega al final de la pista.",
            "🏁",
        ),
        Paso(
            "Coef. de fricción experimental", "mu",
            r"\mu_{exp} = \dfrac{g\sin\theta - a_{exp}}{g\cos\theta}",
            rf"\mu_{{exp}} = \dfrac{{9.81\sin({angulo_deg:.0f}°) - {a_exp:.3g}}}{{9.81\cos({angulo_deg:.0f}°)}} = {mu_exp:.4g}",
            mu_exp, "",
            "Fricción real de la superficie, deducida de la 2ª ley de Newton.",
            "🧲",
        ),
        Paso(
            "Altura de la rampa", "h",
            r"h = L\sin\theta",
            rf"h = 0.37\sin({angulo_deg:.0f}°) = {h:.4g}",
            h, "m",
            "Altura vertical desde donde parte el carrito.",
            "📏",
        ),
        Paso(
            "Energía potencial", "Ep",
            r"E_p = m\,g\,h",
            rf"E_p = 0.032 \times 9.81 \times {h:.3g} = {ep:.4g}",
            ep, "J",
            "Energía almacenada en la parte superior de la rampa.",
            "🔋",
        ),
        Paso(
            "Energía cinética final", "Ec",
            r"E_c = \tfrac{1}{2}\,m\,v_f^{\,2}",
            rf"E_c = 0.5 \times 0.032 \times ({v_exp:.3g})^2 = {ec:.4g}",
            ec, "J",
            "Energía de movimiento al final; la diferencia con Ep se disipa por fricción.",
            "⚡",
        ),
    ]
    return r


# ══════════════════════════════════════════════════════════════
#  Ensayo teórico (a partir del μ de la superficie)
# ══════════════════════════════════════════════════════════════

def calcular_teorico(angulo_deg: float, superficie: Superficie) -> Resultados:
    """Calcula las magnitudes teóricas usando el μ de referencia de la superficie."""
    theta = math.radians(angulo_deg)
    L, m, g, mu = LONGITUD_M, MASA_KG, GRAVEDAD, superficie.mu

    a_teo = g * (math.sin(theta) - mu * math.cos(theta))
    if a_teo <= 0:
        # La fricción estática vence a la componente del peso: no hay movimiento.
        a_teo = 0.0
        t_teo = float("inf")
        v_teo = 0.0
    else:
        t_teo = math.sqrt(2 * L / a_teo)
        v_teo = a_teo * t_teo

    h = L * math.sin(theta)
    ep = m * g * h
    ec = 0.5 * m * v_teo**2

    r = Resultados(titulo="Teórico")
    r.pasos = [
        Paso(
            "Aceleración teórica", "a",
            r"a_{teo} = g(\sin\theta - \mu\cos\theta)",
            rf"a_{{teo}} = 9.81(\sin{angulo_deg:.0f}° - {mu}\cos{angulo_deg:.0f}°) = {a_teo:.4g}",
            a_teo, "m/s²",
            f"2ª ley de Newton sobre el plano, con μ = {mu} ({superficie.nombre}).",
            "🚀",
        ),
        Paso(
            "Tiempo teórico de bajada", "t",
            r"t_{teo} = \sqrt{\dfrac{2L}{a_{teo}}}",
            (rf"t_{{teo}} = \sqrt{{\dfrac{{2(0.37)}}{{{a_teo:.3g}}}}} = {t_teo:.4g}"
             if math.isfinite(t_teo) else r"t_{teo} \to \infty"),
            t_teo, "s",
            "Tiempo que la teoría predice para recorrer los 37 cm de pista.",
            "⏱️",
        ),
        Paso(
            "Velocidad final teórica", "v",
            r"v_f = a_{teo}\cdot t_{teo}",
            rf"v_f = {a_teo:.3g} \times {t_teo:.3g} = {v_teo:.4g}" if math.isfinite(t_teo) else r"v_f = 0",
            v_teo, "m/s",
            "Velocidad predicha al final de la pista.",
            "🏁",
        ),
        Paso(
            "Energía potencial", "Ep",
            r"E_p = m\,g\,h",
            rf"E_p = 0.032 \times 9.81 \times {h:.3g} = {ep:.4g}",
            ep, "J",
            "Igual para ambos ensayos: depende solo de la geometría.",
            "🔋",
        ),
        Paso(
            "Energía cinética final", "Ec",
            r"E_c = \tfrac{1}{2}\,m\,v_f^{\,2}",
            rf"E_c = 0.5 \times 0.032 \times ({v_teo:.3g})^2 = {ec:.4g}",
            ec, "J",
            "Energía de movimiento predicha por el modelo.",
            "⚡",
        ),
    ]
    return r


# ══════════════════════════════════════════════════════════════
#  Comparación entre ensayos
# ══════════════════════════════════════════════════════════════

@dataclass
class Comparacion:
    error_aceleracion: float   # [%]
    error_tiempo: float        # [%]
    error_velocidad: float     # [%]
    dif_energia: float         # Ep − Ec experimental [J]  (energía disipada)
    mu_exp: float
    mu_teo: float


def comparar(exp: Resultados, teo: Resultados, superficie: Superficie) -> Comparacion:
    """Error porcentual y diferencias energéticas entre ambos ensayos."""

    def err(experimental: float, teorico: float) -> float:
        if not math.isfinite(teorico) or teorico == 0:
            return float("nan")
        return abs(experimental - teorico) / teorico * 100

    t_exp = 2 * exp.get("v").valor / exp.get("a").valor if exp.get("a").valor else float("nan")
    return Comparacion(
        error_aceleracion=err(exp.get("a").valor, teo.get("a").valor),
        error_tiempo=err(t_exp, teo.get("t").valor),
        error_velocidad=err(exp.get("v").valor, teo.get("v").valor),
        dif_energia=exp.get("Ep").valor - exp.get("Ec").valor,
        mu_exp=exp.get("mu").valor,
        mu_teo=superficie.mu,
    )
