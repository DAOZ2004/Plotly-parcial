# ==========================================
# Plotly — 15 gráficos interactivos (3 por tipo)
# Autor: Yopocoyo 😎
# ==========================================
# Categorías:
# 1) Clásicos: Línea, Área, Histograma
# 2) Composición: Donut, Treemap, Funnel
# 3) Geográficos: Choropleth, Scatter Geo, Scatter Mapbox (OSM)
# 4) Financieros/Científicos: Candlestick, Heatmap (correl), 3D Scatter
# 5) Avanzados: Animado por tiempo, Facet, Parallel Coordinates
# ==========================================

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pathlib import Path
import os, subprocess, webbrowser, random

random.seed(42)
np.random.seed(42)

# ------------------------------
# Helper para exportar y abrir
# ------------------------------
def safe_show(fig, filename="grafico.html"):
    """
    1) Exportar HTML auto-contenido (sin servidor, sin CDN).
    2) Abre con el navegador predeterminado.
    3) Si falla, intenta rutas comunes de Edge/Chrome.
    4) Último recurso: webbrowser.
    """
    out = Path(filename).resolve()
    fig.write_html(out, include_plotlyjs=True, full_html=True)

    try:
        os.startfile(out)
        print(f"✔ Gráfico abierto: {out}")
        return
    except Exception:
        pass

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

    try:
        webbrowser.open_new_tab(out.as_uri())
        print(f"✔ Gráfico abierto (webbrowser): {out}")
    except Exception:
        print(f"⚠ No se pudo abrir automáticamente. Ábrelo manualmente: {out}")

# ==========================================
# 1) CLÁSICOS (3)
# ==========================================

# 1.1 Línea — Evolución mensual de ventas por modelo (Concesionaria)
def grafico_linea_concesionaria():
    meses = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
    modelos = ["Sedán","SUV","Pickup"]
    data = []
    for m in modelos:
        base = np.linspace(18, 40, 12) + np.random.randint(-5, 6, 12)
        base = np.clip(base, 8, None)
        data += [{"Mes": meses[i], "Modelo": m, "Ventas": int(base[i])} for i in range(12)]
    df = pd.DataFrame(data)
    fig = px.line(df, x="Mes", y="Ventas", color="Modelo",
                  markers=True, title="Concesionaria — Ventas mensuales por modelo (Línea)")
    safe_show(fig, "01_linea_concesionaria.html")

# 1.2 Área — Usuarios activos semanales (App de Tecnología)
def grafico_area_usuarios():
    semanas = [f"S{i+1}" for i in range(16)]
    activos = np.cumsum(np.random.randint(50, 150, size=16)) + 500
    df = pd.DataFrame({"Semana": semanas, "UsuariosActivos": activos})
    fig = px.area(df, x="Semana", y="UsuariosActivos",
                  title="Tecnología — Usuarios activos semanales (Área)")
    safe_show(fig, "02_area_usuarios.html")

# 1.3 Histograma — Distribución de edades de estudiantes
def grafico_histograma_edades():
    edades = np.random.normal(21, 3.5, 400).astype(int)
    edades = np.clip(edades, 16, 45)
    df = pd.DataFrame({"Edad": edades})
    fig = px.histogram(df, x="Edad", nbins=15, marginal="box",
                       title="Estudiantes — Distribución de edades (Histograma)")
    safe_show(fig, "03_histograma_edades.html")

# ==========================================
# 2) COMPOSICIÓN (3)
# ==========================================

# 2.1 Donut — Ventas tecnológicas por región
def grafico_donut_tecnologia():
    regiones = ["Norte","Sur","Este","Oeste","Centro"]
    ventas = [12000, 8500, 7600, 9400, 11000]
    df = pd.DataFrame({"Región": regiones, "Ventas": ventas})
    fig = px.pie(df, names="Región", values="Ventas", hole=0.4,
                 title="Tecnología — Distribución de ventas por región (Donut)")
    fig.update_traces(textinfo="percent+label")
    safe_show(fig, "04_donut_tecnologia.html")


