import csv
from negocio_v2 import (cargar, normalizar, promedio_pm25, ARCHIVO, CONTAMINANTE, EXPOSICION,
                        REPRESENTATIVIDAD_MINIMA, VARIABLE, TIEMPO, ANIO, PROMEDIO, REPRESENTATIVIDAD, DEPARTAMENTO)

DEPTO, ANIO_CONTROL = "ANTIOQUIA", 2022
CIFRA_DE_CONTROL = 18.0   # promedio de PM2.5 de ANTIOQUIA en 2022, en µg/m³


def numero(texto):
    """'2,011' -> 2011.0; vacíos o 'N/A' cuentan como 0 (igual que pandas los descarta)."""
    try:
        return float(texto.replace(",", ""))
    except ValueError:
        return 0.0


def test_promedio_por_otro_camino():
    """Recalcula el promedio leyendo el CSV línea por línea, sin pandas."""
    valores = []
    with open(ARCHIVO, encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            if (fila[VARIABLE] == CONTAMINANTE
                    and numero(fila[TIEMPO]) == EXPOSICION
                    and numero(fila[REPRESENTATIVIDAD]) >= REPRESENTATIVIDAD_MINIMA
                    and normalizar(fila[DEPARTAMENTO]) == DEPTO
                    and int(numero(fila[ANIO])) == ANIO_CONTROL):
                valores.append(numero(fila[PROMEDIO]))
    assert promedio_pm25(cargar(), DEPTO, ANIO_CONTROL) == round(sum(valores) / len(valores), 1)
    assert round(sum(valores) / len(valores), 1) == CIFRA_DE_CONTROL


def test_cifra_de_control():
    assert promedio_pm25(cargar(), DEPTO, ANIO_CONTROL) == CIFRA_DE_CONTROL