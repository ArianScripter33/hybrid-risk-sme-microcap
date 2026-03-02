"""
Módulo 3: Predictive Risk Engine — Time Series Analysis
========================================================

BOILERPLATE CODE — Schema de referencia para implementación futura.
Este módulo será activado cuando tengamos:
  1. Los schemas base funcionando (BalanceSheet, IncomeStatement, CashFlowStatement) ✅
  2. El módulo de Ratios implementado (Módulo 2) 🔲
  3. Datos históricos de al menos 4 trimestres por empresa 🔲

Arquitectura de Modelos (Roadmap):
  - MVP:     XGBoost con features tabulares de 4-8 trimestres
  - v2.0:    LSTM/TFT para capturar secuencia temporal
  - v3.0:    CoxPH/DeepHit para survival analysis (¿CUÁNDO quiebra?)

Fuentes de datos potenciales:
  - 10-Q / 10-K (SEC EDGAR API) — Empresas públicas USA
  - CFDIs del SAT — PyMEs México (requiere convenio institucional)
  - Reportes anuales BMV — Empresas públicas México
"""

from pydantic import BaseModel, Field
from typing import Optional

# =========================================================
# FINANCIAL SNAPSHOT (Un período individual)
# =========================================================

class FinancialSnapshot(BaseModel):
    """
    Representación de UN período financiero (trimestre o año).
    Agrupa los 3 estados financieros + ratios derivados.
    """
    
    period_label: str = Field(..., description="Ej: 'Q4-2025' o '2025-12-31'")
    
    # --- Métricas del Income Statement ---
    revenue: float = Field(..., description="Net Sales del período")
    cogs: float = Field(0.0, description="Cost of Goods Sold")
    sga: float = Field(0.0, description="SG&A (Selling, General & Administrative)")
    depreciation_amortization: float = Field(0.0, description="D&A del período")
    interest_expense: float = Field(0.0, description="Intereses pagados al banco")
    income_tax: float = Field(0.0, description="Provisión de impuestos")
    net_income: float = Field(..., description="Bottom Line del Income Statement")
    
    # --- Métricas del Cash Flow ---
    cfo: float = Field(..., description="Cash From Operations")
    capex: float = Field(0.0, description="Capital Expenditures (usualmente negativo)")
    cfi: float = Field(0.0, description="Cash From Investing")
    cff: float = Field(0.0, description="Cash From Financing")
    
    # --- Métricas del Balance Sheet ---
    total_current_assets: float = Field(0.0, description="Activos Circulantes totales")
    total_current_liabilities: float = Field(0.0, description="Pasivos Circulantes totales")
    total_assets: float = Field(0.0, description="Activos totales")
    total_liabilities: float = Field(0.0, description="Pasivos totales")
    retained_earnings: float = Field(0.0, description="Utilidades retenidas históricas")
    cash_and_equivalents: float = Field(0.0, description="Efectivo en banco")
    accounts_receivable: float = Field(0.0, description="Cuentas por cobrar")
    
    # --- Propiedades Derivadas ---
    @property
    def gross_profit(self) -> float:
        return self.revenue - self.cogs
    
    @property
    def ebit(self) -> float:
        return self.gross_profit - self.sga
    
    @property
    def ebitda(self) -> float:
        return self.ebit + self.depreciation_amortization
    
    @property
    def fcf(self) -> float:
        return self.cfo - abs(self.capex)
    
    @property
    def current_ratio(self) -> float:
        if self.total_current_liabilities == 0:
            return float('inf')
        return self.total_current_assets / self.total_current_liabilities
    
    @property
    def ar_revenue_ratio(self) -> float:
        if self.revenue == 0:
            return 0.0
        return self.accounts_receivable / self.revenue


# =========================================================
# COMPANY TIME SERIES (La serie completa de una empresa)
# =========================================================

