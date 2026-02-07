# Ruta de Aprendizaje Financiero — Just-in-Time Learning

> **Regla:** No estudies nada que no vayas a programar ese mismo día.
> **Método:** Espiral de 3 pasadas. Cada concepto se visita 3 veces con profundidad creciente.

---

## 1. El Método Espiral

Cada concepto financiero pasa por 3 niveles:

| Pasada | Pregunta | Semana Típica | Profundidad |
|:---|:---|:---|:---|
| **Pasada 1: Ingesta** | "¿Dónde está esto en el PDF?" | Sem 1-3 | Reconocer el campo |
| **Pasada 2: Cálculo** | "¿Cuál es la fórmula en Python?" | Sem 4-7 | Implementar la lógica |
| **Pasada 3: Narrativa** | "¿Qué significa esto para el Agente CFO?" | Sem 8-10 | Interpretar y explicar |

**Ejemplo con EBITDA:**
1. Sem 1: "EBITDA está en el Income Statement, entre Operating Income y Net Income."
2. Sem 4: `ebitda = operating_income + depreciation_amortization`
3. Sem 9: "EBITDA de 2.3M con margen de 15% indica generación de caja operativa moderada. Sin embargo, al ajustar por CapEx elevado, el FCF cae a territorio negativo, lo cual plantea riesgos de sostenibilidad."

---

## 2. Los 3 Estados Financieros (El ABC)

### 2.1 Balance Sheet (Estado de Situación Financiera)

**¿Qué es?**
Una foto instantánea de lo que la empresa TIENE (Activos), lo que DEBE (Pasivos), y lo que VALE para sus dueños (Capital) en un momento específico.

**La Ecuación Fundamental:**
```
Activos = Pasivos + Capital Contable
Assets = Liabilities + Stockholders' Equity
```
Si esta ecuación no cuadra → algo está mal en los datos.

**Estructura:**
```
ACTIVOS (Assets)
├── Activos Circulantes (Current Assets) — se convierten en cash en <12 meses
│   ├── Efectivo (Cash & Equivalents)
│   ├── Cuentas por Cobrar (Accounts Receivable) — te deben dinero
│   ├── Inventarios (Inventory)
│   └── Otros activos circulantes
├── Activos No Circulantes (Non-Current Assets) — largo plazo
│   ├── Propiedad, Planta y Equipo (PP&E) — cosas físicas
│   ├── Intangibles — patentes, software
│   └── Goodwill — prima pagada en adquisiciones

PASIVOS (Liabilities)
├── Pasivos Circulantes (Current Liabilities) — debes pagar en <12 meses
│   ├── Cuentas por Pagar (Accounts Payable) — debes a proveedores
│   ├── Deuda a Corto Plazo (Short-Term Debt)
│   └── Porción circulante de deuda LP
├── Pasivos No Circulantes (Non-Current Liabilities)
│   └── Deuda a Largo Plazo (Long-Term Debt) — préstamos >12 meses

CAPITAL CONTABLE (Stockholders' Equity)
└── Lo que queda para los accionistas
```

**Mapeo a código:**
- `total_current_assets` → Lo que puedes convertir en cash rápido
- `total_current_liabilities` → Lo que debes pagar pronto
- `Working Capital = CA - CL` → ¿Sobrevives los próximos 12 meses?

**Red Flags en el Balance:**
- Activos circulantes < Pasivos circulantes → Working Capital negativo → PELIGRO
- Goodwill muy grande → puede haber "aire" en los activos
- Deuda LP creciente sin crecimiento en activos → se está apalancando sin generar valor

---

### 2.2 Income Statement (Estado de Resultados)

**¿Qué es?**
Una película de cómo la empresa generó (o perdió) dinero durante un período (trimestre o año). Es la "opinión contable" de si ganó.

