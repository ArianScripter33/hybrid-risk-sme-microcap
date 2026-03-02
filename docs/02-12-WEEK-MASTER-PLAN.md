# Plan de Ejecución: 12 Semanas — Día por Día

> **Filosofía:** Aprende construyendo. No estudies teoría si no la vas a programar ese mismo día.
> **Cadencia:** 5 días/semana. Cada día = ~4-6 horas de trabajo enfocado.
> **Regla de Oro:** Al final de cada día, debes tener un commit con código funcional o un artefacto tangible.

### ⚠️ Ajuste de orden recomendado (Feb 2026)
**Orden original:** Fase 0 → 1 → 2 (PDFs) → 3 (ML) → 4-7
**Orden ajustado:** Fase 0 → 1 → **3 (ML)** → **2 (PDFs)** → 4-7

**Razón:** El motor de riesgo debe funcionar impecablemente con JSONs manuales ANTES de invertir en PDF ingestion. Docling + table extraction + schema normalization es un proyecto entero en sí mismo. Si la Fase 3 funciona con datos manuales de Koss Corp, ENTONCES conectas la ingesta automática. Si inviertes 2 semanas en Docling y el motor aún no calcula bien, perdiste tiempo.

### ⚠️ Nota sobre Fase 5 (Agente CFO, Semana 9)
Antes de implementar el agente desde cero, evaluar si componentes de K.I.M.E.R.A. (DS-STAR, hallucination guards, prompt patterns) pueden reutilizarse. El Librarian Protocol y el sistema de verificación de hechos ya existen en ese codebase.

---

## FASE 0: Fundamentos Financieros + Setup (Semana 1)

### Objetivo de Negocio
Hablar el idioma financiero básico. Entender los 3 estados financieros lo suficiente para diseñar un JSON Schema que los represente.

### Concepto Financiero Clave
**Los 3 Estados Financieros:** Balance Sheet, Income Statement, Cash Flow Statement.

### Git Deliverable
`PR #1: Project scaffold + Pydantic schemas + basic ratio calculator`

---

#### Día 1 (Lun) — Setup + Balance Sheet
**Aprender:**
- Qué es un Balance Sheet (Estado de Situación Financiera).
- La ecuación fundamental: `Activos = Pasivos + Capital`.
- Diferencia entre activos circulantes y no circulantes.
- Recurso: Buscar "Balance Sheet explained for developers" (15 min) + descargar un 10-K real de SEC EDGAR (Koss Corp, ticker: KOSS).

**Programar:**
1. Inicializar el proyecto:
   ```bash
   poetry init --name hybrid-risk-engine --python "^3.11"
   poetry add pydantic pandas numpy
   poetry add --group dev pytest ruff mypy
   ```
2. Crear estructura de carpetas (`src/`, `tests/`, `data/`).
3. Implementar `src/schemas/financial_data.py` — modelo `BalanceSheet` en Pydantic.
4. Escribir un test que valide que `total_assets == total_liabilities + total_stockholders_equity`.

**Entregable:** Proyecto inicializado. `BalanceSheet` schema con test pasando.

---

#### Día 2 (Mar) — Income Statement
**Aprender:**
- Qué es un Income Statement (Estado de Resultados).
- El cascade: Revenue → Gross Profit → Operating Income → Net Income.
- Diferencia entre **Profit** (opinión contable) y **Cash** (realidad).
- Qué es EBITDA y por qué existe (eliminar decisiones contables).
- Fórmula: `EBITDA = Operating Income + Depreciation + Amortization`.

**Programar:**
1. Implementar modelo `IncomeStatement` en Pydantic.
2. Implementar modelo `CashFlowStatement`.
3. Crear `CompanyMetadata` y el schema maestro `FinancialData`.
4. Tests de validación cruzada (Net Income en IS == Net Income en CF).

**Entregable:** Los 3 schemas financieros completos con validaciones.

---

#### Día 3 (Mié) — Primeros Ratios: Liquidez
**Aprender:**
- Qué es **Working Capital** y por qué es la primera cosa que un banquero mira.
  - `Working Capital = Current Assets - Current Liabilities`
- **Current Ratio** = Current Assets / Current Liabilities (> 1.0 = puede pagar).
- **Quick Ratio** = (Current Assets - Inventory) / Current Liabilities (más conservador).
- Por qué una empresa puede ser "rentable" pero quedarse sin cash.

**Programar:**
1. Crear `src/calculation/__init__.py` y `src/calculation/liquidity.py`.
2. Implementar funciones:
   ```python
   def calculate_current_ratio(bs: BalanceSheet) -> float
   def calculate_quick_ratio(bs: BalanceSheet) -> float
   def calculate_working_capital(bs: BalanceSheet) -> float
   ```
3. Crear un JSON de ejemplo con datos reales del 10-K de Koss Corp.
4. Test: cargar JSON → calcular ratios → verificar contra valores calculados a mano.

**Entregable:** `liquidity.py` funcional con 3+ ratios y tests.

---

#### Día 4 (Jue) — EBITDA y Márgenes
**Aprender:**
- **EBITDA vs Net Income:** Por qué EBITDA es el "cash proxy" que usan los banqueros.
- **Gross Margin** = Gross Profit / Revenue (eficiencia operativa).
- **Operating Margin** = Operating Income / Revenue.
- **Net Margin** = Net Income / Revenue.
- **EBITDA Margin** = EBITDA / Revenue.

**Programar:**
1. Crear `src/calculation/coverage.py`:
   ```python
   def calculate_ebitda(is_data: IncomeStatement) -> float
   def calculate_ebitda_margin(is_data: IncomeStatement) -> float
   ```
2. Crear `src/calculation/growth.py`:
   ```python
   def calculate_gross_margin(is_data: IncomeStatement) -> float
   def calculate_operating_margin(is_data: IncomeStatement) -> float
   def calculate_net_margin(is_data: IncomeStatement) -> float
   ```
