import pytest
from pydantic import ValidationError
from src.schemas.financial_data import BalanceSheet

def test_balance_sheet_happy_path():
    """Caso ideal: Empresa sana con working capital positivo"""
    bs = BalanceSheet(
        # Assets Circulantes ($60k)
        cash_and_equivalents=10_000,
        accounts_receivable=20_000,
        inventory=30_000,
        
        # Assets No Circulantes ($40k)
        property_plant_equipment=40_000,
        
        # Liabilities Circulantes ($30k)
        accounts_payable=15_000,
        short_term_debt=15_000,
        
        # Liabilities No Circulantes ($20k)
        long_term_debt=20_000,
        
        # Equity ($50k)
        total_stockholders_equity=50_000
    )
    
    # Assert Assets = 100k
    assert bs.total_current_assets == 60_000
    assert bs.total_non_current_assets == 40_000
    assert bs.total_assets == 100_000
    
    # Assert Liabilities = 50k
    assert bs.total_current_liabilities == 30_000
    assert bs.total_non_current_liabilities == 20_000
    assert bs.total_liabilities == 50_000
    
    # Assert Checksum: 100k (Assets) == 50k (Liabs) + 50k (Equity)
    # Pydantic validator passes silently if correct

def test_balance_sheet_accounting_breach():
    """Caso error: El OCR leyó mal y los números no cuadran"""
    with pytest.raises(ValidationError) as exc:
        BalanceSheet(
            cash_and_equivalents=10_000,
            accounts_payable=5_000,
            total_stockholders_equity=1_000
            # Total Assets = 10k
            # Liabs + Equity = 6k
            # Diff = 4k -> DEBE FALLAR
        )
    assert "Accounting Equation Breach" in str(exc.value)

def test_working_capital_calculation():
    """Caso: Verificar cálculo de WC"""
    bs = BalanceSheet(
        cash_and_equivalents=100,
        accounts_payable=80,
        total_stockholders_equity=20
    )
    # WC = 100 - 80 = 20
    assert bs.working_capital == 20.0

def test_asset_heavy_cash_poor():
    """
    Caso: La empresa de los servidores del Día 1.
    Tiene muchos activos fijos pero 0 liquidez.
    """
    bs = BalanceSheet(
        cash_and_equivalents=0,          # Caja vacía
        property_plant_equipment=5_000,  # Servidores
        
        accounts_payable=1_000,          # Debe luz/nómina
        total_stockholders_equity=4_000
    )
    
    # Working Capital negativo
    # WC = 0 - 1000 = -1000
    assert bs.working_capital == -1_000
    assert bs.total_assets == 5_000
