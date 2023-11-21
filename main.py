import math
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="My Personal Finance App!",
    layout="wide",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug': 'https://www.google.com/',
        'About': '# Welcome to HCI. Developed by Rodney Graham'
    }
)

# Add a sidebar with the selectbox
option = st.sidebar.selectbox("Select an Option:", ["Home", "Budgeting", "Investing", "Debt Management"])


def calculate_time_to_pay_off(initial_debt, interest_rate, monthly_payment):
    initial_debt = float(initial_debt)
    interest_rate = float(interest_rate)
    monthly_payment = float(monthly_payment)

    if monthly_payment <= 0:
        return -1  # Indicate that the debt will never be paid off with the current payment

    if interest_rate <= 0:
        return int(initial_debt / monthly_payment)

    monthly_interest_rate = interest_rate / 12 / 100

    if initial_debt * monthly_interest_rate >= monthly_payment:
        return -1  # Indicate that the debt will never be paid off with the current payment

    n = -math.log(1 - (initial_debt * monthly_interest_rate) / monthly_payment) / math.log(1 + monthly_interest_rate)
    return int(n)

def calculate_time_to_pay_off_with_extra_payment(initial_debt, interest_rate, monthly_payment, extra_payment):
    initial_debt = float(initial_debt)
    interest_rate = float(interest_rate)
    monthly_payment = float(monthly_payment)
    extra_payment = float(extra_payment)

    if monthly_payment <= 0:
        return -1  # Indicate that the debt will never be paid off with the current payment

    if interest_rate <= 0:
        return int(initial_debt / (monthly_payment + extra_payment))

    monthly_interest_rate = interest_rate / 12 / 100

    if initial_debt * monthly_interest_rate >= (monthly_payment + extra_payment):
        return -1  # Indicate that the debt will never be paid off with the current payment

    n = -math.log(1 - (initial_debt * monthly_interest_rate) / (monthly_payment + extra_payment)) / math.log(1 + monthly_interest_rate)
    return int(n)

if option == "Home":
    st.title("My Personal Finance App!")
    st.subheader("Created by Rodney Graham")
    st.text("Welcome to Simple Personal Finance")

elif option == "Budgeting":
    st.title("Budget")
    st.text("Here we are going to build a simple budget")

    st.header("**Monthly Income**")
    st.subheader("Salary")
    # Consider adding a 3rd column to include a table showing the tax brackets
    colAnnualSal, colTax = st.columns(2)

    with colAnnualSal:
        salary = st.number_input("Enter your annual salary($): ", min_value=0.0, format='%f')
    with colTax:
        tax_rate = st.radio('What is your tax rate %?',
                            [10, 12, 22, 24, 32, 35, 37])

    tax_rate = tax_rate / 100.0
    salary_after_taxes = salary * (1 - tax_rate)
    monthly_takehome_salary = round(salary_after_taxes / 12.0, 2)

    st.write(
        "Your gross yearly income is", salary, ","
                                               " after taxes your net yearly income is", salary_after_taxes,
        " and your "
        "monthly net income is $", monthly_takehome_salary)

    st.header("**Monthly Expenses**")
    colExpenses1, colExpenses2 = st.columns(2)

    with colExpenses1:
        st.subheader("Monthly Rent")
        monthly_rent = st.number_input(
            "Enter your monthly rent($): ", min_value=0.0, format='%f')

        st.subheader("Monthly Utilities")
        monthly_utilities = st.number_input(
            "Enter your monthly expenses on utilities ($): ", min_value=0.0, format='%f')

        st.subheader("Savings")
        monthly_savings = st.number_input(
            "Enter your monthly contributions towards savings: ", min_value=0.0, format='%f')

        st.subheader("Monthly Bills")
        st.text("Include here one time bills such as, Car Insurance, Streaming subscriptions, etc")
        monthly_bills = st.number_input(
            "Enter the total that goes towards bills: ", min_value=0.0, format='%f')

    with colExpenses2:

        st.subheader("Groceries")
        weekly_groceries = st.number_input(
            "Enter your weekly expenses on groceries: ", min_value=0.0, format='%f')
        weekly_groceries = weekly_groceries * 4

        st.subheader("Entertainment")
        weekly_entertainment = st.number_input(
            "Enter your weekly expenses on entertainment: ", min_value=0.0, format='%f')
        weekly_entertainment = weekly_entertainment * 4

        st.subheader("Transportation")
        weekly_transport = st.number_input(
            "Enter your weekly expenses on transportation: ", min_value=0.0, format='%f')

        st.subheader("Buffer")
        weekly_buffer = st.number_input(
            "Enter a weekly buffer for unexpected expenses: ", min_value=0.0, format='%f')

    monthly_expenses = monthly_rent + monthly_utilities + monthly_bills
    weekly_expenses = weekly_groceries + weekly_entertainment + weekly_transport + weekly_buffer

    surplus_or_deficit = monthly_takehome_salary - (monthly_expenses + weekly_expenses + monthly_savings)

    if surplus_or_deficit > 0:
        st.write(f"You have a monthly surplus of $ :green[{surplus_or_deficit:.2f}]")
    elif surplus_or_deficit < 0:
        st.write(f"You have a monthly deficit of $ :red[{surplus_or_deficit:.2f}]")

    graphCol1, graphCol2 = st.columns(2)

    with graphCol1:
        expense_labels = ["Rent", "Utilities", "Bills", "Groceries", "Entertainment", "Transportation", "Buffer"]
        expense_values = [monthly_rent, monthly_utilities, monthly_bills, weekly_groceries, weekly_entertainment,
                          weekly_transport, weekly_buffer]

        expense_breakdown = px.pie(
            names=expense_labels,
            values=expense_values,
            title="Monthly Expenses Breakdown"
        )

        st.plotly_chart(expense_breakdown)

    with graphCol2:
        remaining_funds = px.pie(
            names=["Expenses", "Remaining Funds", "Savings"],
            values=[surplus_or_deficit, monthly_expenses, monthly_savings],
            color_discrete_sequence=["green", "red", "blue"],
            title="Remaining Funds Breakdown"
        )

        st.plotly_chart(remaining_funds)


