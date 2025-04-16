from dashboard import app_state
from calculator.loan_data import LoanData
from calculator.overpayment import Overpayment, OverpaymentType, OverpaymentData
import streamlit as st

from utils import language_labels

state = app_state
_ = state.translation


def get_language_option():
    lang_code = st.session_state.get('language', 'en')
    label = language_labels[lang_code]['label']
    options = language_labels[lang_code]['options']

    current_option = options[0] if lang_code == 'en' else options[1]
    chosen = st.sidebar.selectbox(label, options, index=options.index(current_option))

    if lang_code == 'en' and (chosen != 'English'):
        state.language = 'pl'
    elif lang_code == 'pl' and (chosen != 'Polski'):
        state.language = 'en'

    state.get_translation(lang_code=lang_code)


def one_time_overpayment_option() -> Overpayment:
    loan_term = state.loan_data.months
    overpayment_month = st.sidebar.number_input(_('Month of Overpayment'), min_value=1, max_value=loan_term, value=10)
    overpayment_value = st.sidebar.number_input(_(f'Overpayment Value in Month {overpayment_month} (PLN)'),
                                                min_value=0.0, value=20000.0)
    increase_overpayment = st.sidebar.checkbox(_(f'Increase Overpayment After Month {overpayment_month}'))

    return Overpayment(overpayment_type=OverpaymentType.ONE_TIME,
                       start_month=overpayment_month,
                       end_month=overpayment_month,
                       value=overpayment_value,
                       is_constant_payment=True if increase_overpayment else False)


def full_term_overpayment_option() -> Overpayment:
    loan_term = state.loan_data.months
    overpayment_value = st.sidebar.number_input(_(f'Overpayment for Entire Loan Term (PLN)'),
                                                min_value=0.0, value=200.0)
    increase_overpayment = st.sidebar.checkbox(_('Keep Fixed Payment for Entire Loan Term'))

    return Overpayment(overpayment_type=OverpaymentType.FULL_TERM,
                       start_month=1,
                       end_month=loan_term,
                       value=overpayment_value,
                       is_constant_payment=True if increase_overpayment else False)


def range_overpayment_option() -> Overpayment:
    loan_term = state.loan_data.months
    start_month = st.sidebar.number_input(_('Start Month of Overpayment Range'), min_value=1, value=1)
    end_month = st.sidebar.number_input(_('End Month of Overpayment Range'), min_value=start_month, max_value=loan_term,
                                        value=10)
    overpayment_value = st.sidebar.number_input(
        _(f'Overpayment Value from Month {start_month} to {end_month} (PLN)'), min_value=0.0, value=200.0)
    increase_overpayment = st.sidebar.checkbox(
        _(f'Keep Fixed Payment with Overpayment Between {start_month} and {end_month}'))

    return Overpayment(overpayment_type=OverpaymentType.RANGE,
                       start_month=start_month,
                       end_month=end_month,
                       value=overpayment_value,
                       is_constant_payment=True if increase_overpayment else False)


def generate_custom_overpayment():
    overpayment_option = st.sidebar.radio(_('Select Overpayment Type'), [_('One-time'), _('Range'), _('Full Term')])
    overpayment = None
    overpayment_name = state.current_overpayment_name

    options_map = {
        _('Full Term'): full_term_overpayment_option,
        _('One-time'): one_time_overpayment_option,
        _('Range'): range_overpayment_option
    }
    overpayment_func = options_map.get(overpayment_option)

    if overpayment_func:
        overpayment = overpayment_func()
    else:
        st.warning(_('Please select an overpayment option.'))

    if overpayment is not None:
        if st.sidebar.button(_('Add')):
            print(f'Button "add" has been clicked')
            for idx, overpayment_data in enumerate(state.custom_overpayments_set):
                if overpayment_data.name == overpayment_name:
                    print(f'Adding {overpayment} to {overpayment_data.name}, idx ={idx}')
                    overpayment_data.add_overpayment(overpayment)
                    break
        print(f'Custom overpayment set: {state.custom_overpayments_set}')
    else:
        st.warning('No overpayment details to add.')


def add_custom_overpayments():
    label = _('Choose overpayment set: ')
    custom_overpayments_set: list[OverpaymentData] = state.custom_overpayments_set

    overpayments_set_options = [item.name for item in custom_overpayments_set]
    chosen_overpayment_set = None

    if overpayments_set_options:
        if state.current_overpayment_name in overpayments_set_options:
            selected_index = overpayments_set_options.index(state.current_overpayment_name)
        else:
            selected_index = 0
        chosen_overpayment_set = st.sidebar.selectbox(
            label,
            overpayments_set_options,
            index=selected_index
        )

        st.sidebar.write(_('or'))

    custom_overpayment_name = st.sidebar.text_input(_('Name your overpayment set: '), key='custom_overpayment_name')

    if custom_overpayment_name and (custom_overpayment_name not in overpayments_set_options):
        overpayment_data = OverpaymentData(name=custom_overpayment_name,
                                           overpayments=[])
        if custom_overpayments_set:
            print(f'Custom overpayment {custom_overpayment_name}')
            state.custom_overpayments_set.append(overpayment_data)
        else:
            state.custom_overpayments_set = [overpayment_data]
        state.current_overpayment_name = custom_overpayment_name
        print(f'New custom overpayment has been added: {custom_overpayment_name}')
        generate_custom_overpayment()
    elif chosen_overpayment_set:
        state.current_overpayment_name = chosen_overpayment_set
        print(f'{chosen_overpayment_set} has been chosen')
        generate_custom_overpayment()