class CompanyTimeSeries(BaseModel):
    """
    Serie temporal de períodos financieros de una empresa.
    Mínimo 4 trimestres (TTM). Óptimo 8-12 trimestres.
    
    Este schema es el INPUT para los modelos predictivos:
      - XGBoost (tabular features derivados de la serie)
      - LSTM/TFT (secuencia directa de snapshots)
      - CoxPH/DeepHit (survival analysis)
    """
    
    company_id: str = Field(..., description="Identificador único (RFC, CIK, Ticker)")
    company_name: str = Field(..., description="Nombre legal de la empresa")
    ticker: Optional[str] = Field(None, description="Ticker bursátil si es pública")
    sector: Optional[str] = Field(None, description="Sector SCIAN/NAICS")
    country: str = Field("MX", description="País de operación")
    
    # Períodos ordenados cronológicamente (más antiguo primero)
    periods: list[FinancialSnapshot] = Field(
        ..., 
        min_length=1,
        description="Lista de snapshots financieros ordenados cronológicamente"
    )
    
    # ---------------------------------------------------------
    # TRAILING TWELVE MONTHS (TTM) — Suaviza estacionalidad
    # ---------------------------------------------------------
    
    @property
    def cfo_ttm(self) -> float:
        """CFO de los últimos 4 trimestres. Elimina ruido estacional."""
        raise NotImplementedError("Implementar en Módulo 3: sum(p.cfo for p in self.periods[-4:])")
    
    @property
    def ebitda_ttm(self) -> float:
        """EBITDA acumulado de los últimos 12 meses."""
        raise NotImplementedError("Implementar en Módulo 3: sum(p.ebitda for p in self.periods[-4:])")
    
    @property
    def fcf_ttm(self) -> float:
        """Free Cash Flow de los últimos 12 meses."""
        raise NotImplementedError("Implementar en Módulo 3: sum(p.fcf for p in self.periods[-4:])")

    # ---------------------------------------------------------
    # TREND ANALYSIS — Pendientes de deterioro/mejora
    # ---------------------------------------------------------
    
    @property
    def ebitda_slope(self) -> float:
        """
        Pendiente de regresión lineal del EBITDA por trimestre.
        Negativa = deterioro acelerado.
        Se calcula con numpy polyfit sobre los últimos 8 trimestres.
        """
        raise NotImplementedError("Implementar en Módulo 3: np.polyfit(x, ebitda_series, 1)[0]")
    
    @property
    def cfo_trend(self) -> list[float]:
        """Serie temporal de CFO para visualización y modelo."""
        raise NotImplementedError("Implementar en Módulo 3: [p.cfo for p in self.periods]")

    # ---------------------------------------------------------
    # RED FLAG ENGINE — Detección automática de patrones
    # ---------------------------------------------------------
    
    @property
    def ebitda_mirage_detected(self) -> bool:
        """
        Red Flag: EBITDA positivo + CFO negativo simultáneamente.
        Empresa rentable en papel, muerta de sed en el banco.
        """
        raise NotImplementedError("Implementar en Módulo 3")
    
    @property
    def asset_liquidation_detected(self) -> bool:
        """
        Red Flag: CFI positivo (vendiendo activos) + CFO negativo.
        Empresa consumiendo su colchón de ahorros para sobrevivir.
        """
        raise NotImplementedError("Implementar en Módulo 3")
    
    @property
    def runway_years(self) -> float:
        """
        Años estimados de supervivencia al ritmo actual de quema de cash.
        runway = cash_and_investments / abs(annual_cfo_burn_rate)
        """
        raise NotImplementedError("Implementar en Módulo 3")
    
    # ---------------------------------------------------------
    # MODEL OUTPUT — Lo que el modelo predictivo generará
    # ---------------------------------------------------------
    # 
    # Cuando el modelo esté entrenado, estas propiedades serán
    # reemplazadas por las predicciones del modelo:
    #
    #   p_default_12m: float  → Probabilidad de quiebra en 12 meses
    #   p_default_24m: float  → Probabilidad en 24 meses
    #   runway_estimated: float → Años de supervivencia
    #   risk_category: str    → "PASS" | "WATCH" | "FAIL"
    #
    # El modelo aprende patrones como:
    #   Si EBITDA_slope < -$150K/trimestre
    #   AND CFO_ttm < 0
    #   AND CFI > 0 (venden activos)
    #   → P(default_18m) = 67%
    # ---------------------------------------------------------
