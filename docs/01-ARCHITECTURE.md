# Arquitectura Técnica — Hybrid SME Credit Risk Engine

## 1. Visión General de la Arquitectura

El sistema sigue una arquitectura de **pipeline secuencial con 4 módulos desacoplados**, cada uno con responsabilidades estrictas. La comunicación entre módulos es vía **schemas JSON tipados** (Pydantic).

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MÓDULO 1      │    │   MÓDULO 2      │    │   MÓDULO 3      │    │   MÓDULO 4      │
│   INGESTA       │───▶│   CÁLCULO       │───▶│   REPORTE       │───▶│   NARRATIVA     │
│   (The Dirty    │    │   (The Quant)   │    │   (The Excel    │    │   (The AI CFO)  │
│    Reader)      │    │                 │    │    Builder)      │    │                 │
│                 │    │                 │    │                 │    │                 │
│ Docling + LLM   │    │ Pandas/NumPy    │    │ xlsxwriter      │    │ Claude Opus     │
│ Probabilístico  │    │ Determinístico  │    │ Determinístico  │    │ Probabilístico  │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
        │                      │                      │                      │
        ▼                      ▼                      ▼                      ▼
   JSON Schema            DataFrame +              Excel .xlsx           Memo PDF +
   Estandarizado          Flag Registry            con fórmulas          Recomendación
```

### Principio Fundamental: Separación Determinista/Probabilística
```
PROBABILÍSTICO (LLM):  Módulo 1 (leer/limpiar) + Módulo 4 (narrar/interpretar)
DETERMINÍSTICO (Python): Módulo 2 (calcular) + Módulo 3 (generar output)
```

---

## 2. Módulo 1: Ingesta (The Dirty Reader)

### 2.1 Responsabilidad
Recibir **cualquier** documento financiero (PDF limpio, escaneado, imagen) y producir un **JSON estandarizado** con los datos financieros extraídos.

### 2.2 Stack Tecnológico
- **OCR/Layout:** Docling (IBM) — extracción de tablas y estructura.
- **Fallback:** LlamaParse — para PDFs especialmente complejos.
- **Limpieza/Normalización:** GPT-5.3 — mapeo semántico de campos.
- **Validación:** Pydantic — enforcement de schema.

### 2.3 Pipeline de Ingesta

```
PDF Input
    │
    ▼
┌──────────────┐
│ Docling OCR  │ ─── Extrae texto + detecta tablas + layout
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Table Extractor  │ ─── Identifica Balance Sheet, Income Statement, Cash Flow
└──────┬───────────┘
       │
       ▼
┌──────────────────────┐
│ Schema Normalizer    │ ─── LLM mapea campos a schema estándar
│ (LLM-Powered)       │     "Ventas Netas" → "revenue"
│                      │     "Pasivos Circulantes" → "current_liabilities"
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Pydantic Validator   │ ─── Valida tipos, ranges, y relaciones
│                      │     Assets == Liabilities + Equity?
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Reconciliation Check │ ─── Cruza totales entre estados financieros
│                      │     Net Income en IS == Net Income en CF?
└──────┬───────────────┘
       │
       ▼
