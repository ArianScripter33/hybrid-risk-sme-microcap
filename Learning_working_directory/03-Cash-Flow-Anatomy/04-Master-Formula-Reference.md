# Master Formula Reference — Hybrid Risk Engine 📐

Todas las fórmulas usadas en el Motor de Riesgo, con sus variables explicadas y ejemplos de Koss Corporation.

---

## 1. Income Statement Formulas

### Gross Profit

$$\text{Gross Profit} = \text{Revenue} - \text{COGS}$$

| Variable | Definición | Koss 6M-2025 |
| :--- | :--- | :--- |
| `Revenue` | Ventas netas totales del período | $6,932,157 |
| `COGS` | Costo directo de fabricar/comprar el producto | $4,472,659 |
| **`Gross Profit`** | Dinero disponible para pagar la corporación | **$2,459,498** |

---

### Gross Margin %

$$\text{Gross Margin \%} = \frac{\text{Gross Profit}}{\text{Revenue}} \times 100$$

| Variable | Definición | Koss |
| :--- | :--- | :--- |
| `Gross Profit` | Resultado de Revenue - COGS | $2,459,498 |
| `Revenue` | Denominador de eficiencia | $6,932,157 |
| **`Gross Margin %`** | Centavos que sobran por cada $1 vendido | **35.47%** |

> **Benchmark:** Hardware/Consumer Electronics: 30-45% saludable. SaaS: 70-85%.

---

### EBIT (Operating Income)

$$\text{EBIT} = \text{Gross Profit} - \text{SG\&A} - \text{R\&D} - \text{D\&A}$$

| Variable | Definición | Koss |
| :--- | :--- | :--- |
| `Gross Profit` | Margen bruto del producto | $2,459,498 |
| `SG&A` | Gastos corporativos: renta, sueldos admin, marketing | $3,520,116 |
| `R&D` | Investigación y Desarrollo (Koss: $0 reportado) | $0 |
| `D&A` | Depreciación + Amortización (aquí incluida en SG&A) | ~$150,000 est. |
| **`EBIT`** | Ganancia/Pérdida del corazón operativo del negocio | **-$1,060,618** |

---

### EBITDA

$$\text{EBITDA} = \text{EBIT} + \text{D\&A}$$

$$\text{EBITDA} = \text{Net Income} + \text{Taxes} + \text{Interest} + \text{D\&A}$$

| Variable | Definición | Koss |
| :--- | :--- | :--- |
| `EBIT` | Operating Income | -$1,060,618 |
| `D&A` | Gasto fantasma devuelto (no salió del banco) | ~$150,000 |
| **`EBITDA`** | Proxy de caja operativa antes de finanzas e impuestos | **~-$910,618** |

> **¿Por qué se suma D&A?** Porque la depreciación se restó en el EBIT como gasto, pero nunca salió efectivo del banco ese año. Se "devuelve" para ver el cash real de operación.

---

### EBT (Earnings Before Taxes)

$$\text{EBT} = \text{EBIT} + \text{Other Income} - \text{Interest Expense}$$

| Variable | Definición | Koss |
| :--- | :--- | :--- |
| `EBIT` | Operating Income | -$1,060,618 |
| `Other Income` | Intereses de bonos + ingresos no operativos | +$744,460 |
| `Interest Expense` | Intereses pagados al banco por deuda | -$1,152 |
| **`EBT`** | Ganancia antes de pagar al gobierno | **-$316,158** |

---

### Net Income (Bottom Line)

$$\text{Net Income} = \text{EBT} - \text{Income Tax}$$

| Variable | Definición | Koss |
| :--- | :--- | :--- |
| `EBT` | Ganancia antes de impuestos | -$316,158 |
| `Income Tax` | Provisión fiscal estimada | $5,520 |
| **`Net Income`** | Lo que queda para los dueños | **-$321,678** |

---

## 2. Cash Flow Formulas

### Cash from Operations (CFO)

$$\text{CFO} = \text{Net Income} + \text{D\&A} + \Delta \text{Working Capital} + \text{Other Items}$$

| Variable | Definición | Koss est. |
| :--- | :--- | :--- |
| `Net Income` | Punto de partida del IS | -$321,678 |
| `D&A Addback` | Gasto fantasma devuelto | +$150,000 |
| `Delta WC` | Cambio en activos/pasivos circulantes | +$155,000 |
| **`CFO`** | Efectivo real generado por la operación | **~-$4,678** |