3. Tests con datos reales.

**Entregable:** Módulo de márgenes y EBITDA funcional.

---

#### Día 5 (Vie) — Deuda y Apalancamiento
**Aprender:**
- **Deuda a Corto Plazo vs Largo Plazo:** Por qué la estructura de deuda importa.
- **Debt-to-Equity Ratio** = Total Debt / Equity (cuánto riesgo toman los accionistas).
- **Debt-to-Assets** = Total Debt / Total Assets.
- **CapEx vs OpEx:** CapEx es inversión (comprar máquina), OpEx es gasto recurrente (pagar luz).
- **Free Cash Flow** = Cash from Operations - CapEx.

**Programar:**
1. Crear `src/calculation/leverage.py`:
   ```python
   def calculate_debt_to_equity(bs: BalanceSheet) -> float
   def calculate_debt_to_assets(bs: BalanceSheet) -> float
   def calculate_total_debt(bs: BalanceSheet) -> float
   def calculate_net_debt(bs: BalanceSheet) -> float
   ```
2. Agregar a `coverage.py`:
   ```python
   def calculate_free_cash_flow(cf: CashFlowStatement) -> float
   ```
3. Refactorizar: crear `LiquidityMetrics`, `LeverageMetrics`, `CoverageMetrics` como Pydantic models.
4. Merge PR #1.

**Entregable:** PR #1 mergeado. 10+ ratios calculados. Schemas validados.

---

## FASE 1: Credit Underwriting (Semanas 2-3)

### Objetivo de Negocio
Pensar como un banquero. Aprender a decidir si una empresa puede pagar un préstamo.

### Concepto Financiero Clave
**DSCR, Altman Z-Score, Covenants, Stress Testing.**

### Git Deliverable
`PR #2: DSCR + Z-Score + Flag Engine` / `PR #3: Stress Testing + Risk Score`

---

### SEMANA 2: El Motor de Decisión

#### Día 6 (Lun) — DSCR (Debt Service Coverage Ratio)
**Aprender:**
- **DSCR** = EBITDA / (Intereses + Principal de deuda del año).
- DSCR > 1.25x = puede pagar cómodamente.
- DSCR < 1.0x = no genera suficiente cash para pagar → default probable.
- Es la métrica #1 que mira un banquero. Si DSCR está mal, nada más importa.

**Programar:**
1. En `src/calculation/coverage.py`:
   ```python
   def calculate_dscr(
       ebitda: float,
       interest_expense: float,
       current_portion_ltd: float
   ) -> float:
       """
       DSCR = EBITDA / Total Debt Service
       Total Debt Service = Interest + Principal Payments (current year)
       """
       debt_service = interest_expense + current_portion_ltd
       if debt_service == 0:
           return float('inf')  # No tiene deuda que servir
       return ebitda / debt_service
   ```
2. Agregar `Interest Coverage Ratio` = EBIT / Interest Expense.
3. Tests con escenarios: empresa sana (DSCR 2.0), borderline (1.1), problemática (0.7).

**Entregable:** DSCR implementado y testeado con 3 escenarios.

---

#### Día 7 (Mar) — Altman Z-Score
**Aprender:**
- **Altman Z-Score:** Modelo de predicción de quiebra (1968, aún usado).
- Fórmula: `Z = 1.2*A + 1.4*B + 3.3*C + 0.6*D + 1.0*E`
  - A = Working Capital / Total Assets
  - B = Retained Earnings / Total Assets
  - C = EBIT / Total Assets
  - D = Market Value of Equity / Total Liabilities (usar Book Value como proxy)
  - E = Revenue / Total Assets
- Zonas: Z > 2.99 = Safe | 1.81-2.99 = Grey | < 1.81 = Distress.

**Programar:**
1. Crear `src/calculation/bankruptcy.py`:
   ```python
   def calculate_altman_z_score(
       bs: BalanceSheet, is_data: IncomeStatement
   ) -> tuple[float, str]:
       """Returns (z_score, zone)"""
   ```
2. Tests con empresa Koss Corp real + empresa ficticia en distress.

**Entregable:** Z-Score implementado con clasificación automática.

---

#### Día 8 (Mié) — Flag Engine (Sistema de Alertas)
**Aprender:**
- Concepto de **Banderas Rojas/Amarillas/Verdes** en análisis de crédito.
- Los bancos usan "triggers" automáticos: si X métrica cruza Y umbral → acción.
- Esto es el equivalente a un sistema de alarmas para tu motor.

**Programar:**
1. Crear `src/calculation/flags.py`:
   ```python
   FLAG_RULES = {
       "DSCR_CRITICAL": {"metric": "dscr", "op": "<", "threshold": 1.0, ...},
       "NEGATIVE_WC": {"metric": "working_capital", "op": "<", "threshold": 0, ...},
       # ... 10+ reglas
   }
   def evaluate_flags(metrics: dict) -> list[RiskFlag]
   ```
2. Crear modelo `RiskFlag` en `src/schemas/risk_report.py`.
3. Tests: pasar métricas de empresa sana → 0 flags critical. Empresa en problemas → flags esperados.

**Entregable:** Flag engine con 10+ reglas configurables.

---

#### Día 9 (Jue) — Composite Risk Score
**Aprender:**
- Cómo los bancos asignan **ratings** (AAA → D, simplificado).
- Concept de **scorecard**: ponderar múltiples métricas en un score único.
- No necesitas ML aquí — un weighted average funciona para el MVP.

**Programar:**
1. Crear `src/calculation/scoring.py`:
   ```python
   SCORE_WEIGHTS = {
       "dscr": 0.25, "altman_z": 0.20, "current_ratio": 0.15,
       "debt_to_equity": 0.15, "ebitda_margin": 0.10,
       "fcf_positive": 0.10, "working_capital_positive": 0.05
   }
   def calculate_risk_score(metrics: dict) -> float  # 0-100
   def score_to_rating(score: float) -> str  # "AAA" to "D"
   ```
