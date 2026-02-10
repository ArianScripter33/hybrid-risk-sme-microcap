# Contexto del Perfil, Post-Mortem y Objetivos Estratégicos

## 1. Perfil del Arquitecto

Soy un Científico de Datos/ML y Constructor de Agentes (AI Builder) con fuerte experiencia en RAG, automatización y desarrollo de productos (UX/UI).

* **Fortaleza:** Capacidad técnica para construir sistemas complejos, orquestación de LLMs, y visión de producto "Zero-to-One".
* **Debilidad Crítica:** Falta de base financiera formal ("Financial Literacy"). No soy contador ni financiero.
* **Objetivo Profesional:** Maximizar empleabilidad en Fintech/Banca (LATAM) y adquirir las capacidades para fundar una startup de infraestructura financiera o inversión.

## 2. Análisis Post-Mortem: Proyecto "TAVI" (Hackathon Banxico)

Recientemente desarrollé una propuesta de arquitectura para pagos digitales (TAVI). Aunque la arquitectura técnica y la visión de producto eran de nivel senior, el proyecto falló ante jurados institucionales por las siguientes razones (Lecciones Aprendidas):

1. **Falta de Rigor Financiero:** Presenté proyecciones de impacto económico optimistas sin un análisis de sensibilidad, escenarios de estrés o "Unit Economics" (CAC/LTV) sólidos.
2. **Ingenuidad Regulatoria:** La solución dependía de cambios legales masivos ("Mandato Reforzado") en lugar de adaptarse a la regulación existente.
3. **Riesgo de "Caja Negra":** Propuse que la IA ejecutara transacciones, lo cual genera rechazo por riesgo operativo.
4. **Ausencia de Métricas de Negocio:** Me enfoqué en la UX y la tecnología, ignorando costos operativos (OPEX/CAPEX) y modelos de rentabilidad bancaria.

## 3. La Nueva Estrategia: "Hybrid SME Credit Risk Engine"

He decidido pivotar de "Pagos" a "Riesgo Crediticio" (SME Lending), ya que es el vertical con mayor demanda y ROI en LATAM.

**Los Principios de Diseño para este nuevo proyecto son:**

1. **Separación de Poderes:** La IA (LLM) nunca calcula números. Python calcula (determinista), la IA razona y narra (probabilística).
2. **Rigor Financiero:** El sistema debe generar Excels con fórmulas vivas y auditable, no valores estáticos.
3. **Realismo de Datos:** Entrenaré el sistema con datos públicos limpios (Microcaps US 10-K) como proxy, pero diseñaré el pipeline de ingesta para tolerar la "suciedad" de datos de PyMEs latinas (PDFs escaneados, formatos variados).
