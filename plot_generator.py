from typing import Callable

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from calculation import summarize_loan


def plot_remaining_balance(schedules: dict, _: Callable[[str], str]):
    plt.figure(figsize=(10, 6))
    for label, df in schedules.items():
        plt.plot(df['month'], df['remaining_balance'], label=label)
    plt.xlabel(_('Month'))
    plt.ylabel(_('Remaining saldo'))
    plt.title(_('Loan Balance Over Time'))
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
    plt.clf()


def plot_total_loan_cost(schedules: dict, _: Callable[[str], str]):
    labels = []
    costs = []
    for label, df in schedules.items():
        summary= summarize_loan(df)
        labels.append(label)
        costs.append(summary.total_loan_cost)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=labels, y=costs, ax=ax)
    ax.set_title(_('Total loan cost'))
    ax.set_ylabel(_('Costs'))
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=90)
    for i, val in enumerate(costs):
        ax.text(i, val + 1000, f"{val:,.0f}", ha='center', fontsize=10)
    st.pyplot(fig)
    plt.clf()


def plot_loan_duration(schedules: dict, _: Callable[[str], str]):
    labels = []
    durations = []
    formatted_labels = []

    for label, df in schedules.items():
        summary = summarize_loan(df)
        months = summary.last_month
        labels.append(label)
        durations.append(months)
        year_and_text = _(' years and ')
        months_text = _(' months')
        formatted_labels.append(f'{months} ({summary.years}{year_and_text}{summary.rest_months}{months_text})')

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=labels, y=durations, ax=ax)
    ax.set_title(_('Loan Term Length'))
    ax.set_ylabel(_('Month'))
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=90)
    for i, val in enumerate(formatted_labels):
        ax.text(i, durations[i] + 1, val, ha='center', fontsize=5)
    st.pyplot(fig)
    plt.clf()
