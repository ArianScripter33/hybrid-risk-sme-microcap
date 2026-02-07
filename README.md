# 🎯 SME Hybrid Credit Risk Engine

A high-performance system for SME Credit Underwriting and Microcap Investment Analysis.

## 🚀 Overview

This repository contains the strategic blueprint, architectural constraints, and context injection modules for building a **Staff-Level Credit Risk Engine**.

The engine uses a **Hybrid Architecture**:

- **Deterministic Layer (Python):** Handles all financial calculations (DSCR, Z-Score, etc.) with 100% auditability.
- **Probabilistic Layer (LLM):** Orchestrates data ingestion from "dirty" sources and generates narrative investment memos.

## 📂 Project Structure

All critical strategic and contextual documentation has been organized into the following folder for review and context injection:

- `files to review/`: Contains the roadmap, post-mortems, and technical specs.

## 🛠 Tech Stack

- **Backend:** Python 3.11+
- **PDF Engine:** Docling / LlamaParse
- **Data:** Pandas / NumPy
- **Reporting:** xlsxwriter (Live Formulas)
- **Intelligence:** GPT-4o / Claude 3.5 Sonnet

## 🧠 Getting Started

To begin development, provide the contents of the `files to review/` directory to your Senior Architect agent and execute the Master Prompt found in `files to review/Repo-context-structure.md`.

---
*Zero-to-One Fintech Infrastructure.*
