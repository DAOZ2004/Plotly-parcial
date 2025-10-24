import plotly.express as px
import pandas as pd
from pathlib import Path
import os
import subprocess
import webbrowser

# === 2) FUNCIÓN PARA MOSTRAR ===
def safe_show(fig, filename="grafico.html"):
    out = Path(filename).resolve()
    fig.write_html(out, include_plotlyjs=True, full_html=True)

    try:
        os.startfile(out)  # Windows
        print(f"✔ Gráfico abierto: {out}")
        return
    except Exception:
        pass

    # Alternativas: Edge / Chrome
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

# === 3) DATOS Y GRÁFICO ===
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
    title=" Distribución de ventas por región (Donut)"
)
fig_donut.update_traces(textinfo="percent+label")

safe_show(fig_donut, "tecnologia_donut.html")


