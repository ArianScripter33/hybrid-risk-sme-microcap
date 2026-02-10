from pydantic import BaseModel, Field, model_validator
from typing import Optional

class BalanceSheet(BaseModel):
    """
    Estado de Situación Financiera.
    Representa una foto instantánea de los activos, pasivos y capital.
    Equation: Assets = Liabilities + Equity
    """
    
    # ---------------------------------------------------------
    # ACTIVOS (ASSETS)
    # ---------------------------------------------------------
    
    # Activos Circulantes (Current Assets) - < 12 meses
    cash_and_equivalents: float = Field(..., description="Efectivo y equivalentes de efectivo")
    accounts_receivable: float = Field(0.0, description="Cuentas por cobrar (clientes)")
    inventory: float = Field(0.0, description="Inventarios")
    other_current_assets: float = Field(0.0, description="Otros activos circulantes")
    
    @property
    def total_current_assets(self) -> float:
        """La sangre del negocio. Activos líquidos a corto plazo."""
        return (self.cash_and_equivalents + 
                self.accounts_receivable + 
                self.inventory + 
                self.other_current_assets)

    # Activos No Circulantes (Non-Current Assets) - > 12 meses
    property_plant_equipment: float = Field(0.0, description="Propiedad, planta y equipo (Neto) PP&E")
    intangible_assets: float = Field(0.0, description="Activos intangibles (patentes, marcas)")
    goodwill: float = Field(0.0, description="Crédito mercantil")
    other_non_current_assets: float = Field(0.0, description="Otros activos no circulantes")
    
    @property
    def total_non_current_assets(self) -> float:
        """El esqueleto del negocio. Infraestructura a largo plazo."""
        return (self.property_plant_equipment + 
                self.intangible_assets + 
                self.goodwill + 
                self.other_non_current_assets)

    # ---------------------------------------------------------
    # PASIVOS (LIABILITIES)
    # ---------------------------------------------------------

    # Pasivos Circulantes (Current Liabilities) - < 12 meses
    accounts_payable: float = Field(..., description="Cuentas por pagar (proveedores)")
    short_term_debt: float = Field(0.0, description="Deuda a corto plazo (bancos, tarjetas)")
    current_portion_long_term_debt: float = Field(0.0, description="Porción circulante de deuda LP")
    other_current_liabilities: float = Field(0.0, description="Otros pasivos circulantes (impuestos, nómina)")
    
    @property
    def total_current_liabilities(self) -> float:
        """La soga al cuello. Obligaciones inmediatas."""
        return (self.accounts_payable + 
                self.short_term_debt + 
                self.current_portion_long_term_debt + 
                self.other_current_liabilities)

    # Pasivos No Circulantes (Non-Current Liabilities) - > 12 meses
    long_term_debt: float = Field(0.0, description="Deuda a largo plazo (>1 año)")
    other_non_current_liabilities: float = Field(0.0, description="Otros pasivos no circulantes")
    
    @property
    def total_non_current_liabilities(self) -> float:
        """Deuda estructural. Financiamiento de largo plazo."""
        return self.long_term_debt + self.other_non_current_liabilities

    # ---------------------------------------------------------
    # CAPITAL (EQUITY)
    # ---------------------------------------------------------
    
    total_stockholders_equity: float = Field(..., description="Capital contable total (Patrimonio)")

    # ---------------------------------------------------------
    # TOTALES & VALIDACIONES
    # ---------------------------------------------------------

    @property
    def total_assets(self) -> float:
        return self.total_current_assets + self.total_non_current_assets

    @property
    def total_liabilities(self) -> float:
        return self.total_current_liabilities + self.total_non_current_liabilities
        
    @property
    def working_capital(self) -> float:
        """
        Métrica de Supervivencia #1.
        Si es negativo, la empresa es insolvente a corto plazo.
        """
        return self.total_current_assets - self.total_current_liabilities

    @model_validator(mode='after')
    def check_accounting_equation(self) -> 'BalanceSheet':
        """
        Valida que Activos = Pasivos + Capital.
        Permite una tolerancia de $1.0 para errores de redondeo en OCR.
        """
        # Calculamos totales usando las properties
        assets = self.total_assets
        liabs_equity = self.total_liabilities + self.total_stockholders_equity
        
        diff = abs(assets - liabs_equity)
        tolerance = 1.0  # $1.0 de tolerancia
        
        if diff > tolerance:
            raise ValueError(
                f"Accounting Equation Breach: Assets (${assets:,.2f}) != "
                f"Liabs+Equity (${liabs_equity:,.2f}). Diff: ${diff:,.2f}"
            )
        return self
