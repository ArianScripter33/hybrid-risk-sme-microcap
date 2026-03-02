from pydantic import BaseModel, Field, model_validator

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

    # --------------------------------------------------------- 
    #  INCOME STATEMENT SECTION (P&L)
    # ---------------------------------------------------------

class IncomeStatement(BaseModel):
    """
    Estado de Resultados (P&L).
    Representa la película de ingresos, gastos y rentabilidad durante un período.
    """
    
    # ---------------------------------------------------------
    # INGRESOS Y COSTOS DIRECTOS (TOP LINE)
    # ---------------------------------------------------------
    
    revenue: float = Field(..., description="Ventas totales (Ingresos)")
    cost_of_goods_sold: float = Field(0.0, description="Costo de Ventas (COGS)")
    
    @property
    def gross_profit(self) -> float:
        """Dinero puro que sobra para pagar la operación."""
        return self.revenue - self.cost_of_goods_sold

    # ---------------------------------------------------------
    # GASTOS OPERATIVOS (OpEx)
    # ---------------------------------------------------------
    
    selling_general_administrative: float = Field(0.0, description="Gastos de Venta, Generales y Admin (SG&A)")
    research_and_development: float = Field(0.0, description="Investigación y Desarrollo (R&D)")
    depreciation_amortization: float = Field(0.0, description="Depreciación y Amortización (D&A)")
    
    @property
    def total_operating_expenses(self) -> float:
        """La carga fija o semifija para mantener el negocio corriendo. Total OpEx = SG&A + R&D + D&A"""
        return (self.selling_general_administrative + 
                self.research_and_development + 
                self.depreciation_amortization)

    @property
    def operating_income(self) -> float:
        """Utilidad Operativa (EBIT). EBIT stands for Earnings Before Interest and Taxes. Lo que realmente genera el negocio. Operating Income = Gross Profit - Total Operating Expenses"""
        return self.gross_profit - self.total_operating_expenses

    @property
    def ebitda(self) -> float:
        """EBITDA stands for Earnings Before Interest, Taxes, Depreciation, and Amortization. Proxy de generación de caja de la operación pura. EBITDA = Operating Income (EBIT) + Depreciation & Amortization"""
        return self.operating_income + self.depreciation_amortization

    # ---------------------------------------------------------
    # FINANCIAMIENTO E IMPUESTOS (BOTTOM LINE)
    # ---------------------------------------------------------
    
    interest_expense: float = Field(0.0, description="Gastos por intereses financieros")
    other_income_expense: float = Field(0.0, description="Otros ingresos/gastos no operativos")
    income_tax: float = Field(0.0, description="Impuestos sobre la renta")
    
    @property
    def operating_income_before_tax(self) -> float:
        """EBT (Earnings Before Tax) = Operating Income - Interest Expense + Other Income/Expense"""
        return self.operating_income - self.interest_expense + self.other_income_expense

    @property
    def net_income(self) -> float:
        """Utilidad Neta (The Bottom Line). Net Income = Operating Income - Interest Expense + Other Income/Expense - Income Tax"""
        return self.operating_income - self.interest_expense + self.other_income_expense - self.income_tax

    # ---------------------------------------------------------
    # MÉTRICAS DE EFICIENCIA DERIVADAS
    # ---------------------------------------------------------
    
    @property
    def gross_margin_pct(self) -> float:
        """Porcentaje de margen bruto."""
        if self.revenue == 0:
            return 0.0
        return (self.gross_profit / self.revenue) * 100

    @property
    def ebitda_margin_pct(self) -> float:
        """Porcentaje de margen EBITDA."""
        if self.revenue == 0:
            return 0.0
        return (self.ebitda / self.revenue) * 100

    # --------------------------------------------------------- 
    #  CASH FLOW STATEMENT SECTION
    # ---------------------------------------------------------

class CashFlowStatement(BaseModel):
    """
    Estado de Flujo de Efectivo.
    La verdad absoluta de cuánto dinero entró y salió de la cuenta bancaria.
    """
    
    # ---------------------------------------------------------
    # 1. OPERATING ACTIVITIES (El motor del negocio)
    # ---------------------------------------------------------
    
    net_income_starting_line: float = Field(..., description="Utilidad Neta (Punto de partida del Income Statement)")
    depreciation_amortization_addback: float = Field(0.0, description="D&A agregada de vuelta (Gasto no efectivo)")
    change_in_working_capital: float = Field(0.0, description="Cambios en activos y pasivos circulantes (Cuentas por cobrar, inventario)")
    other_operating_cash_flow: float = Field(0.0, description="Otros flujos operativos")
    
    @property
    def cash_from_operations(self) -> float:
        """CFO stands for Cash From Operations. Cuánto efectivo generó la operación diaria."""
        return (self.net_income_starting_line + 
                self.depreciation_amortization_addback + 
                self.change_in_working_capital + 
                self.other_operating_cash_flow)

    # ---------------------------------------------------------
    # 2. INVESTING ACTIVITIES (Comprando o vendiendo el futuro)
    # ---------------------------------------------------------
    
    capital_expenditures: float = Field(..., description="CapEx: Inversión en equipo, maquinaria, software")
    other_investing_cash_flow: float = Field(0.0, description="Otras inversiones (Venta de activos, comprar bonos)")
    
    @property
    def cash_from_investing(self) -> float:
        """CFI stands for Cash From Investing. Efectivo gastado o recibido por inversiones. Usualmente es negativo."""
        # Se asume que en el JSON de entrada las salidas (compras) vienen como números negativos.
        return self.capital_expenditures + self.other_investing_cash_flow

    # ---------------------------------------------------------
    # 3. FINANCING ACTIVITIES (Los bancos y los inversores)
    # ---------------------------------------------------------
    
    debt_issued_repaid: float = Field(0.0, description="Préstamos recibidos (positivo) o pagados (negativo)")
    dividends_paid: float = Field(0.0, description="Dividendos pagados a accionistas (negativo)")
    other_financing_cash_flow: float = Field(0.0, description="Otros flujos de financiamiento")
    
    @property
    def cash_from_financing(self) -> float:
        """CFF stands for Cash From Financing. El movimiento de dinero con los que fondean la empresa."""
        return self.debt_issued_repaid + self.dividends_paid + self.other_financing_cash_flow

    # ---------------------------------------------------------
    # TOTALES & DERIVADAS (Net Change & FCF)
    # ---------------------------------------------------------
    
    @property
    def net_change_in_cash(self) -> float:
        """El cambio real absoluto en la cuenta bancaria este período."""
        return self.cash_from_operations + self.cash_from_investing + self.cash_from_financing

    @property
    def free_cash_flow(self) -> float:
        """
        FCF stands for Free Cash Flow. Free Cash Flow (El Santo Grial).
        El efectivo libre después de operar y mantener la infraestructura.
        Usamos `abs()` previendo que K.I.M.E.R.A (LLM) pueda extraer el CapEx 
        como positivo o negativo. CapEx siempre resta efectivo al CFO.
        """
        return self.cash_from_operations - abs(self.capital_expenditures)


