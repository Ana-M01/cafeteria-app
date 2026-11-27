import os
import solara
from negocio_v2 import (cargar, departamentos, anios, filas, estaciones, promedio_pm25, estaciones_sobre,
                        ESTACION, MUNICIPIO, PROMEDIO, REPRESENTATIVIDAD)

# Configuración y secreto: vienen del entorno (en Render, del panel Environment).
NOMBRE = os.environ.get("NOMBRE_APP", "Aire en Colombia")
CLAVE_ADMIN = os.environ.get("CLAVE_ADMIN", "")
# Para quién es, qué resuelve y de dónde salen los datos: se ven en pantalla.
NECESIDAD = ("Para habitantes, colegios y autoridades locales: ¿qué tan contaminado está el aire con "
             "material particulado fino (PM2.5) en mi departamento, y cuántas estaciones superan el límite que elijo?")
FUENTE = ("Datos: [Calidad del Aire en Colombia (Promedio Anual)](https://www.datos.gov.co/d/kekd-7v7h), "
          "IDEAM – SISAIRE, publicado en datos.gov.co. Licencia: CC BY-SA 4.0. "
          "Se usan solo registros de PM2.5 (24 h) con representatividad temporal de 75 % o más.")

aire = cargar()
DEPARTAMENTOS = departamentos(aire)
ANIOS = [str(a) for a in anios(aire)]

departamento = solara.reactive("ANTIOQUIA" if "ANTIOQUIA" in DEPARTAMENTOS else DEPARTAMENTOS[0])
anio = solara.reactive(ANIOS[-1])
umbral = solara.reactive(25)
clave = solara.reactive("")


@solara.component
def Page():
    solara.Markdown(f"# {NOMBRE}\n\n{NECESIDAD}")
    solara.Select(label="Departamento", value=departamento, values=DEPARTAMENTOS)
    solara.Select(label="Año", value=anio, values=ANIOS)
    solara.SliderInt("Límite de PM2.5 (µg/m³)", value=umbral, min=5, max=50)

    a = int(anio.value)
    promedio = promedio_pm25(aire, departamento.value, a)
    if promedio is None:
        solara.Markdown(f"No hay estaciones representativas de PM2.5 en {departamento.value} para {a}.")
    else:
        total = estaciones(aire, departamento.value, a)
        sobre = estaciones_sobre(aire, departamento.value, a, umbral.value)
        solara.Markdown(f"Promedio anual de PM2.5 en {departamento.value} ({a}): **{promedio} µg/m³**")
        solara.Markdown(f"Estaciones representativas: {total} · por encima de {umbral.value} µg/m³: **{sobre}**")
        solara.Markdown("Referencias: guía OMS 2021 = 5 µg/m³ al año; norma colombiana (Res. 2254 de 2017) = 25 µg/m³ al año.")

    solara.InputText("Clave de administración", value=clave, password=True)
    if CLAVE_ADMIN and clave.value == CLAVE_ADMIN:
        tabla = filas(aire, departamento.value, a)[[ESTACION, MUNICIPIO, PROMEDIO, REPRESENTATIVIDAD]]
        solara.DataFrame(tabla)

    solara.Markdown(FUENTE)
