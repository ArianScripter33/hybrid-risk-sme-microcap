# Conceptos Financieros - Día 1: Fundamentos del Arquitecto 🏛️

Este índice rastrea el progreso de aprendizaje en el **Día 1** del Master Plan. Aquí es donde transformamos la "Contabilidad Escolar" en **Ingeniería de Riesgo**.

## 📚 I. La Estructura Atómica (Data DNA)

### 1.1 Precisión Computacional: `float` vs. `Decimal`

- **Concepto:** La aritmética binaria (`float`) tiene errores de redondeo inherentes.
- **Riesgo:** En banca, perder centavos es un riesgo legal y financiero.
- **Solución:** Usar `Decimal` para precisión exacta monetaria, aunque para el MVP usaremos `float` con redondeo defensivo.
- [Leer más](./01-Financial-Foundations/05-Precision-Engineering.md)

### 1.2 Reconciliación Contable (Checksum)

- **Concepto:** Principio de Partida Doble. La ecuación `Assets = Liabilities + Equity` es inquebrantable.
- **Implementación:** `model_validator` en Pydantic actúa como "checksum" de integridad de datos.
- [Leer más](./01-Financial-Foundations/01-The-Accounting-Equation.md)

## 💰 II. El Mapa de los Activos (Liquidez y Colateral)

### 2.1 Jerarquía de Liquidez: Circulante vs. No Circulante

- **Concepto:** Velocidad de conversión a efectivo.
- **Circulante (Current):** <12 meses (Cash, Inventario). La "sangre" del negocio.
- **No Circulante (Fixed):** >12 meses (Maquinaria, Edificios). El "esqueleto" del negocio.
- [Leer más](./01-Financial-Foundations/02-Liquidity-Hierarchy.md)

### 2.2 Activos Fijos y Colateral (LTV)

- **Concepto:** Activos que respaldan un préstamo.
- **LTV (Loan-to-Value):** Ratio de seguridad (`Monto Préstamo / Valor Garantía`).x
- [Leer más](./01-Financial-Foundations/04-LTV-and-Collateral.md)

## 📊 III. La Clasificación del Gasto (P&L Dynamics)

### 3.1 CapEx vs. OpEx vs. COGS

- **CapEx:** Inversión a largo plazo (Activo). Drena caja hoy, se deprecia mañana.
- **OpEx:** Gasto operativo recurrente (Luz, Renta). Impacto inmediato en utilidad.
- **COGS:** Costo directo de ventas. Eficiencia pura de producción.
- [Leer más](./01-Financial-Foundations/03-CapEx-OpEx-COGS.md)

## 🛡️ IV. El Framework del Prestamista

### 4.1 El Memorándum de Crédito

- **Concepto:** El "Producto Final" que aprueba o rechaza el dinero.
- **Rol del Agente:** Traducir matemáticas (Python) a narrativa bancaria (Claude).

---

> **Regla de Oro:** "Ventas es vanidad, Utilidad es sanidad, Caja es realidad."
