from abc import ABC, abstractmethod

class EntidadBase(ABC):
    """Clase abstracta general que representa cualquier entidad principal del sistema."""
    
    def __init__(self, codigo: str):
        self._codigo = codigo

    @property
    def codigo(self) -> str:
        return self._codigo

    @abstractmethod
    def obtener_detalles(self) -> str:
        """Método abstracto que deben implementar todas las clases hijas."""
        pass