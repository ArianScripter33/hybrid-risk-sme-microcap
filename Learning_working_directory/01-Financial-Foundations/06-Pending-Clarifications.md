# Clarificaciones de Cierre Día 1

## Precisión Numérica

- **float:** Números con decimales, pero imprecisos (`0.1 + 0.2 = 0.30000000000000004` en Python).
- **Decimal:** Precisión exacta para centavos. Bancos usan esto en producción.
- **Decisión MVP:** Usamos `float` con `round()` defensivo. Migraremos a `Decimal` en semana 8.

## Sobre el LTV (Loan-to-Value)

- **No es un evento de cobro.** Es una métrica de análisis **ex-ante** (antes de prestar).
- **Fórmula:** `LTV = Monto Préstamo / Valor Colateral`.
- **Interpretación:** LTV 80% = Prestas $80k sobre un activo de $100k. Tienes $20k de "colchón" si tienes que rematar el activo.