2. Implementar el modelo completo `RiskReport` (reúne todas las métricas + flags + score).

**Entregable:** Risk Score composite funcional.

---

#### Día 10 (Vie) — Integración Semana 2 + PR
**Aprender:**
- Revisar: ¿Puedes explicar en voz alta qué es DSCR, Z-Score, y por qué importan?
- Si no puedes, re-leer. Si puedes, avanza.

**Programar:**
1. Crear función integradora:
   ```python
   def calculate_all_metrics(data: FinancialData) -> RiskReport
   ```
2. End-to-end test: JSON de Koss Corp → RiskReport completo con todas las métricas.
3. Refactorizar, limpiar, pasar `ruff` y `mypy`.
4. Merge PR #2.

**Entregable:** PR #2 mergeado. Motor de cálculo completo (15+ ratios, flags, score).

---

### SEMANA 3: Stress Testing y Covenants

#### Día 11 (Lun) — Stress Testing: Concepto
**Aprender:**
- **Stress Testing:** "¿Qué pasa si todo sale mal?"
- Los reguladores (Basilea III, Banxico) exigen que los bancos lo hagan.
- 3 escenarios estándar: Base (sin cambios), Conservador (recesión leve), Agresivo (crisis).
- Variables a estresar: Revenue (-15%, -30%), COGS (+5%, +10%), Interest Rates (+200bps, +500bps).

**Programar:**
1. Crear `src/calculation/stress.py`:
   ```python
   def apply_stress_scenario(
       data: FinancialData, scenario: StressScenario
   ) -> FinancialData:
       """Aplica shocks a los datos y devuelve datos estresados"""

   def run_stress_tests(
       data: FinancialData, scenarios: list[StressScenario]
   ) -> dict[str, RiskReport]:
       """Corre los 3 escenarios y devuelve métricas por escenario"""
   ```
2. Tests: mismo dato, 3 escenarios → DSCR debe bajar progresivamente.

**Entregable:** Stress testing engine con 3 escenarios.

---

#### Día 12 (Mar) — Covenants
**Aprender:**
- **Covenants:** Condiciones contractuales que un banco impone al prestatario.
- Ejemplo: "Si tu Current Ratio baja de 1.5x, el préstamo se acelera (lo pagas todo YA)."
- Tipos: Financial Covenants (métricas) vs. Non-Financial (restricciones operativas).
- Common covenants: Minimum DSCR, Maximum D/E, Minimum Current Ratio.

**Programar:**
1. Agregar a `src/schemas/risk_report.py`:
   ```python
   class Covenant(BaseModel):
       name: str           # "Minimum DSCR"
       metric: str         # "dscr"
       operator: str       # ">="
       threshold: float    # 1.25
       current_value: float
       in_compliance: bool
       headroom: float     # Cuánto margen tiene antes de violar

   class CovenantPackage(BaseModel):
       covenants: list[Covenant]
       all_in_compliance: bool
       weakest_covenant: str  # El que tiene menos headroom
   ```
2. Implementar `suggest_covenants(risk_report: RiskReport) -> CovenantPackage`.
3. Tests con empresa sana (todos cumplen) y empresa borderline (1 violación).

**Entregable:** Covenant engine con sugerencia automática.

---

#### Día 13 (Mié) — PD/LGD/EAD (Conceptual)
**Aprender:**
- **PD** (Probability of Default): Probabilidad de que no pague. Tu Z-Score es un proxy.
- **LGD** (Loss Given Default): Si no paga, ¿cuánto pierdo? Depende de colateral.
- **EAD** (Exposure at Default): ¿Cuánto me debe cuando deja de pagar?
- **Expected Loss** = PD × LGD × EAD.
- Para el MVP, esto es conceptual. La implementación real requiere datos históricos que no tenemos.

**Programar:**
1. Crear `src/calculation/expected_loss.py`:
   ```python
   def estimate_pd_from_zscore(z_score: float) -> float:
       """Mapeo simplificado: Z-Score → PD estimada"""
       # Basado en estudios empíricos de Altman
       if z_score > 2.99: return 0.01   # 1%
       elif z_score > 2.50: return 0.05
       elif z_score > 1.81: return 0.15
       elif z_score > 1.20: return 0.35
       else: return 0.60                 # 60%

   def calculate_expected_loss(pd: float, lgd: float, ead: float) -> float:
       return pd * lgd * ead
   ```
2. Agregar al `RiskReport`.

**Entregable:** Expected Loss estimado (simplificado).

---

#### Día 14 (Jue) — Memo de Crédito (Texto, sin agente aún)
**Aprender:**
- Estructura de un **Credit Memo** real.
- Secciones: Executive Summary, Company Overview, Financial Analysis, Risk Assessment, Recommendation.
- El tono: conservador, datos-primero, sin marketing.

**Programar:**
1. Crear un template de memo en texto plano (Jinja2 o f-strings):
   ```python
   def generate_memo_text(report: RiskReport) -> str:
       """Genera memo de crédito en texto estructurado (sin LLM por ahora)"""
   ```
2. El template usa los datos del RiskReport para llenar secciones.
3. Esto es el "baseline" contra el cual compararemos al Agente CFO en la Semana 9.

**Entregable:** Template de memo generado automáticamente (regla-based).

---

#### Día 15 (Vie) — Integración Fase 1 + PR
**Programar:**
1. Integrar stress testing + covenants + expected loss en `calculate_all_metrics()`.
2. End-to-end test completo: JSON → RiskReport con stress, covenants, EL, memo text.
3. Escribir 2-3 JSONs más de prueba (diferentes perfiles de riesgo).
4. Linting + type checking.
5. Merge PR #3.

**Entregable:** PR #3 mergeado. Motor de underwriting completo. 20+ métricas.

---

## FASE 2: Ingesta de PDFs (Semanas 4-5)

