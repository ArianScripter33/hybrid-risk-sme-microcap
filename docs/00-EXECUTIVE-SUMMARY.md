# Hybrid SME Credit Risk Engine — Executive Summary

## 1. Declaración de Misión

Construir un **Motor de Riesgo Crediticio Híbrido de Grado Institucional** que automatiza el análisis de solvencia de PyMEs (SMEs) en LATAM, reduciendo el tiempo de evaluación de **4 horas manuales a 3 minutos**, con output auditable y narrativa de nivel CFO.

El sistema entrena sobre datos públicos de Microcaps estadounidenses (SEC 10-K/10-Q) como proxy estructural, y está diseñado desde el día cero para tolerar la "suciedad" de datos financieros de PyMEs latinoamericanas.

---

## 2. El Problema

### 2.1 Contexto de Mercado
- **$400B+ USD** en demanda insatisfecha de crédito PyME en LATAM (IFC, World Bank).
- Los bancos rechazan ~70% de solicitudes PyME por **falta de datos estructurados**.
- Las Fintechs de préstamo necesitan motores de riesgo que procesen **estados financieros sucios** (PDFs escaneados, formatos inconsistentes, contabilidad informal).

### 2.2 El Gap Técnico
- Los analistas de crédito pasan **4-8 horas** por caso extrayendo datos manualmente.
- Los LLMs solos **alucinan números** — no son confiables para cálculos financieros.
- Los sistemas legacy (SAS, SPSS) no procesan PDFs ni generan narrativa.

### 2.3 La Oportunidad
Un sistema que combine **extracción inteligente** (LLM) + **cálculo determinista** (Python) + **narrativa institucional** (Agente CFO) resuelve las tres carencias simultáneamente.

---

## 3. La Estrategia: "Microcap-as-Proxy"

### ¿Por qué Microcaps de EE.UU.?
Los datos financieros de PyMEs LATAM son privados. Pero las **Microcaps** (empresas < $300M market cap) comparten características fundamentales con PyMEs:

| Característica | PyME LATAM | Microcap US |
|:---|:---|:---|
| Tamaño | Pequeño | Pequeño |
| Volatilidad | Alta | Alta |
| Datos disponibles | Privados/Sucios | Públicos/SEC (10-K) |
| Complejidad contable | Baja-Media | Baja-Media |
| Riesgo de quiebra | Alto | Alto |

**Ventaja:** Usamos datos limpios de la SEC para construir y validar la arquitectura, luego adaptamos la capa de ingesta para datos sucios de LATAM.

---

## 4. Principios de Diseño (Innegociables)

### P1: Separación de Poderes
```
LLM → Lee, Limpia, Narra (Probabilístico)
Python → Calcula, Valida, Genera Output (Determinístico)
```
**La IA NUNCA calcula números.** Python calcula. La IA solo escribe código y genera narrativa. Esto elimina el problema de "Caja Negra" que hundió a TAVI.

### P2: Auditabilidad Total
- Los Excels tienen **fórmulas vivas** (`=B2/B3`), no valores pegados.
- Cada cálculo tiene un **audit trail** que un regulador puede verificar.
- Las celdas de input son azules; las de fórmulas son negras/protegidas.

### P3: Tolerancia a Suciedad (LATAM-Ready)
- El pipeline de ingesta acepta PDFs escaneados, imágenes, formatos mixtos.
- El schema normalizer mapea variaciones locales (`Ventas`, `Ingresos`, `Facturación`) → `revenue`.
- Validación cruzada: `Assets = Liabilities + Equity` (si no cuadra → flag).

### P4: Doble Propósito (Risk + Growth)
El mismo core de datos alimenta dos modos:
- **Modo Escudo (Lending/Banks):** DSCR, Z-Score, Covenants → ¿Aprobamos el crédito?
- **Modo Cohete (Investing/VCs):** CAGR, Rule of 40, Margin Expansion → ¿Es una gema oculta?

### P5: Just-in-Time Learning
Los conceptos financieros se aprenden **cuando se programan**, no antes. Espiral de 3 pasadas:
1. **Ingesta:** "¿Dónde está el EBITDA en el PDF?"
2. **Cálculo:** "¿Cuál es la fórmula del EBITDA en Python?"
3. **Narrativa:** "¿Qué significa un EBITDA negativo para el Agente CFO?"

