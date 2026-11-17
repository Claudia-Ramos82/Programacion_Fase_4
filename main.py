from models.servicio import ServicioSalas, ServicioEquipos, ServicioAsesorias
from models.cliente import Cliente
from models.reserva import Reserva
from models.excepciones import SoftwareFJError, ServicioInvalidoError, LoggerSistema

def ejecutar_simulaciones():
    logger = LoggerSistema()
    logger.registrar("INFO", "=== INICIO DE EJECUCIÓN DEL SISTEMA SOFTWARE FJ ===")
    
    print("==================================================")
    print("   SOFTWARE FJ - SISTEMA INTEGRAL DE GESTIÓN     ")
    print("   Orquestación de las 15 Simulaciones Oficiales  ")
    print("==================================================\n")

    # Listas en memoria (sin base de datos, según la guía)
    clientes = []
    servicios = [
        ServicioSalas("S001", 100.0, 20),
        ServicioEquipos("E001", 50.0, "Laptop Dev"),
        ServicioAsesorias("A001", 150.0, "Arquitectura Software")
    ]
    reservas = []

    # --- SIMULACIÓN 1: Registro válido de Cliente 1 ---
    print("--- Simulación 1: Registro válido de Cliente 1 ---")
    try:
        c1 = Cliente("C001", "Deivinson Fontalvo", "1045678901", "deivinson@unad.edu.co")
        clientes.append(c1)
        print(f"  -> Éxito: {c1.obtener_detalles()}")
    except SoftwareFJError as e:
        print(f"  -> Error controlado: {e}")

    # --- SIMULACIÓN 2: Registro válido de Cliente 2 ---
    print("\n--- Simulación 2: Registro válido de Cliente 2 ---")
    try:
        c2 = Cliente("C002", "Claudia Líder", "1098765432", "claudia@unad.edu.co")
        clientes.append(c2)
        print(f"  -> Éxito: {c2.obtener_detalles()}")
    except SoftwareFJError as e:
        print(f"  -> Error controlado: {e}")

    # --- SIMULACIÓN 3: Registro INVÁLIDO de Cliente (documento corto y correo sin @) ---
    print("\n--- Simulación 3: Registro INVÁLIDO de Cliente (Datos erróneos) ---")
    try:
        c_invalido = Cliente("C003", "Jo", "123", "correo_invalido")
        clientes.append(c_invalido)
    except SoftwareFJError as e:
        print(f"  -> Excepción capturada correctamente: {e}")

    # --- SIMULACIÓN 4: Reserva EXITOSA de Sala (con IVA) ---
    print("\n--- Simulación 4: Reserva EXITOSA de Sala (3 horas con IVA) ---")
    try:
        r1 = Reserva("R001", clientes[0], servicios[0], 3)
        total = r1.procesar_y_confirmar(aplicar_iva=True)
        reservas.append(r1)
        print(f"  -> {r1.obtener_detalles()}")
    except SoftwareFJError as e:
        print(f"  -> Error controlado: {e}")

    # --- SIMULACIÓN 5: Reserva EXITOSA de Equipos (con descuento del 15%) ---
    print("\n--- Simulación 5: Reserva EXITOSA de Equipos (5 días, 15% desc.) ---")
    try:
        r2 = Reserva("R002", clientes[1], servicios[1], 5)
        total = r2.procesar_y_confirmar(descuento_porcentaje=15.0)
        reservas.append(r2)
        print(f"  -> {r2.obtener_detalles()}")
    except SoftwareFJError as e:
        print(f"  -> Error controlado: {e}")

    # --- SIMULACIÓN 6: Reserva EXITOSA de Asesoría (con recargo por complejidad) ---
    print("\n--- Simulación 6: Reserva EXITOSA de Asesoría (2 sesiones + recargo) ---")
    try:
        r3 = Reserva("R003", clientes[0], servicios[2], 2)
        total = r3.procesar_y_confirmar(recargo_complejidad=80.0)
        reservas.append(r3)
        print(f"  -> {r3.obtener_detalles()}")
    except SoftwareFJError as e:
        print(f"  -> Error controlado: {e}")

    # --- SIMULACIÓN 7: Reserva FALLIDA por duración inválida (0 o negativa) ---
    print("\n--- Simulación 7: Reserva FALLIDA (Duración negativa) ---")
    try:
        r_err1 = Reserva("R004", clientes[0], servicios[0], -2)
        r_err1.procesar_y_confirmar()
    except SoftwareFJError as e:
        print(f"  -> Excepción capturada correctamente: {e}")

    # --- SIMULACIÓN 8: Reserva FALLIDA por servicio inexistente (None) ---
    print("\n--- Simulación 8: Reserva FALLIDA (Servicio no disponible / None) ---")
    try:
        r_err2 = Reserva("R005", clientes[1], None, 4)
        r_err2.procesar_y_confirmar()
    except SoftwareFJError as e:
        print(f"  -> Excepción capturada correctamente: {e}")

    # --- SIMULACIÓN 9: Cancelación de reserva y reintento de confirmación (Operación no permitida) ---
    print("\n--- Simulación 9: Cancelación de reserva y bloqueo de re-confirmación ---")
    try:
        reservas[0].cancelar()
        print(f"  -> Reserva cancelada: {reservas[0].obtener_detalles()}")
        reservas[0].procesar_y_confirmar()  # Debe fallar porque ya está cancelada
    except SoftwareFJError as e:
        print(f"  -> Operación bloqueada correctamente: {e}")

    # ==================================================================
    # Simulaciones 10 a 14 - Aporte de Jonathan Gómez Lobo
    # Creación correcta e incorrecta de servicios, disponibilidad y
    # métodos sobrecargados de cotización.
    # ==================================================================

    # --- SIMULACIÓN 10: Creación CORRECTA de un nuevo servicio ---
    print("\n--- Simulación 10: Creación CORRECTA de un servicio (Sala auditorio) ---")
    try:
        auditorio = ServicioSalas("S002", 250.0, 80)
    except SoftwareFJError as e:
        print(f"  -> Error controlado: {e}")
    else:
        # El bloque else solo se ejecuta si la creación no lanzó excepciones
        servicios.append(auditorio)
        print(f"  -> Éxito: {auditorio.describir()}")

    # --- SIMULACIÓN 11: Creación INCORRECTA de servicios (datos mal formados) ---
    print("\n--- Simulación 11: Creación INCORRECTA de servicios (tarifa, código y capacidad) ---")
    datos_invalidos = [
        (ServicioEquipos, ("E002", -30.0, "Proyector")),   # Tarifa negativa
        (ServicioAsesorias, ("", 120.0, "Ciberseguridad")),  # Código vacío
        (ServicioSalas, ("S003", "cien", 10)),             # Tarifa no numérica
        (ServicioSalas, ("S004", 90.0, 0)),                # Capacidad en cero
    ]
    for clase, argumentos in datos_invalidos:
        try:
            servicios.append(clase(*argumentos))
        except ServicioInvalidoError as e:
            causa = f" (causa original: {type(e.__cause__).__name__})" if e.__cause__ else ""
            print(f"  -> Servicio rechazado: {e}{causa}")

    # --- SIMULACIÓN 12: Reserva FALLIDA porque el servicio NO está disponible ---
    print("\n--- Simulación 12: Reserva FALLIDA (servicio en mantenimiento) ---")
    servicios[1].desactivar("mantenimiento preventivo")
    try:
        r_err3 = Reserva("R006", clientes[1], servicios[1], 2)
        r_err3.procesar_y_confirmar()
    except SoftwareFJError as e:
        print(f"  -> Excepción capturada correctamente: {e}")
        print(f"     Causa encadenada: {type(e.__cause__).__name__}: {e.__cause__}")
    finally:
        # El finally siempre deja el equipo activo de nuevo para las demás operaciones
        servicios[1].activar()
        print("  -> El equipo vuelve a quedar disponible (bloque finally).")

    # --- SIMULACIÓN 13: Cálculo con parámetros inválidos (descuento del 150 %) ---
    print("\n--- Simulación 13: Cálculo FALLIDO por parámetros inválidos ---")
    try:
        r_err4 = Reserva("R007", clientes[0], servicios[1], 3)
        r_err4.procesar_y_confirmar(descuento_porcentaje=150.0)
    except SoftwareFJError as e:
        print(f"  -> Excepción capturada correctamente: {e}")
        print(f"     Causa encadenada: {type(e.__cause__).__name__}: {e.__cause__}")

    # --- SIMULACIÓN 14: Métodos sobrecargados de cotización ---
    print("\n--- Simulación 14: Cotización con métodos sobrecargados ---")
    asesoria = servicios[2]
    cotizaciones = [
        ("Entero (2 sesiones)", 2),
        ("Diccionario (3 sesiones + recargo)", {"cantidad": 3, "recargo_complejidad": 60.0}),
        ("Lista (pedidos de 1, 2 y 4 sesiones)", [1, 2, 4]),
        ("Diccionario sin 'cantidad' (inválido)", {"recargo_complejidad": 10.0}),
        ("Texto (tipo no soportado)", "tres"),
    ]
    for descripcion, argumento in cotizaciones:
        try:
            valor = asesoria.cotizar(argumento)
            print(f"  -> {descripcion}: ${valor}")
        except SoftwareFJError as e:
            print(f"  -> {descripcion}: rechazada -> {e}")

    # --- SIMULACIÓN 15: Reporte polimórfico general de entidades en memoria ---
    print("\n--- Simulación 15: Reporte Polimórfico de Todas las Entidades ---")
    entidades = clientes + servicios + reservas
    for entidad in entidades:
        print(f"  * {entidad.obtener_detalles()}")

    logger.registrar("INFO", "=== FIN DE EJECUCIÓN SIN INTERRUPCIONES ===")
    print("\n==================================================")
    print(" EJECUCIÓN FINALIZADA CON ÉXITO. Revise sistema_logs.txt")
    print("==================================================")

if __name__ == "__main__":
    ejecutar_simulaciones()