### Objetivo de Negocio
Sobrevivir datos sucios. Que el sistema pueda leer un PDF 10-K y convertirlo en el JSON que el motor necesita.

### Concepto Financiero Clave
OCR no es financiero, pero el **mapping semántico** sí: saber que "Net Sales" = "Revenue".

### Git Deliverable
`PR #4: Docling integration + PDF→JSON pipeline` / `PR #5: Batch processing + validation`

---

### SEMANA 4: El Lector de PDFs

#### Día 16 (Lun) — SEC EDGAR + Descarga de 10-Ks
**Aprender:**
- Cómo funciona SEC EDGAR (base de datos pública de filings).
- Diferencia entre 10-K (anual) y 10-Q (trimestral).
- Cómo buscar Microcaps: filtrar por market cap < $300M.

**Programar:**
1. Crear `src/utils/sec_downloader.py`:
   ```python
   def download_10k(ticker: str, year: int) -> Path:
       """Descarga el 10-K de SEC EDGAR y lo guarda localmente"""
   ```
2. Descargar 5 PDFs de ejemplo: Koss Corp, otra Microcap de manufactura, una tech, una retail, una que haya quebrado.
3. Guardar en `data/raw/`.

**Entregable:** 5 PDFs 10-K descargados y catalogados.

---

#### Día 17 (Mar) — Docling Setup + Primera Extracción
**Aprender:**
- Cómo funciona Docling: PDF → Markdown/JSON con detección de tablas.
- Diferencia entre OCR (imagen → texto) y Layout Analysis (estructura → tablas).

**Programar:**
1. `poetry add docling`
2. Crear `src/ingestion/pdf_reader.py`:
   ```python
   def extract_from_pdf(pdf_path: Path) -> DoclingResult:
       """Usa Docling para extraer texto y tablas del PDF"""
   ```
3. Correr en el PDF de Koss Corp. Inspeccionar output.
4. Identificar: ¿Dónde están las tablas del Balance Sheet? ¿Income Statement?

**Entregable:** Docling extrayendo contenido del 10-K. Identificación manual de tablas financieras.

---

#### Día 18 (Mié) — Table Extractor
**Aprender:**
- Las tablas financieras tienen headers como "Assets", "Liabilities", patrones reconocibles.
- Estrategia: buscar keywords en headers de tablas para clasificar.

**Programar:**
1. Crear `src/ingestion/table_extractor.py`:
   ```python
   def identify_financial_tables(docling_output: DoclingResult) -> dict:
       """Identifica cuáles tablas son BS, IS, CF basándose en keywords"""
       # Buscar: "total assets", "revenue", "cash from operations"
   ```
2. Extraer las 3 tablas principales como DataFrames raw.
3. Test con 2 PDFs diferentes → ¿encuentra las tablas correctas?

**Entregable:** Extractor que identifica las 3 tablas financieras principales.

---

#### Día 19 (Jue) — Schema Normalizer (LLM-Powered)
**Aprender:**
- **Normalización semántica:** "Net Sales" → `revenue`, "Stockholders' Equity" → `total_stockholders_equity`.
- Este es el punto donde el LLM agrega valor real: entender contexto.

**Programar:**
1. Crear `src/ingestion/field_aliases.py` con el diccionario completo.
2. Crear `src/ingestion/schema_normalizer.py`:
   ```python
   async def normalize_to_schema(
       raw_tables: dict, aliases: dict
   ) -> FinancialData:
       """
       Usa LLM para mapear campos raw → schema estándar.
       El LLM recibe: raw table + target schema + alias dictionary.
       Devuelve: JSON que cumple con FinancialData.
       """
   ```
3. Prompt engineering: darle al LLM la tabla raw + el schema Pydantic + pedir que llene.
4. Validar output con Pydantic.

**Entregable:** Normalizer que convierte tabla raw → FinancialData con LLM.

---

#### Día 20 (Vie) — Validation + Reconciliation
**Programar:**
1. Crear `src/ingestion/validator.py`:
   ```python
   def validate_financial_data(data: FinancialData) -> tuple[bool, list[str]]:
       """
       Ejecuta RECONCILIATION_RULES.
       Returns: (is_valid, list_of_warnings)
       """
   ```
2. Pipeline completo: PDF → Docling → Table Extract → Normalize → Validate → FinancialData.
3. Correr en 3 PDFs. Documentar cuáles campos fallan y por qué.
4. Merge PR #4.

**Entregable:** PR #4 mergeado. Pipeline PDF→JSON funcional para 1 empresa.

---

### SEMANA 5: Robustez y Batch Processing

#### Día 21 (Lun) — Handling de Errores + Fallbacks
**Programar:**
1. Agregar manejo de campos faltantes:
   ```python
   # Si Docling no encuentra un campo, usar default 0.0 + warning
   extraction_warnings.append("inventory: not found, defaulting to 0.0")
   ```
2. Implementar retry logic si LLM falla en la normalización.
3. Agregar `extraction_confidence` score basado en % de campos extraídos exitosamente.

**Entregable:** Pipeline robusto que no crashea en campos faltantes.

---

#### Día 22 (Mar) — Batch Processing (5 empresas)
**Programar:**
1. Script de batch:
   ```python
   async def process_batch(pdf_paths: list[Path]) -> list[FinancialData]:
       """Procesa múltiples PDFs en secuencia con logging"""
   ```
2. Correr los 5 PDFs descargados. Documentar resultados:
   - ¿Cuántos campos se extrajeron correctamente?
   - ¿Cuáles fallaron?
   - ¿Cuál es el extraction_confidence promedio?

**Entregable:** 5 empresas procesadas. Benchmark de calidad documentado.

---

#### Día 23 (Mié) — Data Quality Dashboard (Notebook)
**Programar:**
1. Crear `notebooks/01_data_quality.ipynb`:
   - Tabla comparativa de 5 empresas: campos extraídos vs faltantes.
   - Histograma de extraction_confidence.
   - Análisis de qué tipos de campos fallan más.