**El Cascade (de arriba a abajo):**
```
Revenue (Ingresos / Ventas)                     $100M
- Cost of Goods Sold (Costo de Ventas)           -$60M
= GROSS PROFIT (Utilidad Bruta)                   $40M  ← Gross Margin = 40%
- Operating Expenses (Gastos Operativos)          -$25M
  ├── SG&A (Ventas, Generales y Admin)
  ├── R&D (Investigación y Desarrollo)
  └── D&A (Depreciación y Amortización)
= OPERATING INCOME / EBIT (Utilidad Operativa)    $15M  ← Operating Margin = 15%
+ D&A (add back)                                   +$5M
= EBITDA                                           $20M  ← EBITDA Margin = 20%
- Interest Expense (Gastos Financieros)            -$3M
± Other Income/Expense                              $0M
= Income Before Tax (Utilidad antes de impuestos)  $12M
- Income Tax (Impuestos)                           -$3M
= NET INCOME (Utilidad Neta)                        $9M  ← Net Margin = 9%
```

**Conceptos Clave:**

**Gross Margin (Margen Bruto):**
- Mide eficiencia de producción.
- Software: 70-90%. Manufactura: 20-40%. Retail: 25-35%.
- Si cae → los costos están creciendo más rápido que los ingresos.

**EBITDA vs Net Income:**
- **Net Income** incluye decisiones contables (depreciación, impuestos) y financieras (intereses).
- **EBITDA** las elimina → muestra la capacidad de generar cash operativo "pura".
- Los banqueros usan EBITDA porque es más comparable entre empresas.
- **CUIDADO:** EBITDA no es cash real. Ignora CapEx, cambios en WC, e impuestos.

**Mapeo a código:**
```python
# El cascade completo
gross_profit = revenue - cogs
operating_income = gross_profit - operating_expenses  # EBIT
ebitda = operating_income + depreciation_amortization
net_income = income_before_tax - income_tax
```

---

### 2.3 Cash Flow Statement (Estado de Flujo de Efectivo)

**¿Qué es?**
La REALIDAD de cuánto cash entró y salió. No es opinión contable — es efectivo en banco.

**¿Por qué importa más que el Income Statement?**
> "Revenue is vanity, profit is sanity, cash is king."
Una empresa puede ser "rentable" (Net Income positivo) pero quedarse sin cash si:
- Los clientes no pagan (Accounts Receivable sube).
- Tiene mucho inventario sin vender.
- Invirtió todo en CapEx.

**Estructura:**
```
OPERATING (Actividades de Operación) — cash del negocio real
├── Net Income (punto de partida)
├── + D&A (add back — no fue cash)
├── ± Cambios en Working Capital
│   ├── ↑ Accounts Receivable = menos cash (te deben más)
│   ├── ↑ Inventory = menos cash (compraste más)
│   └── ↑ Accounts Payable = más cash (debes más, no has pagado)
└── = Cash from Operations (CFO)  ← LA MÉTRICA MÁS IMPORTANTE

INVESTING (Actividades de Inversión) — cash para crecer
├── - Capital Expenditures (CapEx) — comprar maquinaria, equipo
├── - Acquisitions — comprar otras empresas
└── = Cash from Investing (CFI)  ← Generalmente negativo (gastas para crecer)

FINANCING (Actividades de Financiamiento) — cash de prestamistas/accionistas
├── + Debt Issued — préstamos recibidos
├── - Debt Repaid — préstamos pagados
├── - Dividends — distribuciones a accionistas
└── = Cash from Financing (CFF)

NET CHANGE IN CASH = CFO + CFI + CFF
```

**Métricas Derivadas Clave:**
```python
free_cash_flow = cash_from_operations - capital_expenditures
# FCF = lo que realmente "sobra" después de operar E invertir
# FCF > 0 = la empresa genera valor
# FCF < 0 = consume más de lo que genera (necesita financiamiento externo)
```

**CapEx vs OpEx:**
- **CapEx** (Capital Expenditure): Comprar una fábrica. Se capitaliza (aparece en Balance como activo).
- **OpEx** (Operating Expenditure): Pagar la luz de la fábrica. Se gasta inmediatamente (aparece en IS).
- Empresas tech clasifican mucho como OpEx → EBITDA se ve mejor, pero el cash sale igual.

---

## 3. Métricas de Underwriting (Pensar como Banquero)

### 3.1 DSCR (Debt Service Coverage Ratio)

**¿Qué es?**
Responde: "¿Genera suficiente cash para pagar su deuda este año?"

```python
dscr = ebitda / (interest_expense + principal_payments)
# principal_payments ≈ current_portion_long_term_debt
```

