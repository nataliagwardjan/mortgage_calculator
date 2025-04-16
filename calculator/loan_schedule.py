class ScheduleUnit:
    def __init__(self, month: int,
                 payment: float,
                 interest: float,
                 capital: float,
                 overpayment: float,
                 remaining_balance: float,
                 remaining_term: int):
        self.month = month
        self.payment = payment
        self.interest = interest
        self.capital = capital
        self.overpayment = overpayment
        self.payment_overpayment = (self.payment + self.overpayment)
        self.remaining_balance = remaining_balance
        self.remaining_term = remaining_term

    def __repr__(self):
        return (f'ScheduleUnit(month={self.month}, '
                f'payment={self.payment}, '
                f'interest={self.interest}, '
                f'capital={self.capital}, '
                f'overpayment={self.overpayment}, '
                f'payment_overpayment={self.payment_overpayment}, '
                f'remaining_balance={self.remaining_balance}, '
                f'remaining_term={self.remaining_term})')

    def __str__(self):
        return (f'month={self.month}, '
                f'payment={self.payment}, '
                f'interest={self.interest}, '
                f'capital={self.capital}, '
                f'overpayment={self.overpayment}, '
                f'payment_overpayment={self.payment_overpayment}, '
                f'remaining_balance={self.remaining_balance}, '
                f'remaining_term={self.remaining_term}')

    def update_overpayment_remaining_balance(self, add_overpayment: float, remaining_balance: float):
        self.overpayment += add_overpayment
        self.payment_overpayment = (self.payment + self.overpayment)
        self.remaining_balance = remaining_balance