2. Esto te da visibilidad de dónde mejorar el pipeline.

**Entregable:** Notebook con análisis de calidad de extracción.

---

#### Día 24 (Jue) — Anomaly Detection en Datos Extraídos
**Aprender:**
- **Reconciliación contable:** Si Assets ≠ Liabilities + Equity → algo salió mal en extracción.
- **Sanity checks:** Revenue negativo, activos negativos, etc.

**Programar:**
1. Ampliar `validator.py` con más reglas:
   ```python
   SANITY_RULES = [
       ("revenue", ">=", 0, "Revenue cannot be negative"),
       ("total_assets", ">", 0, "Total assets must be positive"),
       ("total_current_assets", "<=", "total_assets", "Current cannot exceed total"),
   ]
   ```
2. Agregar detección de outliers: si un ratio es 100x mayor que el promedio → flag.

**Entregable:** Validator enriquecido con sanity checks.

---

#### Día 25 (Vie) — Pipeline End-to-End Integrado + PR
**Programar:**
1. Integrar Módulo 1 (ingesta) → Módulo 2 (cálculo):
   ```python
   # PDF → FinancialData → RiskReport (todo automático)
   data = await ingest_pdf("data/raw/koss_10k_2024.pdf")
   report = calculate_all_metrics(data)
   print(report.risk_rating)  # "BB"
   ```
2. End-to-end test con 3 PDFs.
3. Linting + cleanup.
4. Merge PR #5.

**Entregable:** PR #5 mergeado. Pipeline PDF→RiskReport funcional.

---

## FASE 3: Motor de Riesgo Avanzado (Semanas 6-7)

### Objetivo de Negocio
Convertir el calculador de ratios en un motor de decisión con capacidad predictiva (ML básico).

### Concepto Financiero Clave
**Scorecards, Monotonic Constraints, Backtesting, Feature Engineering.**

### Git Deliverable
`PR #6: ML Scorecard + Feature Store` / `PR #7: Backtesting + Monitoring`

---

### SEMANA 6: Credit Scorecard con ML

#### Día 26 (Lun) — Feature Engineering
**Aprender:**
- Las métricas que ya calculas SON features para un modelo de ML.
- **Feature engineering financiero:** ratios, deltas YoY, flags como binarios.

**Programar:**
1. Crear `src/calculation/features.py`:
   ```python
   def build_feature_vector(report: RiskReport) -> dict:
       """Convierte RiskReport en un vector de features para ML"""
       return {
           "dscr": report.coverage.dscr,
           "z_score": report.bankruptcy.altman_z_score,
           "current_ratio": report.liquidity.current_ratio,
           "debt_to_equity": report.leverage.debt_to_equity,
           "ebitda_margin": report.coverage.ebitda_margin,
           "negative_wc_flag": 1 if report.liquidity.working_capital < 0 else 0,
           # ...
       }
   ```
2. Generar dataset de features para las 5 empresas.

**Entregable:** Feature vector builder.

---

#### Día 27 (Mar) — Logistic Regression Scorecard
**Aprender:**
- **Scorecard bancario:** Es un modelo logístico que predice PD.
- Por qué los bancos prefieren Logistic Regression sobre Random Forest: **interpretabilidad**.
- **Monotonic constraints:** DSCR mayor → riesgo menor (siempre). El modelo debe respetar esto.

**Programar:**
1. `poetry add scikit-learn`
2. Crear `src/calculation/scorecard.py`:
   ```python
   def train_scorecard(features_df: pd.DataFrame, labels: pd.Series):
       """Entrena un scorecard logístico con constrains monotónicas"""
   ```
3. Problema: no tenemos labels (default/no-default). Solución para MVP:
   - Usar Z-Score zone como proxy de label (Distress = 1, Safe = 0).
   - Esto es circular pero sirve para construir la infraestructura.
   - **Para CV/entrevista:** Describir como "infraestructura de scorecard con monotonic constraints" — no como "modelo ML de scoring crediticio" (los labels son proxy, no reales). La honestidad sobre limitaciones demuestra más madurez que inflar el claim.

**Entregable:** Scorecard básico entrenado (infraestructura, no accuracy).

---

#### Día 28 (Mié) — XGBoost con Monotonic Constraints
**Aprender:**
- **XGBoost** permite monotonic constraints nativas.
- Constraint: "Si DSCR sube, risk score DEBE bajar."
- Esto da poder predictivo sin perder interpretabilidad.

**Programar:**
1. `poetry add xgboost`
2. Entrenar modelo XGBoost con constraints.
3. Comparar con Logistic Regression.
4. Feature importance plot.

**Entregable:** Modelo XGBoost con monotonic constraints.

---

#### Día 29 (Jue) — Feature Store (Local)
**Aprender:**
- **Feature Store:** Un lugar centralizado donde guardas las features calculadas.
- Para MVP: un directorio de JSONs/Parquet. En producción sería Redis/Feast.

**Programar:**
1. Crear `src/utils/feature_store.py`:
   ```python
   def save_features(company: str, period: str, features: dict) -> Path
   def load_features(company: str, period: str) -> dict
   def list_all_features() -> pd.DataFrame
   ```
2. Guardar features de las 5 empresas procesadas.

**Entregable:** Feature store local funcional.

---

#### Día 30 (Vie) — Integración + PR
**Programar:**
1. Integrar scorecard en el pipeline:
   ```python
   report = calculate_all_metrics(data)
   ml_score = predict_with_scorecard(build_feature_vector(report))
   report.ml_risk_score = ml_score
   ```
2. Tests.
3. Merge PR #6.

**Entregable:** PR #6 mergeado. Scorecard ML integrado en pipeline.

---

### SEMANA 7: Backtesting y Monitoring

#### Día 31 (Lun) — Backtesting Framework
**Aprender:**
- **Backtesting:** Probar tu modelo con datos históricos.
- Para Microcaps: ¿las empresas que tu modelo marcó como "Distress" en año T, efectivamente quebraron/cayeron en año T+1?

