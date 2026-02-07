# Decisiones Tecnológicas — Tech Stack Rationale

## 1. Stack Definitivo

```
LAYER           │ TECHNOLOGY          │ ROLE
────────────────┼─────────────────────┼──────────────────────────────
Runtime         │ Python 3.11+        │ Strict typing, performance
Dependencies    │ Poetry              │ Reproducible builds
Validation      │ Pydantic v2         │ Schema contracts between modules
Data            │ Pandas + NumPy      │ Deterministic calculations
PDF Ingestion   │ Docling (IBM)       │ OCR + table detection
PDF Fallback    │ LlamaParse          │ Complex PDFs that Docling misses
LLM (Code)      │ GPT-5.3             │ Code generation, data cleaning
LLM (Narrative) │ Claude Opus         │ Credit memos, narrative
Excel           │ xlsxwriter          │ Live formulas, institutional format
PDF Reports     │ fpdf2               │ Memo generation
ML              │ scikit-learn + XGB  │ Scorecards with monotonic constraints
Web UI          │ Streamlit           │ MVP interface
Container       │ Docker              │ Reproducible environment
Linting         │ Ruff                │ Fast Python linter
Type Checking   │ mypy                │ Static type safety
Testing         │ pytest              │ Unit + integration tests
```

---

## 2. Decisiones Clave y Trade-offs

### 2.1 Python 3.11+ (no 3.12/3.13)

**Decisión:** Python 3.11 como mínimo.

**Razón:**
- 3.11 tiene mejoras significativas de performance (10-60% faster).
- Mejor soporte para `typing` y `ExceptionGroup`.
- Docling y la mayoría de dependencias financieras tienen buen soporte 3.11.
- 3.12+ introduce cambios en GIL que aún no están estabilizados para todas las deps.

**Alternativa descartada:** Rust/Go para el módulo de cálculo.
- Overkill para el MVP. El bottleneck es I/O (OCR + LLM calls), no CPU.
- Pandas es lo suficientemente rápido para 1 empresa a la vez.
- Si eventualmente se necesita batch de 10K empresas → considerar Polars o Rust bindings.

---

### 2.2 Poetry (no pip, no uv, no conda)

**Decisión:** Poetry para gestión de dependencias.

**Razón:**
- `pyproject.toml` como single source of truth.
- Lock file garantiza reproducibilidad exacta.
- Separación clara de deps de producción vs desarrollo.
- Virtual environments automatizados.

**Alternativa considerada:** `uv` (de Astral, creadores de Ruff).
- Más rápido que Poetry para resolver deps.
- Pero el ecosistema aún está madurando (Feb 2026).
- **Nota:** Si para cuando empieces uv es estable, es una buena alternativa.

**Alternativa descartada:** conda.
- Demasiado pesado. No necesitamos environments con C libraries complejas.
- Docker cubre la necesidad de reproducibilidad de sistema.

---

### 2.3 Pydantic v2 (no dataclasses, no attrs)

**Decisión:** Pydantic v2 para todos los schemas.

**Razón:**
- **Validación automática:** Convierte strings a floats, detecta campos faltantes.
- **Serialización:** `.model_dump()` → JSON directo, sin código extra.
- **Performance:** v2 es 5-50x más rápido que v1 (core en Rust).
- **Documentación:** Cada campo tiene `description`, útil para el LLM normalizer.
- **Contrato entre módulos:** Si el schema cambia, los tests fallan inmediatamente.

**Alternativa descartada:** dataclasses.
- Sin validación automática. Tendrías que escribir validators a mano.
- Sin serialización a JSON nativa.
- OK para internal data, pero no para contratos entre módulos.

---

### 2.4 Docling (no Unstructured, no LlamaParse primary)

**Decisión:** Docling (IBM) como motor primario de ingesta.

**Razón:**
- **Open-source:** No requiere API key. Corre localmente.
- **Table detection:** Excelente detección de tablas en PDFs financieros.
- **Layout analysis:** Entiende estructura de página (headers, footers, multi-column).
- **Activamente mantenido** por IBM Research.

**Fallback:** LlamaParse.
- Mejor para PDFs con layouts muy complejos o escaneados de baja calidad.
- Requiere API key (servicio cloud).
- Más caro en batch processing.

**Alternativa descartada:** Unstructured.
- Bueno para documentos genéricos, menos optimizado para tablas financieras.
- Más pesado de configurar.

**Alternativa descartada:** PyMuPDF + regex.
- Funciona para PDFs nativos (no escaneados).
- Falla completamente con PDFs escaneados o con layouts complejos.
- No detecta tablas automáticamente.

---

### 2.5 xlsxwriter (no openpyxl, no pandas.to_excel)

**Decisión:** xlsxwriter para generación de Excel.

