"""Casos inválidos para ServicioAsesorias (asesorías especializadas)."""

from models.servicio import ServicioAsesorias


def simular_asesorias(simulador) -> None:
    asesoria = ServicioAsesorias("A001", 150.0, "Arquitectura Software")

    simulador.ejecutar("Asesoría con sesiones negativas (-1)",
                       lambda: asesoria.calcular_costo(sesiones=-1))
    simulador.ejecutar("Asesoría con recargo negativo que deja el total en negativo (-500)",
                       lambda: asesoria.calcular_costo(sesiones=1, recargo_complejidad=-500.0))
    simulador.ejecutar("Asesoría con recargo escrito como texto ('alto')",
                       lambda: asesoria.calcular_costo(sesiones=1, recargo_complejidad="alto"))
    simulador.ejecutar("Crear asesoría con área de especialidad vacía ('')",
                       lambda: ServicioAsesorias("A002", 150.0, ""))
