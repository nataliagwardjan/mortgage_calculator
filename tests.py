import pytest

from calculation import generate_schedule
from overpayment import Overpayment, OverpaymentType, overpayments_to_df

test_cases = [
    {
        'name': 'No overpayment',
        'loan_amount': 30000.0,
        'annual_rate': 0.05,
        'loan_term': 60,
        'overpayments': [],
        'results': {
            'payment_value': {
                1: 566.14,
                9: 566.14,
                10: 566.14,
                11: 566.14,
                19: 566.14,
                20: 566.14,
                21: 566.14,
                29: 566.14,
                30: 566.14,
                31: 566.14,
                60: 565.96,
            },
            'last_month': 60,
            'overpayment_value': {
                1: 0.0,
                9: 0.0,
                10: 0.0,
                11: 0.0,
                19: 0.0,
                20: 0.0,
                21: 0.0,
                29: 0.0,
                30: 0.0,
                31: 0.0,
                60: 0.0,
            }
        }
    },
    {
        'name': 'ONE_TIME, 5000.0, 20-20, False',
        'loan_amount': 30000.0,
        'annual_rate': 0.05,
        'loan_term': 60,
        'overpayments': [Overpayment(overpayment_type=OverpaymentType.ONE_TIME,
                                     start_month=20,
                                     end_month=20,
                                     value=5000.0,
                                     is_constant_payment=False)],
        'results': {
            'payment_value': {
                1: 566.14,
                9: 566.14,
                10: 566.14,
                11: 566.14,
                19: 566.14,
                20: 566.14,
                21: 471.78,
                29: 471.78,
                30: 471.78,
                31: 471.78,
                57: 90.76,
            },
            'last_month': 57,
            'overpayment_value': {
                1: 0.0,
                9: 0.0,
                10: 0.0,
                11: 0.0,
                19: 0.0,
                20: 5000.0,
                21: 0.0,
                29: 0.0,
                30: 0.0,
                31: 0.0,
                57: 0.0
            }
        }
    },
    {
        'name': 'ONE_TIME, 5000.0, 20-20, True',
        'loan_amount': 30000.0,
        'annual_rate': 0.05,
        'loan_term': 60,
        'overpayments': [Overpayment(overpayment_type=OverpaymentType.ONE_TIME,
                                     start_month=20,
                                     end_month=20,
                                     value=5000.0,
                                     is_constant_payment=True)],
        'results': {
            'payment_value': {
                1: 566.14,
                9: 566.14,
                10: 566.14,
                11: 566.14,
                19: 566.14,
                20: 566.14,
                21: 471.78,
                29: 456.56,
                30: 454.49,
                31: 452.38,
                50: 403.87
            },
            'last_month': 50,
            'overpayment_value': {
                1: 0.0,
                9: 0.0,
                10: 0.0,
                11: 0.0,
                19: 0.0,
                20: 5000.0,
                21: 94.36,
                29: 109.58,
                30: 111.65,
                31: 113.76,
                50: 31.6
            }
        }
    },
    {
        'name': 'RANGE, 300.0, 10-30, True',
        'loan_amount': 30000.0,
        'annual_rate': 0.05,
        'loan_term': 60,
        'overpayments': [Overpayment(overpayment_type=OverpaymentType.RANGE,
                                     start_month=10,
                                     end_month=30,
                                     value=300.0,
                                     is_constant_payment=True)],
        'results': {
            'payment_value': {
                1: 566.14,
                9: 566.14,
                10: 566.14,
                11: 560.48,
                19: 511.16,
                20: 504.47,
                21: 497.64,
                29: 438.19,
                30: 430.12,
                31: 421.89,
                48: 99.04
            },
            'last_month': 48,
            'overpayment_value': {
                1: 0.0,
                9: 0.0,
                10: 300.0,
                11: 305.66,
                19: 354.98,
                20: 361.67,
                21: 368.5,
                29: 427.95,
                30: 436.02,
                31: 144.25,
                48: 0.0
            }
        }
    },
    {
        'name': 'RANGE, 300.0, 10-30, False',
        'loan_amount': 30000.0,
        'annual_rate': 0.05,
        'loan_term': 60,
        'overpayments': [Overpayment(overpayment_type=OverpaymentType.RANGE,
                                     start_month=10,
                                     end_month=30,
                                     value=300.0,
                                     is_constant_payment=False)],
        'results': {
            'payment_value': {
                1: 566.14,
                9: 566.14,
                10: 566.14,
                11: 560.48,
                19: 515.18,
                20: 509.52,
                21: 503.86,
                29: 458.57,
                30: 452.91,
                31: 447.25,
                55: 433.88
            },
            'last_month': 55,
            'overpayment_value': {
                1: 0.0,
                9: 0.0,
                10: 300.0,
                11: 300.0,
                19: 300.0,
                20: 300.0,
                21: 300.0,
                29: 300.0,
                30: 300.0,
                31: 0.0,
                55: 0.0
            }
        }
    },
    {
        'name': 'FULL_TERM, 300.0, 1-60, False',
        'loan_amount': 30000.0,
        'annual_rate': 0.05,
        'loan_term': 60,
        'overpayments': [Overpayment(overpayment_type=OverpaymentType.FULL_TERM,
                                     start_month=1,
                                     end_month=60,
                                     value=300.0,
                                     is_constant_payment=False)],
        'results': {
            'payment_value': {
                1: 566.14,
                9: 520.85,
                10: 515.18,
                11: 509.52,
                19: 464.23,
                20: 458.57,
                21: 452.91,
                29: 407.62,
                30: 401.96,
                31: 396.3,
                44: 322.7
            },
            'last_month': 44,
            'overpayment_value': {
                1: 300.0,
                9: 300.0,
                10: 300.0,
                11: 300.0,
                19: 300.0,
                20: 300.0,
                21: 300.0,
                29: 300.0,
                30: 300.0,
                31: 300.0,
                44: 272.59
            }
        }
    },
    {
        'name': 'FULL_TERM, 300.0, 1-60, True',
        'loan_amount': 30000.0,
        'annual_rate': 0.05,
        'loan_term': 60,
        'overpayments': [Overpayment(overpayment_type=OverpaymentType.FULL_TERM,
                                     start_month=1,
                                     end_month=60,
                                     value=300.0,
                                     is_constant_payment=True)],
        'results': {
            'payment_value': {
                1: 566.14,
                9: 517.74,
                10: 511.16,
                11: 504.47,
                19: 446.12,
                20: 438.19,
                21: 430.12,
                29: 359.77,
                30: 350.22,
                31: 340.48,
                38: 266.98
            },
            'last_month': 38,
            'overpayment_value': {
                1: 300.0,
                9: 348.4,
                10: 354.98,
                11: 361.67,
                19: 420.02,
                20: 427.95,
                21: 436.02,
                29: 506.37,
                30: 515.92,
                31: 525.66,
                38: 152.32
            }
        }
    },
]


@pytest.mark.parametrize('case', test_cases,
                         ids=[case['name'] for case in test_cases])
def test_generate_schedule(case):
    loan_amount = case['loan_amount']
    annual_rate = case['annual_rate']
    loan_term = case['loan_term']
    overpayments = overpayments_to_df(case['overpayments'])

    schedule = generate_schedule(loan_amount, annual_rate, loan_term, case['name'], overpayments)

    results = case['results']
    for month, expected_payment in results['payment_value'].items():
        actual_payment = schedule.loc[schedule['month'] == month, 'payment'].values[0]
        assert float(actual_payment) == pytest.approx(expected_payment, abs=0.01), f'Payment mismatch in month {month}'

    for month, expected_overpayment in results['overpayment_value'].items():
        actual_overpayment = schedule.loc[schedule['month'] == month, 'overpayment'].values[0]
        assert float(actual_overpayment) == pytest.approx(expected_overpayment,
                                                          abs=0.01), f'Overpayment mismatch in month {month}'

    last_month = results['last_month']
    last_month_remaining_balance = schedule.loc[schedule['month'] == last_month, 'remaining_balance'].values[0]
    assert last_month_remaining_balance == 0, f'Remaining balance in last month {last_month} should be zero'
