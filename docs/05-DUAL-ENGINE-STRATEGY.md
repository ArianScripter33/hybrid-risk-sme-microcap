# Estrategia de Motor Dual — Risk (Escudo) + Growth (Cohete)

## 1. El Concepto: "La Moneda de Dos Caras"

Las PyMEs y las Microcaps son, en esencia, lo mismo: **empresas pequeñas con alta volatilidad**. La diferencia está en la **pregunta** que le haces a los datos:

```
MISMOS DATOS (Revenue, Margen, Deuda, FCF)
         │
    ┌────┴────┐
    ▼         ▼
CARA A       CARA B
ESCUDO       COHETE
(Risk)       (Growth)
    │         │
    ▼         ▼
"¿Sobrevive?" "¿Explota?"
```

### Cara A: El Escudo (Credit Risk / Lending)
- **Pregunta:** "¿Esta empresa va a quebrar en 12 meses?"
- **Objetivo:** Protección del capital (Downside Protection).
- **Cliente:** Bancos, Fintechs de préstamo, Reguladores.
- **Tono:** Conservador, escéptico, datos-primero.

### Cara B: El Cohete (Growth / Investing)
- **Pregunta:** "¿Esta empresa puede multiplicar su valor x10 en 5 años?"
- **Objetivo:** Retorno asimétrico (Upside Potential).
- **Cliente:** VCs, Hedge Funds, Angel Investors, Tu propio portafolio.
- **Tono:** Analítico, forward-looking, buscando asimetría.

**La clave:** Para responder **ambas** preguntas necesitas **exactamente los mismos datos limpios.** La infraestructura técnica es idéntica.

---

## 2. Arquitectura del Switch

### 2.1 El Motor Común (Siempre ejecuta)

```
PDF → Docling OCR → Schema Normalizer → FinancialData (JSON)
                                              │
                                              ▼
                                    Módulo 2: Cálculo
                                    ┌─────────────────┐
                                    │ Todas las        │
                                    │ métricas se      │
                                    │ calculan SIEMPRE │
                                    │ (Risk + Growth)  │
                                    └────────┬────────┘
                                             │
                              ┌──────────────┼──────────────┐
                              ▼              ▼              ▼
                         Risk Metrics   Growth Metrics   Combined
```

### 2.2 El Switch en Python (Módulo 2)

**Métricas de Escudo (Risk)** — siempre se calculan:
```python
risk_metrics = {
    # Liquidez
    "current_ratio": current_assets / current_liabilities,
    "quick_ratio": (current_assets - inventory) / current_liabilities,
    "working_capital": current_assets - current_liabilities,

    # Cobertura
    "dscr": ebitda / debt_service,
    "interest_coverage": ebit / interest_expense,
    "fcf_to_debt": free_cash_flow / total_debt,

    # Apalancamiento
    "debt_to_equity": total_debt / equity,
    "debt_to_assets": total_debt / total_assets,
    "net_debt": total_debt - cash,

    # Quiebra
    "altman_z_score": altman_formula(...),

    # Expected Loss
    "pd_estimate": map_zscore_to_pd(z_score),
}
```

**Métricas de Cohete (Growth)** — siempre se calculan:
```python
growth_metrics = {
    # Crecimiento
    "revenue_growth_yoy": (rev_t - rev_t1) / rev_t1,
    "revenue_cagr_3y": (rev_t / rev_t3) ** (1/3) - 1,  # Si hay datos

    # Eficiencia
    "gross_margin": gross_profit / revenue,
    "gross_margin_expansion": gm_t - gm_t1,  # ¿Mejora?
    "operating_margin": operating_income / revenue,
    "ebitda_margin": ebitda / revenue,

    # Retorno
    "roe": net_income / equity,
    "roa": net_income / total_assets,
    "asset_turnover": revenue / total_assets,

    # Calidad
    "rule_of_40": revenue_growth_pct + ebitda_margin_pct,
    "fcf_yield": free_cash_flow / market_cap_proxy,
}
```

**Flags de Escudo:**
```python
RISK_FLAGS = {
    "DSCR_CRITICAL":   ("dscr", "<", 1.0, "critical"),
    "NEGATIVE_WC":     ("working_capital", "<", 0, "critical"),
    "ZSCORE_DISTRESS": ("altman_z_score", "<", 1.81, "critical"),
    "HIGH_LEVERAGE":   ("debt_to_equity", ">", 3.0, "warning"),
    "NEGATIVE_FCF":    ("free_cash_flow", "<", 0, "warning"),
}
```

