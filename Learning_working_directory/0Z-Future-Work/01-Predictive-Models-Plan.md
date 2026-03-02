# Future Work: Predictive Risk Model Stack 🤖

Este documento describe la arquitectura de modelos de Machine Learning que el Hybrid
Risk Engine implementará en fases posteriores al Módulo 2 (Ratios Engine). Incluye
las ecuaciones fundamentales de cada modelo, la estrategia de benchmarking, y las
decisiones de diseño para el pipeline de experimentación.

---

## Contexto: ¿Por Qué Necesitamos Modelos?

Los ratios financieros (Current Ratio, DSCR, Z-Score) son reglas heurísticas basadas
en umbrales fijos. Funcionan, pero tienen limitaciones críticas:

1. **No aprenden:** El umbral `DSCR < 1.25` fue definido hace 40 años por bancos
   estadounidenses. No está calibrado para PyMEs mexicanas en 2025.
2. **No combinan señales:** Un modelo ML puede detectar que la combinación de
   `(CFO_slope negativo) + (CFI positivo) + (AR_ratio alto)` predice default  
   con 72% de precisión, algo que ninguna regla fija puede capturar.
3. **No aprenden de errores:** Cuando un crédito que aprobaste entra en default,  
   el modelo ajusta sus pesos. Una regla fija no aprende.

---

## Fase 1: XGBoost como Modelo Base (El Estándar de Producción)

### ¿Qué hace XGBoost?

XGBoost (Extreme Gradient Boosting) construye un ensamble de árboles de decisión de
forma secuencial. Cada árbol corrige los errores del anterior, minimizando una función
de pérdida diferenciable.

**Función objetivo de XGBoost:**

$$\mathcal{L} = \sum_{i=1}^{n} \ell(y_i, \hat{y}_i) + \sum_{k=1}^{K} \Omega(f_k)$$

Donde:

- $\ell(y_i, \hat{y}_i)$: Función de pérdida (LogLoss para clasificación binaria de default)
- $\Omega(f_k) = \gamma T + \frac{1}{2}\lambda\|w\|^2$: Regularización del árbol $k$
- $T$: Número de hojas del árbol
- $w$: Pesos de las hojas (las predicciones)

**¿Por qué LogLoss para default?**

$$\text{LogLoss} = -\frac{1}{n}\sum_{i=1}^{n}\left[y_i \log(\hat{p}_i) + (1-y_i)\log(1-\hat{p}_i)\right]$$

Penaliza fuertemente las predicciones muy confiadas pero incorrectas  
(ej: decirle al modelo que está 99% seguro y equivocarse cuesta el doble que estar 70% seguro y equivocarse).

### Features de Entrada (Input del Modelo)

Cada empresa se representa como un vector de features derivados de su serie temporal:

| Feature | Descripción | Horizonte |
| :--- | :--- | :--- |
| `ebitda_ttm` | EBITDA acumulado últimos 12m | Nivel actual |
| `cfo_ttm` | CFO acumulado últimos 12m | Nivel actual |
| `fcf_ttm` | FCF acumulado últimos 12m | Nivel actual |
| `ebitda_slope` | Pendiente de regresión del EBITDA (8 períodos) | Velocidad de deterioro |
| `cfo_qoq_change` | Cambio trimestral del CFO | Momentum |
| `current_ratio` | Activo Circ / Pasivo Circ | Snapshot |
| `dscr` | EBITDA / Debt Service | Snapshot |
| `ar_revenue_ratio` | A/R / Revenue | Calidad de ventas |
| `cfi_positive_streak` | Trimestres consecutivos con CFI > 0 | Señal de liquidación |
| `sector_encoded` | Sector SCIAN one-hot encoded | Contexto sectorial |
| `company_age_years` | Antigüedad de la empresa | Madurez |

### Estrategia de Benchmarking y Validación

Para datos financieros, el **Cross-Validation estándar viola la temporalidad**.  
Un modelo no puede "aprender" del futuro para predecir el pasado.

