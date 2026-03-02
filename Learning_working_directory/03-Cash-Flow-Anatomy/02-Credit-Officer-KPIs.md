# Day 3 — Part 2: Credit Officer KPIs & Red Flags 🚨

Este documento cubre las métricas que un Credit Officer (Analista de Riesgo) revisa
DESPUÉS de leer los estados financieros: los ratios que resumen la salud financiera en
un solo número. Son las entradas al Flag Engine del Módulo 2 de tu Motor de Riesgo.

---

## 1. Current Ratio (Ratio de Liquidez Corriente)

**¿Qué mide?**  
La capacidad de una empresa para pagar sus deudas de corto plazo (< 12 meses)
usando solo sus activos líquidos de corto plazo.

```
Current Ratio = Activos Circulantes / Pasivos Circulantes
              = Total Current Assets / Total Current Liabilities
```

**Ejemplo con Koss:**

```
Current Assets (Activos Circulantes):  ~$10,000,000
Current Liabilities (Pasivos Circulantes): ~$2,000,000

Current Ratio = 10,000,000 / 2,000,000 = 5.0
```

Un Current Ratio de 5.0 significa que Koss puede pagar 5 veces todas sus deudas
de corto plazo solo con lo que tiene en activos líquidos. **Muy sano.**

**Tabla de Interpretación:**

| Current Ratio | Significado | Acción del Banco |
| :--- | :--- | :--- |
| > 2.0 | Excelente liquidez | Aprobar con confianza |
| 1.5 - 2.0 | Buena liquidez | Aprobar con monitoreo |
| 1.0 - 1.5 | Liquidez ajustada | Aprobar con covenants |
| < 1.0 | Ilíquido a corto plazo | **DECLINAR** (no puede pagar deudas inmediatas) |
| < 0 | Insolvencia técnica | **Red Line absoluta** |

> **Nota de Riesgo:**  
> Un Current Ratio muy alto (> 6.0 en una manufacturera) también puede ser una señal
> de que tienen demasiado inventario que no se vende. No siempre "más es mejor".

---

## 2. DSCR (Debt Service Coverage Ratio)

**DSCR** significa **Debt Service Coverage Ratio** (Razón de Cobertura del Servicio de Deuda).

**¿Qué mide?**  
Responde a la pregunta del banquero #1:
> *"¿Genera suficiente efectivo operativo para pagar las cuotas del préstamo que le voy a dar?"*

```
DSCR = EBITDA / (Interest Expense + Principal Payments)
     = EBITDA / Debt Service
```

- **`EBITDA`:** El proxy de generación de caja operativa.
- **`Debt Service`:** Todo lo que la empresa tiene que pagarle al banco este año  
  (intereses + el capital que se va amortizando del préstamo).

**Ejemplo:**

```
EBITDA: $500,000
Interest Expense del año: $80,000
Principal del préstamo que vence este año: $120,000
Debt Service Total: $200,000

DSCR = 500,000 / 200,000 = 2.5x
```

Un DSCR de 2.5x significa que la empresa genera 2.5 veces más cash del que necesita
para pagar la deuda. **Muy cómodo para el banco.**

**Tabla de Interpretación:**

| DSCR | Significado | Acción |
| :--- | :--- | :--- |
| > 2.0x | Cobertura excelente | Aprobar con confianza |
| 1.5x - 2.0x | Cobertura buena | Aprobar con monitoreo normal |
| 1.25x - 1.5x | Cobertura ajustada | Aprobar con covenants estrictos |
| 1.0x - 1.25x | Cobertura mínima | Probablemente declinar |
| < 1.0x | **NO puede pagar la deuda** | **Red Line. Siempre DECLINAR.** |

> **Covenant típico:** El banco pone en el contrato:  
> *"Si el DSCR cae por debajo de 1.25x en cualquier trimestre, el crédito completo  
> vence de inmediato."* (Acceleration Clause).

---

## 3. FCF (Free Cash Flow)

**FCF** significa **Free Cash Flow** (Flujo de Caja Libre).

**¿Qué mide?**  
El dinero que le sobra a la empresa después de operar su negocio Y después de pagar  
por mantener/crecer su infraestructura (CapEx). Es el efectivo **verdaderamente libre**.

```
FCF = CFO - |CapEx|
    = Cash From Operations - Capital Expenditures (en valor absoluto)
```