**Programar:**
1. Descargar datos de 10-15 Microcaps adicionales (mix de survivors y delisted).
2. Procesar todas con el pipeline.
3. Crear `src/calculation/backtest.py`:
   ```python
   def backtest_model(predictions: list, actuals: list) -> BacktestReport
   ```

**Entregable:** Backtesting framework con resultados iniciales.

---

#### Día 32 (Mar) — PSI (Population Stability Index)
**Aprender:**
- **PSI:** Mide si la distribución de tus features ha cambiado (drift).
- Si PSI > 0.25 → tu modelo puede estar desactualizado.

**Programar:**
1. Implementar cálculo de PSI:
   ```python
   def calculate_psi(expected: np.ndarray, actual: np.ndarray, buckets: int = 10) -> float
   ```
2. Agregar al monitoring dashboard.

**Entregable:** PSI calculator.

---

#### Día 33 (Mié) — Fairness Check (Bias)
**Aprender:**
- **Fairness en crédito:** El modelo no debe discriminar por sector inadvertidamente.
- Revisar si el modelo penaliza excesivamente a ciertos tipos de empresas.

**Programar:**
1. Análisis de feature importance por sector.
2. Verificar que las monotonic constraints se respetan.
3. Documentar en notebook.

**Entregable:** Fairness analysis notebook.

---

#### Día 34 (Jue) — Monitoring Dashboard (Notebook)
**Programar:**
1. Crear `notebooks/02_model_monitoring.ipynb`:
   - Score distribution.
   - Feature importance.
   - PSI over time.
   - Confusion matrix.
2. Esto será la base para un dashboard real más adelante.

**Entregable:** Monitoring notebook.

---

#### Día 35 (Vie) — Integración + PR
**Programar:**
1. Clean up de todo el módulo de cálculo.
2. Documentar funciones clave.
3. Merge PR #7.

**Entregable:** PR #7 mergeado. Motor de riesgo con ML, backtesting, y monitoring.

---

## FASE 4: Excel Automático (Semana 8)

### Objetivo de Negocio
Producir output que un comité de crédito pueda usar directamente. El Excel ES el producto.

### Concepto Financiero Clave
**Sensitivity tables, formatos institucionales, auditing.**

### Git Deliverable
`PR #8: Excel Generator with live formulas`

---

### SEMANA 8: The Excel Builder

#### Día 36 (Lun) — xlsxwriter Setup + Balance Sheet Sheet
**Aprender:**
- xlsxwriter: write-only, soporta fórmulas nativas de Excel.
- Convención de colores: azul = input, blanco = fórmula, rojo = alert.

**Programar:**
1. `poetry add xlsxwriter`
2. Crear `src/reporting/excel_builder.py` y `excel_formats.py`.
3. Implementar `write_balance_sheet(workbook, report)`:
   - Celdas azules para datos raw.
   - Fórmula de validación: `=SUM(B5:B8)` para Total Assets.
   - Fórmula: `=B15+B20` (Total Liabilities + Equity = Total Assets check).

**Entregable:** Sheet de Balance Sheet con fórmulas vivas.

---

#### Día 37 (Mar) — Income Statement + Cash Flow Sheets
**Programar:**
1. Sheet de Income Statement:
   - Cascade con fórmulas: `Gross Profit = =B2-B3`.
   - EBITDA calculado con fórmula.
   - Márgenes como `=B5/B2` (formato porcentaje).
2. Sheet de Cash Flow:
   - FCF = `=B10-B15` (CFO - CapEx).

**Entregable:** 3 sheets financieros con fórmulas completas.

---

#### Día 38 (Mié) — Ratio Analysis Sheet + Conditional Formatting
**Programar:**
1. Sheet "Ratio Analysis":
   - Cada ratio referencia celdas de los sheets anteriores.
   - Ejemplo: `Current Ratio = ='Balance Sheet'!B10/'Balance Sheet'!B15`.
2. Conditional formatting:
   ```python
   worksheet.conditional_format('C2:C20', {
       'type': 'cell', 'criteria': '<', 'value': 1.0,
       'format': warning_format
   })
   ```
3. Columna de benchmarks de industria (hardcoded para MVP).

**Entregable:** Ratio Analysis sheet con semáforos visuales.

---

#### Día 39 (Jue) — Stress Testing Sheet + Summary Dashboard
**Programar:**
1. Sheet "Stress Testing":
   - 3 columnas: Base | Conservative | Aggressive.
   - Revenue estresado: `=Base*(1-0.15)` para conservative.
   - DSCR recalculado por escenario con fórmulas.
2. Sheet "Summary Dashboard":
   - Risk Rating grande.
   - Top 5 métricas en formato semáforo.
   - Top 5 flags.
3. Sheet "Flags & Alerts": tabla con todas las banderas.
4. Sheet "Data Sources & Audit": metadata, timestamps, confidence.

**Entregable:** Workbook completo con 8 sheets.

---

#### Día 40 (Vie) — Polish + PR
**Programar:**
1. Protección de celdas de fórmulas (locked).
2. Print areas configuradas.
3. Nombre del archivo: `{Company}_{Date}_CreditAnalysis.xlsx`.
4. End-to-end: PDF → JSON → Metrics → Excel.
5. Abrir Excel manualmente y verificar que las fórmulas funcionan.
6. Merge PR #8.

**Entregable:** PR #8 mergeado. Excel profesional generado automáticamente.

---

## FASE 5: Agente CFO (Semana 9)

### Objetivo de Negocio
Reemplazar el template de texto plano (Semana 3) con un agente de IA que escribe memos de crédito de nivel institucional.

### Concepto Financiero Clave
**Tono institucional, Central Bank Speak, narrativa basada en evidencia.**

### Git Deliverable
`PR #9: CFO Agent + PDF Memo Generator`

---

### SEMANA 9: The AI CFO

