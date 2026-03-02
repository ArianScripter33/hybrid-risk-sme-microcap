# Biblia de Acrónimos y Métricas Operativas 📖

Este documento desglosa los términos técnicos que alimentarán los algoritmos de cálculo del motor.

---

## 🏗️ 1. Conceptos de Costo

- **COGS (Cost of Goods Sold):** Costos variables directos. La madera de la silla.
- **OpEx (Operating Expense):** Gastos fijos operativos. El alquiler del taller donde haces las sillas.

---

## ⏱️ 2. El Ciclo de Conversión de Efectivo (CCC)

Es la métrica de tiempo que mide la eficiencia de la "tubería" de dinero.

### DIO (Days Inventory Outstanding) - Días de Inventario

- **Fórmula:** `(Inventario Promedio / COGS Anual) * 365`
- **En el código:** `src.calculation.metrics.calculate_dio()`

### DSO (Days Sales Outstanding) - Días de Cobro

- **Fórmula:** `(Cuentas por Cobrar / Ventas Anuales) * 365`
- **En el código:** `src.calculation.metrics.calculate_dso()`

### DPO (Days Payable Outstanding) - Días de Pago

- **Fórmula:** `(Cuentas por Pagar / COGS Anual) * 365`
- **En el código:** `src.calculation.metrics.calculate_dpo()`

---

## ⚡ 3. La Regla de Oro del Cash Flow

$$CCC = DIO + DSO - DPO$$

> **Interpretación para el Motor de Riesgo:**
>
> - Un **CCC mayor a 90 días** en una empresa sin ahorros es una "trampa de muerte" de liquidez.
> - Una empresa con **CCC Negativo** (ej. Amazon) es una joya crediticia porque genera cash antes de pagar deudas.