# ==========================================
# 3) GEOGRÁFICOS (3)
# ==========================================

# 3.1 Choropleth — Ventas por país (códigos ISO Alpha-3)
def grafico_choropleth_paises():
    paises = ["USA","MEX","CAN","COL","BRA","ARG","ESP"]
    ventas = [50000, 18000, 15000, 9000, 22000, 12000, 16000]
    df = pd.DataFrame({"iso_alpha": paises, "Ventas": ventas})
    fig = px.choropleth(df, locations="iso_alpha", color="Ventas",
                        color_continuous_scale="Blues",
                        title="Concesionaria — Ventas por país (Choropleth)")
    safe_show(fig, "05_choropleth_paises.html")

# 3.2 Scatter Geo — Envíos internacionales (coordenadas aproximadas)
def grafico_scatter_geo_envios():
    data = {
        "Ciudad": ["San Salvador","Ciudad de México","Miami","Madrid","Bogotá","São Paulo"],
        "Lat": [13.6929, 19.4326, 25.7617, 40.4168, 4.7110, -23.5505],
        "Lon": [-89.2182, -99.1332, -80.1918, -3.7038, -74.0721, -46.6333],
        "Envíos": [210, 380, 270, 160, 190, 250]
    }
    df = pd.DataFrame(data)
    fig = px.scatter_geo(df, lat="Lat", lon="Lon", size="Envíos", hover_name="Ciudad",
                         projection="natural earth",
                         title="Tecnología — Envíos internacionales (Scatter Geo)")
    safe_show(fig, "06_scatter_geo_envios.html")

# 3.3 Scatter Mapbox (OSM) — Sucursales locales
def grafico_scatter_mapbox_sucursales():
    # No requiere token si usamos estilo "open-street-map"
    data = {
        "Sucursal": ["Sucursal Centro","Sucursal Norte","Sucursal Este","Sucursal Oeste"],
        "Lat": [13.70, 13.75, 13.71, 13.69],
        "Lon": [-89.20, -89.22, -89.17, -89.25],
        "Ventas": [120, 90, 80, 110]
    }
    df = pd.DataFrame(data)
    fig = px.scatter_mapbox(df, lat="Lat", lon="Lon", size="Ventas", hover_name="Sucursal",
                            zoom=10, height=500, title="Concesionaria — Sucursales locales (Mapbox/OSM)")
    fig.update_layout(mapbox_style="open-street-map")
    safe_show(fig, "07_scatter_mapbox_sucursales.html")

# ==========================================
# 4) FINANCIEROS / CIENTÍFICOS (3)
# ==========================================

# 4.1 Candlestick — Precio de acción tecnológica (simulado)
def grafico_candlestick_tecnologia():
    dias = pd.date_range("2025-01-01", periods=40, freq="B")
    precio = np.cumsum(np.random.randn(40)) + 100
    open_ = precio + np.random.randn(40)
    close = precio + np.random.randn(40)
    high = np.maximum(open_, close) + abs(np.random.randn(40))*1.5
    low  = np.minimum(open_, close) - abs(np.random.randn(40))*1.5
    df = pd.DataFrame({"Fecha": dias, "Open": open_, "High": high, "Low": low, "Close": close})
    fig = go.Figure(data=[go.Candlestick(
        x=df["Fecha"], open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"]
    )])
    fig.update_layout(title="Tecnología — Candlestick de precio (simulado)",
                      xaxis_title="Fecha", yaxis_title="Precio")
    safe_show(fig, "08_candlestick_tecnologia.html")


