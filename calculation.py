import numpy_financial as npf
import pandas as pd
from pandas import DataFrame

from loan_schedule import ScheduleUnit
from overpayment import OverpaymentType, Overpayment
from utils import OVERPAYMENT_IS_CONSTANT, OVERPAYMENT_VALUE, OVERPAYMENT_START, OVERPAYMENT_END, round_math, \
    OVERPAYMENT_TYPE


def generate_schedule(principal: float,
                      annual_rate: float,
                      months: int,
                      overpayment_name: str,
                      overpayments: DataFrame) -> pd.DataFrame:
    print(f'Start schedule calculation for {overpayment_name}...') if overpayment_name else print(
        'Start schedule calculation...')
    r = annual_rate / 12
    saldo = round_math(principal, 2)
    remaining_term = months
    schedule = []
    monthly_overpayment_value = 0.0
    range_monthly_overpayment_value = {}
    remaining_balance = round_math(principal, 2)
    const_payment = round_math(npf.pmt(r, months, -saldo), 2)
    const_saldo = round_math(principal, 2)

    for m in range(1, remaining_term + 1):
        payment = round_math(npf.pmt(r, months, -saldo), 2)
        interest = round_math((remaining_balance * r), 2)
        capital = round_math((payment - interest), 2)
        schedule_unit = ScheduleUnit(month=m,
                                     payment=payment,
                                     interest=interest,
                                     capital=capital,
                                     overpayment=0.0,
                                     remaining_balance=round_math((remaining_balance - capital), 2),
                                     remaining_term=remaining_term)

        if remaining_balance <= capital:
            payment = interest + remaining_balance
            schedule_unit = ScheduleUnit(month=m,
                                         payment=payment,
                                         interest=interest,
                                         capital=remaining_balance,
                                         overpayment=0.0,
                                         remaining_balance=0.0,
                                         remaining_term=remaining_term)

        elif remaining_balance <= (capital + monthly_overpayment_value):
            overpayment = round_math((remaining_balance - capital), 2)
            schedule_unit = ScheduleUnit(month=m,
                                         payment=payment,
                                         interest=interest,
                                         capital=remaining_balance,
                                         overpayment=overpayment,
                                         remaining_balance=0.0,
                                         remaining_term=remaining_term)

        elif not overpayments.empty:
            for idx, row in overpayments.iterrows():
                overpayment_type = row[OVERPAYMENT_TYPE]
                start = row[OVERPAYMENT_START]
                end = row[OVERPAYMENT_END]
                overpayment = row[OVERPAYMENT_VALUE]
                is_constant = row[OVERPAYMENT_IS_CONSTANT]

                if start <= m <= end:
                    if remaining_balance <= (overpayment + monthly_overpayment_value + capital):
                        full_overpayment = round_math((remaining_balance - capital), 2)
                        total_capital = round_math((capital + full_overpayment), 2)
                        remaining_balance = round_math((remaining_balance - total_capital), 2)
                        schedule_unit.overpayment = full_overpayment
                        schedule_unit.remaining_balance = remaining_balance  # should be 0.0
                        break

                    full_overpayment = round_math((overpayment + monthly_overpayment_value), 2)
                    saldo -= round_math(full_overpayment, 2)
                    if is_constant:
                        if overpayment_type == OverpaymentType.ONE_TIME.name:
                            new_payment = round_math(npf.pmt(r, months, -saldo), 2)
                            delta = const_payment - new_payment
                            const_payment = new_payment
                            new_monthly_overpayment = Overpayment(overpayment_type=OverpaymentType.RANGE,
                                                                  start_month=start + 1,
                                                                  end_month=months,
                                                                  value=delta,
                                                                  is_constant_payment=True)
                            new_monthly_overpayment_df = pd.DataFrame([new_monthly_overpayment.convert_to_dict()])
                            overpayments = pd.concat([overpayments, new_monthly_overpayment_df], ignore_index=True)

                        elif overpayment_type == OverpaymentType.RANGE.name and end == m:
                            new_payment = round_math(npf.pmt(r, months, -saldo), 2)
                            delta = const_payment - new_payment
                            const_payment = new_payment
                            monthly_overpayment_value = range_monthly_overpayment_value[idx]
                            new_monthly_overpayment = Overpayment(overpayment_type=OverpaymentType.RANGE,
                                                                  start_month=end + 1,
                                                                  end_month=months,
                                                                  value=delta,
                                                                  is_constant_payment=True)
                            new_monthly_overpayment_df = pd.DataFrame([new_monthly_overpayment.convert_to_dict()])
                            overpayments = pd.concat([overpayments, new_monthly_overpayment_df], ignore_index=True)
                        else:
                            if overpayment_type == OverpaymentType.RANGE.name and start == m:
                                range_monthly_overpayment_value[idx] = monthly_overpayment_value
                            new_payment = round_math(npf.pmt(r, months, -saldo), 2)
                            delta = const_payment - new_payment
                            monthly_overpayment_value = round_math(delta, 2)

                    else:
                        const_saldo -= round_math(overpayment, 2)
                        new_payment = round_math(npf.pmt(r, months, -const_saldo), 2)
                        const_payment = new_payment

                    total_capital = round_math((capital + full_overpayment), 2)
                    remaining_balance -= total_capital
                    schedule_unit.update_overpayment_remaining_balance(add_overpayment=full_overpayment,
                                                                       remaining_balance=remaining_balance)
        if m > months:
            print(f'Overpayment in month {m} was ignored because the loan term ended.')
            break

        schedule.append(schedule_unit)
        remaining_term -= 1
        remaining_balance = schedule_unit.remaining_balance

        if remaining_balance <= 0:
            print(f'The loan has been fully repaid.')
            return pd.DataFrame([vars(item) for item in schedule])

    return pd.DataFrame([vars(item) for item in schedule])


def summarize_loan(df: DataFrame) -> dict:
    loan_amount = df['capital'][0] + df['overpayment'][0] + df['remaining_balance'][0]
    total_interest = df['interest'].sum()
    total_cost = loan_amount + total_interest
    last_month = int(df['month'].max())
    years = last_month // 12
    rest_month = last_month - (years * 12)

    return {
        'Loan amount': round_math(loan_amount, 2),
        'Total interest': round_math(total_interest, 2),
        'Total loan cost': round_math(total_cost, 2),
        'Last month': f'{last_month} ({years} years and {rest_month} months)'
    }