**Interpretación:**
| DSCR | Significado | Acción del Banco |
|:---|:---|:---|
| > 2.0x | Excelente cobertura | Aprobar con confianza |
| 1.5x - 2.0x | Buena cobertura | Aprobar con monitoreo |
| 1.25x - 1.5x | Aceptable pero ajustado | Aprobar con covenants estrictos |
| 1.0x - 1.25x | Peligro — apenas cubre | Probablemente declinar |
| < 1.0x | No puede pagar | DECLINAR. Default inminente |

**¿Por qué es la métrica #1?**
- Si DSCR < 1.0 → no genera suficiente para pagar intereses + principal.
- Los banqueros dicen: "Todo lo demás es ruido si no puede servir la deuda."
- Los covenants típicos exigen DSCR mínimo de 1.25x.

**Edge Cases en código:**
```python
if debt_service == 0:
    return float('inf')  # No tiene deuda → DSCR "infinito"
if ebitda < 0:
    return ebitda / debt_service  # Retorna negativo (peor que 0)
```

---

### 3.2 Working Capital

**¿Qué es?**
El "colchón de efectivo" a corto plazo.

```python
working_capital = total_current_assets - total_current_liabilities
```

**¿Por qué es crítico?**
- WC > 0: Puede pagar sus obligaciones de corto plazo.
- WC < 0: Necesita financiamiento externo para operar → MUY PELIGROSO para PyMEs.
- Una empresa puede tener buen Net Income pero WC negativo si los clientes no pagan.

**Relación con Ratios de Liquidez:**
```python
current_ratio = total_current_assets / total_current_liabilities
# > 1.0 = WC positivo, > 2.0 = muy líquido

quick_ratio = (total_current_assets - inventory) / total_current_liabilities
# Más conservador: ignora inventario (que puede no venderse)

cash_ratio = cash_and_equivalents / total_current_liabilities
# Ultra conservador: solo cuenta efectivo real
```

---

### 3.3 Apalancamiento (Leverage)

**¿Qué mide?**
Cuánto de la empresa está financiado con deuda (dinero ajeno) vs capital propio.

```python
debt_to_equity = total_debt / total_stockholders_equity
# > 3.0x = muy apalancado → mayor riesgo de default

debt_to_assets = total_debt / total_assets
# > 0.6 = más del 60% financiado con deuda

interest_coverage = operating_income / interest_expense
# < 2.0x = difícilmente cubre intereses
```

**Deuda a Corto vs Largo Plazo:**
- **Corto plazo (< 12 meses):** Más peligroso. Si no puedes refinanciar → default.
- **Largo plazo (> 12 meses):** Más manejable. Pero acumula intereses.
- **Estructura ideal:** Mayoría LP, poco CP.
- **Red Flag:** Mucha deuda CP → "refinancing risk" (dependes de que te renueven el crédito).

```python
total_debt = short_term_debt + current_portion_long_term_debt + long_term_debt
net_debt = total_debt - cash_and_equivalents
# Net Debt negativo = tiene más cash que deuda (posición fuerte)
```

---

### 3.4 Altman Z-Score (Predicción de Quiebra)

**¿Qué es?**
Un modelo de 1968 (Edward Altman) que combina 5 ratios para predecir quiebra.
Sigue usándose como benchmark en la industria.

```python
z_score = (1.2 * A) + (1.4 * B) + (3.3 * C) + (0.6 * D) + (1.0 * E)

# A = Working Capital / Total Assets         → Liquidez
# B = Retained Earnings / Total Assets       → Rentabilidad acumulada
# C = EBIT / Total Assets                    → Productividad de activos
# D = Book Value Equity / Total Liabilities  → Solvencia
# E = Revenue / Total Assets                 → Eficiencia (asset turnover)
```

**Zonas:**
| Z-Score | Zona | Significado |
|:---|:---|:---|
| > 2.99 | Safe | Baja probabilidad de quiebra |
| 1.81 - 2.99 | Grey | Zona gris — monitorear de cerca |
| < 1.81 | Distress | Alta probabilidad de quiebra |

**Limitaciones:**
- Diseñado para manufactura. Para tech/servicios, usar Z''-Score modificado.
- No considera factores cualitativos (management, mercado).
- Para el MVP es un excelente punto de partida.

---

### 3.5 Covenants (Cláusulas Restrictivas)

