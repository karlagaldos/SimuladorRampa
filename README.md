# 🛗 Simulador · Carrito sobre Plano Inclinado

> Proyecto del curso de Física · **Universidad Tecnológica del Perú (UTP)**

Laboratorio virtual de Física que simula el movimiento de un carrito sobre un plano inclinado y **compara los resultados experimentales** (tiempo cronometrado en el laboratorio) **con las predicciones teóricas** del modelo de fricción cinética.

Desarrollado con **Python + Streamlit + Plotly**, con animaciones SVG, cálculos paso a paso y observaciones automáticas.

---

## ✨ Características

- **Simulación animada**: rampa SVG que se reconfigura con el ángulo; al presionar *Calcular* el carrito desciende con una duración igual al tiempo experimental medido.
- **Diagrama de cuerpo libre dinámico**: muestra Peso, Normal y Fricción con flechas escaladas a la magnitud real de cada fuerza.
- **Tarjetas de resultados** con nombre, fórmula, valor, unidad e ícono (sin tablas tradicionales), con animación en cascada.
- **Selector de superficies por tarjetas** con textura: Mica lisa de anillado, Arena y Madera tipo canaleta.
- **Cálculos paso a paso**: fórmula → sustitución → resultado → explicación breve de cada magnitud.
- **Gráficos interactivos (Plotly)**: velocidad vs tiempo, aceleración vs ángulo, comparación experimental/teórica y gauge de error porcentual.
- **Observaciones automáticas**: el sistema genera conclusiones (nivel de fricción, calidad del ajuste, energía disipada) como badges de colores.

## 🔬 Modelo físico

| Magnitud | Fórmula |
|---|---|
| Aceleración experimental | `a_exp = 2L / t²` (parte del reposo) |
| Velocidad final | `v = a · t` |
| μ experimental | `μ_exp = (g·sinθ − a_exp) / (g·cosθ)` |
| Aceleración teórica | `a_teo = g(sinθ − μ·cosθ)` |
| Energía potencial | `Ep = m·g·L·sinθ` |
| Energía cinética | `Ec = ½·m·v²` |

**Datos constantes del ensayo:** masa = 32 g · longitud de pista = 37 cm · g = 9.81 m/s² · ángulo variable entre 30° y 40°.

> Los coeficientes de fricción de cada superficie son valores de referencia y pueden calibrarse en `physics/constants.py` con los resultados reales del laboratorio.

## 🚀 Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/simulador-plano-inclinado.git
cd simulador-plano-inclinado

# 2. Crear un entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
streamlit run app.py
```

La aplicación se abre en `http://localhost:8501`.

## ☁️ Despliegue en Streamlit Community Cloud

1. Sube el repositorio a GitHub.
2. Entra en [share.streamlit.io](https://share.streamlit.io) y conecta tu cuenta de GitHub.
3. Selecciona el repositorio, rama `main` y archivo principal `app.py`.
4. Presiona **Deploy**: las dependencias se instalan automáticamente desde `requirements.txt`.

## 🗂️ Arquitectura

```
simulador-plano-inclinado/
├── app.py                        # Punto de entrada: layout y orquestación
├── physics/
│   ├── constants.py              # Datos del ensayo y superficies (μ)
│   └── calculations.py           # Motor de cálculos con pasos detallados
├── components/
│   ├── simulation.py             # Rampa + carrito animado (SVG)
│   ├── free_body_diagram.py      # DCL con fuerzas escaladas
│   ├── cards.py                  # Tarjetas de resultados y pasos
│   └── surface_selector.py       # Selector de superficies por tarjetas
├── charts/
│   └── plots.py                  # Gráficos interactivos Plotly
├── utils/
│   └── observations.py           # Conclusiones automáticas del ensayo
├── styles/
│   └── custom.css                # Tema "laboratorio virtual" + identidad UTP
├── assets/
│   └── utp_logo.png              # Logo institucional (fondo transparente)
├── .streamlit/config.toml        # Tema base de Streamlit
├── requirements.txt
├── LICENSE                       # MIT
└── README.md
```

Cada módulo tiene una única responsabilidad: la física no conoce la interfaz, los componentes no calculan y los gráficos solo reciben resultados ya procesados.

## 🧭 Cómo usarlo

1. Ajusta el **ángulo** (30°–40°) en la barra lateral: la rampa y el DCL se actualizan al instante.
2. Elige la **superficie** tocando su tarjeta: cambia la textura y el μ teórico.
3. Ingresa el **tiempo cronometrado** en el laboratorio.
4. Presiona **▶️ Calcular y simular**: el carrito baja, las tarjetas aparecen y se generan gráficos, pasos y observaciones.

## 📄 Licencia

Distribuido bajo licencia [MIT](LICENSE).
