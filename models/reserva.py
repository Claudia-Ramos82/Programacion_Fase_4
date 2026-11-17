from models.base import EntidadBase
from models.cliente import Cliente
from models.servicio import Servicio
from models.excepciones import ReservaInvalidaError, ServicioNoDisponibleError, LoggerSistema

logger = LoggerSistema()

class Reserva(EntidadBase):
    """Clase Reserva que integra Cliente, Servicio, duración y estado."""
    
    def __init__(self, codigo: str, cliente: Cliente, servicio: Servicio, duracion: int):
        super().__init__(codigo)
        if not isinstance(cliente, Cliente):
            msg = "La reserva requiere una instancia válida de Cliente."
            logger.registrar("ERROR", msg)
            raise ReservaInvalidaError(msg)
        if not isinstance(servicio, Servicio):
            msg = "La reserva requiere una instancia válida de Servicio."
            logger.registrar("ERROR", msg)
            raise ServicioNoDisponibleError(msg)

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.costo_total = 0.0

    @property
    def duracion(self) -> int:
        return self.__duracion

    @duracion.setter
    def duracion(self, valor: int):
        try:
            val = int(valor)
            if val <= 0:
                raise ValueError("La duración debe ser mayor a cero.")
            self.__duracion = val
        except (ValueError, TypeError) as e:
            msg = f"Duración inválida en reserva [{self._codigo}]: '{valor}'."
            logger.registrar("ERROR", msg)
            raise ReservaInvalidaError(msg) from e

    def procesar_y_confirmar(self, **kwargs) -> float:
        """Procesa el cálculo polimórfico del servicio y confirma la reserva."""
        try:
            if self.estado == "Cancelada":
                raise ReservaInvalidaError(f"La reserva [{self._codigo}] está cancelada y no puede confirmarse.")

            # Antes de calcular se comprueba que el servicio siga disponible
            self.servicio.verificar_disponibilidad()

            # Llama polimórficamente a calcular_costo de Sala, Equipo o Asesoría
            self.costo_total = self.servicio.calcular_costo(self.duracion, **kwargs)
            if self.costo_total <= 0:
                raise ReservaInvalidaError("El cálculo de costo resultó en un valor inconsistente ($0 o negativo).")
        except Exception as e:
            self.estado = "Fallida"
            logger.registrar("ERROR", f"Fallo al procesar reserva [{self._codigo}]: {e}")
            raise ReservaInvalidaError(f"No se pudo completar la reserva [{self._codigo}]") from e
        else:
            self.estado = "Confirmada"
            logger.registrar("INFO", f"Reserva [{self._codigo}] CONFIRMADA para {self.cliente.nombre}. Total: ${self.costo_total}")
            return self.costo_total
        finally:
            print(f"   [Auditoría Reserva {self._codigo}] Estado final: {self.estado}")

    def cancelar(self):
        if self.estado == "Cancelada":
            msg = f"La reserva [{self._codigo}] ya se encontraba cancelada."
            logger.registrar("WARNING", msg)
            raise ReservaInvalidaError(msg)
        self.estado = "Cancelada"
        logger.registrar("INFO", f"Reserva [{self._codigo}] CANCELADA por el cliente {self.cliente.nombre}.")

    def obtener_detalles(self) -> str:
        """Implementación obligatoria del método abstracto de EntidadBase."""
        return (f"Reserva [{self._codigo}] | Estado: {self.estado} | "
                f"{self.cliente.nombre} -> {self.servicio.nombre} ({self.duracion} unds) | Total: ${self.costo_total}")
