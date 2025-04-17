import numpy_financial as npf
import streamlit as st

from calculator.calculation import calculate_result
from dashboard.sidebar import display_sidebar
from calculator.loan_data import LoanData, LoanSummary
from dashboard.plot_generator import plot_remaining_balance, plot_total_loan_cost, plot_loan_duration
from utils import round_math
from . import app_state

state = app_state
_ = state.translation


def display_summary(summary: LoanSummary):
    years_and_text = _(' years and ')
    months_text = _(' months')
    loan_amount_text = _('Loan amount: ')
    total_interest_text = _('Total interest: ')
    total_costs = _('Total loan costs: ')
    loan_term_text = _('Last month: ')

    st.write(f'{loan_amount_text}{round_math(summary.loan_amount, 2)} PLN')
    st.write(f'{total_interest_text}{round_math(summary.total_interest, 2)} PLN')
    st.write(f'{total_costs}{round_math(summary.total_loan_cost, 2)} PLN')
    st.write(
        f'{loan_term_text}{summary.last_month} ({summary.years}{years_and_text}{summary.rest_months}{months_text})')


def display_loan_details():
    loan_data: LoanData = state.loan_data

    annual_rate = loan_data.loan_annual_rate
    monthly_rate = annual_rate / 12
    months = loan_data.months
    loan_amount = loan_data.loan_amount
    initial_payment = round_math(npf.pmt(monthly_rate, months, -loan_amount), 2)

    years = months // 12
    rest_months = months - (years * 12)

    years_and_text = _(' years and ')
    months_text = _(' months')
    loan_amount_text = _('Loan amount: ')
    annual_rate_text = _('Annual rate: ')
    loan_term_text = _('Loan term: ')
    initial_monthly_payment_text = _('Initial Monthly Payment: ')

    st.subheader(_('Loan Details'))
    st.write(f'{loan_amount_text}{round_math(loan_amount, 2)} PLN')
    st.write(f'{annual_rate_text}{round_math(annual_rate * 100, 2)}%')
    st.write(f'{loan_term_text}{months} ({years}{years_and_text}{rest_months}{months_text})')
    st.write(f'{initial_monthly_payment_text}{round_math(initial_payment, 2)} PLN')


def display_calculation():
    result = calculate_result()
    loan_summary_text = _('Loan Summary: ')
    repayment_schedule_text = _('Repayment Schedule for ')
    diagrams_text = _('Diagrams for comparison')
    for key, summary in result.summarises.items():
        st.subheader(f'{loan_summary_text}"{key}"')
        display_summary(summary=summary)

    for key, schedule in result.schedules.items():
        st.subheader(f'{repayment_schedule_text}"{key}"')
        st.dataframe(schedule)

    if result.schedules:
        st.subheader(diagrams_text)

        plot_remaining_balance(result.schedules)
        plot_total_loan_cost(result.schedules)
        plot_loan_duration(result.schedules)


def display_details():
    st.subheader(_('Loan details:'))
    loan_amount = _('Loan amount: ')
    annual_rate = _('Annual rate: ')
    loan_term = _('Loan Term: ')
    init_payment = _('Initial payment: ')
    initial_payment_value = round_math(npf.pmt(state.loan_data.loan_annual_rate/12, state.loan_data.months, -state.loan_data.loan_amount), 2)

    st.write(f'{loan_amount}{state.loan_data.loan_amount} PLN')
    st.write(f'{annual_rate}{round_math(state.loan_data.loan_annual_rate * 100, 2)}%')
    st.write(f'{loan_term}{state.loan_data.months}')
    st.write(f'{init_payment}{initial_payment_value} PLN')


def display_dashboard():
    display_sidebar()
    st.header(_('Mortgage Calculator with Overpayments'))
    if state.calculate_schedule:
        display_details()
        display_calculation()


if __name__ == '__main__':
    display_dashboard()
