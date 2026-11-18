"""
Software FJ - Fase 4: simulaciones de casos inválidos.

Complementa a main.py (que ejecuta las 10 simulaciones válidas y de prueba
límite) probando entradas que el sistema debería rechazar.

Cómo ejecutarlo, desde la raíz del repositorio:
    python simulaciones_invalidas.py

Cada caso queda clasificado como DETECTADO (el sistema lanzó una excepción)
o NO DETECTADO (el sistema aceptó el dato inválido sin avisar). Al final se
muestra un resumen. La aplicación nunca debe detenerse ante un fallo.
"""

from simulaciones.casos_asesorias import simular_asesorias
from simulaciones.casos_equipos import simular_equipos
from simulaciones.casos_generales import simular_generales
from simulaciones.casos_salas import simular_salas
from simulaciones.ejecutor import Simulador


def ejecutar_simulaciones_invalidas() -> None:
    print("==================================================")
    print("   SOFTWARE FJ - SIMULACIONES DE CASOS INVÁLIDOS  ")
    print("==================================================\n")

    simulador = Simulador()
    simular_salas(simulador)
    simular_equipos(simulador)
    simular_asesorias(simulador)
    simular_generales(simulador)
    simulador.resumen()


if __name__ == "__main__":
    ejecutar_simulaciones_invalidas()
