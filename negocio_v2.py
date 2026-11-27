import unicodedata
import pandas as pd

# CSV tal como se descarga de datos.gov.co (Exportar -> CSV), renombrado a calidad_aire.csv.
ARCHIVO = "datos/calidad_aire.csv"
CONTAMINANTE = "PM2.5"          # material particulado fino
EXPOSICION = 24                 # promedio diario (horas)
REPRESENTATIVIDAD_MINIMA = 75   # % de datos válidos para que la estación cuente

# Columnas del archivo oficial que usa la app.
VARIABLE = "Variable"
TIEMPO = "Tiempo de exposición (horas)"
ANIO = "Año"
PROMEDIO = "Promedio"
REPRESENTATIVIDAD = "Representatividad Temporal"
ESTACION = "Estación"
DEPARTAMENTO = "Nombre del Departamento"
MUNICIPIO = "Nombre del Municipio"


def normalizar(nombre):
    """'Bogotá, D.C.', 'BOGOTA, D.C.' y 'Bogotá, D.C.' quedan iguales: mayúsculas y sin tildes."""
    sin_tildes = unicodedata.normalize("NFKD", str(nombre)).encode("ascii", "ignore").decode()
    return " ".join(sin_tildes.upper().split())


def cargar():
    """Lee el CSV oficial y deja solo PM2.5, promedio de 24 h, estaciones representativas."""
    df = pd.read_csv(ARCHIVO, thousands=",")   # el archivo escribe 2,011 para el año 2011
    df = df[(df[VARIABLE] == CONTAMINANTE)
            & (df[TIEMPO] == EXPOSICION)
            & (df[REPRESENTATIVIDAD] >= REPRESENTATIVIDAD_MINIMA)].copy()
    df["departamento"] = df[DEPARTAMENTO].map(normalizar)
    df["anio"] = df[ANIO].astype(int)
    return df


def departamentos(df):
    return sorted(str(d) for d in df["departamento"].unique())


def anios(df):
    return sorted(int(a) for a in df["anio"].unique())


def filas(df, departamento, anio):
    return df[(df["departamento"] == departamento) & (df["anio"] == anio)]


def estaciones(df, departamento, anio):
    return int(filas(df, departamento, anio)[ESTACION].nunique())


def promedio_pm25(df, departamento, anio):
    """Promedio de las concentraciones anuales registradas en el departamento (µg/m³), con un decimal."""
    datos = filas(df, departamento, anio)
    return round(float(datos[PROMEDIO].mean()), 1) if len(datos) else None


def estaciones_sobre(df, departamento, anio, umbral):
    datos = filas(df, departamento, anio)
    return int(datos[datos[PROMEDIO] > umbral][ESTACION].nunique())
