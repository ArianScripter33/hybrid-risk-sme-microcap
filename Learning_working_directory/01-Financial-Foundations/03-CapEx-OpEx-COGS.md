# Clasificación de Costos: CapEx vs OpEx vs COGS 🏭

Aquí resolvemos *"¿Cuál es la diferencia entre el gross profit y el gross margin? Puedes ejemplificar explicando mucho más lo del costo variable y los costos fijos?"*.

## 1. La Trinidad del Costo: COGS, OpEx y CapEx 🔻

En tu código, **ingesta/ingestion.py** leerá PDFs y tendrá que mapear cada gasto a una de estas tres categorías.

### A. Costo de Ventas (COGS - Cost of Goods Sold)

**Definición:** **Variables**. Si no vendes producto mañana, no lo gastas.

- **Ejemplo (Taquería):**
  - Tortillas (1000)
  - Carne (50 kg)
  - Salsa
- **Test:** Si vendes 0 tacos, gastas $0 (excepto carne podrida).

### B. Gastos Operativos (OpEx - Operating Expenses)

**Definición:** **Fijos/Semi-Fijos**. Ganas dinero o pierdes dinero, igual pagas.

- **Ejemplo (Taquería):**
  - Renta del Local ($10k/mes)
  - Sueldo del Taquero ($8k/mes)
  - Luz ($2k/mes)
- **Test:** Si vendes 0 tacos, sigues pagando $20k. **Te desangran.**

### C. Gasto de Capital (CapEx - Capital Expenditure)

**Definición:** **Inversión**. Dinero que sale pero crea un Activo en el Balance.

- **Ejemplo (Taquería):**
  - Comprar el Comal ($20k)
  - Computadora POS ($15k)
- **Impacto:** Drena Cash hoy. Crea Activo (No Circulante). Se deprecia poco a poco.

## 2. Gross Profit vs. Gross Margin: Dinero vs. Porcentaje % 💰

Una empresa dice: *"Gané 1 millón de Gross Profit"*
Otra dice: *"Tengo 80% de Gross Margin"*
¿Cuál es mejor?

### Gross Profit (Utilidad Bruta) - DINERO ($)

$$Gross\ Profit = Revenue - COGS$$

- **Ejemplo:** Vendes un iphone por $1000. Te costó $400 hacerlo.
- **Gross Profit:** $600.
Mide: **Masa de dinero** para pagar OpEx.

### Gross Margin (Margen Bruto) - PORCENTAJE (%)

$$Gross\ Margin = \frac{Gross\ Profit}{Revenue} \times 100$$

- **Ejemplo:** $600 / $1000 = **60%**
Mide: **Eficiencia**. ¿Qué tan rentable es CADA unidad vendida?

#### ¿Por qué importa para Riesgo?

- **SaaS:** Gross Margin 80% (Suben nubes baratas, cobran caro). Escalables.
- **Supermercado:** Gross Margin 20% (Walmart). Ganan por volumen masivo.
- **Riesgo:** Si el Gross Margin **baja** (de 60% a 50%), significa que te cuesta más producir o estás bajando precios. **Mala señal.**

> **En tu Motor:**
>
> - Calcularemos `gross_margin` como métrica clave de calidad.
> - Si `gross_margin` < 10% y OpEx es alto -> **ALERTA ROJA (Negocio Inviable)**.