# 4.3 3D Scatter — Sensores AgroSense (Humedad vs Temp vs Índice Salud)
def grafico_scatter3d_agrosense():
    n = 120
    df = pd.DataFrame({
        "Humedad": np.random.uniform(20, 90, n),
        "Temperatura": np.random.uniform(15, 38, n),
        "Salud": np.random.uniform(0.4, 0.95, n),
        "Lote": np.random.choice(["A","B","C"], n)
    })
    fig = px.scatter_3d(df, x="Humedad", y="Temperatura", z="Salud",
                        color="Lote", title="AgroSense — Dispersión 3D de sensores")
    safe_show(fig, "09_scatter3d_agrosense.html")

# ==========================================
# 5) AVANZADOS (3)
# ==========================================

# 5.1 Animado — Ventas por modelo a lo largo de meses
def grafico_animado_ventas():
    meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio"]
    modelos = ["Sedán","SUV","Pickup"]
    registros = []
    for mes in meses:
        for m in modelos:
            registros.append({"Mes": mes, "Modelo": m,
                              "Ventas": np.random.randint(12, 45)})
    df = pd.DataFrame(registros)
    fig = px.bar(df, x="Modelo", y="Ventas", color="Modelo",
                 animation_frame="Mes", range_y=[0, 50],
                 title="Concesionaria — Ventas por modelo (Animado por mes)")
    safe_show(fig, "10_animado_ventas.html")

# 5.2 Facet — Calificaciones por materia y grupo
def grafico_facet_estudiantes():
    materias = ["Estadistica computacional","ADMON BD 2","Circuitos digitales","Progra 3","Ingles basico"]
    grupos = ["A1","A2","A3"]
    data = []
    for g in grupos:
        for mat in materias:
            data.append({"Grupo": g, "Materia": mat, "Promedio": np.random.randint(70, 98)})
    df = pd.DataFrame(data)
    fig = px.bar(df, x="Materia", y="Promedio", facet_col="Grupo",
                 title="Estudiantes — Promedios por materia y grupo (Facet)")
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("Grupo=", "")))
    safe_show(fig, "11_facet_estudiantes.html")

# 5.3 Parallel Coordinates — KPIs por modelo
def grafico_parallel_coords():
    modelos = ["Sedán","SUV","Pickup","Coupé","Hatchback"]
    df = pd.DataFrame({
        "Modelo": modelos,
        "PrecioPromedio": np.random.randint(15000, 38000, len(modelos)),
        "Satisfacción": np.random.randint(70, 98, len(modelos)),
        "Consumo(km/l)": np.random.uniform(9, 18, len(modelos)).round(1),
        "Mantenimiento(USD/año)": np.random.randint(300, 1100, len(modelos))
    })
    dims = [
        dict(label="Precio", values=df["PrecioPromedio"]),
        dict(label="Satisfacción", values=df["Satisfacción"]),
        dict(label="Consumo (km/l)", values=df["Consumo(km/l)"]),
        dict(label="Mantenimiento", values=df["Mantenimiento(USD/año)"]),
    ]
    fig = go.Figure(data=go.Parcoords(
        line=dict(color=df["PrecioPromedio"], colorscale="Viridis"),
        dimensions=dims
    ))
    fig.update_layout(title="Concesionaria — Parallel Coordinates de KPIs por modelo")
    safe_show(fig, "12_parallel_coords.html")

# ==========================================
# Ejecutar todos
# ==========================================
if __name__ == "__main__":
    # 1) Clásicos
    grafico_linea_concesionaria()
    grafico_area_usuarios()
    grafico_histograma_edades()

    # 2) Composición
    grafico_donut_tecnologia()

    # 3) Geográficos
    grafico_choropleth_paises()
    grafico_scatter_geo_envios()
    grafico_scatter_mapbox_sucursales()

    # 4) Financieros / Científicos
    grafico_candlestick_tecnologia()
    grafico_scatter3d_agrosense()

    # 5) Avanzados
    grafico_animado_ventas()
    grafico_facet_estudiantes()
    grafico_parallel_coords()