Standardized JSON (FinancialData)
```

### 2.4 Schema Principal: `FinancialData`

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum

class FilingType(str, Enum):
    SEC_10K = "10-K"
    SEC_10Q = "10-Q"
    SME_ANNUAL = "sme_annual"
    SME_QUARTERLY = "sme_quarterly"

class BalanceSheet(BaseModel):
    """Estado de Situación Financiera / Balance General"""
    # Assets
    cash_and_equivalents: float = Field(..., description="Efectivo y equivalentes")
    accounts_receivable: float = Field(..., description="Cuentas por cobrar")
    inventory: float = Field(0.0, description="Inventarios")
    other_current_assets: float = Field(0.0, description="Otros activos circulantes")
    total_current_assets: float = Field(..., description="Total activos circulantes")

    property_plant_equipment: float = Field(0.0, description="Propiedad, planta y equipo (neto)")
    intangible_assets: float = Field(0.0, description="Activos intangibles")
    goodwill: float = Field(0.0, description="Crédito mercantil")
    other_non_current_assets: float = Field(0.0, description="Otros activos no circulantes")
    total_assets: float = Field(..., description="Total de activos")

    # Liabilities
    accounts_payable: float = Field(..., description="Cuentas por pagar")
    short_term_debt: float = Field(0.0, description="Deuda a corto plazo")
    current_portion_long_term_debt: float = Field(0.0, description="Porción circulante de deuda LP")
    other_current_liabilities: float = Field(0.0, description="Otros pasivos circulantes")
    total_current_liabilities: float = Field(..., description="Total pasivos circulantes")

    long_term_debt: float = Field(0.0, description="Deuda a largo plazo")
    other_non_current_liabilities: float = Field(0.0, description="Otros pasivos no circulantes")
    total_liabilities: float = Field(..., description="Total de pasivos")

    # Equity
    total_stockholders_equity: float = Field(..., description="Capital contable total")

class IncomeStatement(BaseModel):
    """Estado de Resultados"""
    revenue: float = Field(..., description="Ingresos / Ventas netas")
    cost_of_goods_sold: float = Field(..., description="Costo de ventas")
    gross_profit: float = Field(..., description="Utilidad bruta")

    operating_expenses: float = Field(..., description="Gastos operativos totales")
    selling_general_admin: float = Field(0.0, description="Gastos de venta, generales y admin")
    research_development: float = Field(0.0, description="Investigación y desarrollo")
    depreciation_amortization: float = Field(0.0, description="Depreciación y amortización")

    operating_income: float = Field(..., description="Utilidad operativa (EBIT)")
    interest_expense: float = Field(0.0, description="Gastos por intereses")
    other_income_expense: float = Field(0.0, description="Otros ingresos/gastos")
    income_before_tax: float = Field(..., description="Utilidad antes de impuestos")
    income_tax: float = Field(0.0, description="Impuestos")
    net_income: float = Field(..., description="Utilidad neta")

class CashFlowStatement(BaseModel):
    """Estado de Flujo de Efectivo"""
    # Operating
    net_income_cf: float = Field(..., description="Utilidad neta (inicio del flujo)")
    depreciation_amortization_cf: float = Field(0.0, description="D&A (add-back)")
    changes_in_working_capital: float = Field(0.0, description="Cambios en capital de trabajo")
    cash_from_operations: float = Field(..., description="Flujo de efectivo operativo")

    # Investing
    capital_expenditures: float = Field(0.0, description="CapEx (inversiones en PP&E)")
    acquisitions: float = Field(0.0, description="Adquisiciones")
    other_investing: float = Field(0.0, description="Otras actividades de inversión")
    cash_from_investing: float = Field(..., description="Flujo de efectivo por inversión")

    # Financing
    debt_issued: float = Field(0.0, description="Deuda emitida")
    debt_repaid: float = Field(0.0, description="Deuda pagada")
    dividends_paid: float = Field(0.0, description="Dividendos pagados")
    stock_issued_repurchased: float = Field(0.0, description="Acciones emitidas/recompradas")
    cash_from_financing: float = Field(..., description="Flujo de efectivo por financiamiento")

    net_change_in_cash: float = Field(..., description="Cambio neto en efectivo")

class CompanyMetadata(BaseModel):
    """Metadatos de la empresa y el filing"""
    company_name: str
    ticker: Optional[str] = None
    cik: Optional[str] = None  # SEC Central Index Key
    filing_type: FilingType
    period_end_date: date
    fiscal_year: int
    currency: str = "USD"
    source_file: str  # Path al PDF original
    extraction_confidence: float = Field(..., ge=0.0, le=1.0)

class FinancialData(BaseModel):
    """Schema maestro — Output del Módulo 1, Input del Módulo 2"""
    metadata: CompanyMetadata
    balance_sheet: BalanceSheet
    income_statement: IncomeStatement
    cash_flow: CashFlowStatement
    notes: Optional[str] = None  # Notas al pie extraídas (texto libre)
    extraction_warnings: list[str] = []  # Campos que no se pudieron extraer
```

### 2.5 Diccionario de Normalización (Extracto)

El LLM usa un diccionario de mapeo para normalizar variaciones lingüísticas:

```python
FIELD_ALIASES = {
    "revenue": [
        "ventas", "ventas netas", "ingresos", "ingresos netos",
        "facturación", "net sales", "net revenue", "total revenue",
        "sales", "turnover"
    ],
    "cost_of_goods_sold": [
        "costo de ventas", "costo de lo vendido", "cost of sales",
        "cost of revenue", "cogs", "costo de producción"
    ],
    "accounts_receivable": [
        "cuentas por cobrar", "clientes", "receivables",
        "trade receivables", "deudores comerciales"
    ],
    "total_current_liabilities": [
        "pasivos circulantes", "pasivo a corto plazo",
        "current liabilities", "pasivos corrientes"
    ],
    # ... 50+ campos más
}
```

