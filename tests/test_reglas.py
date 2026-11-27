from negocio_v2 import cargar, normalizar, departamentos, anios, estaciones, estaciones_sobre


def test_nombres_de_departamento_quedan_iguales():
    assert normalizar("Bogotá, D.C.") == normalizar("BOGOTA, D.C.") == "BOGOTA, D.C."


def test_estaciones_sobre_el_limite_no_superan_el_total():
    aire = cargar()
    for depto in departamentos(aire):
        for anio in anios(aire):
            assert 0 <= estaciones_sobre(aire, depto, anio, 25) <= estaciones(aire, depto, anio)


def test_limite_mas_bajo_nunca_da_menos_estaciones():
    aire = cargar()
    assert estaciones_sobre(aire, "ANTIOQUIA", 2022, 5) >= estaciones_sobre(aire, "ANTIOQUIA", 2022, 25)
