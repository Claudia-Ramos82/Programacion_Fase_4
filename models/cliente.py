from models.base import EntidadBase
from models.excepciones import ClienteInvalidoError, LoggerSistema

logger = LoggerSistema()

class Cliente(EntidadBase):
    """Clase Cliente que hereda de EntidadBase con encapsulación y validaciones estrictas."""
    
    def __init__(self, codigo: str, nombre: str, documento: str, correo: str):
        super().__init__(codigo)
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        logger.registrar("INFO", f"Cliente registrado exitosamente: [{self.codigo}] {self.nombre}")

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            msg = f"Error al validar nombre de cliente ('{valor}'): mínimo 3 caracteres."
            logger.registrar("ERROR", msg)
            raise ClienteInvalidoError(msg)
        self.__nombre = valor.strip()

    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor: str):
        doc = str(valor).strip()
        if not doc.isdigit() or len(doc) < 6:
            msg = f"Error al validar documento ('{valor}'): debe ser numérico y tener mínimo 6 dígitos."
            logger.registrar("ERROR", msg)
            raise ClienteInvalidoError(msg)
        self.__documento = doc

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            msg = f"Error al validar correo ('{valor}'): formato inválido."
            logger.registrar("ERROR", msg)
            raise ClienteInvalidoError(msg)
        self.__correo = valor.strip()

    def obtener_detalles(self) -> str:
        """Implementación obligatoria del método abstracto de EntidadBase."""
        return f"Cliente [{self._codigo}]: {self.__nombre} | Doc: {self.__documento} | Correo: {self.__correo}"