elif option == "Investing":
    st.text("Here we are going to learn the basics about investing")

elif option == "Debt Management":
    st.title("Debt Management")
    st.text("Track and Manage Your Debts")

    # Initialize debts and total_debt if not already initialized
    if "debts" not in st.session_state:
        st.session_state.debts = []

    if "total_debt" not in st.session_state:
        st.session_state.total_debt = 0.0

    # Initialize a dictionary to store the total amount owed for each specific form of debt
    if "total_amounts" not in st.session_state:
        st.session_state.total_amounts = {}

    with st.form("debt_form"):
        debt_name = st.text_input("Debt Name")
        interest_rate = st.number_input("Interest Rate (%)", value=0.0, min_value=0.0)
        initial_debt = st.number_input("Initial Debt Amount ($)", value=0.0, min_value=0.0)
        min_monthly_payment = st.number_input("Minimum Monthly Payment ($)", value=0.0, min_value=0.0)
        loan_length = st.number_input("Loan Length in Months", value=0, min_value=0)

        add_debt = st.form_submit_button("Add Debt")

        if add_debt:
            if debt_name:
                new_debt = {
                    "Debt Name": debt_name,
                    "Interest Rate": interest_rate,
                    "Minimum Monthly Payment": min_monthly_payment,
                    "Loan Length": loan_length,
                    "Initial Debt": initial_debt
                }
                st.session_state.debts.append(new_debt)

                # Update the total amount owed for this specific form of debt
                if debt_name in st.session_state.total_amounts:
                    st.session_state.total_amounts[debt_name] += initial_debt
                else:
                    st.session_state.total_amounts[debt_name] = initial_debt

    st.subheader("Your Debts:")
    for debt in st.session_state.debts:
        st.write("Debt name:", debt["Debt Name"])
        st.write("Initial Debt: $", debt["Initial Debt"])
        st.write("Interest Rate: %", debt["Interest Rate"])
        st.write("Loan Length (in months):", debt["Loan Length"])
        st.write("Minimum Monthly Payments: $", debt["Minimum Monthly Payment"])

    st.write("Total Amount Owed for Each Form of Debt:")
    for debt in st.session_state.debts:
        debt_name = debt["Debt Name"]
        total_amount = debt["Initial Debt"]

        st.write(f"{debt_name}: ${total_amount:.2f}")

        # Calculate time to pay off the debt
        time_to_pay_off = calculate_time_to_pay_off(
            total_amount, debt["Interest Rate"], debt["Minimum Monthly Payment"]
        )
        if time_to_pay_off < 0:
            st.write(f":red[You will not be able to pay off the debt at this rate, consider increasing monthly payments]")
        else:
            st.write(f"Time to Pay Off: :green[{time_to_pay_off} months]")

    # Calculate the total debt amount across all forms of debt
    st.session_state.total_debt = sum(st.session_state.total_amounts.values())
    st.subheader(f"Total Debt Amount: $:red[{st.session_state.total_debt:.2f}]")



    st.header("Additional Payments to Pay Off Debts Faster")
    with st.form("extra_payment_form"):
        extra_payment = st.number_input("Enter Extra Payment Amount $", value=0.0, min_value=0.0)
        add_extra_payment = st.form_submit_button("Add Extra Payment")

        if add_extra_payment:
            if extra_payment > 0:
                st.session_state.total_debt -= extra_payment
                st.write(f"New Total Debt Amount After Extra Payment: ${st.session_state.total_debt:.2f}")

                # Update the time frame after the extra payment
                st.subheader("Updated Time Frames:")
                total_payment_amount = 0  # Initialize total payment amount

                for debt in st.session_state.debts:
                    debt_name = debt["Debt Name"]
                    initial_debt = debt["Initial Debt"]

                    # Calculate time to pay off the debt with the updated total debt amount
                    time_to_pay_off_updated = calculate_time_to_pay_off_with_extra_payment(
                        initial_debt, debt["Interest Rate"], debt["Minimum Monthly Payment"], extra_payment
                    )
                    if time_to_pay_off_updated < 0:
                        st.write(
                            f"{debt_name}: :red[You will not be able to pay off the debt at this rate, "
                            f"consider increasing monthly payments]")
                    else:
                        st.write(f"{debt_name}: Pay Off in :green[{time_to_pay_off_updated} months]")

                    # Update the total payment amount
                    total_payment_amount += debt["Minimum Monthly Payment"]  # Add monthly payment

                total_payment_amount += extra_payment  # Add extra payment

                # Update the time frame for the total debt amount
                st.subheader("Total Debt Pay Off:")
                total_time_to_pay_off = calculate_time_to_pay_off(
                    st.session_state.total_debt, 0, total_payment_amount
                )
                st.write(f"Total Debt Pay Off in :green[{total_time_to_pay_off} months]")



