import math

OVERPAYMENT_TYPE = 'type'
OVERPAYMENT_START = 'start'
OVERPAYMENT_END = 'end'
OVERPAYMENT_VALUE = 'value'
OVERPAYMENT_IS_CONSTANT = 'is_constant_payment'


def round_math(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier + 0.5) / multiplier

