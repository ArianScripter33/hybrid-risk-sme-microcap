# 📂 Hybrid SME Credit Risk Engine — Context Injection Manifest

**Project:** `hybrid-risk-sme-microcap`
**Goal:** Build a Staff-Level, Fintech-Ready Credit Risk Engine using Hybrid Architecture (Python + LLM).
**Status:** Planning & Context Definition Phase.

---

## 1. Repository Structure & File Purposes

This repository is structured to provide a **complete context injection** for an advanced AI Architect (e.g., Claude Opus 3.5, Gemini 1.5 Pro). Each file serves a specific "memory module".

| File | Purpose | Content Summary |
| :--- | :--- | :--- |
| **`00-PROMPT.md`** | **Execution Trigger** | The "Super Prompt" to start the 12-week plan generation. Usage instructions. |
| **`01-EstrategiaMacroGemini.md`** | **Initial Roadmap** | First draft of the 12-week plan. Focus on "Just-in-Time Learning" of financial concepts. |
| **`02-EstrategiaMacroGPT5.2.md`** | **Detailed Master Plan** | **[CORE TRUTH]** The refined, institutional-grade roadmap. Includes specific deliverables (Phase 0-7), architecture diagrams, and "Central Bank Speak" requirements. |
| **`03-Contexto-errores.md`** | **User Context** | "Why we are here". Profile of the Architect (Data Scientist, not Financier), Post-Mortem of "TAVI" (failed hackathon project), and learning goals. |
| **`04-Arquitectura-a-evaluar.md`** | *Duplicate* | (Currently a duplicate of `03`. Ignore in favor of `03` or use for future architecture drafts). |
| **`05-estrategia-profesional.md`** | **Advanced Strategy** | The "Double Purpose" Engine concept: Same core (Python) can calculate **Risk** (Downside/Banks) and **Growth** (Upside/VCs) just by changing the interpretation layer. |

---

## 2. Technical Constraints (Stack Definition)

* **Language:** Python 3.11+ (Strict typing, Pydantic).
* **Dependency Management:** `poetry` (Reliable reproduction).
* **Ingestion:** `Docling` (IBM) or `LlamaParse` for PDF-to-Markdown/JSON.
* **Calculation:** `pandas` / `numpy` (Deterministic only. No LLM math).
* **Output:** `xlsxwriter` (Excel with live formulas), `fpdf2` or `reportlab` for PDFs.
* **LLM Orchestration:** `ell` or `langchain` (minimalist) for narrative generation.
* **Containerization:** Docker (Standardized environment).

---

## 3. The "Context Injection" Protocol

To generate the **Final 12-Week Execution Plan**, you must feed the AI the content of these files.

### Step-by-Step Execution

1. **Read** the contents of `02-EstrategiaMacroGPT5.2.md`, `03-Contexto-errores.md`, and `05-estrategia-profesional.md`.
2. **Use** the constraint list from Section 2 above.
3. **Execute** the following **MASTER PROMPT** (copy-paste into Claude Opus/Gemini 1.5):

---

## 4. The MASTER PROMPT (Optimized)

> **Role:** Senor Fintech Architect & Technical Mentor (Staff Level).
>
> **Objective:** Generate a granular, day-by-day execution plan (12 Weeks) to build the "Hybrid SME Credit Risk Engine".
>
> **Input Context:**
> I am putting together a high-performance architecture. I have attached/pasted 3 key documents:
>
> 1. **Macro Strategy (`02-EstrategiaMacroGPT5.2.md`):** The roadmap phases, from Financial Foundations to VC Deck. **This is the Source of Truth for the timeline.**
> 2. **Context & Failures (`03-Contexto-errores.md`):** My background (Data Scientist needing Financial Literacy). Why my previous project ("TAVI") failed (lack of rigor, black box).
> 3. **Dual Strategy (`05-estrategia-profesional.md`):** The requirement for the engine to serve both "Defensive Risk" (Lending) and "Offensive Growth" (Microcap Alpha).
>
> **Technical Stack Constraint:**
>
> * Python 3.11 + Poetry + Docker.
> * **Ingestion:** Docling (OCR/Layout).
> * **Calculation:** Pandas (Deterministic). **NO LLM MATH.**
> * **Output:** Excel with LIVE FORMULAS (`xlsxwriter`).
>
> **Your Output Requirement:**
> Create a **"Builder's Log"** for the next 12 Weeks. For each week, define:
>
> * **The Financial Concept**: (e.g., "Understanding DSCR").
> * **The Code Implementation**: (e.g., "Implement `calculate_dscr(ebitda, debt_service)` in `metrics.py`").
> * **The Git Deliverable**: (e.g., "Merge PR #4: Basic Ratio Engine").
>
> **Focus:**
> Week 1 must start IMMEDIATE execution. Less theory, more coding. Integration of financial concepts must be "Just-in-Time" (learn it, code it).
>
> Await your detailed plan. 🚀
