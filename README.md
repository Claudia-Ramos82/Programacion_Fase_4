# Software FJ - Sistema Integral de Gestión (Fase 4)

Aplicación desarrollada en Python bajo el paradigma de Programación Orientada a Objetos (POO) para la gestión de servicios y reservas, sin uso de bases de datos.

## Estructura del Proyecto
- `models/`: Clases principales del sistema (Entidades abstractas y servicios especializados).
- `main.py`: Orquestador principal con la ejecución de las 15 simulaciones (casos válidos e inválidos).

## Autores y Roles
- **Claudia Ramos (Líder)**: Arquitectura base, jerarquía de servicios, polimorfismo, métodos sobrecargados y orquestación de simulaciones.
- **Jonathan Gómez Lobo**: Validación estricta de servicios (`ServicioInvalidoError`, `ParametroServicioError`, `CalculoInconsistenteError`), control de disponibilidad (`activar`, `desactivar`, `verificar_disponibilidad`), métodos sobrescritos `validar_parametros()` y `describir()`, método sobrecargado `cotizar()` (entero, diccionario y lista) y simulaciones 10 a 14 (creación correcta e incorrecta de servicios, servicio no disponible, parámetros inválidos y cotizaciones).

## Ejecución
```bash
python main.py
```
Los eventos y errores quedan registrados en `sistema_logs.txt`.
