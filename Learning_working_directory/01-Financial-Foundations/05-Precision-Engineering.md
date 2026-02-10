# Precisión Computacional: `float` vs `Decimal` 🧮

## La Paradoja: ¿Por qué mi computadora no sabe sumar dinero?

Tú preguntaste: *"¿El decimal es otra forma de representar igual operaciones de punto flotante o solo son redondeados? ¿Literal decimal son solo números enteros?"*

### 1. El Problema del `float` (Binario)

Las computadoras piensan en **binario** (0s y 1s).

- El número `0.5` (1/2) es fácil en binario: `0.1`.
- Pero el número `0.1` (1/10) es **infinito periódico** en binario (como 1/3 es 0.3333... en decimal).
- La computadora tiene que cortar la secuencia en algún punto. Eso genera un **error de precisión**.

```python
# Inténtalo en tu terminal python:
>>> 0.1 + 0.2
0.30000000000000004  # <--- ERROR! Debería ser 0.3
```

**Riesgo Bancario:** Si sumas millones de transacciones de centavos con este error, al final del día te faltan (o sobran) dólares reales. Eso es inaudito en contabilidad.

### 2. La Solución: `Decimal` (Base 10)

La librería `decimal` de Python no usa la CPU binaria directamente para calcular. Usa un algoritmo de software para simular cómo los humanos hacemos matemáticas en papel (base 10).

- **No son solo enteros.** `Decimal` maneja puntos decimales con perfección absoluta.
- `Decimal('0.1')` es, internamente, exactamente un décimo.

```python
from decimal import Decimal
>>> Decimal('0.1') + Decimal('0.2')
Decimal('0.3')  # <--- EXACTO.
```

### 3. Decisión de Arquitectura

- **float:** Rápido. Inexacto. Bueno para ciencia (física, ML).
- **Decimal:** Lento. Exacto. Obligatorio para dinero (Fintech).

> **En nuestro código:** Por ahora usaremos `float` porque es más fácil de escribir, pero pondremos `round(x, 2)` defensivos. En la Fase 4 (Excel Builder), migraremos a `Decimal` para garantizar que el Balance cuadre al centavo.
