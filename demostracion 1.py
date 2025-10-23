# ==========================================
# Demostración Plotly — Yopocoyo 😎
# 1) Bubble (concesionaria)
# 2) Radar (estudiantes)
# 3) Donut (ventas por región)
# 4) Sunburst (concesionaria jerárquico)
# ==========================================

import plotly.express as px
import pandas as pd
from pathlib import Path
import os
import subprocess
import webbrowser

def safe_show(fig, filename="grafico.html"):
    """
    1) Exporta HTML auto-contenido (sin servidor ni internet).
    2) Abre con navegador predeterminado (Windows: os.startfile).
    3) Si falla, intenta rutas típicas de Edge/Chrome.
    4) Último recurso: webbrowser.
    """
    out = Path(filename).resolve()
    fig.write_html(out, include_plotlyjs=True, full_html=True)

    # Plan A: navegador por defecto del sistema
    try:
        os.startfile(out)  # Windows
        print(f"✔ Gráfico abierto: {out}")
        return
    except Exception:
        pass

    # Plan B: Edge/Chrome por ruta
    candidates = [
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for exe in candidates:
        if Path(exe).exists():
            try:
                subprocess.Popen([exe, str(out)])
                print(f"✔ Gráfico abierto con: {exe}\n   Archivo: {out}")
                return
            except Exception:
                continue

    # Plan C: webbrowser
    try:
        webbrowser.open_new_tab(out.as_uri())
        print(f"✔ Gráfico abierto (webbrowser): {out}")
    except Exception:
        print(f"⚠ No se pudo abrir automáticamente. Ábrelo manualmente: {out}")

# ============================================================
# 🚗 1) Concesionaria — Bubble Chart (Ventas vs Ganancia)
# ============================================================
data_carros = {
    "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"] * 3,
    "Modelo": ["Sedán"] * 6 + ["SUV"] * 6 + ["Pickup"] * 6,
    "Ventas": [20, 25, 30, 28, 35, 40, 15, 18, 20, 22, 25, 30, 10, 12, 14, 16, 18, 20],
    "Ganancia": [8000, 10000, 12000, 11000, 13000, 15000,
                 9000, 9500, 11000, 11500, 12500, 14000,
                 6000, 7000, 8000, 8500, 9000, 9500]
}
df_carros = pd.DataFrame(data_carros)

fig_bubble = px.scatter(
    df_carros,
    x="Mes",
    y="Ganancia",
    size="Ventas",
    color="Modelo",
    hover_name="Modelo",
    size_max=60,
    title="🚘 Concesionaria: Ventas vs Ganancia por Mes y Modelo (Bubble Chart)"
)
safe_show(fig_bubble, "concesionaria_bubble.html")

# ============================================================
# 🎓 2) Estudiantes — Radar Chart (Promedio por Materia)
# ============================================================
data_estudiantes = {
    "Materia": ["Matemáticas", "Ciencias", "Historia", "Inglés", "Arte"],
    "Promedio": [85, 78, 90, 88, 92]
}
df_estudiantes = pd.DataFrame(data_estudiantes)

fig_radar = px.line_polar(
    df_estudiantes,
    r="Promedio",
    theta="Materia",
    line_close=True,
    markers=True,
    title="🎓 Estudiantes: Promedio de calificaciones por materia (Radar)"
)
fig_radar.update_traces(fill="toself")
safe_show(fig_radar, "estudiantes_radar.html")

# ============================================================
# 💻 3) Tecnología — Donut Chart (Ventas por Región)
# ============================================================
data_tecnologia = {
    "Región": ["Norte", "Sur", "Este", "Oeste", "Centro"],
    "Ventas": [12000, 8500, 7600, 9400, 11000]
}
df_tecnologia = pd.DataFrame(data_tecnologia)

fig_donut = px.pie(
    df_tecnologia,
    names="Región",
    values="Ventas",
    hole=0.4,
    title="💻 Tecnología: Distribución de ventas por región (Donut)"
)
fig_donut.update_traces(textinfo="percent+label")
safe_show(fig_donut, "tecnologia_donut.html")

# ============================================================
# 🌞 4) Concesionaria — Sunburst (Jerarquía Modelo → Mes)
#     - Valores: Ventas (suma)
#     - Color: Ganancia (suma)
# ============================================================
# Agregamos por Modelo y Mes para que el Sunburst muestre totales correctos
agg_carros = (
    df_carros
    .groupby(["Modelo", "Mes"], as_index=False)
    .agg(Ventas=("Ventas", "sum"), Ganancia=("Ganancia", "sum"))
)

fig_sunburst = px.sunburst(
    agg_carros,
    path=["Modelo", "Mes"],
    values="Ventas",
    color="Ganancia",
    color_continuous_scale="Tealgrn",
    title="🌞 Concesionaria: Jerarquía Modelo → Mes por Ventas (color = Ganancia)"
)
# Hover personalizado para ver totales claros
fig_sunburst.update_traces(
    hovertemplate="<b>%{label}</b><br>Ventas: %{value}<br>Ganancia: %{color:.0f}<extra></extra>"
)
safe_show(fig_sunburst, "concesionaria_sunburst.html")
