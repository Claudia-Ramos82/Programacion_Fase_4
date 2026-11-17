"""
Módulo de servicios de Software FJ.

Contiene la clase abstracta Servicio y sus tres especializaciones:
ServicioSalas, ServicioEquipos y ServicioAsesorias.

Aporte de Jonathan Gómez Lobo:
- Validación estricta de los datos al crear un servicio (ServicioInvalidoError).
- Método sobrescrito validar_parametros() en cada servicio (ParametroServicioError).
- Método sobrescrito describir() con la descripción propia de cada servicio.
- Control de disponibilidad: activar(), desactivar() y verificar_disponibilidad()
  (ServicioNoDisponibleError).
- Método sobrecargado cotizar() con singledispatchmethod: acepta un entero,
  un diccionario de opciones o una lista de cantidades.
- Validación del resultado de cada cálculo (CalculoInconsistenteError).
"""

from abc import abstractmethod
from functools import singledispatchmethod

from models.base import EntidadBase
from models.excepciones import (
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    ParametroServicioError,
    CalculoInconsistenteError,
    LoggerSistema,
)

# Logger compartido por todos los servicios (escribe en sistema_logs.txt)
logger = LoggerSistema()

IVA = 0.19  # Impuesto al valor agregado aplicado en Colombia (19 %)


