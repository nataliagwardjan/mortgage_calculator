import numpy_financial as npf
import pandas as pd
from pandas import DataFrame

from dashboard import app_state
from loan_data import LoanSummary
from loan_schedule import ScheduleUnit
from overpayment import OverpaymentType, Overpayment, OverpaymentData, overpayments_to_df
from utils import OVERPAYMENT_IS_CONSTANT, OVERPAYMENT_VALUE, OVERPAYMENT_START, OVERPAYMENT_END, round_math, \
    OVERPAYMENT_TYPE

state = app_state
_ = app_state.translation


class Result:
    def __init__(self, schedules: dict, summarises: dict):
        self.schedules = schedules
        self.summarises = summarises


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


def summarize_loan(df: DataFrame) -> LoanSummary:
    loan_amount = df['capital'][0] + df['overpayment'][0] + df['remaining_balance'][0]
    total_interest = df['interest'].sum()
    total_cost = loan_amount + total_interest
    last_month = int(df['month'].max())

    return LoanSummary(loan_amount=round_math(loan_amount, 2),
                       total_interest=round_math(total_interest, 2),
                       total_loan_cost=round_math(total_cost, 2),
                       last_month=round_math(last_month, 2))


def calculate_result() -> Result:
    custom_overpayments = state.custom_overpayments_set
    if state.is_custom_overpayment and custom_overpayments:
        print(f'Custom_overpayments = {custom_overpayments}')
        for overpayment_data in custom_overpayments:
            state.overpayments_set.append(overpayment_data)

    schedules = {}
    summarises = {}
    no_overpayment_schedule = generate_schedule(principal=state.loan_data.loan_amount,
                                                annual_rate=state.loan_data.loan_annual_rate,
                                                months=state.loan_data.months,
                                                overpayment_name=_('No overpayment'),
                                                overpayments=pd.DataFrame())
    no_overpayment_summary = summarize_loan(no_overpayment_schedule)
    schedules[_('No overpayment')] = no_overpayment_schedule
    summarises[_('No overpayment')] = no_overpayment_summary

    if state.is_custom_overpayment or state.is_analysis_constant_overpayment:
        overpayments: list[OverpaymentData] = state.overpayments_set
        for overpayment in overpayments:
            name = overpayment.name
            print(f'Overpayment name {name}')
            schedule = generate_schedule(principal=state.loan_data.loan_amount,
                                         annual_rate=state.loan_data.loan_annual_rate,
                                         months=state.loan_data.months,
                                         overpayment_name=name,
                                         overpayments=overpayments_to_df(overpayments=overpayment.overpayments))
            summarises[name] = summarize_loan(schedule)
            schedules[name] = schedule

    return Result(schedules=schedules, summarise=summarises)
