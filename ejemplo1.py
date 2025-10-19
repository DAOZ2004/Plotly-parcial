import plotly.express as px

# Datos de ejemplo
datos = {"Año": [2020, 2021, 2022, 2023],
         "Ventas": [500, 800, 1200, 1500]}

# Crear gráfico de líneas
fig = px.line(datos, x="Año", y="Ventas", title="Crecimiento de ventas anuales")
fig.show()
