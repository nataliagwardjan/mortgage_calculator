import streamlit as st
import pandas as pd
import numpy_financial as npf

from calculation import generate_schedule, summarize_loan
from loan_data import LoanData
from overpayment import Overpayment, OverpaymentType, OverpaymentData, overpayments_to_df
from plot_generator import plot_remaining_balance, plot_total_loan_cost, plot_loan_duration
from utils import round_math

if 'custom_overpayments' not in st.session_state:
    st.session_state.custom_overpayments = []

if 'loan_data' not in st.session_state:
    st.session_state.loan_data = LoanData

if 'overpayments' not in st.session_state:
    st.session_state.overpayments = []

if 'is_analysis_constant_overpayment' not in st.session_state:
    st.session_state.is_analysis_constant_overpayment = False

if 'is_custom_overpayment' not in st.session_state:
    st.session_state.is_custom_overpayment = False


def one_time_overpayment_option(loan_term: int) -> Overpayment:
    overpayment_month = st.sidebar.number_input('Month of Overpayment', min_value=1, max_value=loan_term, value=10)
    overpayment_value = st.sidebar.number_input(f'Overpayment Value in Month {overpayment_month} (PLN)',
                                                min_value=0.0, value=20000.0)
    increase_overpayment = st.sidebar.checkbox(f'Increase Overpayment After Month {overpayment_month}')

    return Overpayment(overpayment_type=OverpaymentType.ONE_TIME,
                       start_month=overpayment_month,
                       end_month=overpayment_month,
                       value=overpayment_value,
                       is_constant_payment=True if increase_overpayment else False)


def full_term_overpayment_option(loan_term: int) -> Overpayment:
    overpayment_value = st.sidebar.number_input(f'Overpayment for Entire Loan Term (PLN)',
                                                min_value=0.0, value=200.0)
    increase_overpayment = st.sidebar.checkbox(f'Keep Fixed Payment for Entire Loan Term')

    return Overpayment(overpayment_type=OverpaymentType.FULL_TERM,
                       start_month=1,
                       end_month=loan_term,
                       value=overpayment_value,
                       is_constant_payment=True if increase_overpayment else False)


def range_overpayment_option(loan_term: int) -> Overpayment:
    start_month = st.sidebar.number_input('Start Month of Overpayment Range', min_value=1, value=1)
    end_month = st.sidebar.number_input('End Month of Overpayment Range', min_value=start_month, max_value=loan_term,
                                        value=10)
    overpayment_value = st.sidebar.number_input(
        f'Overpayment Value from Month {start_month} to {end_month} (PLN)', min_value=0.0, value=200.0)
    increase_overpayment = st.sidebar.checkbox(
        f'Keep Fixed Payment with Overpayment Between {start_month} and {end_month}')

    return Overpayment(overpayment_type=OverpaymentType.RANGE,
                       start_month=start_month,
                       end_month=end_month,
                       value=overpayment_value,
                       is_constant_payment=True if increase_overpayment else False)


def generate_overpayment(loan_term: int):
    overpayment_option = st.sidebar.radio('Select Overpayment Type', ['One-time', 'Range', 'Full Term'])
    overpayment = None
    if overpayment_option == 'Full Term':
        overpayment = full_term_overpayment_option(loan_term=loan_term)
    elif overpayment_option == 'One-time':
        overpayment = one_time_overpayment_option(loan_term=loan_term)
    elif overpayment_option == 'Range':
        overpayment = range_overpayment_option(loan_term=loan_term)
    else:
        st.warning('Please select an overpayment option.')

    if overpayment is not None:
        if st.sidebar.button('Add'):
            st.session_state.custom_overpayments.append(overpayment)
    else:
        st.warning('No overpayment details to add.')


def overpayment_display(overpayment: Overpayment, idx: int):
    if overpayment.overpayment_type.name == OverpaymentType.ONE_TIME:
        st.sidebar.text(f'Type: {overpayment.overpayment_type.name}, '
                        f'{overpayment.start_month}, '
                        f'{overpayment.value} PLN, '
                        f'{overpayment.is_constant_payment}')
    else:
        st.sidebar.text(f'Type: {overpayment.overpayment_type.name}, '
                        f'{overpayment.start_month} - {overpayment.end_month}, '
                        f'{overpayment.value} PLN, {overpayment.is_constant_payment}')
    if st.sidebar.button(f'Remove', key=f'remove_{idx}'):
        st.session_state.custom_overpayments.pop(idx)
        st.rerun()


def display_custom_overpayment():
    for idx, overpayment in enumerate(st.session_state.custom_overpayments):
        overpayment_display(overpayment=overpayment, idx=idx)


def generate_schemas_dict(*schemas_pairs):
    return {label: data_frame for label, data_frame in schemas_pairs}