### Delta WC — La Regla Contraintuitiva Explicada

El Working Capital Delta (`Delta WC`) se calcula comparando **dos Balance Sheets consecutivos**. Es la única métrica del Cash Flow Statement que requiere datos de dos períodos distintos.

$$\Delta \text{WC}_{\text{CFO}} = -(\Delta \text{A/R}) - (\Delta \text{Inventory}) - (\Delta \text{Prepaid}) + (\Delta \text{A/P}) + (\Delta \text{Accrued Liabilities})$$

**Todas las Variables de la Fórmula — Con Definición:**

| Variable | Tipo | Definición | Impacto en CFO |
| :--- | :--- | :--- | :--- |
| `Δ A/R` (Accounts Receivable) | Activo Circulante | Dinero que te deben clientes. Si sube = vendiste fiado y el cash no llegó. | Si `Δ A/R > 0` → CFO baja |
| `Δ Inventory` | Activo Circulante | Mercancía en bodega. Si sube = compraste más stock con tu cash. | Si `Δ Inv > 0` → CFO baja |
| `Δ Prepaid Expenses` | Activo Circulante | **Cash prepagado por algo que aún no consumes.** Ej: pagas 12 meses de seguro en enero. Ese cash ya salió de tu banco pero se registra como "activo" que se consume mes a mes. | Si `Δ Prepaid > 0` → CFO baja |
| `Δ A/P` (Accounts Payable) | Pasivo Circulante | Lo que le debes a proveedores. Si sube = recibiste bienes sin pagar aún. Te jineteas el cash del proveedor. | Si `Δ A/P > 0` → CFO sube |
| `Δ Accrued Liabilities` | Pasivo Circulante | **Gastos causados pero no pagados en efectivo todavía.** Ej: nómina del 31 de diciembre que se paga el 5 de enero. El gasto se reconoció, el cash no salió. | Si `Δ Accrued > 0` → CFO sube |

**Por qué la regla es contraintuitiva:**

| Evento real | Activo/Pasivo | Delta en Balance | Impacto en CFO |
| :--- | :--- | :--- | :--- |
| Compraste inventario por $50K | AC (Inventory) | **sube** +$50K | `-$50K` ❌ (cash salió) |
| Clientes te deben $100K más | AC (A/R) | **sube** +$100K | `-$100K` ❌ (cash bloqueado en papel) |
| Pagas seguro anual por adelantado | AC (Prepaid) | **sube** +$24K | `-$24K` ❌ (cash salió) |
| Proveedor te fía mercancía $80K | PC (A/P) | **sube** +$80K | `+$80K` ✅ (cash te quedas) |
| Nómina de dic, se paga en enero | PC (Accrued) | **sube** +$80K | `+$80K` ✅ (cash te quedas) |

**Mnemotécnica permanente:**
> `"Si eres más rico en papel (AC sube), pagaste por esa riqueza (cash salió). Si debes más (PC sube), te jinesteaste el pago (cash se quedó)."`

**Verificación matemática con el ejemplo Koss:**

```text
Fórmula: Delta_WC = -(-87K) - (-45K) + (23K)
                  = +87K   + 45K   + 23K
                  = +$155,000 ✅

Interpretación: Koss "liberó" $155K de cash de su ciclo operativo
porque cobró deudas de clientes y vendió inventario viejo.
Ese $155K alimenta directamente al CFO como componente positivo.
```

> **Fuente de datos:** SIEMPRE dos columnas del Balance Sheet (período actual vs. período anterior).
> En el 10-Q de Koss: columnas "December 31, 2025" y "June 30, 2025".
> En el PDF de Koss aparece como "Changes in operating assets and liabilities" en la sección
> de Operating Activities del Cash Flow Statement.

---

### Free Cash Flow (FCF) — El Rey

$$\text{FCF} = \text{CFO} - |\text{CapEx}|$$

| Variable | Definición | Koss est. |
| :--- | :--- | :--- |
| `CFO` | Cash from Operations | -$4,678 |
| `CapEx` | Inversión en infraestructura (valor absoluto) | $35,000 |
| **`FCF`** | Cash libre después de mantener el negocio vivo | **-$39,678** |