**¿Por qué absoluto el CapEx?**  
En el PDF del 10-Q, el CapEx puede aparecer como positivo o negativo dependiendo  
de la convención del contador. Con `abs()` nos protegemos de alucinaciones del LLM  
que pueda extraerlo con el signo equivocado (Zero-Trust Engineering).

**Ejemplo de una Aerolínea:**

```
CFO:   $2,000,000,000  (Genera mucho cash volando personas)
CapEx: $1,800,000,000  (OBLIGADA a renovar aviones cada ciclo)

FCF = 2B - 1.8B = $200,000,000
```

El FCF real es solo el 10% del CFO. La mayoría del cash se lo traga la infraestructura.

**Jerarquía de Confianza de Métricas:**

```
FCF  >  CFO  >  Net Change in Cash  >  EBITDA  >  Net Income
(más real)                                       (más "opinión contable")
```

---

## 4. La Red Flag Combinada: EBITDA Mirage

> **⚠️ CORRECCIÓN IMPORTANTE:**  
> EBITDA > 0 **solo** NO es una Red Flag. Al contrario, es positivo.  
> La Red Flag es la COMBINACIÓN: **EBITDA > 0 Y CFO < 0 al mismo tiempo.**

```python
# Así lo detecta el Flag Engine del Motor:
if cfo < 0 and ebitda > 0:
    raise RiskFlag("EBITDA Mirage: empresa rentable en papel, 
                    muerta de sed en el banco")
```

**¿Por qué esto pasa?**  

- El EBITDA empieza desde arriba (Operating Income). Ignora el Working Capital.
- El CFO empieza desde abajo (Net Income). SÍ aplica el castigo del Working Capital.
- Si la empresa creció agresivamente y tiene mucho dinero "atorado" en cuentas  
  por cobrar o inventario, el EBITDA sigue siendo positivo, pero el CFO se vuelve  
  negativo porque el efectivo físico está preso en papeles de clientes y bodegas.

---

## 5. Accounts Receivable / Revenue > 40% — ¿Por Qué es "Aire"?

**Accounts Receivable (Cuentas por Cobrar):** Dinero que la empresa YA RECONOCIÓ  
como ingreso (Revenue) en el Income Statement, pero que **todavía no ha cobrado en efectivo.**

**La Regla del 40%:**

```
AR / Revenue > 40% → Red Flag: La empresa está "vendiendo aire"
```

**¿Por qué "aire"?**  
Si el Revenue de TacoTech es $2,000,000 y sus Accounts Receivable son $900,000:

```
AR / Revenue = 900,000 / 2,000,000 = 45%  → ⚠️ Red Flag
```

Significa que el **45% de todos sus "ingresos"** del año todavía son promesas de pago  
en el papel. No son billetes físicos en el banco.

**Lo que puede estar pasando:**

1. Sus clientes son lentos pagando (Cash Collection Problem).
2. Les están dando crédito a clientes de mala calidad que nunca van a pagar (Bad Debt).
3. Están **reconociendo ingresos de forma agresiva** antes de tener derecho a cobrarlos.  
   En casos extremos, esto es la primera señal de **fraude contable** (como en Koss pero en Revenue).

**¿Por qué > 40% específicamente?**  
Es una regla empírica de la industria crediticia. En promedio, en negocios B2B saludables,  
si corres el año en 365 días y tus términos de pago son 30-45 días, tu AR debería ser  
aproximadamente `45/365 = 12%` de tu Revenue anual. Llegar al 40% significa que tus  
clientes te están pagando como si hubieran negociado 146 días de crédito. Eso es anormal.

---

## 6. Resumen: El Semáforo del Credit Officer

| Métrica | Verde ✅ | Amarillo ⚠️ | Rojo 🚨 |
| :--- | :--- | :--- | :--- |
| **Current Ratio** | > 2.0x | 1.0x - 2.0x | < 1.0x |
| **DSCR** | > 1.5x | 1.25x - 1.5x | < 1.25x |
| **FCF** | Positivo | Negativo pero mínimo | Negativo profundo varios años |
| **AR / Revenue** | < 20% | 20% - 40% | > 40% |
| **EBITDA Mirage** | CFO y EBITDA positivos | CFO ligeramente negativo | CFO negativo + EBITDA positivo |
| **Net Debt / EBITDA** | < 2.5x | 2.5x - 4.0x | > 4.0x (Red Line) |