**¿Qué son?**
Condiciones que el banco impone en el contrato de crédito. Si la empresa las viola → el banco puede acelerar el pago (exigir todo de vuelta).

**Financial Covenants (los que puedes medir):**
```python
covenants_tipicos = {
    "Minimum DSCR":         {"metric": "dscr", "op": ">=", "threshold": 1.25},
    "Maximum D/E":          {"metric": "debt_to_equity", "op": "<=", "threshold": 3.0},
    "Minimum Current Ratio":{"metric": "current_ratio", "op": ">=", "threshold": 1.5},
    "Minimum Net Worth":    {"metric": "equity", "op": ">=", "threshold": 1_000_000},
    "Maximum CapEx":        {"metric": "capex", "op": "<=", "threshold": 500_000},
}
```

**Headroom (Colchón):**
```python
headroom = (current_value - threshold) / threshold * 100
# Headroom de 20% = tiene 20% de margen antes de violar
# Headroom < 10% = "thin cushion" → warning
# Headroom < 0% = VIOLACIÓN → default trigger
```

---

### 3.6 Stress Testing

**¿Qué es?**
Simular escenarios adversos para ver si la empresa sobrevive.

**Variables a estresar:**
| Variable | Conservative | Aggressive |
|:---|:---|:---|
| Revenue | -15% | -30% |
| COGS | +5% | +10% |
| Interest Rate | +200bps | +500bps |

**Qué mirar en cada escenario:**
1. ¿DSCR sigue > 1.0? (¿Puede pagar la deuda?)
2. ¿Working Capital sigue positivo? (¿Sobrevive operativamente?)
3. ¿FCF sigue positivo? (¿O necesita rescue financing?)
4. ¿Viola algún covenant?

**En código:**
```python
def apply_stress(data: FinancialData, scenario: StressScenario) -> FinancialData:
    stressed = data.copy()
    stressed.income_statement.revenue *= (1 + scenario.revenue_shock)
    stressed.income_statement.cost_of_goods_sold *= (1 + scenario.cogs_increase)
    stressed.income_statement.interest_expense *= (1 + scenario.interest_rate_shock)
    # Recalcular derivados
    return recalculate_derived_fields(stressed)
```

---

## 4. Métricas de Crecimiento (Pensar como Inversionista)

### 4.1 Revenue CAGR (Compound Annual Growth Rate)

```python
cagr = (revenue_final / revenue_initial) ** (1 / years) - 1
# CAGR > 20% = crecimiento fuerte
# CAGR > 40% = hypergrowth (raro, típico de tech)
```

### 4.2 Gross Margin Expansion

```python
margin_expansion = gross_margin_t - gross_margin_t_minus_1
# Si expande → cada vez más eficiente (positivo)
# Si contrae → costos están comiendo margen (negativo)
```

### 4.3 Rule of 40

```python
rule_of_40 = revenue_growth_pct + ebitda_margin_pct
# > 40 = empresa de alta calidad (crecimiento + rentabilidad)
# Ejemplo: 30% growth + 15% margin = 45 → PASA
# Ejemplo: 10% growth + 5% margin = 15 → NO PASA
```

### 4.4 Return on Equity (ROE)

```python
roe = net_income / total_stockholders_equity
# > 15% = buen retorno para accionistas
# Descomposición DuPont: ROE = Net Margin × Asset Turnover × Leverage
# Esto te dice SI el ROE viene de eficiencia o de deuda
```

---

## 5. Conceptos Avanzados (Semanas 6+)

### 5.1 PD / LGD / EAD (Basilea II/III)

**PD (Probability of Default):**
- Probabilidad de que la empresa no pague.
- Tu Z-Score es un proxy: Z < 1.81 → PD alta (~35-60%).
- En producción se estima con modelos logísticos + datos históricos.

**LGD (Loss Given Default):**
- Si no paga, ¿cuánto pierdes?
- Depende de: colateral, seniority de la deuda, jurisdicción.
- Estándar: 40-60% para deuda senior unsecured.
- PyMEs sin colateral: LGD ~70-80%.

**EAD (Exposure at Default):**
- ¿Cuánto te debe cuando deja de pagar?
- Para un préstamo: monto desembolsado - pagos recibidos.
- Para línea de crédito: puede ser mayor al monto actual (drawdown risk).

