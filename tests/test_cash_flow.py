import pytest
from src.schemas.financial_data import CashFlowStatement

def test_cash_flow_healthy_growth():
    """
    Test de una empresa estructurada normalmente:
    - Genera caja operando.
    - Gasta caja invirtiendo para crecer (CapEx negativo).
    - El Free Cash Flow (FCF) es positivo.
    """
    cfs = CashFlowStatement(
        net_income_starting_line=500_000,
        depreciation_amortization_addback=50_000,
        change_in_working_capital=-20_000,  # Aumento de inventario (sacó plata)
        capital_expenditures=-100_000,      # Compró maquinaria
        debt_issued_repaid=-30_000,         # Pagó préstamos
        dividends_paid=-50_000              # Pagó a accionistas
    )
    
    # Cash From Operations (500k + 50k - 20k) = 530k
    assert cfs.cash_from_operations == 530_000
    
    # Cash From Investing (-100k)
    assert cfs.cash_from_investing == -100_000
    
    # Cash From Financing (-30k - 50k) = -80k
    assert cfs.cash_from_financing == -80_000
    
    # Net Change in Cash (530k - 100k - 80k) = 350k
    assert cfs.net_change_in_cash == 350_000
    
    # Free Cash Flow (530k CFO - 100k CapEx) = 430k
    assert cfs.free_cash_flow == 430_000

def test_free_cash_flow_capex_sign_normalization():
    """
    Validamos que el arquitecto (tú) previó las alucinaciones del OCR.
    Si el LLM saca el CapEx como positivo en vez de negativo, 
    el FCF debe calcularse correctamente de todos modos (CFO siempre pierde el CapEx).
    """
    cfs_llm_hallucination = CashFlowStatement(
        net_income_starting_line=100_000,
        capital_expenditures=50_000  # LLM olvidó que era negativo/salida
    )
    
    # CFO = 100k
    # CapEx = 50k (extraído mal sin signo negativo)
    # FCF = 100k - abs(50k) = 50k (Defensa ejecutada)
    
    assert cfs_llm_hallucination.free_cash_flow == 50_000