### 2.6 Validaciones Cruzadas (Reconciliation)

```python
RECONCILIATION_RULES = [
    # Balance Sheet debe cuadrar
    ("total_assets", "==", "total_liabilities + total_stockholders_equity",
     "tolerance_pct=0.01"),

    # Gross Profit = Revenue - COGS
    ("gross_profit", "==", "revenue - cost_of_goods_sold",
     "tolerance_pct=0.02"),

    # Net Income debe coincidir entre IS y CF
    ("income_statement.net_income", "==", "cash_flow.net_income_cf",
     "tolerance_pct=0.01"),

    # Current Assets >= Cash (sanity check)
    ("total_current_assets", ">=", "cash_and_equivalents",
     "always"),
]
```

---

## 3. Módulo 2: Cálculo (The Deterministic Quant)

### 3.1 Responsabilidad
Recibir el `FinancialData` JSON y calcular **todas las métricas financieras** de forma determinista. Produce un `RiskReport` con ratios, flags y escenarios de estrés.

### 3.2 Stack Tecnológico
- **Cálculo:** Pandas + NumPy (puro Python, sin LLM).
- **Validación:** Pydantic para output tipado.
- **Logging:** Audit trail de cada cálculo.

### 3.3 Categorías de Métricas

#### A) Métricas de Escudo (Risk/Solvencia)

```python
class LiquidityMetrics(BaseModel):
    """Ratios de Liquidez — ¿Puede pagar sus deudas a corto plazo?"""
    current_ratio: float          # Current Assets / Current Liabilities
    quick_ratio: float            # (Current Assets - Inventory) / Current Liabilities
    cash_ratio: float             # Cash / Current Liabilities
    working_capital: float        # Current Assets - Current Liabilities
    working_capital_ratio: float  # Working Capital / Total Assets

class LeverageMetrics(BaseModel):
    """Ratios de Apalancamiento — ¿Cuánta deuda tiene?"""
    debt_to_equity: float         # Total Debt / Equity
    debt_to_assets: float         # Total Debt / Total Assets
    interest_coverage: float      # EBIT / Interest Expense
    total_debt: float             # Short-term + Long-term debt
    net_debt: float               # Total Debt - Cash

class CoverageMetrics(BaseModel):
    """Ratios de Cobertura — ¿Puede servir su deuda?"""
    dscr: float                   # EBITDA / Total Debt Service
    ebitda: float                 # EBIT + D&A
    ebitda_margin: float          # EBITDA / Revenue
    free_cash_flow: float         # CFO - CapEx
    fcf_to_debt: float            # FCF / Total Debt

class BankruptcyMetrics(BaseModel):
    """Métricas de Quiebra — ¿Va a sobrevivir?"""
    altman_z_score: float         # Fórmula de Altman (5 componentes)
    z_score_zone: str             # "Safe" | "Grey" | "Distress"
    burn_rate_months: Optional[float]  # Cash / Monthly Burn (si aplica)
```

#### B) Métricas de Cohete (Growth/Potencial)

```python
class GrowthMetrics(BaseModel):
    """Métricas de Crecimiento — ¿Tiene potencial exponencial?"""
    revenue_growth_yoy: Optional[float]   # (Rev_t - Rev_t-1) / Rev_t-1
    gross_margin: float                   # Gross Profit / Revenue
    operating_margin: float               # Operating Income / Revenue
    net_margin: float                     # Net Income / Revenue
    return_on_equity: float               # Net Income / Equity
    return_on_assets: float               # Net Income / Total Assets
    asset_turnover: float                 # Revenue / Total Assets
    rule_of_40: Optional[float]           # Revenue Growth + EBITDA Margin
```

#### C) Flags y Alertas

