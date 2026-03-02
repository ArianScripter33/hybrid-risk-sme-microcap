# Glosario Senior: El Idioma del Capital 🎩

Este glosario define los términos de "alto nivel" que conectan tu motor de riesgo con las decisiones de negocio de la Fintech.

---

## 1. Instrumentos de Liquidez (Financiar el Gap)

- **Working Capital Financing:** Término paraguas para préstamos destinados a cubrir el desfase entre pagos y cobros.
- **Factoring (Factoraje):** Venta de cuentas por cobrar (facturas) con un descuento a cambio de efectivo inmediato. El banco asume el riesgo de cobro.
- **Asset-Based Lending (ABL):** Préstamos garantizados por activos específicos (inventario o facturas). El motor evalúa la calidad de estos activos.
- **Gap Financing (La Estrategia):** El acto de financiar un "hueco" específico en la estructura de capital. Se refiere a la necesidad de cubrir el espacio entre los fondos disponibles y el capital total requerido para un hito.
- **Bridge Loan (El Instrumento):** Es el "puente" legal. Un préstamo de corto plazo con un **evento de salida (Exit)** definido (ej. una ronda de inversión o un contrato por cobrar).

---

## 2. Métricas de Riesgo Estándar (Basilea III)

- **PD (Probability of Default):** La probabilidad (0 a 1) de que el cliente no pague. Tu modelo de ML (XGBoost) disparará este número.
- **LTV (Loan-to-Value):** La proporción del valor del activo que se presta. Si el activo valora 100 y prestas 50, el LTV es 50%.
- **LGD (Loss Given Default):** Qué porcentaje del dinero perdemos si el cliente falla. Si el LTV es 50%, el LGD es bajo porque vendemos la garantía.
- **EAD (Exposure at Default):** Cuánto dinero nos debe el cliente en el momento preciso del fallo.

- **Regulatory Ceiling (Leyes de Usura):** En muchos países, hay un tope legal a lo que puedes cobrar. Si tu modelo dice que debes cobrar 100% pero la ley dice máximo 45%, simplemente no le prestas.

---

## 3. Arquitectura de la Tasa de Interés

- **Cost of Funds:** La tasa a la que la Fintech consigue dinero (Proxy: TIIE en México, SOFR en USA).
- **Risk-Based Pricing:** El método de cobrar una tasa más alta a clientes con mayor PD (o mayor opacidad financiera).
- **Spread:** La diferencia entre la tasa que cobras al cliente y el costo de conseguir ese dinero. Es la ganancia bruta de la Fintech.

---

> **Insight para el Arquitecto:** "No fijas el precio, pero fijas el riesgo que dicta el precio. Si tu PD es imprecisa, el banco pierde dinero aunque cobre tasas del 100%."
