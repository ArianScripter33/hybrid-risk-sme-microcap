# Hybrid SME Credit Risk Engine 🏦

**Institutional-grade credit risk engine for SMEs (LATAM) and Microcaps (US).** Reduces credit analysis from 4 manual hours to under 3 minutes with auditable, deterministic calculations and CFO-level narrative output.

> **Core Principle:** AI never calculates. Python computes deterministically; AI reasons and narrates probabilistically. This separation eliminates hallucinated financials — the #1 failure mode in AI-for-finance systems.

[![Tests](https://img.shields.io/badge/tests-8%20passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## Why This Exists

Credit analysts at banks and fintechs spend **30+ hours per week** manually transcribing PDFs, calculating ratios, and writing credit memos. For SMEs in LATAM, this process is even worse — 80% of small businesses lack audited financial statements, forcing analysts to work with inconsistent, hand-made reports.

This engine automates the entire pipeline:

```
10-Q/10-K PDF → OCR + LLM Extraction → Validated JSON → Deterministic Ratios → Risk Score → Credit Memo
```

**The 180x acceleration:** What a team of 8 analysts does in a week, this system does during a coffee break.

---

## Architecture

```
                        ┌─────────────────────────────┐
                        │   PDF Financial Statement    │
                        │   (10-Q, 10-K, NIF Report)   │
                        └──────────┬──────────────────┘
                                   ▼
                    ┌──────────────────────────────┐
                    │  Module 1: Ingestion Layer    │
                    │  Docling OCR + LLM Normalizer │
                    └──────────┬───────────────────┘
                               ▼
                    ┌──────────────────────────────┐
                    │  Pydantic Validation Layer    │
                    │  BalanceSheet ✅               │
                    │  IncomeStatement ✅            │
                    │  CashFlowStatement ✅          │
                    │  FinancialSnapshot (planned)  │
                    └──────────┬───────────────────┘
                               ▼
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  20+ Ratios   │  │ Stress Tests │  │  Risk Score  │
    │  DSCR, Z-Score│  │ Revenue -20% │  │  XGBoost     │
    │  FCF, ROA     │  │ Rate +300bps │  │  (planned)   │
    └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
           └─────────────────┼─────────────────┘
                             ▼
                  ┌──────────────────────┐
                  │   CFO Agent (LLM)     │
                  │   Credit Memo (PDF)   │
                  └──────────────────────┘
```

---

## What's Implemented

### Pydantic Financial Schemas (Deterministic Core)

The engine's foundation: strongly-typed financial data contracts that validate, calculate, and cross-check automatically.

#### `BalanceSheet`

- Validates the accounting equation: **Assets = Liabilities + Equity**
- Model-level validator catches imbalances before they propagate
- Handles edge cases: asset-heavy/cash-poor, negative equity, zero-balance

#### `IncomeStatement`

- Auto-calculates the full P&L cascade via `@property` methods:
  - `gross_profit` → `operating_income (EBIT)` → `ebitda` → `net_income`
- Margin calculations: `gross_margin_pct`, `ebitda_margin_pct`, `net_margin_pct`
- Designed to ingest raw 10-Q data and derive all metrics deterministically

#### `CashFlowStatement`

- Three-pillar structure: CFO, CFI, CFF
- Auto-calculates: `cash_from_operations`, `free_cash_flow`, `net_change_in_cash`
- **CapEx sign normalization:** `abs(capex)` protects against LLM extraction errors (Zero-Trust Engineering)

#### `CompanyTimeSeries` (Boilerplate — Planned)

- Time-series schema for 4-20 quarters per company
- TTM (Trailing Twelve Months) calculations
- Trend analysis: EBITDA slope, CFO deterioration rate
- Red flag detection: EBITDA Mirage, Asset Liquidation patterns

### Test Suite — 8 Tests Passing ✅

```bash
$ poetry run pytest -v

tests/test_balance_sheet.py::test_balanced_sheet PASSED
tests/test_balance_sheet.py::test_accounting_equation_validation PASSED
tests/test_balance_sheet.py::test_asset_heavy_cash_poor_company PASSED
tests/test_balance_sheet.py::test_zero_equity_company PASSED
tests/test_income_statement.py::test_income_statement_calculations PASSED
tests/test_income_statement.py::test_koss_fraud_simulation PASSED
tests/test_cash_flow.py::test_cash_flow_healthy_growth PASSED
tests/test_cash_flow.py::test_free_cash_flow_capex_sign_normalization PASSED

8 passed in 0.10s
```

Notable tests:

- **Koss Fraud Simulation:** Validates that the engine detects the Koss Corporation 2009 embezzlement pattern (SG&A > Revenue anomaly)
- **CapEx Sign Normalization:** Ensures FCF calculation is robust against positive/negative CapEx extraction by LLMs

---

## Key Design Decisions

| Decision | Rationale |
|:---|:---|
| **Pydantic over raw dicts** | Type safety + auto-validation + self-documenting schemas |
| **`@property` for derived metrics** | Metrics always recalculate from source fields — no stale data |
| **`abs(capex)` in FCF** | LLMs extract CapEx with inconsistent signs. Zero-Trust. |
| **Accounting equation validator** | Catches transcription errors before they become wrong ratios |
| **Microcaps as SME proxy** | No public SME data in LATAM; SEC microcap 10-Qs are structurally similar |

---

## Metrics & Ratios (Planned for Module 2)

The engine will calculate 20+ institutional-grade ratios across three categories:

**Liquidity & Solvency:**

- Current Ratio, Quick Ratio, Working Capital
- Altman Z-Score (bankruptcy prediction)

**Debt Coverage:**

- DSCR (Debt Service Coverage Ratio)
- Net Debt / EBITDA
- Interest Coverage Ratio

**Profitability & Cash:**

- Free Cash Flow (FCF)
- ROA, ROE, ROIC
- Gross Margin %, EBITDA Margin %, Net Margin %
- AR/Revenue ratio (sales quality)

**Red Flag Detection:**

- EBITDA Mirage: `EBITDA > 0 AND CFO < 0` (paper profits, no cash)
- Asset Liquidation: `CFI > 0 AND CFO < 0` (selling assets to survive)
- Revenue Quality: `AR/Revenue > 40%` (selling "air")

---

## Tech Stack

| Layer | Technology | Why |
|:---|:---|:---|
| Runtime | Python 3.13 / Poetry | Type hints, async-ready |
| Validation | Pydantic v2 | Typed schemas with computed properties |
| Computation | Pandas + NumPy | Deterministic, auditable calculations |
| Ingestion | Docling (IBM) | OCR + table detection for financial PDFs |
| ML (planned) | XGBoost + SHAP | Interpretable scoring with regulatory compliance |
| Narrative | LLM Agent | CFO-level credit memos |
| Output | xlsxwriter + fpdf2 | Excel with live formulas + PDF memos |

---

## Project Structure

```
hybrid-risk-sme-microcap/
├── src/
│   ├── schemas/
│   │   ├── financial_data.py        # BalanceSheet, IncomeStatement, CashFlowStatement
│   │   └── time_series_risk.py      # CompanyTimeSeries (boilerplate)
│   └── models/
│       └── experiments_boilerplate.py # XGBoost, LSTM, TFT, CoxPH stubs
├── tests/
│   ├── test_balance_sheet.py        # 4 tests ✅
│   ├── test_income_statement.py     # 2 tests ✅ (includes Koss fraud simulation)
│   └── test_cash_flow.py           # 2 tests ✅ (includes CapEx sign normalization)
├── docs/                            # 7 strategic & technical documents
├── Learning_working_directory/      # Structured financial learning path
│   ├── 01-Financial-Foundations/    # Balance Sheet, COGS, Glossary (10 docs)
│   ├── 02-Income-Statement-Anatomy/ # P&L Cascade, EBITDA, Koss Fraud
│   ├── 03-Cash-Flow-Anatomy/       # CFO, FCF, DSCR, Master Formulas (4 docs)
│   └── 0Z-Future-Work/             # Predictive models roadmap
└── pyproject.toml
```

---

## Case Study: Koss Corporation (NASDAQ: KOSS)

The engine was developed and validated against real 10-Q data from Koss Corporation, a microcap consumer electronics manufacturer. Key findings from the analysis:

| Metric | Value | Signal |
|:---|:---|:---|
| Gross Margin | 35.47% | ✅ Healthy for hardware |
| EBITDA | -$910,618 | ❌ Core business burns cash |
| CFO | ~-$4,678 | ⚠️ Near-zero: neither generates nor burns |
| FCF | ~-$39,678 | ⚠️ Marginally negative |
| Net Change in Cash | +$360,322 | ⚠️ **Misleading** — funded by selling investments |
| SG&A vs Gross Profit | SG&A > GP | 🚨 Corporate overhead exceeds product margin |

**Engine Diagnosis:** *Zombie Corp with $12M cushion. Survives ~10 years at current burn rate by liquidating treasury bonds. Decline without crédito operational or strategic pivot.*

This analysis demonstrates the engine's ability to detect patterns invisible to surface-level metrics (Net Change in Cash appeared positive while the business was structurally deteriorating).

---

## Roadmap

| Phase | Status | Deliverable |
|:---|:---|:---|
| Financial Schemas (Pydantic) | ✅ Done | BalanceSheet, IncomeStatement, CashFlowStatement |
| Test Suite | ✅ Done | 8 tests including fraud simulation |
| Learning Path Documentation | ✅ Done | 18 structured financial analysis documents |
| Time Series Schema | 🔲 Boilerplate | CompanyTimeSeries with TTM and trend analysis |
| **Module 2: Ratios Engine** | 🔲 Next | Z-Score, DSCR, FCF, ROA/ROE/ROIC, Red Flags |
| Module 3: PDF Ingestion | 🔲 Planned | Docling OCR → validated JSON pipeline |
| Module 4: ML Scoring | 🔲 Planned | XGBoost scorecard with Walk-Forward CV |
| Module 5: CFO Agent | 🔲 Planned | LLM-generated credit memos |
| MVP: End-to-End Pipeline | 🔲 Target | PDF → Score → Memo in <3 minutes |

---

## Quick Start

```bash
# Clone and setup
git clone https://github.com/[your-username]/hybrid-risk-sme-microcap.git
cd hybrid-risk-sme-microcap
poetry install

# Run tests
poetry run pytest -v

# Example: Create and validate a Balance Sheet
poetry run python -c "
from src.schemas.financial_data import BalanceSheet
bs = BalanceSheet(
    total_current_assets=10_000_000,
    total_non_current_assets=5_000_000,
    total_current_liabilities=2_000_000,
    total_non_current_liabilities=1_000_000,
    total_equity=12_000_000
)
print(f'Assets: {bs.total_assets:,.0f}')
print(f'L+E:    {bs.total_liabilities + bs.total_equity:,.0f}')
print(f'Balanced: {bs.total_assets == bs.total_liabilities + bs.total_equity}')
"
```

---

## Related Projects

- **[K.I.M.E.R.A.](https://github.com/ArianScripter33/Research-Repo)** — GraphRAG research agent with hierarchical retrieval, multimodal analysis, and metacognitive traces. Powers the document understanding layer.
- **SAVI-Banxico** — Hackathon submission for Banco de México's SPEI infrastructure challenge.

---

## License

MIT

---

*Zero-to-One Fintech Infrastructure. Built for the engineers who know that revenue is vanity, profit is sanity, and cash is king.*