def sidebar():
    st.sidebar.header('Loan Parameters')
    loan_amount = st.sidebar.number_input('Loan Amount (PLN)', min_value=10000.0, max_value=50000000.0,
                                          value=450000.0) * 1.0
    annual_rate = st.sidebar.number_input('Annual Interest Rate (%)', min_value=0.1, max_value=30.0, value=7.58) / 100
    months = st.sidebar.number_input('Loan Term (months)', min_value=12, max_value=360, value=240)

    st.session_state.loan_data = LoanData(loan_amount=loan_amount,
                                          loan_annual_rate=annual_rate,
                                          months=months)

    is_analysis_constant_overpayment = st.sidebar.toggle('Include prepayment', value=False)
    if is_analysis_constant_overpayment:
        st.session_state.is_analysis_constant_overpayment = True
        analysis_overpayment_value = st.sidebar.number_input('Const overpayment (PLN)', min_value=1.0,
                                                             max_value=loan_amount,
                                                             value=200.0)
        constant_overpayment_by_value = Overpayment(overpayment_type=OverpaymentType.FULL_TERM,
                                                    start_month=1,
                                                    end_month=st.session_state.loan_data.months,
                                                    value=analysis_overpayment_value,
                                                    is_constant_payment=False)
        constant_overpayment_by_payment = Overpayment(overpayment_type=OverpaymentType.FULL_TERM,
                                                      start_month=1,
                                                      end_month=st.session_state.loan_data.months,
                                                      value=analysis_overpayment_value,
                                                      is_constant_payment=True)
        st.session_state.overpayments.append(
            OverpaymentData(name='Overpayment with constant overpayment value',
                            overpayments=overpayments_to_df([constant_overpayment_by_value])))
        st.session_state.overpayments.append(
            OverpaymentData(name='Overpayment with constant monthly payment value',
                            overpayments=overpayments_to_df([constant_overpayment_by_payment])))
    else:
        st.session_state.is_analysis_constant_overpayment = False

    is_add_custom_overpayments = st.sidebar.toggle('Current custom overpayments', value=False)

    # todo - generate multi custom overpayments examples, not only one with one or more overpayments
    # user can give a name for his custom overpayments
    if is_add_custom_overpayments:
        generate_overpayment(st.session_state.loan_data.months)
        st.session_state.is_custom_overpayment = True
    else:
        st.session_state.is_custom_overpayment = False

    if st.session_state.is_custom_overpayment and st.session_state.custom_overpayments:
        st.sidebar.title('Current custom overpayments')
        display_custom_overpayment()


def main():
    st.title('Mortgage Calculator with Overpayments')

    sidebar()

    if st.sidebar.button('Calculate Loan Schedule'):
        custom_overpayments = st.session_state.custom_overpayments
        if st.session_state.is_custom_overpayment and custom_overpayments is not None and custom_overpayments:
            print(f'custom_overpayments = {custom_overpayments}')
            st.session_state.overpayments.append(OverpaymentData(name='Custom overpayment',
                                                                 overpayments=overpayments_to_df(custom_overpayments)))

        overpayments: list[OverpaymentData] = st.session_state.overpayments
        loan_data: LoanData = st.session_state.get('loan_data', None)

        annual_rate = loan_data.loan_annual_rate
        monthly_rate = annual_rate / 12
        months = loan_data.months
        loan_amount = loan_data.loan_amount
        initial_payment = round_math(npf.pmt(monthly_rate, months, -loan_amount), 2)

        years = months // 12
        rest_months = months - (years * 12)

        st.subheader(f'Loan Details')
        st.write(f'Loan amount: {round_math(loan_amount, 2)} PLN')
        st.write(f'Annual rate: {round_math(annual_rate * 100, 2)}%')
        st.write(f'Loan term: {months} ({years} years and {rest_months} month(s))')
        st.write(f'Initial Monthly Payment: {initial_payment} PLN')

        schedules = {}
        summarises = {}
        no_overpayment_schedule = generate_schedule(principal=loan_amount,
                                                    annual_rate=annual_rate,
                                                    months=months,
                                                    overpayment_name='no overpayment',
                                                    overpayments=pd.DataFrame())
        no_overpayment_summary = summarize_loan(no_overpayment_schedule)
        schedules['No overpayment'] = no_overpayment_schedule
        summarises['No overpayment'] = no_overpayment_summary

        if st.session_state.is_custom_overpayment or st.session_state.is_analysis_constant_overpayment:
            for overpayment in overpayments:
                name = overpayment.name
                print(f'overpayment name {name}')
                schedule = generate_schedule(principal=loan_amount,
                                             annual_rate=annual_rate,
                                             months=months,
                                             overpayment_name=name,
                                             overpayments=overpayment.overpayments)
                summarises[name] = summarize_loan(schedule)
                schedules[name] = schedule

        for key, summary in summarises.items():
            st.subheader(f'Loan Summary: {key}')
            st.write(summary)

        for key, schedule in schedules.items():
            st.subheader(f'Repayment Schedule for {key}')
            st.dataframe(schedule)

        if schedules:
            st.subheader('Diagrams for comparison')

            plot_remaining_balance(schedules)
            plot_total_loan_cost(schedules)
            plot_loan_duration(schedules)


if __name__ == '__main__':
    main()
