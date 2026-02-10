# Partida Doble: La Verdad Contable

## Concepto

Toda transacción contable afecta **dos** cuentas. No desaparece el dinero, cambia de forma.

$$Activos = Pasivos + Capital$$

- **Activos (Lo que tienes):** Dinero, mercancía, fábrica.
- **Financiamiento (Cómo lo tienes):**
  - **Pasivos (Deuda):** Dinero ajeno (banco, proveedores).
  - **Capital (Equity):** Dinero propio (inversión inicial, ganancias reinvertidas).

## Checksum en Pydantic

En nuestro motor, esta ecuación actúa como un **Checksum de Integridad de Datos**. Si `Total Assets` no cuadra con la suma de `Liabilities` y `Equity`, significa que el OCR leyó mal un número o la contabilidad original está corrupta.

```python
@model_validator(mode='after')
def check_accounting_equation(self) -> 'BalanceSheet':
    tolerance = 1.0  # Tolerancia de $1 por errores de redondeo en PDFs
    diff = abs(self.total_assets - (self.total_liabilities + self.total_equity))
    if diff > tolerance:
        raise ValueError(f"Accounting Equation Breach: Diff ${diff}")
    return self
```