**Expected Loss:**
```python
expected_loss = pd * lgd * ead
# Si PD=5%, LGD=60%, EAD=$1M → EL = $30,000
# El banco debe provisionar $30,000 contra esta exposición
```

### 5.2 IFRS vs NIF (MX GAAP)

**Diferencias clave para el pipeline:**
| Concepto | US GAAP / IFRS | NIF (México) |
|:---|:---|:---|
| Nomenclatura | "Total Assets" | "Activo Total" |
| Formato numérico | 1,000,000.00 | 1.000.000,00 (o mixto) |
| Moneda | USD | MXN (pesos) |
| Depreciación | Línea recta o acelerada | Similar, pero nomenclatura diferente |
| Inventarios | FIFO/LIFO | Generalmente FIFO |

**Implicación para el código:**
- El `schema_normalizer.py` debe manejar ambas nomenclaturas.
- El parser numérico debe detectar si la coma es separador de miles o decimal.
- El tipo de cambio debe ser configurable.

### 5.3 Shadow Accounting (Realidad LATAM)

**El problema:**
- Muchas PyMEs en LATAM llevan 2 juegos de libros:
  1. El "real" (para el dueño).
  2. El "fiscal" (para el SAT/SUNAT/DIAN).
- Los estados financieros que recibes pueden no reflejar la realidad.

**Qué puedes hacer (en el código):**
- **Data completeness score:** Si faltan muchos campos → flag.
- **Reconciliation failures:** Si BS no cuadra → posible manipulación.
- **Revenue/Employee ratio:** Si es anormalmente bajo → posible sub-reporte.
- **Cash ratio muy bajo con buenas ventas:** Posible fuga de efectivo.

---

## 6. Glosario Rápido (Referencia)

| Término | Fórmula/Definición | Para qué sirve |
|:---|:---|:---|
| **Revenue** | Ventas totales | Tamaño del negocio |
| **COGS** | Costo directo de producción | Eficiencia de producción |
| **Gross Profit** | Revenue - COGS | Margen del producto |
| **EBIT** | Operating Income | Rentabilidad operativa |
| **EBITDA** | EBIT + D&A | Cash proxy operativo |
| **Net Income** | Bottom line (después de todo) | Rentabilidad total |
| **FCF** | CFO - CapEx | Cash "libre" real |
| **Working Capital** | CA - CL | Colchón de liquidez |
| **Current Ratio** | CA / CL | Test de liquidez rápido |
| **DSCR** | EBITDA / Debt Service | ¿Puede pagar la deuda? |
| **D/E** | Total Debt / Equity | Nivel de apalancamiento |
| **Z-Score** | 5-factor Altman | Probabilidad de quiebra |
| **ROE** | Net Income / Equity | Retorno para accionistas |
| **CAGR** | Growth compuesto | Tasa de crecimiento real |
| **Rule of 40** | Growth + Margin | Calidad de empresa tech |
| **PD** | Probability of Default | Riesgo de impago |
| **LGD** | Loss Given Default | Pérdida si no paga |
| **EAD** | Exposure at Default | Monto expuesto |
| **EL** | PD × LGD × EAD | Pérdida esperada |

---

## 7. Recursos Recomendados (Mínimos, Just-in-Time)

### Semana 1 (Fundamentos):
- **Video:** "Financial Statements Explained" (The Plain Bagel, YouTube, 15 min)
- **Lectura:** Un 10-K real de Koss Corp (SEC EDGAR) — léelo completo

### Semana 2 (Underwriting):
- **Video:** "How Banks Assess Credit Risk" (búsqueda YouTube, 20 min)
- **Lectura:** "Altman Z-Score" (Wikipedia es suficiente para el concepto)

### Semana 3 (Stress Testing):
- **Lectura:** Basel III overview (BIS.org, sección de stress testing — solo el resumen)

### Semana 6 (Scorecards):
- **Paper:** "Credit Scoring and Its Applications" (Thomas, Edelman, Crook) — Capítulo 1 solo

### Semana 9 (Narrativa):
- **Lectura:** 2-3 Credit Memos reales (buscar "credit memo template PDF")
- **Referencia:** Moody's / S&P rating methodology (solo la estructura, no el detalle)

---

*"No necesitas un MBA. Necesitas saber lo suficiente para que tu código sea correcto y tu agente suene creíble."*