**Razón:**
- **Fórmulas nativas:** Puede escribir `=B2/B3` como fórmula real de Excel.
- **Formatos ricos:** Conditional formatting, colores, bordes, protección de celdas.
- **Gráficos:** Puede generar charts dentro del Excel.
- **Performance:** Más rápido que openpyxl para write-only operations.
- **Es lo que necesitamos:** Solo escribimos, nunca leemos.

**Alternativa considerada:** openpyxl.
- Read-write (podría leer templates).
- Más lento para write-only.
- Útil si necesitas modificar un Excel existente → no aplica para nuestro caso.

**Alternativa descartada:** pandas.to_excel.
- Exporta DataFrames como valores estáticos.
- **No genera fórmulas.** Esto viola el principio P2 (Auditabilidad).
- Un analista no puede cambiar un input y ver el impacto.

---

### 2.6 Claude Opus para Narrativa (no GPT para memos)

**Decisión:** Claude para generación de memos. GPT para código y limpieza.

**Razón de la separación:**
- **Claude Opus** tiene ventana de contexto más larga y mejor razonamiento para textos largos y complejos.
- **GPT-5.3** es superior para code generation y structured output.
- Usar cada uno en su fortaleza maximiza calidad.

**Flujo:**
```
GPT-5.3  → Limpia el PDF (structured extraction)
GPT-5.3  → Genera código Python cuando necesites
Claude   → Escribe el Credit Memo (narrativa de 2-3 páginas)
Claude   → Interpreta flags y sugiere covenants
```

**Alternativa considerada:** Solo GPT para todo.
- Funciona, pero los memos tienden a ser más "formulaic" y menos "institutional".
- Claude produce texto más natural y con mejor tone control.

**Alternativa considerada:** Solo Claude para todo.
- Funciona, pero GPT tiene mejor structured output y function calling para la parte de ingesta.

**Nota pragmática:** Si el presupuesto es limitado, puedes usar solo uno de los dos. El sistema está diseñado para que el LLM sea intercambiable. El schema (Pydantic) es el contrato, no el LLM.

---

### 2.7 scikit-learn + XGBoost (no PyTorch, no TensorFlow)

**Decisión:** Modelos tabular clásicos para el scorecard.

**Razón:**
- **Interpretabilidad:** Los bancos/reguladores necesitan entender el modelo.
- **Monotonic constraints:** XGBoost las soporta nativamente. "Si DSCR sube, riesgo baja."
- **Tamaño de datos:** Con 20-100 empresas, deep learning es overkill.
- **Feature importance:** Crucial para explicar decisiones de crédito.
- **Compliance:** Reguladores de LATAM (CNBV, SBS) piden modelos explicables.

**Alternativa descartada:** Deep learning (PyTorch/TF).
- Black box. Reguladores lo rechazan para credit scoring.
- Requiere miles de muestras. Nosotros tenemos ~20-100.
- Overkill total.

**Alternativa descartada:** LightGBM.
- Similar a XGBoost en performance.
- XGBoost tiene mejor soporte de monotonic constraints documentado.
- Ambos son válidos; XGBoost es la elección más conservadora.

---

### 2.8 Streamlit (no Gradio, no FastAPI+React)

**Decisión:** Streamlit para la UI del MVP.

**Razón:**
- **Velocidad de desarrollo:** De 0 a UI funcional en ~4 horas.
- **Python-only:** No necesitas JavaScript/React.
- **File upload + download:** Built-in, perfecto para nuestro caso.
- **Métricas y tables:** `st.metric()`, `st.dataframe()` son exactamente lo que necesitamos.

**Alternativa considerada:** Gradio.
- Más orientado a ML demos.
- Menos flexible para dashboards multi-page.
- Buena alternativa si prefieres la API de Gradio.

**Alternativa para producción:** FastAPI + React/Next.js.
- Para cuando el MVP esté validado y necesites una UI real.
- FastAPI para el backend API.
- React/Next.js para el frontend.
- Esto sería Fase 2 (post-MVP).

---

### 2.9 fpdf2 (no reportlab, no weasyprint)

**Decisión:** fpdf2 para generación de PDFs de memo.

**Razón:**
- **Lightweight:** Mínimas dependencias.
- **Suficiente:** Headers, párrafos, tablas simples, páginas.
- **Python puro:** No requiere wkhtmltopdf ni dependencias de sistema.

**Alternativa considerada:** reportlab.
- Más poderoso (pixel-perfect PDFs).
- Más complejo de aprender.
- Overkill para un memo de 2-3 páginas.
- **Upgrade path:** Si necesitas PDFs más sofisticados (branding, gráficos), migrar a reportlab.

**Alternativa descartada:** weasyprint (HTML→PDF).
- Requiere dependencias de sistema (GTK, Cairo).
- Más frágil en Docker.
- Overkill para nuestro caso.

