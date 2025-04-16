from typing import Optional, Callable
import gettext

from calculator.loan_data import LoanData
from calculator.overpayment import OverpaymentData


class AppState:
    def __init__(self):
        self.language: str = 'en'
        self.loan_data: Optional[LoanData] = None
        self.custom_overpayments_set: list[OverpaymentData] = []
        self.overpayments_set: list[OverpaymentData] = []
        self.is_analysis_constant_overpayment: bool = False
        self.is_custom_overpayment: bool = False
        self.current_overpayment_name: Optional[str] = None
        self.translation: Callable[[str], str] = self.get_translation('en')
        self.calculate_schedule: bool = False

    def set_language(self, lang_code: str):
        self.language = lang_code
        self.translation = self.get_translation(lang_code)

    @staticmethod
    def get_translation(lang_code: str):
        try:
            trans = gettext.translation(
                'messages',
                localedir='locales',
                languages=[lang_code],
                fallback=True
            )
            return trans.gettext
        except (FileNotFoundError, gettext.GNUTranslations):
            return gettext.NullTranslations()

    def to_dict(self):
        return {
            'language': self.language,
            'custom_overpayments_set': self.custom_overpayments_set,
            'overpayments_set': self.overpayments_set,
            'is_analysis_constant_overpayment': self.is_analysis_constant_overpayment,
            'is_custom_overpayment': self.is_custom_overpayment,
            'current_overpayment_name': self.current_overpayment_name,
            'calculate_schedule': self.calculate_schedule
        }