> **¿Por qué `abs(CapEx)`?** El LLM puede extraer el CapEx como positivo o negativo según el formato del PDF. El valor absoluto garantiza que siempre reste del CFO (Zero-Trust Engineering).

### ¿Por qué NO hay "Doble Conteo" entre SG&A y CapEx?

Esta es la confusión más común al leer la fórmula del FCF por primera vez.

$$\text{EBIT} = \text{Gross Profit} - \underbrace{\text{SG\&A}}_{{\text{OPEX}}} - \underbrace{\text{D\&A}}_{{\text{slice del CapEx pasado}}}$$
$$\text{FCF} = \text{CFO} - \underbrace{|\text{CapEx}|}_{{\text{Nuevo activo hoy}}}$$

| Concepto | ¿Qué es? | ¿Dónde aparece? | Ejemplo Koss |
| :--- | :--- | :--- | :--- |
| **OPEX / SG&A** | Gasto diario de operar: sueldos, renta, marketing | Income Statement (reduce EBIT) | $3.52M de gastos corp. este semestre |
| **CapEx** | Compra de activo duradero (>1 año): maquinaria, servidores | Balance Sheet + CFI (sale cash) | $35K en equipo nuevo |
| **D&A** | El costo anual de "consumir" el CapEx del **pasado** | Income Statement (dentro de SG&A o COGS) | ~$150K por máquinas compradas hace años |

**El flujo sin doble conteo — Ejemplo:**

```text
Año 0: Koss compra una máquina de $100,000 (CapEx)
    → Balance Sheet: Activo +$100K
    → CFI: -$100K (salió cash del banco)
    → Income Statement: NADA todavía.

Año 1 al 5 (vida útil 5 años):
    D&A = $20,000/año → reduce EBIT/Net Income
    CFO hace Addback: +$20K (el cash no salió este año)

FCF = CFO - CapEx:
    CFO ya incluye el Addback de la D&A de máquinas VIEJAS
    CapEx = la NUEVA máquina que acaba de salir del banco HOY
    ↳ Son eventos completamente distintos. Zero double-counting.
```

> **Regla Mental Definitiva:**
>
> - `SG&A / OPEX` = Dinero que gastas para **OPERAR hoy**. → Income Statement.
> - `CapEx` = Dinero que inviertes para **EXISTIR mañana**. → Balance Sheet + CFI.
> - `D&A` = El costo contable de **consumir el CapEx del pasado** año a año. → Conecta ambos.

---

## 3. Balance Sheet Ratios

### Working Capital

$$\text{WC} = \text{Total Current Assets} - \text{Total Current Liabilities}$$

| Variable | Definición | Uso en Motor |
| :--- | :--- | :--- |
| `Current Assets` | Activos líquidos a < 12 meses | Numerador de liquidez |
| `Current Liabilities` | Deudas a pagar en < 12 meses | Denominador de liquidez |
| **`WC`** | Colchón de liquidez operativa | Positivo = sobrevive el año |

---

### Current Ratio

$$\text{Current Ratio} = \frac{\text{Total Current Assets}}{\text{Total Current Liabilities}}$$

| Valor | Interpretación | Acción del Motor |
| :--- | :--- | :--- |
| > 2.0x | Liquidez excelente | ✅ Aprobar |
| 1.0 - 2.0x | Liquidez ajustada | ⚠️ Monitorear |
| < 1.0x | Ilíquido | 🚨 Declinar |

---

### DSCR (Debt Service Coverage Ratio)

$$\text{DSCR} = \frac{\text{EBITDA}}{\text{Interest Expense} + \text{Principal Payments}}$$

**¿Qué nos dice?**
Responde la pregunta del Credit Officer:
> *"Para cada $1 que esta empresa debe pagarle al banco este año, ¿cuántos $1 de caja operativa genera?"*

**Variables detalladas:**

| Variable | Definición Exacta | Ejemplo Koss |
| :--- | :--- | :--- |
| `EBITDA` | Proxy de caja operativa (Operating Income + D&A) | ~-$910,618 (seis meses) |
| `Interest Expense` | Los **intereses** devengados sobre deuda bancaria. Solo el costo del dinero prestado. Si tienes un crédito de $1M al 10% anual → Interest = $100K/año | $1,152 (seis meses, mínimo) |
| `Principal Payments` | La **amortización del capital** prestado. Si tu préstamo es de $1M a 5 años → Principal = $200K/año | $0 (Koss no tiene deuda significativa) |
| `Debt Service` | `Interest Expense + Principal Payments` = Todo el pago al banco en el año | ~$2,304 anualizado |
| **`DSCR`** | Cuántas veces cubre la caja operativa el servicio de deuda | **No aplica** (no tiene deuda) |