#### Día 41 (Lun) — Claude Integration + Banker Prompt
**Programar:**
1. `poetry add anthropic`
2. Crear `src/agents/prompts.py` con `BANKER_SYSTEM_PROMPT` y `INVESTOR_SYSTEM_PROMPT`.
3. Crear `src/agents/cfo_agent.py`:
   ```python
   async def generate_credit_memo(
       report: RiskReport, mode: str = "risk"
   ) -> str:
       """Genera memo de crédito usando Claude"""
   ```
4. Primer test: pasar RiskReport de Koss Corp → leer memo generado.

**Entregable:** Agente CFO básico generando memos.

---

#### Día 42 (Mar) — Prompt Engineering + Rubric
**Aprender:**
- **Rubric scoring:** Evaluar la calidad del memo con criterios específicos.
- ¿El memo referencia métricas específicas? ¿Usa tono conservador? ¿Sugiere covenants?

**Programar:**
1. Refinar el prompt con ejemplos de memos reales.
2. Crear `src/agents/rubric.py`:
   ```python
   def score_memo(memo_text: str, risk_report: RiskReport) -> dict:
       """Evalúa: cita métricas? tono correcto? sugiere covenants?"""
   ```
3. Iterar prompt hasta que los memos pasen la rubric.

**Entregable:** Prompt refinado con rubric scoring.

---

#### Día 43 (Mié) — Hallucination Guard
**Aprender:**
- Los LLMs pueden inventar números. Tu guard debe verificar que los números del memo coincidan con el RiskReport.

**Programar:**
1. Crear `src/agents/hallucination_guard.py`:
   ```python
   def verify_memo_numbers(memo: str, report: RiskReport) -> list[str]:
       """Extrae números del memo y verifica contra el report"""
       # Si el memo dice "DSCR is 1.5" pero el report dice 1.1 → flag
   ```
2. Si hay discrepancias → regenerar con corrección.

**Entregable:** Hallucination guard funcional.

---

#### Día 44 (Jue) — PDF Memo Generator
**Programar:**
1. `poetry add fpdf2`
2. Crear `src/reporting/pdf_builder.py`:
   ```python
   def generate_memo_pdf(memo_text: str, report: RiskReport) -> Path:
       """Genera PDF con formato institucional"""
   ```
3. Formato: logo placeholder, headers formales, footer con disclaimer.
4. Memo de 2-3 páginas.

**Entregable:** PDF Memo generado automáticamente.

---

#### Día 45 (Vie) — Dual Mode (Banker + Investor) + PR
**Programar:**
1. Implementar switch de modo:
   ```python
   memo_risk = await generate_credit_memo(report, mode="risk")
   memo_growth = await generate_credit_memo(report, mode="growth")
   ```
2. Generar ambos memos para la misma empresa. Comparar tono y contenido.
3. End-to-end: PDF → JSON → Metrics → Excel + Memo PDF.
4. Merge PR #9.

**Entregable:** PR #9 mergeado. Agente CFO dual-mode con memos en PDF.

---

## FASE 6: Orquestación — MVP (Semana 10)

### Objetivo de Negocio
Producto funcional end-to-end. Una persona puede subir un PDF y recibir Excel + Memo.

### Git Deliverable
`PR #10: Full pipeline + Streamlit UI`

---

### SEMANA 10: MVP Packaging

#### Día 46 (Lun) — Pipeline Orchestrator
**Programar:**
1. Crear `src/orchestrator/pipeline.py` con `run_pipeline()`.
2. Implementar logging estructurado en cada paso.
3. Audit trail: cada ejecución guarda un JSONL con timestamps, métricas, y paths de output.

**Entregable:** Orchestrator completo.

---

#### Día 47 (Mar) — Error Recovery + Human-in-the-Loop
**Programar:**
1. Implementar circuit breakers: si ingesta falla, intentar 3 veces.
2. Si falla definitivamente → output parcial con warning.
3. Modo human-in-the-loop: pausa después de ingesta para que el usuario revise JSON antes de calcular.

**Entregable:** Pipeline robusto con error recovery.

---

#### Día 48 (Mié) — Streamlit UI
**Programar:**
1. `poetry add streamlit`
2. Crear `app.py`:
   ```python
   st.title("Hybrid SME Credit Risk Engine")
   uploaded_file = st.file_uploader("Upload 10-K PDF")
   mode = st.selectbox("Mode", ["Risk Analysis", "Growth Analysis", "Both"])
   if st.button("Analyze"):
       results = await run_pipeline(uploaded_file, mode)
       st.download_button("Download Excel", results.excel_path)
       st.download_button("Download Memo", results.memo_path)
       st.metric("Risk Rating", results.risk_report.risk_rating)
   ```
3. Mostrar flags, score, y key metrics en la UI.

**Entregable:** Streamlit UI funcional.

---

#### Día 49 (Jue) — Testing End-to-End
**Programar:**
1. Test con 5 PDFs diferentes.
2. Documentar: tiempo de procesamiento, calidad de output, errores encontrados.
3. Fix bugs críticos.

**Entregable:** 5 análisis completos generados.

---

#### Día 50 (Vie) — MVP Launch + PR
**Programar:**
1. Cleanup final.
2. README actualizado con instrucciones de uso.
3. `Dockerfile` funcional.
4. Merge PR #10.
5. Tag: `v0.1.0-mvp`.

**Entregable:** MVP LANZADO. PR #10 mergeado. Tag v0.1.0.

---

## FASE 7: LATAM Realism + Demo (Semanas 11-12)

### Objetivo de Negocio
Demostrar que el sistema funciona con datos reales de LATAM y preparar materiales para presentar a Fintechs/VCs.

### Git Deliverable
`PR #11: LATAM adaptation` / `PR #12: Demo materials`

---

### SEMANA 11: LATAM Adaptation