Se usa **Time-Series Cross-Validation (Walk-Forward Validation)**:

```text
Fold 1: Train [Q1-2019 a Q4-2021] → Test [Q1-2022 a Q2-2022]
Fold 2: Train [Q1-2019 a Q2-2022] → Test [Q3-2022 a Q4-2022]
Fold 3: Train [Q1-2019 a Q4-2022] → Test [Q1-2023 a Q2-2023]
Fold 4: Train [Q1-2019 a Q2-2023] → Test [Q3-2023 a Q4-2023]
```

**Métricas de evaluación:**

$$\text{AUC-ROC} = \int_0^1 \text{TPR}(\text{FPR}) \, d(\text{FPR})$$

$$\text{KS Statistic} = \max(\text{TPR} - \text{FPR})$$

> La Industria crediticia usa KS > 0.4 como mínimo aceptable para scoring models.

**Comparación de Ensambles (Model Shootout):**

| Modelo | Fortaleza | Debilidad | Métrica esperada |
| :--- | :--- | :--- | :--- |
| **XGBoost** | Datos tabulares, interpretable (SHAP) | No captura secuencias | AUC ~0.78-0.85 |
| **LightGBM** | Más rápido que XGBoost, similar performance | Igual limitación | AUC ~0.77-0.84 |
| **Random Forest** | Más robusto a outliers | Generalmente inferior | AUC ~0.72-0.79 |
| **Logistic Regression** | Ultra interpretable, baseline regulatorio | Insuficiente en datos no lineales | AUC ~0.65-0.72 |
| **Stacking Ensemble** | Combina todos los anteriores | Más costoso, más difícil de auditar | AUC ~0.82-0.88 |

---

## Fase 2A: Prophet — Anomaly Detection y Forecasting

### ¿Qué hace Prophet?

Prophet (Meta Research, 2017) descompone la serie temporal en tres componentes:

$$y(t) = g(t) + s(t) + h(t) + \epsilon_t$$

Donde:

- $g(t)$: Tendencia (crecimiento lineal o logístico)
- $s(t)$: Estacionalidad (Fourier series para capturar patrones anuales/trimestrales)
- $h(t)$: Efectos de eventos especiales (ej: COVID, meme stock rally de Koss en 2021)
- $\epsilon_t$: Error residual

**¿Por qué Prophet en el Motor de Riesgo?**  
No para predecir default (XGBoost lo hace mejor). Para:

1. **Anomaly detection por métrica:** Si el Revenue de una PyME está 2 desviaciones estándar por debajo del forecast de Prophet para ese trimestre → Red Flag automático.
2. **Forecasting de métricas individuales:** "¿Cuánto EBITDA tendrá esta empresa en Q3-2026?" para calcular el runway dinámicamente.

**Evaluación de Prophet:** MAPE (Mean Absolute Percentage Error) por métrica individual. Se evalúa independientemente del modelo de default porque es un problema de regresión, no de clasificación. No compite con XGBoost; son complementarios.

---

## Fase 2B: LSTM / GRU — Capturando Dependencias Temporales

### ¿Qué hace una LSTM?

Las LSTM (Long Short-Term Memory, Hochreiter & Schmidhuber 1997) son redes recurrentes con memoria explícita. A diferencia de una DNN densa, la LSTM mantiene un **Cell State** $C_t$ que fluye a través del tiempo.

**Las 3 compuertas (equations simplificadas):**

$$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) \quad \text{(Forget Gate)}$$

$$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) \quad \text{(Input Gate)}$$

$$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o) \quad \text{(Output Gate)}$$

$$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t \quad \text{(Cell State Update)}$$

**En lenguaje humano:**

- **Forget Gate:** ¿Qué del pasado ya no importa? (Ej: el meme stock rally de 2021 ya no es relevante para predecir default en 2026)
- **Input Gate:** ¿Qué nuevo información de este trimestre es relevante?
- **Output Gate:** ¿Qué del estado actual debo comunicar al siguiente período?

