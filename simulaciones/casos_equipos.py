"""Casos inválidos para ServicioEquipos (alquiler de equipos)."""

from models.servicio import ServicioEquipos


def simular_equipos(simulador) -> None:
    equipo = ServicioEquipos("E001", 50.0, "Laptop Dev")

    simulador.ejecutar("Equipo con días negativos (-2)",
                       lambda: equipo.calcular_costo(dias=-2))
    simulador.ejecutar("Equipo con descuento mayor a 100 % (150)",
                       lambda: equipo.calcular_costo(dias=4, descuento_porcentaje=150.0))
    simulador.ejecutar("Equipo con descuento negativo (-20)",
                       lambda: equipo.calcular_costo(dias=4, descuento_porcentaje=-20.0))
    simulador.ejecutar("Equipo con días sin valor (None)",
                       lambda: equipo.calcular_costo(dias=None))
    simulador.ejecutar("Crear equipo con tipo vacío ('')",
                       lambda: ServicioEquipos("E002", 50.0, ""))
    simulador.ejecutar("Crear equipo con tarifa escrita como texto ('cincuenta')",
                       lambda: ServicioEquipos("E003", "cincuenta", "Proyector"))
