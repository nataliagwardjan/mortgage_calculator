import pandas as pd
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from utils import OVERPAYMENT_TYPE, OVERPAYMENT_START, OVERPAYMENT_END, OVERPAYMENT_VALUE, OVERPAYMENT_IS_CONSTANT


class OverpaymentType(Enum):
    ONE_TIME = 'ONE_TIME',
    RANGE = 'RANGE',
    FULL_TERM = 'FULL_TERM'


@dataclass
class Overpayment:
    overpayment_type: OverpaymentType = OverpaymentType.ONE_TIME
    start_month: int = 1
    end_month: Optional[int] = None
    value: float = 0.0
    is_constant_payment: bool = False
    loan_term: int = 300

    def __post_init__(self):
        if self.overpayment_type == OverpaymentType.ONE_TIME:
            self.end_month = self.start_month
        elif self.end_month is None:
            self.end_month = self.start_month
        if self.end_month and self.end_month > self.loan_term:
            self.end_month = self.loan_term

    def __str__(self):
        return (f'type={self.overpayment_type}, '
                f'start_month={self.start_month}, end_month={self.end_month}, '
                f'value={self.value}, is_constant_payment={self.is_constant_payment}')

    def convert_to_dict(self) -> dict:
        return {
            OVERPAYMENT_TYPE: self.overpayment_type.name,
            OVERPAYMENT_START: self.start_month,
            OVERPAYMENT_END: self.end_month,
            OVERPAYMENT_VALUE: self.value,
            OVERPAYMENT_IS_CONSTANT: self.is_constant_payment
        }


class OverpaymentData:
    def __init__(self, name: str,
                 overpayments: list[Overpayment]):
        self.name = name
        self.overpayments = overpayments

    def __repr__(self):
        return (f'OverpaymentData(name={self.name}, '
                f'overpayment={self.overpayments})')

    def __str__(self):
        return f'{self.name}: {self.overpayments}'

    def add_overpayment(self, overpayment: Overpayment):
        self.overpayments.append(overpayment)


def overpayments_to_df(overpayments: list[Overpayment]) -> pd.DataFrame:
    if not overpayments:
        return pd.DataFrame()

    data = [op.convert_to_dict() for op in overpayments]
    return pd.DataFrame(data)
