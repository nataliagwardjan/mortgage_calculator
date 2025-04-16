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


class LoanSummary:
    def __init__(self, loan_amount: float, total_interest: float, total_loan_cost: float, last_month: int):
        self.loan_amount = loan_amount
        self.total_interest = total_interest
        self.total_loan_cost = total_loan_cost
        self.last_month = last_month
        self.years = self.last_month // 12
        self.rest_months = self.last_month - (self.years * 12)

