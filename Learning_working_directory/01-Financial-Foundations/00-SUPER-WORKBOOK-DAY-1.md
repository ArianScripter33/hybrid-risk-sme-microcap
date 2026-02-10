# 📕 SUPER WORKBOOK - DÍA 1: Fundamentos del Arquitecto de Riesgo

Este documento consolida los pilares financieros, técnicos y de riesgo aprendidos hoy. Es tu "Manual de Operaciones" para el desarrollo del **Hybrid Risk Engine**.

---

## 🏗️ 0. El Concepto de "Scaffold"

En ingeniería de software, un **Scaffold** (andamiaje) es el esqueleto inicial de un proyecto. Proporciona la estructura de carpetas, archivos de configuración (Poetry) y el código base necesario para que la aplicación crezca sin desorden. Hoy construimos el scaffold legal y financiero de nuestro motor.

---

## 🧮 1. Precisión Computacional: `float` vs `Decimal`

*Basado en [05-Precision-Engineering.md](./05-Precision-Engineering.md)*

### La Paradoja: ¿Por qué mi computadora no sabe sumar dinero?

Las computadoras piensan en **binario** (base 2). El número `0.1` es infinito periódico en binario, lo que genera errores de redondeo.

- **`float` (Binario):** Rápido pero inexacto. `0.1 + 0.2 = 0.30000000000000004`.
- **`Decimal` (Base 10):** Exactitud absoluta. Obligatorio en banca para evitar que los centavos "desaparezcan".

**Decisión Técnica:** Usaremos `Decimal` para el motor de producción para garantizar que el Balance cuadre al centavo.

---

## ⚖️ 2. Partida Doble: La Verdad Contable

*Basado en [01-The-Accounting-Equation.md](./01-The-Accounting-Equation.md)*

### La Ecuación Fundamental

$$Activos = Pasivos + Capital$$

- **Activos:** Lo que la empresa TIENE.
- **Pasivos:** Lo que la empresa DEBE a terceros.
- **Capital (Equity):** Lo que pertenece a los DUEÑOS.

**Checksum en Pydantic:** Usamos esta ecuación como un validador de integridad. Si el OCR lee mal un número y la ecuación no cuadra, el sistema detiene el proceso inmediatamente.

---

## 🩸 3. Jerarquía de Liquidez: Circulante vs. No Circulante

*Basado en [02-Liquidity-Hierarchy.md](./02-Liquidity-Hierarchy.md)*

### Liquidez = Velocidad de Conversión a Cash

1. **Activos Circulantes (RAM):** Efectivo, Inventario, Cuentas por Cobrar. (< 12 meses).
2. **Activos No Circulantes (Disco Duro):** Maquinaria, Edificios, Patentes. (> 12 meses).

### El Pulmón: Working Capital (Capital de Trabajo)

Es el dinero libre para operar mañana: `Activos Circulantes - Pasivos Circulantes`.

- **Positivo:** Salud.
- **Negativo:** Colapso inminente (no hay dinero para la nómina del viernes).

> **Riesgo AR:** Si las ventas suben pero las "Cuentas por Cobrar" (AR) suben más, la empresa está "muriendo de éxito": vende mucho pero nadie le paga real.

---

## 🏭 4. Clasificación de Costos: CapEx, OpEx y COGS

*Basado en [03-CapEx-OpEx-COGS.md](./03-CapEx-OpEx-COGS.md)*

### La Trinidad del Gasto

- **COGS (Cost of Goods Sold):** Costo variable directo de ventas. Eficiencia de producción.
- **OpEx (Operating Expense):** Costos fijos (Renta, Nómina técnica). Fragilidad del negocio.
- **CapEx (Capital Expenditure):** Inversión en activos (Hardware). Drena caja hoy, fortalece el Balance mañana.

### Gross Profit ($) vs Gross Margin (%)

- **Gross Profit:** Dinero neto que queda para pagar el resto del negocio.
- **Gross Margin:** Eficiencia porcentual. ¿Qué tan rentable es CADA unidad?
*Un margen decreciente es una alerta roja de pérdida de competitividad.*

---

## 🛡️ 5. Garantías y Riesgo: LTV (Loan-to-Value)

*Basado en [04-LTV-and-Collateral.md](./04-LTV-and-Collateral.md)*

### El Colchón de Seguridad

$$LTV\ (\%) = \frac{Monto\ Préstamo}{Valor\ de\ la\ Garantía}$$

- **LTV Bajo (ej. 50%):** Mucha seguridad para el banco.
- **LTV Alto (ej. 100%):** Riesgo extremo. Si el mercado cae, el banco pierde.

---

## 🚀 6. Métricas Maestras y Prevención

*Basado en [07-Derived-Metrics-Dictionary.md](./07-Derived-Metrics-Dictionary.md)*

### ¿Cómo prevenir la Muerte por Éxito?

1. **Factoring:** Cash hoy por facturas mañana.
2. **Líneas Revolventes:** Crédito flexible para COGS.
3. **DPO Negotiation:** Pagar más tarde para empatar con el cobro.

### El "Cheat Sheet" del Motor

- **DSO Alto:** El cliente pierde poder de cobro. **Riesgo.**
- **Gross Margin Bajo:** Suben costos o bajas precios. **Alerta.**
- **OpEx crecido:** Ineficiencia operativa. **Peligro.**

---

## 📝 7. Clarificaciones Finales

*Basado en [06-Pending-Clarifications.md](./06-Pending-Clarifications.md)*

- **Cash vs Cash Flow:** El Cash es la foto del banco hoy; el Cash Flow es la película de cuánto dinero real se movió en el mes.
- **Intangibles (Patentes):** Casi lo opuesto a la liquidez. Son valiosos en el futuro, pero valen poco como garantía inmediata en caso de quiebra.
- **CCC (Cash Conversion Cycle):** La métrica que mide la velocidad del dinero en el negocio.

---

> **Veredicto del Día 1:** Hemos construido el "Backend Financiero". Estamos listos para inyectar estos datos en nuestro motor determinista. 🚀
