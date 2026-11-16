import datetime

# --- EXCEPCIONES PERSONALIZADAS ---
class SoftwareFJError(Exception):
    """Excepción base para todo el sistema Software FJ."""
    pass

class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no pasan las validaciones."""
    pass

class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando un servicio no existe, está inactivo o tiene parámetros inválidos."""
    pass

class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva tiene datos erróneos o falla al procesarse."""
    pass


# --- SISTEMA DE REGISTRO DE LOGS ---
class LoggerSistema:
    """Gestiona la escritura segura de eventos y errores en un archivo plano."""
    
    def __init__(self, ruta_archivo: str = "sistema_logs.txt"):
        self.ruta_archivo = ruta_archivo

    def registrar(self, nivel: str, mensaje: str):
        """Registra un evento o error aplicando try/except/else/finally."""
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registro = f"[{fecha_hora}] [{nivel.upper()}] {mensaje}\n"
        archivo = None
        try:
            archivo = open(self.ruta_archivo, "a", encoding="utf-8")
            archivo.write(registro)
        except OSError as e:
            # Encadenamiento de excepciones exigido en la rúbrica
            raise RuntimeError("Error crítico de E/S al intentar escribir en el archivo de logs.") from e
        else:
            pass  # Escritura confirmada sin errores
        finally:
            if archivo and not archivo.closed:
                archivo.close()