```python
class RiskFlag(BaseModel):
    """Una alerta individual"""
    code: str           # e.g., "DSCR_LOW"
    severity: str       # "critical" | "warning" | "info"
    metric: str         # e.g., "dscr"
    value: float        # e.g., 0.8
    threshold: float    # e.g., 1.2
    message: str        # e.g., "DSCR below 1.2x — cannot service debt"

# Reglas de flags
FLAG_RULES = {
    "DSCR_CRITICAL":    {"metric": "dscr", "op": "<", "threshold": 1.0,
                         "severity": "critical", "msg": "Cannot cover debt service"},
    "DSCR_WARNING":     {"metric": "dscr", "op": "<", "threshold": 1.25,
                         "severity": "warning", "msg": "Thin debt service coverage"},
    "ZSCORE_DISTRESS":  {"metric": "altman_z_score", "op": "<", "threshold": 1.81,
                         "severity": "critical", "msg": "High bankruptcy probability (Altman)"},
    "ZSCORE_GREY":      {"metric": "altman_z_score", "op": "<", "threshold": 2.99,
                         "severity": "warning", "msg": "Grey zone — inconclusive"},
    "NEGATIVE_WC":      {"metric": "working_capital", "op": "<", "threshold": 0,
                         "severity": "critical", "msg": "Negative working capital"},
    "LOW_CURRENT":      {"metric": "current_ratio", "op": "<", "threshold": 1.0,
                         "severity": "warning", "msg": "Current ratio below 1.0x"},
    "HIGH_LEVERAGE":    {"metric": "debt_to_equity", "op": ">", "threshold": 3.0,
                         "severity": "warning", "msg": "Debt-to-Equity above 3.0x"},
    "NEGATIVE_FCF":     {"metric": "free_cash_flow", "op": "<", "threshold": 0,
                         "severity": "warning", "msg": "Negative free cash flow"},
    "GROWTH_STAR":      {"metric": "rule_of_40", "op": ">", "threshold": 40,
                         "severity": "info", "msg": "Passes Rule of 40 — strong growth profile"},
}
```

### 3.4 Motor de Stress Testing

```python
class StressScenario(BaseModel):
    """Un escenario de estrés"""
    name: str                    # "base" | "conservative" | "aggressive"
    revenue_shock: float         # e.g., -0.20 (caída de 20%)
    cogs_increase: float         # e.g., 0.10 (aumento de 10%)
    interest_rate_shock: float   # e.g., 0.03 (300bps adicionales)
    description: str

SCENARIOS = [
    StressScenario(
        name="base",
        revenue_shock=0.0,
        cogs_increase=0.0,
        interest_rate_shock=0.0,
        description="Escenario base — sin cambios"
    ),
    StressScenario(
        name="conservative",
        revenue_shock=-0.15,
        cogs_increase=0.05,
        interest_rate_shock=0.02,
        description="Recesión moderada: ventas -15%, costos +5%, tasas +200bps"
    ),
    StressScenario(
        name="aggressive",
        revenue_shock=-0.30,
        cogs_increase=0.10,
        interest_rate_shock=0.05,
        description="Crisis severa: ventas -30%, costos +10%, tasas +500bps"
    ),
]
```

### 3.5 Output del Módulo 2: `RiskReport`

```python
class RiskReport(BaseModel):
    """Output completo del análisis — alimenta Módulo 3 y 4"""
    metadata: CompanyMetadata
    financial_data: FinancialData

    # Métricas calculadas
    liquidity: LiquidityMetrics
    leverage: LeverageMetrics
    coverage: CoverageMetrics
    bankruptcy: BankruptcyMetrics
    growth: GrowthMetrics

    # Flags
    flags: list[RiskFlag]
    overall_risk_score: float  # 0-100 (composite)
    risk_rating: str           # "AAA" to "D" (simplified)

    # Stress Testing
    stress_results: dict[str, dict]  # scenario_name → recalculated metrics

    # Audit
    calculation_timestamp: str
    engine_version: str
```

---

## 4. Módulo 3: Reporte (The Excel Builder)

### 4.1 Responsabilidad
Generar un **archivo Excel profesional** con fórmulas vivas, formatos institucionales, y múltiples hojas.

### 4.2 Stack Tecnológico
- **Motor:** xlsxwriter (write-only, fórmulas nativas).
- **Alternativa:** openpyxl (read-write, para templates).

### 4.3 Estructura del Workbook

