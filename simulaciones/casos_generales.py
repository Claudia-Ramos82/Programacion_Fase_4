"""Casos inválidos sobre la jerarquía: clases abstractas y polimorfismo."""

from models.base import EntidadBase
from models.servicio import Servicio, ServicioSalas


def simular_generales(simulador) -> None:
    sala = ServicioSalas("S001", 100.0, 20)

    simulador.ejecutar("Instanciar directamente la clase abstracta EntidadBase",
                       lambda: EntidadBase("X001"))
    simulador.ejecutar("Instanciar directamente la clase abstracta Servicio",
                       lambda: Servicio("X002", "Genérico", 100.0))
    simulador.ejecutar("Recorrer una lista polimórfica que incluye un objeto que no es Servicio",
                       lambda: [s.calcular_costo() for s in [sala, "no soy un servicio"]])
