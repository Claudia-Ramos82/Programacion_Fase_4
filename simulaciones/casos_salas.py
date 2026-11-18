"""Casos inválidos para ServicioSalas (reserva de salas)."""

from models.servicio import ServicioSalas


def simular_salas(simulador) -> None:
    sala = ServicioSalas("S001", 100.0, 20)

    simulador.ejecutar("Sala con horas negativas (-3)",
                       lambda: sala.calcular_costo(horas=-3))
    simulador.ejecutar("Sala con 0 horas",
                       lambda: sala.calcular_costo(horas=0))
    simulador.ejecutar("Sala con horas escritas como texto ('tres')",
                       lambda: sala.calcular_costo(horas="tres"))
    simulador.ejecutar("Sala con un parámetro que no existe (dias=2)",
                       lambda: sala.calcular_costo(dias=2))
    simulador.ejecutar("Crear sala con tarifa negativa (-100)",
                       lambda: ServicioSalas("S002", -100.0, 20))
    simulador.ejecutar("Crear sala con capacidad negativa (-5)",
                       lambda: ServicioSalas("S003", 100.0, -5))
    simulador.ejecutar("Crear sala con código vacío ('')",
                       lambda: ServicioSalas("", 100.0, 20))
