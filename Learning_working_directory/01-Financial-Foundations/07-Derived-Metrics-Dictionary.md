# Diccionario de Señales: Métricas Derivadas 📊

Este documento define las "Features" que nuestro Módulo de Cálculo (Python) debe generar a partir de los datos crudos para alimentar al Agente Narrativo.

---

## 1. ¿Cómo se previene la Muerte por Éxito? 🛡️

No basta con "planificar" el CCC; se trata de **financiar el Gap**. Si tu sistema detecta que una empresa tiene un CCC de 90 días, la solución no es "vender menos", sino:

* **Factoring:** Vender tus facturas por cobrar a un banco para tener el cash hoy (sacrificando un pequeño %).
* **Líneas de Crédito Revolventes:** Créditos que se activan automáticamente cuando suben las ventas para cubrir el COGS.
* **Negociación con Proveedores (DPO):** Intentar pagar a tus proveedores a 90 días para que el dinero salga al mismo tiempo que entra el de tus clientes.

---

## 2. Métricas Derivadas (Las "Features" de tu Motor)

Dividiremos estas métricas en los dos modos de tu arquitectura: **Modo Escudo (Riesgo)** y **Modo Cohete (Crecimiento)**.

### 🛡️ Modo Escudo: Salud y Supervivencia (Risk Mode)

Estas métricas nos dicen si la empresa va a explotar mañana por falta de aire (cash).

| Métrica | Fórmula | Qué mide | Umbral Alerta Roja 🚨 |
| :--- | :--- | :--- | :--- |
| **Quick Ratio (Prueba Ácida)** | `(Cash + AR) / Current Liabilities` | Liquidez sin depender de inventario. | `< 0.8` |
| **DSO (Days Sales Outstanding)** | `(AR / Revenue) * 365` | ¿Cuántos días tardas realmente en cobrar? | `> 60 días` (en retail) |
| **Daily Burn Rate** | `(Cash mes ant. - Cash mes act.) / 30` | ¿Cuánto dinero pierdes cada día? | Si Cash / Burn < 3 meses |
| **DPO / DSO Ratio** | `Días Pago / Días Cobro` | ¿Tardas más en cobrar que en pagar? | `< 1.0` |

### 🚀 Modo Cohete: Potencial de Escalabilidad (Growth Mode)

Estas métricas nos dicen si la empresa es una "Gema" que vale la pena para un inversionista.

| Métrica | Fórmula | Qué mide | Potencial Unicornio 🦄 |
| :--- | :--- | :--- | :--- |
| **Gross Margin %** | `(Gross Profit / Revenue)` | Eficiencia de producción. | `> 70%` |
| **Operating Leverage** | `% Cambio EBIT / % Cambio Revenue` | ¿Qué tanto crece la utilidad vs la venta? | Alto (Fijos bajos) |
| **NWC / Revenue** | `Working Capital / Revenue` | ¿Cuánto cash "bloqueas" para ganar $1? | Cerca de 0 o Negativo |
| **Rule of 40** | `Crecimiento Ventas + Margen Profit` | Equilibrio crecimiento vs rentabilidad. | `> 40%` |

---

## 🧠 El "Cheat Sheet" del Arquitecto

Si vas a modelar el riesgo, grábate esto:

1. **Si el DSO (Días de Cobro) sube:** El cliente está perdiendo poder contra sus compradores. **Riesgo alto.**
2. **Si el Gross Margin baja:** El COGS está subiendo (materia prima cara) o el cliente está perdiendo "Pricing Power".
3. **Si el OpEx sube más rápido que el Revenue:** La empresa se está volviendo ineficiente y burocrática.

> **Regla Final para el Motor:** "Data is noise, Ratios are signals, Patterns are truth."