**Flags de Cohete:**
```python
GROWTH_FLAGS = {
    "RULE_OF_40_PASS":     ("rule_of_40", ">", 40, "positive"),
    "HYPERGROWTH":         ("revenue_growth_yoy", ">", 0.40, "positive"),
    "MARGIN_EXPANSION":    ("gross_margin_expansion", ">", 0.02, "positive"),
    "HIGH_ROE":            ("roe", ">", 0.20, "positive"),
    "REVENUE_CONTRACTION": ("revenue_growth_yoy", "<", 0, "negative"),
    "MARGIN_COMPRESSION":  ("gross_margin_expansion", "<", -0.03, "negative"),
    "VALUE_TRAP":          ("roe", "<", 0.05, "negative"),  # Barato pero sin retorno
}
```

### 2.3 El Switch en Claude (Módulo 4)

El mismo `RiskReport` (que contiene TODAS las métricas) se pasa a Claude con **prompts diferentes:**

**Prompt A — El Banquero (Modo Escudo):**
```
ROLE: Senior Credit Risk Officer at a conservative bank.
TONE: Formal, cautious, data-driven. Default stance: SKEPTICAL.
FOCUS: Downside protection. Can this company service its debt?
KEY METRICS TO EMPHASIZE: DSCR, Working Capital, Z-Score, Leverage.
STRUCTURE: Risk Assessment → Mitigants → Recommended Covenants → Decision.
OUTPUT: APPROVE / CONDITIONAL / DECLINE with conditions.
NEVER speculate on growth potential. Focus on survival and repayment.
```

**Prompt B — El Inversionista (Modo Cohete):**
```
ROLE: Senior Equity Research Analyst at a growth-focused fund.
TONE: Analytical, forward-looking. Looking for asymmetric upside.
FOCUS: Can this company 10x in 5 years? Is this a compounder or a value trap?
KEY METRICS TO EMPHASIZE: Revenue CAGR, Margin Expansion, Rule of 40, ROE.
STRUCTURE: Growth Thesis → Key Drivers → Risks → Valuation Framework.
OUTPUT: STRONG BUY / BUY / HOLD / AVOID with price target framework.
Explicitly differentiate between compounders, turnarounds, and value traps.
```

**Prompt C — Ambos (Full Report):**
```
ROLE: Chief Investment Officer evaluating a private credit opportunity.
TONE: Balanced. Evaluate both the risk of loss AND the opportunity for gain.
PROVIDE: Two-sided analysis. Section 1: Credit Risk. Section 2: Growth Potential.
CONCLUDE: Risk-adjusted recommendation considering both upside and downside.
```

---

## 3. La Matriz de Decisión

Con ambos sets de métricas, el motor puede clasificar empresas en 4 cuadrantes:

```
                    GROWTH POTENTIAL
                Low ◄──────────────► High
           ┌────────────────┬────────────────┐
     Low   │                │                │
           │   ZOMBIE        │   TURNAROUND   │
  R        │   Avoid         │   Speculative  │
  I        │   No prestar    │   Alto riesgo, │
  S        │   No invertir   │   alto retorno │
  K        │                │                │
           ├────────────────┼────────────────┤
     High  │                │                │
           │   CASH COW      │   UNICORN      │
           │   Prestar OK    │   Invertir +   │
           │   Bajo retorno  │   Prestar      │
           │   Estable       │   Oportunidad  │
           │                │                │
           └────────────────┴────────────────┘
                  (Safety)        (Safety)
```

**Implementación en código:**
```python
def classify_company(report: RiskReport) -> str:
    risk_ok = report.bankruptcy.z_score_zone != "Distress" and report.coverage.dscr > 1.25
    growth_ok = report.growth.revenue_growth_yoy and report.growth.revenue_growth_yoy > 0.15

    if risk_ok and growth_ok:
        return "UNICORN"       # Prestar + Invertir
    elif risk_ok and not growth_ok:
        return "CASH_COW"      # Prestar, no invertir
    elif not risk_ok and growth_ok:
        return "TURNAROUND"    # Especulativo
    else:
        return "ZOMBIE"        # Evitar
```

---

## 4. Output por Modo

### Modo Escudo: Output para Bancos/Fintechs
```
Outputs generados:
├── Excel: "CreditAnalysis_{Company}.xlsx"
│   ├── Balance Sheet + IS + CF (con fórmulas)
│   ├── Ratio Analysis (liquidez, leverage, cobertura)
│   ├── Stress Testing (3 escenarios)
│   ├── Covenant Compliance table
│   └── Risk Score + Rating
│
├── PDF Memo: "CreditMemo_{Company}.pdf"
│   ├── Executive Summary: APPROVE/CONDITIONAL/DECLINE
│   ├── Financial Analysis (tono conservador)
│   ├── Risk Factors
│   ├── Recommended Covenants
│   └── Monitoring Triggers
│
└── JSON: risk_report.json (para integración API)
```