```
📊 Workbook: "{CompanyName}_CreditAnalysis_{Date}.xlsx"
│
├── Sheet 1: "Summary Dashboard"
│   ├── Key metrics overview (semáforo visual)
│   ├── Risk rating badge
│   └── Top 5 flags
│
├── Sheet 2: "Balance Sheet"
│   ├── Datos raw (celdas azules = input)
│   ├── Fórmulas de validación (Total Assets = L + E)
│   └── YoY comparativo (si hay datos multi-periodo)
│
├── Sheet 3: "Income Statement"
│   ├── Revenue → Net Income cascade
│   ├── Márgenes calculados con fórmulas (=B5/B2)
│   └── EBITDA line item
│
├── Sheet 4: "Cash Flow"
│   ├── CFO, CFI, CFF desglosados
│   ├── Free Cash Flow = CFO - CapEx (fórmula)
│   └── Net Change reconciliation
│
├── Sheet 5: "Ratio Analysis"
│   ├── Todas las métricas del RiskReport
│   ├── Cada celda es una fórmula que referencia las hojas anteriores
│   ├── Conditional formatting (rojo/amarillo/verde)
│   └── Benchmarks de industria (columna adicional)
│
├── Sheet 6: "Stress Testing"
│   ├── 3 columnas: Base | Conservative | Aggressive
│   ├── Revenue con shock aplicado (=B2*(1+shock))
│   ├── DSCR recalculado por escenario
│   └── Sensitivity table (data table de Excel)
│
├── Sheet 7: "Flags & Alerts"
│   ├── Tabla de todas las banderas
│   ├── Severity, metric, value, threshold
│   └── Color-coded por severidad
│
└── Sheet 8: "Data Sources & Audit"
    ├── Source file path
    ├── Extraction confidence
    ├── Calculation engine version
    ├── Timestamp
    └── Reconciliation results
```

### 4.4 Convenciones de Formato

```python
# Formato de celdas
CELL_FORMATS = {
    "input":    {"bg_color": "#DCE6F1", "font_color": "#000000",
                 "border": 1, "locked": False},     # Azul claro — editable
    "formula":  {"bg_color": "#FFFFFF", "font_color": "#000000",
                 "border": 1, "locked": True},       # Blanco — protegido
    "header":   {"bg_color": "#1F4E79", "font_color": "#FFFFFF",
                 "bold": True, "border": 1},          # Azul oscuro
    "warning":  {"bg_color": "#FFC7CE", "font_color": "#9C0006"},  # Rojo
    "good":     {"bg_color": "#C6EFCE", "font_color": "#006100"},  # Verde
    "neutral":  {"bg_color": "#FFEB9C", "font_color": "#9C5700"},  # Amarillo
}
```

---

## 5. Módulo 4: Narrativa (The AI CFO)

### 5.1 Responsabilidad
Recibir el `RiskReport` completo y generar un **memo de crédito institucional** en PDF, con tono de "banquero conservador senior".

### 5.2 Stack Tecnológico
- **LLM:** Claude Opus (narrativa superior, contexto largo).
- **Orquestación:** `ell` (lightweight) o custom prompt chain.
- **PDF:** fpdf2 o reportlab.

### 5.3 Estructura del Memo

```
📄 Credit Memo: "{CompanyName}" — Confidencial
│
├── 1. Executive Summary (1 párrafo)
│   └── Recomendación: APPROVE / CONDITIONAL / DECLINE
│
├── 2. Company Overview
│   └── Qué hace, tamaño, sector
│
├── 3. Financial Analysis
│   ├── 3.1 Liquidity Position
│   ├── 3.2 Leverage & Debt Structure
│   ├── 3.3 Profitability & Cash Generation
│   └── 3.4 Key Concerns (flags narrativizados)
│
├── 4. Stress Test Results
│   └── Narrativa de cada escenario
│
├── 5. Risk Assessment
│   ├── Overall Rating: [X]
│   ├── Primary Risks
│   └── Mitigants
│
├── 6. Recommendation & Conditions
│   ├── Recomendación final
│   ├── Covenants sugeridos
│   └── Monitoring triggers
│
└── Disclaimer & Methodology Note
```

### 5.4 Prompt Strategy (Dual Mode)

```python
# Modo Escudo (Banquero)
BANKER_SYSTEM_PROMPT = """
You are a Senior Credit Risk Officer at a conservative bank.
Your tone is formal, cautious, and data-driven.
You NEVER speculate. Every statement must reference a specific metric.
If data is missing, you flag it as a risk, you do not assume.
Your default stance is SKEPTICAL — the burden of proof is on the borrower.
Use "Central Bank Speak": precise, measured, institutional.
"""

# Modo Cohete (Inversionista)
INVESTOR_SYSTEM_PROMPT = """
You are a Senior Equity Research Analyst at a growth-focused fund.
Your tone is analytical but forward-looking.
You look for asymmetric upside: high growth + improving margins.
You explicitly call out whether this is a 'compounder' or a 'value trap'.
Reference Rule of 40, CAGR, and margin expansion trends.
"""
```