---

## 5. Definición de Éxito

### MVP (Semana 10)
- **Input:** Subir un PDF 10-K de Microcap.
- **Output:** Excel con fórmulas vivas + Memo PDF escrito por Agente CFO.
- **Métricas:**
  - Extracción correcta de ≥90% de campos financieros.
  - Cálculo de ≥15 ratios financieros.
  - Generación de 3 escenarios de estrés (Base, Conservador, Agresivo).
  - Memo con tono institucional ("Central Bank Speak").

### Producto Final (Semana 12)
- Interfaz Streamlit/Gradio funcional.
- Procesamiento de PDFs "sucios" de PyMEs LATAM.
- Demo video de 2 minutos listo para VCs/Fintechs.
- Deck de presentación preparado.

---

## 6. Perfil del Builder

- **Fortalezas:** Data Science/ML, RAG, Agentes LLM, orquestación, visión de producto Zero-to-One.
- **Gap a cerrar:** Vocabulario financiero estructural, underwriting, lenguaje regulatorio.
- **Perfil objetivo:** **AI Credit/Risk Systems Architect for SMEs & Fintech.**

---

## 7. Lecciones de TAVI (Anti-Patrones a Evitar)

| Error en TAVI | Corrección en este proyecto |
|:---|:---|
| Proyecciones optimistas sin sensibilidad | Stress testing obligatorio (3 escenarios) |
| Dependencia en cambios regulatorios | Diseño dentro del marco legal existente |
| IA como "Caja Negra" | Separación LLM/Python + Excel auditable |
| Sin Unit Economics | DSCR, Break-even, Payback integrados |
| Sin métricas canónicas | Framework financiero estándar completo |

---

## 8. Estructura del Repositorio

```
hybrid-risk-sme-microcap/
├── docs/                              # ← Documentación estratégica (estás aquí)
│   ├── 00-EXECUTIVE-SUMMARY.md        # Visión y principios
│   ├── 01-ARCHITECTURE.md             # Arquitectura técnica detallada
│   ├── 02-12-WEEK-MASTER-PLAN.md      # Plan día por día (12 semanas)
│   ├── 03-FINANCIAL-LEARNING-PATH.md  # Ruta de aprendizaje financiero
│   ├── 04-CAREER-ROADMAP.md           # Roadmap profesional
│   ├── 05-DUAL-ENGINE-STRATEGY.md     # Estrategia Risk + Growth
│   └── 06-TECH-STACK-RATIONALE.md     # Decisiones tecnológicas
├── files to review/                   # Contexto original (input estratégico)
├── src/                               # Código fuente (por crear)
│   ├── ingestion/                     # Módulo de Ingesta
│   ├── calculation/                   # Módulo de Cálculo Determinista
│   ├── reporting/                     # Módulo de Excel/PDF
│   ├── agents/                        # Módulo de Agentes (CFO, etc.)
│   └── orchestrator/                  # Pipeline orquestador
├── tests/                             # Tests
├── data/                              # Datos (10-K PDFs, JSONs)
├── notebooks/                         # Exploración y prototipos
├── pyproject.toml                     # Poetry config
├── Dockerfile                         # Containerización
└── README.md                          # Punto de entrada
```

---

## 9. Timeline de Alto Nivel

| Fase | Semanas | Foco | Entregable Clave |
|:---|:---|:---|:---|
| **Fase 0** | 1 | Fundamentos Financieros | JSON Schema + Ratios básicos |
| **Fase 1** | 2-3 | Credit Underwriting | Score simple + Memo + Stress tests |
| **Fase 2** | 4-5 | Ingesta de PDFs | Pipeline OCR → JSON limpio |
| **Fase 3** | 6-7 | Motor de Riesgo | Credit Engine + Dashboard |
| **Fase 4** | 8 | Excel Automático | Workbook institucional |
| **Fase 5** | 9 | Agente CFO | Memo ejecutivo PDF |
| **Fase 6** | 10 | Orquestación (MVP) | Pipeline completo end-to-end |
| **Fase 7** | 11-12 | LATAM Realism + Demo | Demo fintech + Deck VC |

---

*"Ya no eres el Data Scientist que no sabe finanzas. Eres el Arquitecto que automatiza lo que un analista senior tarda horas en hacer."*