class Servicio(EntidadBase):
    """Clase abstracta Servicio que hereda de EntidadBase."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float):
        # Se valida el código antes de llamar al constructor de la clase base
        if not isinstance(codigo, str) or not codigo.strip():
            msg = f"No se puede crear el servicio '{nombre}': el código está vacío o no es texto."
            logger.registrar("ERROR", msg)
            raise ServicioInvalidoError(msg)
        super().__init__(codigo.strip())
        self.nombre = nombre
        self.tarifa_base = tarifa_base      # Pasa por el setter con validación
        self._disponible = True             # Todo servicio nace disponible

    # ------------------------------------------------------------------
    # Encapsulación de la tarifa base
    # ------------------------------------------------------------------
    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float):
        try:
            tarifa = float(valor)
        except (TypeError, ValueError) as e:
            msg = f"Tarifa inválida para el servicio [{self._codigo}]: '{valor}' no es numérica."
            logger.registrar("ERROR", msg)
            # Encadenamiento: se conserva el error original de conversión
            raise ServicioInvalidoError(msg) from e
        if tarifa <= 0:
            msg = f"Tarifa inválida para el servicio [{self._codigo}]: debe ser mayor a cero (recibido {tarifa})."
            logger.registrar("ERROR", msg)
            raise ServicioInvalidoError(msg)
        self._tarifa_base = tarifa

    # ------------------------------------------------------------------
    # Disponibilidad del servicio
    # ------------------------------------------------------------------
    @property
    def disponible(self) -> bool:
        return self._disponible

    def activar(self):
        """Marca el servicio como disponible para nuevas reservas."""
        self._disponible = True
        logger.registrar("INFO", f"Servicio [{self._codigo}] {self.nombre} ACTIVADO.")

    def desactivar(self, motivo: str = "mantenimiento"):
        """Marca el servicio como no disponible (por ejemplo, en mantenimiento)."""
        self._disponible = False
        logger.registrar("WARNING", f"Servicio [{self._codigo}] {self.nombre} DESACTIVADO por {motivo}.")

    def verificar_disponibilidad(self):
        """Lanza ServicioNoDisponibleError si el servicio no puede reservarse."""
        if not self._disponible:
            msg = f"El servicio [{self._codigo}] {self.nombre} no está disponible en este momento."
            logger.registrar("ERROR", msg)
            raise ServicioNoDisponibleError(msg)

    # ------------------------------------------------------------------
    # Métodos abstractos que cada servicio debe sobrescribir
    # ------------------------------------------------------------------
    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """Método polimórfico para el cálculo de costos."""
        pass

    @abstractmethod
    def validar_parametros(self, cantidad, **kwargs):
        """Valida los parámetros de cálculo propios de cada servicio."""
        pass

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción comercial propia de cada servicio."""
        pass

    # ------------------------------------------------------------------
    # Utilidades comunes
    # ------------------------------------------------------------------
    def _validar_cantidad(self, cantidad, unidad: str):
        """Comprueba que la cantidad (horas, días o sesiones) sea un entero positivo."""
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            msg = f"[{self._codigo}] La cantidad de {unidad} debe ser un entero mayor a cero (recibido '{cantidad}')."
            logger.registrar("ERROR", msg)
            raise ParametroServicioError(msg)

    def _verificar_total(self, total: float) -> float:
        """Comprueba que el total calculado sea coherente antes de devolverlo."""
        if not isinstance(total, (int, float)) or total <= 0:
            msg = f"[{self._codigo}] Cálculo inconsistente: el total obtenido fue {total}."
            logger.registrar("ERROR", msg)
            raise CalculoInconsistenteError(msg)
        return round(total, 2)

    # ------------------------------------------------------------------
    # Método sobrecargado: cotizar()
    # Python no admite sobrecarga clásica; singledispatchmethod elige la
    # implementación según el tipo del primer argumento.
    # ------------------------------------------------------------------
    @singledispatchmethod
    def cotizar(self, argumento):
        msg = f"[{self._codigo}] Tipo de cotización no soportado: {type(argumento).__name__}."
        logger.registrar("ERROR", msg)
        raise ParametroServicioError(msg)

    @cotizar.register
    def _(self, cantidad: int) -> float:
        """Variante 1: cotización simple con la cantidad y opciones por defecto."""
        return self.calcular_costo(cantidad)

    @cotizar.register
    def _(self, opciones: dict) -> float:
        """Variante 2: cotización con un diccionario de opciones
        (ejemplo: {'cantidad': 3, 'descuento_porcentaje': 10})."""
        datos = dict(opciones)
        if "cantidad" not in datos:
            msg = f"[{self._codigo}] Falta el parámetro obligatorio 'cantidad' en la cotización."
            logger.registrar("ERROR", msg)
            raise ParametroServicioError(msg)
        cantidad = datos.pop("cantidad")
        return self.calcular_costo(cantidad, **datos)

    @cotizar.register
    def _(self, cantidades: list) -> float:
        """Variante 3: cotización acumulada de varias cantidades (varios pedidos)."""
        if not cantidades:
            msg = f"[{self._codigo}] La lista de cantidades está vacía."
            logger.registrar("ERROR", msg)
            raise ParametroServicioError(msg)
        return round(sum(self.calcular_costo(c) for c in cantidades), 2)

    def obtener_detalles(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return f"Servicio [{self._codigo}]: {self.nombre} - Tarifa Base: ${self._tarifa_base} - {estado}"


class ServicioSalas(Servicio):
    """Servicio especializado 1: Reserva de salas para reuniones o conferencias."""

    def __init__(self, codigo: str, tarifa_base: float, capacidad: int):
        super().__init__(codigo, "Reserva de Salas", tarifa_base)
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            msg = f"No se puede crear la sala [{codigo}]: la capacidad debe ser un entero positivo (recibido '{capacidad}')."
            logger.registrar("ERROR", msg)
            raise ServicioInvalidoError(msg)
        self.capacidad = capacidad
        logger.registrar("INFO", f"Servicio creado: [{self._codigo}] Sala para {capacidad} personas.")

    def validar_parametros(self, cantidad, aplicar_iva: bool = True, **kwargs):
        self._validar_cantidad(cantidad, "horas")
        if not isinstance(aplicar_iva, bool):
            msg = f"[{self._codigo}] El parámetro aplicar_iva debe ser True o False."
            logger.registrar("ERROR", msg)
            raise ParametroServicioError(msg)

    def calcular_costo(self, horas: int = 1, aplicar_iva: bool = True) -> float:
        self.validar_parametros(horas, aplicar_iva=aplicar_iva)
        subtotal = self.tarifa_base * horas
        if aplicar_iva:
            subtotal *= (1 + IVA)
        return self._verificar_total(subtotal)

    def describir(self) -> str:
        return (f"Sala [{self._codigo}] con capacidad para {self.capacidad} personas, "
                f"a ${self.tarifa_base} por hora (IVA del 19 % opcional).")


class ServicioEquipos(Servicio):
    """Servicio especializado 2: Alquiler de equipos tecnológicos."""

    def __init__(self, codigo: str, tarifa_base: float, tipo_equipo: str):
        super().__init__(codigo, "Alquiler de Equipos", tarifa_base)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            msg = f"No se puede crear el alquiler [{codigo}]: el tipo de equipo es obligatorio."
            logger.registrar("ERROR", msg)
            raise ServicioInvalidoError(msg)
        self.tipo_equipo = tipo_equipo.strip()
        logger.registrar("INFO", f"Servicio creado: [{self._codigo}] Alquiler de {self.tipo_equipo}.")

    def validar_parametros(self, cantidad, descuento_porcentaje: float = 0.0, **kwargs):
        self._validar_cantidad(cantidad, "días")
        if not isinstance(descuento_porcentaje, (int, float)) or not 0 <= descuento_porcentaje < 100:
            msg = f"[{self._codigo}] Descuento fuera de rango: debe estar entre 0 y 99 % (recibido {descuento_porcentaje})."
            logger.registrar("ERROR", msg)
            raise ParametroServicioError(msg)

    def calcular_costo(self, dias: int = 1, descuento_porcentaje: float = 0.0) -> float:
        self.validar_parametros(dias, descuento_porcentaje=descuento_porcentaje)
        subtotal = self.tarifa_base * dias
        if descuento_porcentaje > 0:
            subtotal *= (1 - (descuento_porcentaje / 100))
        return self._verificar_total(subtotal)

    def describir(self) -> str:
        return (f"Alquiler [{self._codigo}] de {self.tipo_equipo} a ${self.tarifa_base} por día "
                f"(admite descuentos de 0 a 99 %).")


class ServicioAsesorias(Servicio):
    """Servicio especializado 3: Asesorías técnicas especializadas."""

    def __init__(self, codigo: str, tarifa_base: float, area_especialidad: str):
        super().__init__(codigo, "Asesorías Especializadas", tarifa_base)
        if not isinstance(area_especialidad, str) or len(area_especialidad.strip()) < 3:
            msg = f"No se puede crear la asesoría [{codigo}]: el área de especialidad es obligatoria."
            logger.registrar("ERROR", msg)
            raise ServicioInvalidoError(msg)
        self.area_especialidad = area_especialidad.strip()
        logger.registrar("INFO", f"Servicio creado: [{self._codigo}] Asesoría en {self.area_especialidad}.")

    def validar_parametros(self, cantidad, recargo_complejidad: float = 0.0, **kwargs):
        self._validar_cantidad(cantidad, "sesiones")
        if not isinstance(recargo_complejidad, (int, float)) or recargo_complejidad < 0:
            msg = f"[{self._codigo}] El recargo por complejidad no puede ser negativo (recibido {recargo_complejidad})."
            logger.registrar("ERROR", msg)
            raise ParametroServicioError(msg)

    def calcular_costo(self, sesiones: int = 1, recargo_complejidad: float = 0.0) -> float:
        self.validar_parametros(sesiones, recargo_complejidad=recargo_complejidad)
        subtotal = (self.tarifa_base * sesiones) + recargo_complejidad
        return self._verificar_total(subtotal)

    def describir(self) -> str:
        return (f"Asesoría [{self._codigo}] en {self.area_especialidad} a ${self.tarifa_base} por sesión "
                f"(con recargo opcional por complejidad).")