**¿Ventaja real sobre XGBoost?**  
En datos financieros con pocas empresas (<10,000) y pocos períodos (<20 trimestres), XGBoost generalmente iguala o supera a LSTM. La LSTM brilla cuando tienes 100,000+ empresas y secuencias de 40+ trimestres.

**Evaluación:** PRUEBAS INDEPENDIENTES de XGBoost. La LSTM requiere un pipeline de datos diferente (secuencias 3D: `[empresas, trimestres, features]` vs. tabla 2D de XGBoost). Se comparan en el mismo hold-out set final.

---

## Fase 3: Temporal Fusion Transformer (TFT) — El Estado del Arte

### ¿Qué hace el TFT?

El TFT (Lim et al., Google/Salesforce, 2020) combina mecanismos de atención (Transformers) con componentes interpretables diseñados específicamente para series temporales multivariadas.

**Variable Selection Network (la joya del TFT):**

$$\tilde{\mathbf{x}} = \sum_{j=1}^{m} v_j^{(\chi)} \cdot \xi_j^{(\chi)}$$

Donde $v_j^{(\chi)}$ son los pesos de selección aprendidos —  
literalmente le pregunta al modelo: *"¿Cuál de los [CFO, EBITDA, DSCR...] importa más para esta empresa en este trimestre?"*

**Interpretability a través de Attention Weights:**

$$\alpha_{t,\tau} = \text{softmax}\left(\frac{Q K^\top}{\sqrt{d_k}}\right)$$

Los pesos $\alpha_{t,\tau}$ te dicen cuánto "atención" presta el modelo al período $\tau$ para hacer la predicción en $t$.  
**Esto es crucial en crédito:** el regulador (CNBV) puede preguntarte exactamente qué datos determinaron la decisión de declinar un crédito.

**Ventajas sobre LSTM para el Motor:**

1. Maneja covariables estáticas (sector, país) y dinámicas (ratios trimestrales) en la misma arquitectura.
2. Sus Attention Weights son auditables — cumplen con regulación bancaria de explicabilidad.
3. Mejor performance en benchmarks de forecasting (M5 Competition, etc.).

**Evaluación:** PRUEBA INDEPENDIENTE con el mismo hold-out set. El TFT requiere implementación con PyTorch Forecasting o NeuralForecast. Más costoso de entrenar pero más poderoso e interpretable que LSTM.

---

## Fase 4: Survival Analysis — La Pregunta Correcta

### ¿Por qué no basta con clasificación binaria?

XGBoost predice P(default = 1). Pero esto no responde la pregunta más valiosa para el banco:  
**"¿En cuántos meses exactamente va a quebrar esta empresa?"**

Esta es exactamente la pregunta de Survival Analysis (Análisis de Supervivencia).

**Cox Proportional Hazards (CoxPH):**

$$h(t | X) = h_0(t) \cdot \exp\left(\beta_1 \text{CFO\_slope} + \beta_2 \text{DSCR} + \beta_3 \text{AR\_ratio} + \cdots\right)$$

Donde:

- $h(t | X)$: Hazard rate — probabilidad de default en el instante $t$
- $h_0(t)$: Baseline hazard (riesgo promedio del sector)
- $e^{\beta_j}$: Hazard Ratio del feature $j$ (ej: cada $1\sigma$ de caída en DSCR → 2.3x más riesgo)

**DeepHit (Neural Survival)** combina la potencia predictiva de redes profundas con el framework de supervivencia, y puede capturar múltiples eventos (default, prepago anticipado, restructuración).

**Evaluación:** C-statistic (equivalente al AUC para survival models). Evaluado independientemente, ya que el target es el tiempo hasta el evento, no binario.

---

## Estrategia de Experimentación y Testing

```text
Pregunta                    → Modelo          → Evaluación
─────────────────────────────────────────────────────────────
¿Qué señal es anómala?      → Prophet         → MAPE (independiente)
¿Va a quebrar? (binario)    → XGBoost vs LGB  → AUC, KS (benchmarking simultáneo)
¿Cuándo va a quebrar?       → CoxPH/DeepHit   → C-statistic (independiente)
¿Qué ves en la secuencia?   → LSTM/TFT        → AUC en hold-out (vs XGBoost final)
```