> **Distinción clave:** El `Interest Expense` es el "alquiler" del dinero (lo pagás siempre).
> El `Principal Payment` es la devolución del capital prestado (reduce la deuda). Son dos flujos distintos.

**Ejemplo ilustrativo para una PyME diferente (con deuda real):**

```text
EBITDA:              $500,000
Interest Expense:     $80,000   (10% sobre $800K de crédito)
Principal Payment:   $160,000   (crédito a 5 años: $800K / 5)
Debt Service:        $240,000

DSCR = 500,000 / 240,000 = 2.08x ✅

Interpretación: la empresa genera 2.08x más caja de la que necesita
para pagar su deuda. El banco respira tranquilo.
```

| Valor | Interpretación | Acción |
| :--- | :--- | :--- |
| > 2.0x | Cobertura excelente | ✅ Aprobar con confianza |
| 1.5x - 2.0x | Cobertura buena | ✅ Aprobar con monitoreo |
| 1.25x - 1.5x | Mínimo aceptable | ⚠️ Covenant: `DSCR >= 1.25x en todo momento` |
| 1.0x - 1.25x | Cobertura mínima | ❌ Probablemente declinar |
| < 1.0x | **No puede pagar la deuda** | 🚨 **Red Line. Declinar siempre.** |

> **Covenant típico de banco:** *"Si el DSCR cae por debajo de 1.25x en cualquier trimestre,
> el crédito completo vence de inmediato."* Esto se llama Acceleration Clause.

---

### Altman Z-Score (Predicción de Quiebra)

$$Z = 1.2 A + 1.4 B + 3.3 C + 0.6 D + 1.0 E$$

| Componente | Fórmula | Qué mide |
| :--- | :--- | :--- |
| **A** | Working Capital / Total Assets | Liquidez |
| **B** | Retained Earnings / Total Assets | Rentabilidad acumulada histórica |
| **C** | EBIT / Total Assets | Productividad de activos |
| **D** | Book Value Equity / Total Liabilities | Solvencia patrimonial |
| **E** | Revenue / Total Assets | Eficiencia (asset turnover) |

| Z-Score | Zona | Probabilidad de quiebra |
| :--- | :--- | :--- |
| > 2.99 | 🟢 Safe Zone | Baja |
| 1.81 - 2.99 | 🟡 Grey Zone | Media — monitorear |
| < 1.81 | 🔴 Distress Zone | Alta — declinar crédito |

---

## 4. La Jerarquía de Confianza (Resumen Visual)

$$\text{FCF} > \text{CFO} > \text{Net Change in Cash} > \text{EBITDA} > \text{Net Income}$$

| Posición | Métrica | ¿Por qué se puede "falsificar"? |
| :--- | :--- | :--- |
| 5° (menos confiable) | Net Income | Depreciación ajustable, ingresos pre-reconocidos, one-time items |
| 4° | EBITDA | Igual que Net Income + ignora Working Capital |
| 3° | Net Change in Cash | Positivo si piden préstamos o venden activos (engañoso) |
| 2° | CFO | Muy difícil de falsificar — requiere mover efectivo bancario real |
| 1° (más confiable) | **FCF** | Casi imposible de manipular — descuenta CapEx real obligatorio |

---

## 5. Fórmulas de Crecimiento (Módulo 4 — VC Mode)

### Revenue CAGR

$$\text{CAGR} = \left(\frac{\text{Revenue}_{\text{final}}}{\text{Revenue}_{\text{inicial}}}\right)^{\frac{1}{n}} - 1$$

### Rule of 40

$$\text{Rule of 40} = \text{Revenue Growth \%} + \text{EBITDA Margin \%}$$

> Si > 40: empresa de alta calidad (balance entre crecimiento y rentabilidad)

### AR / Revenue (Calidad de las Ventas)

$$\text{AR Ratio} = \frac{\text{Accounts Receivable}}{\text{Revenue}}$$

> Si > 40%: Red Flag — la empresa "vende aire" (ingresos no cobrados)
