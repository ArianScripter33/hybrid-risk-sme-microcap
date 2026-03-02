import pytest
from src.schemas.financial_data import IncomeStatement

def test_income_statement_healthy_company():
    """Prueba de un P&L sano, como una empresa de software (SaaS)"""
    pl = IncomeStatement(
        revenue=1_000_000,
        cost_of_goods_sold=200_000,           # 80% Gross Margin típico de SaaS
        selling_general_administrative=300_000,
        research_and_development=150_000,
        depreciation_amortization=50_000,
        interest_expense=10_000,
        income_tax=58_000
    )
    
    assert pl.gross_profit == 800_000
    assert pl.gross_margin_pct == 80.0
    
    # OPEX = 300k + 150k + 50k = 500k
    assert pl.total_operating_expenses == 500_000
    
    # Operating Income (EBIT) = 800k - 500k = 300k
    assert pl.operating_income == 300_000
    
    # EBITDA = 300k + 50k = 350k
    assert pl.ebitda == 350_000
    assert pl.ebitda_margin_pct == 35.0
    
    # Net Income = 300k - 10k - 58k = 232k
    assert pl.net_income == 232_000

def test_income_statement_koss_fraud_anomaly():
    """
    Simulación del The Koss Corporation Embezzlement.
    Sujata Sachdeva robó ~$34 millones durante años y los escondió
    inflando Cost of Goods Sold y SG&A.
    """
    # 1. Koss normal (antes del fraude masivo)
    pl_normal = IncomeStatement(
        revenue=40_000_000,
        cost_of_goods_sold=24_000_000,  # 40% Gross Margin (normal para hardware)
        selling_general_administrative=10_000_000,
        depreciation_amortization=1_000_000,
        interest_expense=500_000,
        income_tax=1_000_000
    )
    
    assert pl_normal.gross_margin_pct == 40.0
    assert pl_normal.ebitda_margin_pct == 15.0  # (16M - 11M + 1M) / 40M
    
    # 2. Koss corrompido (Fraude oculto en SG&A y COGS)
    # Revenue subió un poco, pero veamos los márgenes...
    pl_fraud = IncomeStatement(
        revenue=42_000_000,
        cost_of_goods_sold=32_000_000,        # Inflado artificialmente
        selling_general_administrative=15_000_000, # Subió un 50% sin razón aparente
        depreciation_amortization=1_000_000,
        interest_expense=500_000,
        income_tax=0
    )
    
    # Análisis de Riesgo Automático
    # A pesar de vender más (Revenue 40M -> 42M), la empresa se destruye por dentro.
    
    # El Gross Margin colapsó de 40% a ~23.8%
    assert round(pl_fraud.gross_margin_pct, 1) == 23.8
    
    # El EBITDA colapsó y ahora es negativo...
    # Gross Profit = 10M
    # OpEx = 16M
    # Operating Income = -6M
    # EBITDA = -6M + 1M = -5M
    assert pl_fraud.ebitda == -5_000_000
    
    # Esto es exactamente lo que el Motor de Riesgo detecta:
    if pl_normal.gross_margin_pct - pl_fraud.gross_margin_pct > 10.0:
        fraud_alert = True
        
    assert fraud_alert is True
