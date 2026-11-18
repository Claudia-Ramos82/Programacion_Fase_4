"""
Ejecutor de simulaciones de casos inválidos.

Cada caso intenta hacer algo que NO debería permitirse (horas negativas,
descuentos imposibles, datos de tipo incorrecto, etc.) y se clasifica así:

  - DETECTADO:    el sistema lanzó una excepción y la aplicación siguió viva.
  - NO DETECTADO: el sistema aceptó el dato inválido y devolvió un resultado
                  sin avisar. Es una señal de que falta una validación.

Ningún caso puede detener el programa: todas las excepciones se capturan aquí.
"""

DETECTADO = "DETECTADO"
NO_DETECTADO = "NO DETECTADO"


class Simulador:
    """Ejecuta casos inválidos uno por uno y lleva la cuenta de los resultados."""

    def __init__(self):
        self.resultados = []  # lista de (numero, descripcion, estado)

    def ejecutar(self, descripcion: str, operacion) -> str:
        """Corre `operacion` (una función sin argumentos) y devuelve el estado del caso."""
        numero = len(self.resultados) + 1
        print(f"--- Simulación inválida {numero}: {descripcion}")
        try:
            resultado = operacion()
        except Exception as error:  # el sistema debe seguir en pie ante cualquier fallo
            estado = DETECTADO
            detalle = f"{type(error).__name__}: {error}"
        else:
            estado = NO_DETECTADO
            if hasattr(resultado, "obtener_detalles"):
                # Se creó un objeto con datos inválidos: se muestra su descripción.
                detalle = f"el sistema creó un objeto inválido -> {resultado.obtener_detalles()}"
            else:
                detalle = f"el sistema aceptó el dato inválido y devolvió: {resultado!r}"
        print(f"    [{estado}] {detalle}")
        self.resultados.append((numero, descripcion, estado))
        return estado

    def resumen(self) -> None:
        """Imprime cuántos casos se detectaron y cuáles quedaron sin validar."""
        total = len(self.resultados)
        detectados = sum(1 for _, _, estado in self.resultados if estado == DETECTADO)
        sin_detectar = [(n, d) for n, d, estado in self.resultados if estado == NO_DETECTADO]

        print("\n" + "=" * 70)
        print("RESUMEN DE SIMULACIONES INVÁLIDAS")
        print("=" * 70)
        print(f"Casos ejecutados : {total}")
        print(f"Detectados       : {detectados}")
        print(f"No detectados    : {len(sin_detectar)}")
        if sin_detectar:
            print("\nCasos que el sistema aceptó sin validar (candidatos a mejora):")
            for numero, descripcion in sin_detectar:
                print(f"  - #{numero}: {descripcion}")
        print("\nLa aplicación terminó sin caerse.")