**Hold-Out Set (Sagrado, NUNCA TOCAR en desarrollo):**

- Empresas que entraron en default en 2024-2025
- Separadas antes de cualquier experimentación
- Solo se usa para el reporte final de performance del modelo ganador

---

> **Decisión Arquitectónica:**
> El modelo de producción del Motor de Riesgo en su MVP será **XGBoost** por su  
> interpretabilidad, velocidad de entrenamiento, y cumplimiento regulatorio con SHAP values.  
> Los experimentos con LSTM/TFT serán pruebas independientes en paralelo que podrán  
> reemplazar al XGBoost solo si superan su AUC en el hold-out set por al menos +3 puntos.

---

## Fase 5: Time Series Foundation Models — El Cambio de Paradigma 🌐

### ¿Por qué los Modelos Autoregresivos Simples le Ganan a LSTM/Transformers?

El paper *"Are Transformers Effective for Time Series Forecasting?"* (Zeng et al., NeurIPS 2022)
demostró que un modelo llamado **DLinear** — una descomposición lineal simple — igualaba o
superaba a Transformers SOTA en la mayoría de benchmarks de forecasting.

**¿Por qué?** Tres razones estructurales:

1. **Series cortas:** Los LSTMs y Transformers necesitan >1,000 pasos temporales.
   Koss tiene 8-20 trimestres. Con tan pocos datos, modelos complejos sobreajustan.
2. **Channel mixing:** Los Transformers mezclan todas las variables (CFO, EBITDA, DSCR)
   entre sí de manera que introduce ruido. Los modelos lineales tratan cada variable
   de forma independiente, que funciona mejor en datos financieros heterogéneos.
3. **No-estacionariedad:** Las series financieras cambian de régimen abruptamente
   (COVID, crisis, meme stocks). Los Transformers suponen cierta estacionariedad implícita.

**La solución al problema de datos escasos:** Pre-entrenar en millones de series.
Esto es exactamente lo que hacen los **Foundation Models de Time Series**.

---

### Chronos (Amazon Research, 2024) 🏆

Chronos convierte series temporales en tokens (como un LLM convierte texto) y
pre-entrena un modelo T5 en 27 millones de series temporales reales y sintéticas.

**Arquitectura conceptual:**

$$\text{Chronos}(x_{1:T}) = \text{T5}\left(\text{Tokenize}(x_{1:T})\right) \rightarrow \hat{x}_{T+1:T+H}$$

Donde la tokenización cuantiza los valores en bins categóricos — el modelo "habla"
en categorías de valores en vez de floats continuos.

**Benchmarks reportados en el paper:**

- Supera a Prophet en ~60% de los datasets sin fine-tuning.
- Supera a ARIMA en ~75% de los datasets.
- Compite con modelos entrenados específicamente en cada dataset (in-domain).

**Caso de uso en el Motor de Riesgo:**

```python
# Zero-shot: sin entrenar nada, predice EBITDA del Q5 con la historia de Koss
from chronos import ChronosPipeline
import torch

pipeline = ChronosPipeline.from_pretrained(
    "amazon/chronos-t5-base",  # Modelo más pequeño, rápido
    device_map="cpu",
    torch_dtype=torch.float32,
)

# Input: 8 trimestres de EBITDA de Koss
context = torch.tensor([200, -100, 50, -300, -600, -800, -910])
forecast = pipeline.predict(context, prediction_length=4)
# Output: distribución de probabilidad del EBITDA para los próximos 4 trimestres
```

**Ventaja clave para este proyecto:**
No necesitas datos históricos propios para empezar. Puedes usar Chronos como
"prior" y fine-tunearlo cuando tengas suficientes Series de PyMEs propias.

---

### Moirai (Salesforce Research, 2024)

Similar a Chronos pero con soporte multivariado nativo — puede manejar
CFO + EBITDA + DSCR + Current Ratio como una sola serie multidimensional,
capturando las correlaciones entre métricas financieras simultáneamente.