---

## 6. Orquestador (Pipeline Controller)

### 6.1 Flujo End-to-End

```python
class PipelineConfig(BaseModel):
    mode: str = "risk"  # "risk" | "growth" | "both"
    stress_testing: bool = True
    generate_excel: bool = True
    generate_memo: bool = True
    human_in_the_loop: bool = False  # Pausa para revisión humana

async def run_pipeline(pdf_path: str, config: PipelineConfig) -> PipelineResult:
    """
    Pipeline completo: PDF → Excel + Memo
    """
    # Módulo 1: Ingesta
    financial_data = await ingest_pdf(pdf_path)
    log_audit("ingestion_complete", financial_data.metadata)

    if config.human_in_the_loop:
        await pause_for_review(financial_data)

    # Módulo 2: Cálculo
    risk_report = calculate_metrics(financial_data, config.stress_testing)
    log_audit("calculation_complete", risk_report.overall_risk_score)

    # Módulo 3: Excel
    excel_path = None
    if config.generate_excel:
        excel_path = generate_excel(risk_report)
        log_audit("excel_generated", excel_path)

    # Módulo 4: Narrativa
    memo_path = None
    if config.generate_memo:
        memo_path = await generate_memo(risk_report, mode=config.mode)
        log_audit("memo_generated", memo_path)

    return PipelineResult(
        risk_report=risk_report,
        excel_path=excel_path,
        memo_path=memo_path,
    )
```

### 6.2 Error Handling & Retries

```python
# Cada módulo tiene circuit breakers independientes
RETRY_CONFIG = {
    "ingestion": {"max_retries": 3, "backoff": "exponential"},
    "calculation": {"max_retries": 1, "backoff": None},  # Determinístico, no retry
    "excel": {"max_retries": 2, "backoff": "linear"},
    "narrative": {"max_retries": 3, "backoff": "exponential"},
}
```

---

## 7. Infraestructura

### 7.1 Estructura de Directorios (Código)

```
src/
├── __init__.py
├── config.py                    # Settings, env vars, constants
├── schemas/
│   ├── __init__.py
│   ├── financial_data.py        # FinancialData, BalanceSheet, IS, CF
│   ├── risk_report.py           # RiskReport, Flags, Metrics
│   └── pipeline.py              # PipelineConfig, PipelineResult
├── ingestion/
│   ├── __init__.py
│   ├── pdf_reader.py            # Docling integration
│   ├── table_extractor.py       # Table detection & extraction
│   ├── schema_normalizer.py     # LLM-powered field mapping
│   ├── validator.py             # Pydantic validation + reconciliation
│   └── field_aliases.py         # FIELD_ALIASES dictionary
├── calculation/
│   ├── __init__.py
│   ├── liquidity.py             # current_ratio, quick_ratio, etc.
│   ├── leverage.py              # debt_to_equity, etc.
│   ├── coverage.py              # dscr, ebitda, fcf
│   ├── bankruptcy.py            # altman_z_score
│   ├── growth.py                # margins, CAGR, rule_of_40
│   ├── flags.py                 # Flag engine + FLAG_RULES
│   ├── stress.py                # Stress testing engine
│   └── scoring.py               # Composite risk score + rating
├── reporting/
│   ├── __init__.py
│   ├── excel_builder.py         # xlsxwriter workbook generation
│   ├── excel_formats.py         # CELL_FORMATS, styles
│   ├── pdf_builder.py           # Memo PDF generation
│   └── templates/               # PDF templates, logos
├── agents/
│   ├── __init__.py
│   ├── cfo_agent.py             # Claude integration for narrative
│   ├── prompts.py               # System prompts (banker/investor)
│   └── hallucination_guard.py   # Post-generation fact-checking
├── orchestrator/
│   ├── __init__.py
│   ├── pipeline.py              # run_pipeline(), PipelineController
│   ├── audit.py                 # Audit trail logging
│   └── retry.py                 # Circuit breakers, retry logic
└── utils/
    ├── __init__.py
    ├── logging.py               # Structured logging
    └── sec_downloader.py        # SEC EDGAR API integration
```

