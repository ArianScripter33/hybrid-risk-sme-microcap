# Hybrid SME Credit Risk Engine

Motor de Riesgo Crediticio Híbrido de grado institucional para PyMEs (LATAM) y Microcaps (US). Reduce el análisis de crédito de **4 horas manuales a 3 minutos**, con output auditable y narrativa de nivel CFO.

## Arquitectura

```
PDF → [Docling OCR + LLM Normalizer] → JSON → [Python/Pandas Calculations] → Excel + PDF Memo
                                                         │
                                          ┌──────────────┼──────────────┐
                                          ▼              ▼              ▼
                                     20+ Ratios    Stress Tests    Risk Score
                                          │              │              │
                                          └──────────────┼──────────────┘
                                                         ▼
                                               [Claude CFO Agent]
                                                         │
                                                         ▼
                                              Credit Memo (PDF)
```

**Principio fundamental:** La IA NUNCA calcula números. Python calcula (determinista), la IA razona y narra (probabilística).

## Tech Stack

- **Runtime:** Python 3.11+ / Poetry / Docker
- **Ingesta:** Docling (IBM) — OCR + table detection
- **Cálculo:** Pandas + NumPy — determinístico, auditable
- **Output:** xlsxwriter (Excel con fórmulas vivas) + fpdf2 (Memos PDF)
- **ML:** scikit-learn + XGBoost — scorecards con monotonic constraints
- **Narrativa:** Claude Opus — Credit Memos institucionales
- **UI:** Streamlit (MVP)

## Documentación

Toda la documentación estratégica y técnica está en `docs/`:

| Documento | Contenido |
|:---|:---|
| [`00-EXECUTIVE-SUMMARY.md`](docs/00-EXECUTIVE-SUMMARY.md) | Visión, principios de diseño, definición de éxito |
| [`01-ARCHITECTURE.md`](docs/01-ARCHITECTURE.md) | Arquitectura de 4 módulos, Pydantic schemas, ADRs |
| [`02-12-WEEK-MASTER-PLAN.md`](docs/02-12-WEEK-MASTER-PLAN.md) | Plan día por día (60 días, 12 semanas) |
| [`03-FINANCIAL-LEARNING-PATH.md`](docs/03-FINANCIAL-LEARNING-PATH.md) | Conceptos financieros JIT con código |
| [`04-CAREER-ROADMAP.md`](docs/04-CAREER-ROADMAP.md) | Roadmap profesional: Data Scientist → Risk Architect |
| [`05-DUAL-ENGINE-STRATEGY.md`](docs/05-DUAL-ENGINE-STRATEGY.md) | Motor dual: Risk (Bancos) + Growth (VCs) |
| [`06-TECH-STACK-RATIONALE.md`](docs/06-TECH-STACK-RATIONALE.md) | Decisiones tecnológicas y trade-offs |

El contexto original del proyecto está en `files to review/`.

## Quick Start

```bash
# Setup
poetry init --name hybrid-risk-engine --python "^3.11"
poetry add pydantic pandas numpy docling xlsxwriter fpdf2 anthropic openai
poetry add --group dev pytest ruff mypy

# Run (after implementation)
poetry run python -m src.orchestrator.pipeline

# UI
poetry run streamlit run app.py
```

## Estructura del Proyecto

```
hybrid-risk-sme-microcap/
├── docs/              # Documentación estratégica y técnica
├── files to review/   # Contexto original (input estratégico)
├── src/               # Código fuente
│   ├── schemas/       # Pydantic models (contratos entre módulos)
│   ├── ingestion/     # PDF → JSON (Docling + LLM)
│   ├── calculation/   # Ratios, flags, stress tests, scoring
│   ├── reporting/     # Excel + PDF generation
│   ├── agents/        # CFO Agent (Claude)
│   └── orchestrator/  # Pipeline controller
├── tests/             # Unit + integration tests
├── data/              # 10-K PDFs, JSONs de prueba
├── notebooks/         # Exploración y prototipos
├── pyproject.toml     # Dependencies (Poetry)
└── Dockerfile         # Container
```

## Timeline

| Fase | Semanas | Entregable |
|:---|:---|:---|
| Fundamentos + Schemas | 1 | JSON Schema + Ratios básicos |
| Credit Underwriting | 2-3 | DSCR, Z-Score, Stress Tests |
| Ingesta de PDFs | 4-5 | Pipeline OCR → JSON |
| Motor de Riesgo (ML) | 6-7 | Scorecard + Backtesting |
| Excel Automático | 8 | Workbook con fórmulas vivas |
| Agente CFO | 9 | Memos PDF institucionales |
| **MVP** | **10** | **Pipeline end-to-end + UI** |
| LATAM + Demo | 11-12 | Adaptación + Video + Deck |

---

*Zero-to-One Fintech Infrastructure.*