$$\mathcal{L}_{\text{Moirai}} = \sum_{t=1}^{T} \log p_\theta(x_t^{(1:D)} | x_{1:t-1}^{(1:D)})$$

Donde $D$ es el número de variables (dimensiones) del panel financiero.

**Evaluación:** MASE (Mean Absolute Scaled Error) para comparar contra Prophet y Chronos.
Se prueba en zero-shot primero; si MASE > Prophet, se descarta para ese dataset.

---

### Tabla Actualizada de Estrategia de Experimentación

```text
Pregunta                    → Modelo            → Evaluación
──────────────────────────────────────────────────────────────────
¿Qué señal es anómala?      → Chronos (zero-shot) → MASE vs Prophet
¿Cuánto EBITDA en Q5?       → Chronos / Moirai  → MAPE (independiente)
¿Va a quebrar? (binario)    → XGBoost vs LGB    → AUC, KS (benchmarking)
¿Cuándo va a quebrar?       → CoxPH / DeepHit   → C-statistic
¿Qué ves en la secuencia?   → LSTM / TFT        → AUC en hold-out
```

---

## 🚀 Expansión Estratégica: De Finanzas a Quant Trading

### Por Qué Dominar Esto Te Da Ventaja Estructural

Los Foundation Models de Time Series **no son exclusivos de finanzas corporativas**.
La misma arquitectura que predice el EBITDA de Koss puede adaptarse a:

| Dominio | Señal Temporal | Datos Disponibles | Ventaja Competitiva |
| :--- | :--- | :--- | :--- |
| **Credit Risk (SME)** | EBITDA, CFO, ratios trimestrales | 4-20 períodos/empresa | Motor de Riesgo actual |
| **Quant Trading (equities)** | OHLCV, order flow, volatility | Millones de ticks/día | Feature engineering de microestructura |
| **DeFi/Solana Blockchain** | TPS, fee markets, TVL, liquidaciones | Datos en tiempo real on-chain | El dataset más masivo y transparente del mundo |
| **Macro Economics** | PIB, inflación, TIIE, spreads | Series largas históricas | Stress testing del portafolio |

### Solana Blockchain — El Dataset Ideal para LSTM/TFT

La Blockchain de Solana genera datos que hacen que los datos financieros tradicionales
parezcan un archivo de texto:

```
Frecuencia:    400ms por bloque (vs trimestral en finanzas corporativas)
Variables:     TPS, fees, validator slots, MEV, DEX volumes, wallet flows
Transparencia: 100% público, inmutable, sin survivorship bias
Tamaño:        100B+ transacciones históricas disponibles en Helius/Triton
```

Con este volumen de datos:

- Un LSTM ya NO es overkill. Es el mínimo viable.
- El TFT puede capturar correlaciones entre pools de liquidez en Jupiter/Orca.
- Chronos y Moirai pueden ser fine-tuneados con ventaja estructural sobre modelos entrenados solo en equity markets.

**El puente de skills:**

```
Módulo 2:  Ratios en Python         → Rigor financiero + Python limpio
Módulo 3:  Series Temporales        → Pipeline de datos temporales
Módulo 4:  XGBoost + SHAP           → ML interpretable y deployable
Módulo 5:  Chronos / TFT            → Foundation Models y fine-tuning
─────────────────────────────────────────────────────────────────────
Aplicación: Solana Quant Strategy   → Todos los anteriores + on-chain data
```

> **Insight de Venture:**
> La razón por la que los fondos quant de Tier-1 (Two Sigma, DE Shaw, Jump Trading)
> dominan DeFi no es porque tengan mejores modelos que tú. Es porque llegaron primero
> y tienen datos etiquetados de ciclos completos de mercado. Tu ventaja es llegar AHORA,
> cuando el mercado DeFi de Solana tiene suficiente historia (2021-2025) para entrenar
> modelos serios, pero no tanta que el alpha esté completamente arbitrado.