### 7.2 Docker

```dockerfile
FROM python:3.11-slim

# System deps for OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev

COPY src/ ./src/
COPY data/ ./data/

EXPOSE 8000
CMD ["python", "-m", "src.orchestrator.pipeline"]
```

### 7.3 Configuración de Entorno

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # LLM
    openai_api_key: str
    anthropic_api_key: str
    default_llm_model: str = "gpt-5.3"
    narrative_llm_model: str = "claude-opus-4-6"

    # Ingestion
    docling_model: str = "docling-v2"
    max_pdf_pages: int = 200
    ocr_language: str = "eng+spa"

    # Calculation
    stress_scenarios_enabled: bool = True
    flag_rules_path: str = "src/calculation/flag_rules.yaml"

    # Output
    output_dir: str = "./output"
    excel_template: str = "institutional"

    # Pipeline
    human_in_the_loop: bool = False
    audit_log_path: str = "./logs/audit.jsonl"

    class Config:
        env_file = ".env"
```

---

## 8. Diagramas de Flujo de Datos

### 8.1 Happy Path

```
User uploads PDF
       │
       ▼
[Módulo 1] PDF → Docling OCR → Raw Text/Tables
       │                              │
       │         LLM normalizes ◄─────┘
       │              │
       ▼              ▼
       Pydantic validates → FinancialData (JSON)
                                   │
                                   ▼
[Módulo 2] FinancialData → Pandas calculates 20+ ratios
                                   │
                                   ├── Flags engine checks thresholds
                                   ├── Stress testing (3 scenarios)
                                   ├── Composite scoring
                                   │
                                   ▼
                            RiskReport (JSON)
                              │           │
                    ┌─────────┘           └──────────┐
                    ▼                                 ▼
[Módulo 3] xlsxwriter generates          [Módulo 4] Claude reads report
           Excel with formulas                      writes Credit Memo
                    │                                 │
                    ▼                                 ▼
            .xlsx file                          .pdf file
                    │                                 │
                    └─────────┐           ┌───────────┘
                              ▼           ▼
                         PipelineResult
                    (excel_path, memo_path)
```

### 8.2 Error Path

```
Any module failure
       │
       ├── Retry (if retries available)
       │       │
       │       ├── Success → Continue pipeline
       │       └── Failure → Circuit break
       │
       ▼
Log to audit trail (JSONL)
       │
       ├── If ingestion fails → Return partial result + warning
       ├── If calculation fails → HALT (deterministic should never fail on valid data)
       ├── If excel fails → Return risk_report without Excel
       └── If narrative fails → Return Excel without Memo
```

---

## 9. Decisiones de Arquitectura (ADRs)

### ADR-001: LLM No Calcula
**Decisión:** Los cálculos financieros son siempre ejecutados por Python/Pandas.
**Razón:** Los LLMs alucinan números. Un banco no puede auditar una "estimación" de GPT.
**Consecuencia:** Mayor complejidad en el Módulo 2, pero 100% auditable.

### ADR-002: Fórmulas Vivas en Excel
**Decisión:** Las celdas de métricas usan fórmulas Excel, no valores pegados.
**Razón:** El analista de crédito puede modificar inputs y ver el impacto inmediatamente.
**Consecuencia:** Requiere xlsxwriter (write-only) en lugar de solo exportar DataFrames.

### ADR-003: Schema-First Design
**Decisión:** Pydantic schemas definen el contrato entre módulos.
**Razón:** Permite desarrollar módulos en paralelo y detectar errores de integración temprano.
**Consecuencia:** Setup inicial más lento, pero integración más rápida.

### ADR-004: Dual Prompt Strategy
**Decisión:** El mismo RiskReport alimenta dos prompts diferentes (Banker vs. Investor).
**Razón:** Maximiza el ROI del motor — sirve para lending Y para investing.
**Consecuencia:** Los prompts deben ser mantenidos como activos de código, no como texto ad-hoc.

### ADR-005: Docling over LlamaParse (Default)
**Decisión:** Docling como motor primario de OCR.
**Razón:** Open-source (IBM), mejor detección de tablas, no requiere API key externa.
**Consecuencia:** LlamaParse queda como fallback para PDFs que Docling no procese bien.