### Modo Cohete: Output para VCs/Fondos
```
Outputs generados:
├── Excel: "InvestmentAnalysis_{Company}.xlsx"
│   ├── Mismos estados financieros
│   ├── Growth Metrics (CAGR, margins, Rule of 40)
│   ├── Comparable Analysis framework
│   ├── Scenario Analysis (bull/base/bear)
│   └── Valuation Framework (multiples)
│
├── PDF Memo: "InvestmentMemo_{Company}.pdf"
│   ├── Investment Thesis
│   ├── Growth Drivers
│   ├── Competitive Position
│   ├── Risk Factors
│   └── Recommendation: BUY/HOLD/AVOID
│
└── JSON: growth_report.json (para screening)
```

### Modo Dual: Output Completo
Ambos reportes generados simultáneamente + clasificación en la matriz de 4 cuadrantes.

---

## 5. Caso de Uso: Screening Masivo

### Microcap Screening Pipeline
```python
async def screen_microcaps(tickers: list[str]) -> pd.DataFrame:
    """
    Procesa N empresas y clasifica en la matriz Risk/Growth.
    Ideal para encontrar 'gemas' en el universo de Microcaps.
    """
    results = []
    for ticker in tickers:
        pdf = await download_10k(ticker)
        data = await ingest_pdf(pdf)
        report = calculate_all_metrics(data)
        classification = classify_company(report)

        results.append({
            "ticker": ticker,
            "classification": classification,
            "dscr": report.coverage.dscr,
            "z_score": report.bankruptcy.altman_z_score,
            "revenue_growth": report.growth.revenue_growth_yoy,
            "ebitda_margin": report.coverage.ebitda_margin,
            "rule_of_40": report.growth.rule_of_40,
            "risk_score": report.overall_risk_score,
        })

    df = pd.DataFrame(results)
    # Filtrar las "UNICORN" — buenas para prestar Y para invertir
    unicorns = df[df.classification == "UNICORN"].sort_values("rule_of_40", ascending=False)
    return unicorns
```

### SME Lending Pipeline
```python
async def evaluate_sme_application(pdf_path: str) -> LendingDecision:
    """
    Un analista sube el PDF → el sistema devuelve decisión + Excel + Memo.
    """
    data = await ingest_pdf(pdf_path)
    report = calculate_all_metrics(data)

    # Decisión automática basada en reglas
    if report.coverage.dscr < 1.0 or report.bankruptcy.z_score_zone == "Distress":
        decision = "DECLINE"
    elif report.coverage.dscr < 1.25 or any(f.severity == "critical" for f in report.flags):
        decision = "CONDITIONAL"
    else:
        decision = "APPROVE"

    excel = generate_excel(report)
    memo = await generate_credit_memo(report, mode="risk")

    return LendingDecision(
        decision=decision,
        risk_rating=report.risk_rating,
        excel_path=excel,
        memo_path=memo,
        conditions=report.covenants if decision == "CONDITIONAL" else None,
    )
```

---

## 6. ROI Profesional del Motor Dual

| Uso del Motor | Cliente | Valor que entregas | Cómo cobras |
|:---|:---|:---|:---|
| Credit Analysis para Fintechs | Konfío, Credijusto, R2 | Reducir tiempo de evaluación 4h→3min | Sueldo / Consultoría |
| Due Diligence para Fondos | PE Funds, Venture Debt | Análisis estandarizado de portafolio | Proyecto / Suscripción |
| Microcap Screening Personal | Tú mismo | Encontrar empresas infravaloradas | Retornos de inversión |
| SME Evaluation API | Plataformas de lending | Decisión automática de crédito | API as-a-Service |
| Regulatory Reporting | Bancos | Generación de reportes para regulador | Enterprise license |

**El punto clave:** No estás construyendo un proyecto académico. Estás construyendo un **activo productivo** con al menos 5 vías de monetización.

---

## 7. Extensiones Futuras

### 7.1 Multi-Period Analysis
Comparar 3-5 años de estados financieros para detectar tendencias:
- Revenue CAGR over time
- Margin expansion/compression trend
- Debt trajectory
- Working Capital cycle changes

### 7.2 Sector Benchmarking
Comparar la empresa contra su sector:
- "Su DSCR de 1.3x está por debajo del promedio del sector (1.8x)."
- Requiere: base de datos de benchmarks por sector.

### 7.3 Portfolio View
Analizar un portafolio completo de préstamos/inversiones:
- Concentración por sector
- Distribution de risk scores
- Aggregate expected loss
- Correlation risk

### 7.4 Real-Time Monitoring
Conectar a fuentes de datos en tiempo real:
- Noticias (NLP sentiment)
- Precio de acción (para Microcaps)
- Credit bureau updates (para PyMEs)
- Trigger alerts cuando una métrica cruza un umbral

---

*"El mismo código que protege el capital de un banco puede encontrar la próxima gema de inversión. Solo cambia la pregunta."*