#### Día 51 (Lun) — PDFs Sucios de PyMEs
**Aprender:**
- **IFRS vs NIF (MX GAAP):** Diferencias principales en nomenclatura.
- **Shadow accounting:** PyMEs en LATAM a menudo tienen 2 juegos de libros.
- **Missing data:** Espera que el 30-40% de campos no existan.

**Programar:**
1. Buscar ejemplos de estados financieros de PyMEs LATAM (Google Images, PDFs de ejemplo).
2. Agregar 5+ nuevos aliases en español al diccionario:
   ```python
   "revenue": [..., "ingresos por servicios", "ventas de exportación"],
   ```
3. Ajustar `schema_normalizer.py` para manejar formato MXN, comas como decimales, etc.

**Entregable:** Pipeline adaptado para documentos en español.

---

#### Día 52 (Mar) — Handling de Datos Faltantes
**Programar:**
1. Estrategia de imputation:
   - Si falta D&A → EBITDA = Operating Income (proxy).
   - Si falta Interest Expense → no calcular DSCR (flag como "insufficient data").
   - Si falta Cash Flow Statement completo → usar solo BS + IS.
2. Agregar `data_completeness_score` al report.

**Entregable:** Pipeline que no crashea con datos 60% completos.

---

#### Día 53 (Mié) — Multi-Currency + Multi-Language
**Programar:**
1. Soporte para MXN, COP, BRL, ARS.
2. Normalización: todo se convierte a USD para comparación (exchange rate configurable).
3. Prompts del Agente CFO en español si el documento fuente es en español.

**Entregable:** Soporte multi-moneda y multi-idioma.

---

#### Día 54 (Jue) — Testing con Datos LATAM
**Programar:**
1. Procesar 3 documentos de PyMEs LATAM.
2. Comparar output con un análisis manual.
3. Documentar gaps y limitaciones.
4. Merge PR #11.

**Entregable:** PR #11 mergeado. LATAM-ready.

---

#### Día 55 (Vie) — Performance Optimization
**Programar:**
1. Benchmark: tiempo promedio por PDF.
2. Identificar bottlenecks (probablemente OCR y LLM calls).
3. Implementar caching de LLM responses.
4. Target: < 3 minutos por análisis completo.

**Entregable:** Pipeline optimizado.

---

### SEMANA 12: Demo Day Preparation

#### Día 56 (Lun) — Demo Script + Video Plan
**Hacer:**
1. Escribir guión del demo de 2 minutos:
   - 0:00 — "El problema: PyMEs en LATAM necesitan crédito, pero sus datos son un caos."
   - 0:30 — "La solución: Subo el PDF..."
   - 1:00 — "En 3 minutos, tengo Excel con fórmulas vivas..."
   - 1:30 — "Y un memo de crédito escrito por IA con tono institucional."
   - 2:00 — "Esto reduce el análisis de 4 horas a 3 minutos."
2. Practicar el demo 3 veces.

**Entregable:** Guión del demo finalizado.

---

#### Día 57 (Mar) — Grabar Demo Video
**Hacer:**
1. Grabar screen recording del sistema funcionando.
2. Voice-over explicando cada paso.
3. Editar a 2 minutos máximo.
4. Subir a YouTube/Loom.

**Entregable:** Video demo publicado.

---

#### Día 58 (Mié) — Deck de Presentación
**Hacer:**
1. Crear deck de 8-10 slides:
   - Problema (gap de crédito PyME en LATAM).
   - Solución (Hybrid Risk Engine).
   - Arquitectura (diagrama simple).
   - Demo (screenshot o GIF).
   - Resultados (tiempo reducido, métricas generadas).
   - Mercado (TAM/SAM).
   - Perfil del builder.
   - Next steps.

**Entregable:** Deck listo para enviar.

---

#### Día 59 (Jue) — README Final + Documentation
**Programar:**
1. README completo con:
   - Quick Start.
   - Architecture overview.
   - Screenshots.
   - API docs (si aplica).
2. Cleanup final del código.
3. Merge PR #12.

**Entregable:** PR #12 mergeado. Repositorio publicable.

---

#### Día 60 (Vie) — Ship It
**Hacer:**
1. Tag `v1.0.0`.
2. Publicar repo en GitHub.
3. Publicar en LinkedIn con video demo.
4. Enviar a 5 contactos en Fintechs/Banca.
5. Publicar en Hacker News / r/fintech.

**Entregable:** PROYECTO LANZADO.

---

## Resumen de PRs y Tags

| PR | Semana | Contenido |
|:---|:---|:---|
| PR #1 | 1 | Project scaffold + Schemas + Basic ratios |
| PR #2 | 2 | DSCR + Z-Score + Flag Engine |
| PR #3 | 3 | Stress Testing + Covenants + Expected Loss |
| PR #4 | 4 | Docling integration + PDF→JSON pipeline |
| PR #5 | 5 | Batch processing + Validation + Anomaly detection |
| PR #6 | 6 | ML Scorecard + Feature Store |
| PR #7 | 7 | Backtesting + PSI + Monitoring |
| PR #8 | 8 | Excel Generator with live formulas |
| PR #9 | 9 | CFO Agent + PDF Memo Generator |
| PR #10 | 10 | Full pipeline + Streamlit UI (MVP) |
| PR #11 | 11 | LATAM adaptation |
| PR #12 | 12 | Demo materials + Final polish |

| Tag | Hito |
|:---|:---|
| `v0.1.0-mvp` | Semana 10 — MVP funcional |
| `v1.0.0` | Semana 12 — Release final |

---

## Métricas de Progreso Semanal

Al final de cada semana, valida:
1. **¿Cuántos tests pasan?** (Target: 100%).
2. **¿Cuántos ratios calcula el motor?** (Target Semana 10: 20+).
3. **¿El pipeline corre sin errores?** (Target Semana 5+: sí).
4. **¿Puedes explicar el concepto financiero de la semana en 1 minuto?** (Siempre).
5. **¿Hay un PR mergeado?** (Siempre).