def display_overpayment(overpayment: Overpayment, overpayment_idx: int, overpayment_data_idx: int):
    if overpayment.overpayment_type.name == OverpaymentType.ONE_TIME.name:
        st.sidebar.text(f'Type: {overpayment.overpayment_type.name}, '
                        f'{overpayment.start_month}, '
                        f'{overpayment.value} PLN, '
                        f'{overpayment.is_constant_payment}')
    else:
        st.sidebar.text(f'Type: {overpayment.overpayment_type.name}, '
                        f'{overpayment.start_month} - {overpayment.end_month}, '
                        f'{overpayment.value} PLN, {overpayment.is_constant_payment}')
    if st.sidebar.button(_(f'Remove'), key=f'remove_overpayment_{overpayment_idx}_for_{overpayment_data_idx}'):
        print(f'Overpayment {overpayment} will be removed from {overpayment_data_idx}')
        state.custom_overpayments_set[overpayment_data_idx].overpayments.pop(overpayment_idx)
        print(f'Custom overpayment set: {state.custom_overpayments_set}')
        st.rerun()


def display_overpayment_set(overpayment_set: OverpaymentData, overpayment_data_idx: int):
    overpayment_set_header = _('Overpayment set: ')
    st.sidebar.write(f'{overpayment_set_header}**{overpayment_set.name}**')
    if st.sidebar.button(_(f'Remove'), key=f'remove_overpayment_data_{overpayment_data_idx}'):
        print(f'Overpayment set {overpayment_data_idx}, name {overpayment_set.name} has been removed')
        state.custom_overpayments_set.pop(overpayment_data_idx)
        print(f'Custom overpayment set: {state.custom_overpayments_set}')
        if state.custom_overpayments_set:
            state.current_overpayment_name = state.custom_overpayments_set[0].name
        else:
            state.current_overpayment_name = None
        st.rerun()
    for idx, overpayment in enumerate(overpayment_set.overpayments):
        display_overpayment(overpayment=overpayment, overpayment_idx=idx, overpayment_data_idx=overpayment_data_idx)


def display_custom_overpayment_set():
    st.sidebar.subheader(_('Custom overpayments sets: '))
    for idx, overpayment_data in enumerate(state.custom_overpayments_set):
        display_overpayment_set(overpayment_set=overpayment_data, overpayment_data_idx=idx)
        st.sidebar.markdown('---')


def get_loan_parameters():
    st.sidebar.header(_('Loan Parameters'))
    loan_amount = st.sidebar.number_input(_('Loan Amount (PLN)'), min_value=10000.0, max_value=50000000.0,
                                          value=450000.0) * 1.0
    annual_rate = st.sidebar.number_input(_('Annual Interest Rate (%)'), min_value=0.1, max_value=30.0,
                                          value=7.58) / 100
    months = st.sidebar.number_input(_('Loan Term (months)'), min_value=12, max_value=360, value=240)

    state.loan_data = LoanData(loan_amount=loan_amount,
                               loan_annual_rate=annual_rate,
                               months=months)


def is_include_prepayment():
    is_analysis_constant_overpayment = st.sidebar.toggle(_('Include prepayment'), value=False)
    if is_analysis_constant_overpayment:
        state.is_analysis_constant_overpayment = True
        analysis_overpayment_value = st.sidebar.number_input(_('Const overpayment (PLN)'), min_value=1.0,
                                                             max_value=state.loan_data.loan_amount,
                                                             value=200.0)
        constant_overpayment_by_value = Overpayment(overpayment_type=OverpaymentType.FULL_TERM,
                                                    start_month=1,
                                                    end_month=state.loan_data.months,
                                                    value=analysis_overpayment_value,
                                                    is_constant_payment=False)
        constant_overpayment_by_payment = Overpayment(overpayment_type=OverpaymentType.FULL_TERM,
                                                      start_month=1,
                                                      end_month=state.loan_data.months,
                                                      value=analysis_overpayment_value,
                                                      is_constant_payment=True)
        state.overpayments_set.append(
            OverpaymentData(name=_('Overpayment with constant overpayment value'),
                            overpayments=[constant_overpayment_by_value]))
        state.overpayments_set.append(
            OverpaymentData(name=_('Overpayment with constant monthly payment value'),
                            overpayments=[constant_overpayment_by_payment]))
    else:
        state.is_analysis_constant_overpayment = False
        state.overpayments_set = []


def is_include_custom_overpayment():
    is_add_custom_overpayments = st.sidebar.toggle(_('Current custom overpayments'), value=False)

    if is_add_custom_overpayments:
        state.is_custom_overpayment = True
        add_custom_overpayments()
    else:
        state.is_custom_overpayment = False
        state.custom_overpayments_set = []

    if state.is_custom_overpayment and state.custom_overpayments_set:
        st.sidebar.title(_('Current custom overpayments'))
        display_custom_overpayment_set()


def display_sidebar():
    get_language_option()
    get_loan_parameters()
    is_include_prepayment()
    is_include_custom_overpayment()

    if st.sidebar.button(_('Calculate Loan Schedule')):
        state.calculate_schedule = True
