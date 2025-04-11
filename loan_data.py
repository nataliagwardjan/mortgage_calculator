class LoanData:
    def __init__(self, loan_amount: float,
                 loan_annual_rate: float,
                 months: int):
        self.loan_amount = loan_amount
        self.loan_annual_rate = loan_annual_rate
        self.months = months

    def __repr__(self):
        return (f'LoanData(loan_amount={self.loan_amount}, '
                f'loan_annual_rate={self.loan_annual_rate}, '
                f'months={self.months})')

    def __str__(self):
        return (f'loan_amount={self.loan_amount}, '
                f'loan_annual_rate={self.loan_annual_rate}, '
                f'months={self.months}')