---

### 2.10 Docker (containerización)

**Decisión:** Docker para reproducibilidad.

**Razón:**
- OCR (Docling) puede necesitar tesseract, poppler, y otras deps de sistema.
- Docker garantiza que el entorno sea idéntico en cualquier máquina.
- Necesario para eventual deploy en cloud.

**Base image:** `python:3.11-slim`.
- Slim reduce el tamaño de la imagen (~150MB vs ~900MB para full).
- Instalar solo las deps de sistema necesarias.

---

## 3. Dependency Map

```
pyproject.toml
├── [tool.poetry.dependencies] (producción)
│   ├── python = "^3.11"
│   ├── pydantic = "^2.0"
│   ├── pydantic-settings = "^2.0"
│   ├── pandas = "^2.0"
│   ├── numpy = "^1.24"
│   ├── docling = "latest"          # PDF ingestion
│   ├── xlsxwriter = "^3.0"        # Excel generation
│   ├── fpdf2 = "^2.7"             # PDF memo generation
│   ├── anthropic = "^0.30"        # Claude API
│   ├── openai = "^1.0"            # GPT API
│   ├── scikit-learn = "^1.3"      # Logistic regression
│   ├── xgboost = "^2.0"           # Gradient boosting
│   ├── streamlit = "^1.30"        # Web UI
│   ├── httpx = "^0.25"            # Async HTTP (SEC downloads)
│   └── jinja2 = "^3.1"            # Template rendering
│
├── [tool.poetry.group.dev.dependencies] (desarrollo)
│   ├── pytest = "^7.0"
│   ├── pytest-asyncio = "^0.21"
│   ├── ruff = "^0.1"              # Linting
│   ├── mypy = "^1.5"              # Type checking
│   ├── jupyter = "^1.0"           # Notebooks
│   └── ipykernel = "^6.0"
```

---

## 4. Configuración de Calidad de Código

### Ruff (Linting)
```toml
# pyproject.toml
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "SIM",  # flake8-simplify
]
```

### mypy (Type Checking)
```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
plugins = ["pydantic.mypy"]

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true
```

### pytest
```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks integration tests",
]
```

---

## 5. Estructura de Configuración (.env)

```bash
# .env (NUNCA commitear)

# LLM APIs
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Models
DEFAULT_LLM_MODEL=gpt-5.3
NARRATIVE_LLM_MODEL=claude-opus-4-6

# Ingestion
DOCLING_MODEL=docling-v2
OCR_LANGUAGE=eng+spa
MAX_PDF_PAGES=200

# Output
OUTPUT_DIR=./output
EXCEL_TEMPLATE=institutional

# Pipeline
STRESS_SCENARIOS_ENABLED=true
HUMAN_IN_THE_LOOP=false
AUDIT_LOG_PATH=./logs/audit.jsonl

# SEC (for downloading 10-Ks)
SEC_USER_AGENT="HybridRiskEngine/1.0 (your-email@example.com)"
```

---

## 6. Upgrade Paths

| Componente | MVP | Producción | Escala |
|:---|:---|:---|:---|
| **UI** | Streamlit | FastAPI + React | Next.js + Vercel |
| **DB** | JSON files | PostgreSQL | PostgreSQL + Redis cache |
| **Feature Store** | Local Parquet | SQLite | Feast / Redis |
| **ML** | XGBoost local | MLflow tracked | SageMaker / Vertex AI |
| **PDF Gen** | fpdf2 | reportlab | LaTeX templates |
| **Monitoring** | Notebooks | Grafana | Datadog / New Relic |
| **Queue** | Sequential | Celery + Redis | AWS SQS / GCP Pub/Sub |
| **Deploy** | Local Docker | AWS ECS / GCP Run | Kubernetes |
| **Auth** | None | JWT (FastAPI) | Auth0 / Clerk |

**Regla:** No prematuramente optimizar. Empezar con MVP stack. Migrar solo cuando el bottleneck sea evidente.

---

## 7. Security Considerations

### API Keys
- NUNCA en código o commits.
- `.env` file en `.gitignore`.
- En producción: AWS Secrets Manager, GCP Secret Manager, o Vault.

### Data Privacy
- PDFs de PyMEs contienen datos sensibles (ingresos, deuda, clientes).
- No enviar datos financieros a LLMs sin anonimización si es requerido por el cliente.
- Audit log registra qué datos se procesaron y cuándo.
- En producción: encriptación at-rest y in-transit.

### LLM Output Verification
- El hallucination guard verifica que los números del memo coincidan con el RiskReport.
- Los cálculos son determinísticos (Python), no dependen del LLM.
- El Excel tiene fórmulas verificables, no valores generados por IA.

---

*"Elige herramientas aburridas para problemas serios. La innovación está en la arquitectura, no en el framework."*
