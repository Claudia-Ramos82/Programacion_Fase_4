from models.servicio import ServicioSalas, ServicioEquipos, ServicioAsesorias

def ejecutar_simulaciones():
    print("==================================================")
    print("   SOFTWARE FJ - SISTEMA INTEGRAL DE GESTIÓN     ")
    print("   Orquestación de las 10 Simulaciones Oficiales  ")
    print("==================================================\n")

    # Inicialización de servicios de prueba
    sala = ServicioSalas("S001", 100.0, 20)
    equipo = ServicioEquipos("E001", 50.0, "Laptop Dev")
    asesoria = ServicioAsesorias("A001", 150.0, "Arquitectura Software")

    simulaciones = [
        ("Simulación 1 (Válido - Salas con IVA)", lambda: sala.calcular_costo(horas=3, aplicar_iva=True)),
        ("Simulación 2 (Válido - Salas sin IVA)", lambda: sala.calcular_costo(horas=2, aplicar_iva=False)),
        ("Simulación 3 (Válido - Equipos 5 días)", lambda: equipo.calcular_costo(dias=5)),
        ("Simulación 4 (Válido - Equipos con Descuento)", lambda: equipo.calcular_costo(dias=4, descuento_porcentaje=10.0)),
        ("Simulación 5 (Válido - Asesoría 2 sesiones)", lambda: asesoria.calcular_costo(sesiones=2)),
        ("Simulación 6 (Válido - Asesoría con Recargo)", lambda: asesoria.calcular_costo(sesiones=1, recargo_complejidad=50.0)),
        ("Simulación 7 (Prueba límite - 0 horas sala)", lambda: sala.calcular_costo(horas=0)),
        ("Simulación 8 (Prueba límite - 10 días equipo)", lambda: equipo.calcular_costo(dias=10, descuento_porcentaje=25.0)),
        ("Simulación 9 (Prueba límite - Múltiples sesiones)", lambda: asesoria.calcular_costo(sesiones=5, recargo_complejidad=100.0)),
        ("Simulación 10 (Prueba polimórfica general)", lambda: [s.obtener_detalles() for s in [sala, equipo, asesoria]])
    ]

    for i, (descripcion, operacion) in enumerate(simulaciones, 1):
        print(f"--- {descripcion} ---")
        try:
            resultado = operacion()
            if isinstance(resultado, list):
                for detalle in resultado:
                    print(f"  > {detalle}")
            else:
                print(f"  -> Resultado obtenido exitosamente: ${resultado}")
        except Exception as e:
            print(f"  -> Excepción controlada capturada: {e}")
        print("-" * 50)

if __name__ == "__main__":
    ejecutar_simulaciones()