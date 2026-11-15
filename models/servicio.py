from abc import abstractmethod
from models.base import EntidadBase

class Servicio(EntidadBase):
    """Clase abstracta Servicio que hereda de EntidadBase."""
    
    def __init__(self, codigo: str, nombre: str, tarifa_base: float):
        super().__init__(codigo)
        self.nombre = nombre
        self.tarifa_base = tarifa_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """Método polimórfico para el cálculo de costos."""
        pass

    def obtener_detalles(self) -> str:
        return f"Servicio [{self._codigo}]: {self.nombre} - Tarifa Base: ${self.tarifa_base}"


class ServicioSalas(Servicio):
    """Servicio especializado 1: Reserva de salas para reuniones o conferencias."""
    
    def __init__(self, codigo: str, tarifa_base: float, capacidad: int):
        super().__init__(codigo, "Reserva de Salas", tarifa_base)
        self.capacidad = capacidad

    def calcular_costo(self, horas: int = 1, aplicar_iva: bool = True) -> float:
        subtotal = self.tarifa_base * horas
        if aplicar_iva:
            subtotal *= 1.19  # IVA del 19%
        return round(subtotal, 2)


class ServicioEquipos(Servicio):
    """Servicio especializado 2: Alquiler de equipos tecnológicos."""
    
    def __init__(self, codigo: str, tarifa_base: float, tipo_equipo: str):
        super().__init__(codigo, "Alquiler de Equipos", tarifa_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, dias: int = 1, descuento_porcentaje: float = 0.0) -> float:
        subtotal = self.tarifa_base * dias
        if descuento_porcentaje > 0:
            subtotal *= (1 - (descuento_porcentaje / 100))
        return round(subtotal, 2)


class ServicioAsesorias(Servicio):
    """Servicio especializado 3: Asesorías técnicas especializadas."""
    
    def __init__(self, codigo: str, tarifa_base: float, area_especialidad: str):
        super().__init__(codigo, "Asesorías Especializadas", tarifa_base)
        self.area_especialidad = area_especialidad

    def calcular_costo(self, sesiones: int = 1, recargo_complejidad: float = 0.0) -> float:
        subtotal = (self.tarifa_base * sesiones) + recargo_complejidad
        return round(subtotal, 2)