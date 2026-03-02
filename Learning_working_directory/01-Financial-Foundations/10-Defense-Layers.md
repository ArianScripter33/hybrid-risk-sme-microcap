# Las 3 Capas de Defensa del Código Financiero 🛡️

En finanzas, un bug no es una molestia; es una pérdida de dinero. Por eso usamos una arquitectura de "Defensa en Profundidad".

---

## 🛑 Capa 1: RUFF (El Policía de Tráfico)

*Misión: Higiene y Estilo.*

**Lo que detecta:**

- Imports no usados.
- Variables con nombres ambiguos (`x`, `y`).
- Complejidad innecesaria.

**Ejemplo:**

```python
import os  # Error: Unused import
def calc(x): return x * 2  # Warning: Variable 'x' is ambiguous
```

---

## 🏗️ Capa 2: MYPY (El Ingeniero Estructural)

*Misión: Coherencia Lógica (Tipos).*

**Lo que detecta:**

- Intentar sumar un número con un texto.
- Funciones que prometen devolver `float` y devuelven `None`.
- Errores de lógica que harían colapsar el programa en runtime.

**Ejemplo Real:**

```python
def get_roi(invested: float) -> float:
    return invested * "0.10"  # Error MyPy: Operator '*' not supported for types 'float' and 'str'
```

*MyPy te salva ANTES de que el código llegue al servidor.*

---

## 🛡️ Capa 3: PYDANTIC (El Cadenero)

*Misión: Integridad de Datos (Runtime).*

**Lo que detecta:**

- Datos basura que vienen de fuera (JSONs, PDFs, excels).
- Números negativos donde debe haber positivos.
- Strings vacíos o emails mal formados.

**Ejemplo Letal:**

```python
class Loan(BaseModel):
    amount: PositiveFloat

# Input: {"amount": -5000}
# Pydantic: ValidationError "Input should be greater than 0"
```

*Si Pydantic no atrapa esto, podrías "prestar" dinero negativo (¡regalar dinero!).*

---

> **Filosofía:**
>
> 1. Ruff mantiene la casa limpia.
> 2. MyPy asegura que los cimientos aguanten.
> 3. Pydantic asegura que no entren ladrones.
