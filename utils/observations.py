"""
Observaciones automáticas del ensayo.

A partir de la comparación experimental/teórica, el sistema genera
conclusiones en lenguaje natural con un nivel de severidad asociado
(ok / info / warn / err), que la interfaz muestra como badges.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from physics.calculations import Comparacion
from physics.constants import Superficie


@dataclass
class Observacion:
    texto: str
    nivel: str  # "ok" | "info" | "warn" | "err"


def generar_observaciones(comp: Comparacion, superficie: Superficie,
                          angulo: float) -> list[Observacion]:
    """Reglas de decisión que convierten los números en conclusiones."""
    obs: list[Observacion] = []
    err = comp.error_aceleracion

    # ── Calidad del ajuste teoría/experimento ──────────────────
    if not math.isfinite(err):
        obs.append(Observacion(
            "⚠️ Con este μ la teoría predice que el carrito no se mueve: "
            "el experimento no puede compararse.", "err"))
    elif err <= 5:
        obs.append(Observacion(
            f"✅ Excelente concordancia: el experimento coincide con la teoría "
            f"(error de {err:.1f} %).", "ok"))
    elif err <= 15:
        obs.append(Observacion(
            f"✅ El error experimental es pequeño ({err:.1f} %): "
            "el modelo describe bien el movimiento.", "ok"))
    elif err <= 30:
        obs.append(Observacion(
            f"⚠️ Diferencia moderada ({err:.1f} %): revisa la medición del tiempo "
            "o el valor de μ de referencia.", "warn"))
    else:
        obs.append(Observacion(
            f"❌ Existe una diferencia considerable ({err:.1f} %): probablemente el μ "
            "real de la superficie difiere del valor tabulado.", "err"))

    # ── Fricción ───────────────────────────────────────────────
    if comp.mu_exp < 0.15:
        obs.append(Observacion(
            f"🧊 La fricción medida es baja (μ ≈ {comp.mu_exp:.2f}): "
            "la superficie se comporta casi como un plano liso.", "info"))
    elif comp.mu_exp > 0.4:
        obs.append(Observacion(
            f"🧱 La fricción medida es alta (μ ≈ {comp.mu_exp:.2f}): "
            "gran parte de la energía se disipa en el contacto.", "warn"))
    else:
        obs.append(Observacion(
            f"⚖️ Fricción moderada (μ ≈ {comp.mu_exp:.2f}), coherente con "
            f"una superficie de {superficie.nombre.lower()}.", "info"))

    dif_mu = comp.mu_exp - comp.mu_teo
    if abs(dif_mu) > 0.1:
        direccion = "mayor" if dif_mu > 0 else "menor"
        obs.append(Observacion(
            f"🔍 El μ experimental resultó {direccion} que el tabulado "
            f"(Δμ = {dif_mu:+.2f}): posible influencia de polvo, humedad o "
            "irregularidades de la pista.", "warn"))

    # ── Energía ────────────────────────────────────────────────
    obs.append(Observacion(
        f"⚡ Se disiparon {comp.dif_energia*1000:.2f} mJ por fricción "
        "(diferencia entre energía potencial y cinética).", "info"))

    # ── Geometría ──────────────────────────────────────────────
    if angulo >= 38:
        obs.append(Observacion(
            "📐 Con ángulos altos el peso domina sobre la fricción: "
            "el tiempo de bajada se vuelve muy corto y difícil de cronometrar.",
            "info"))

    return obs
