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
option = st.sidebar.selectbox("Select an Option:", ["Home", "Budgeting", "Investing", "Debt"])


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

    tax_rate = tax_rate /100.0
    salary_after_taxes = salary * (1 - tax_rate)
    monthly_takehome_salary = round(salary_after_taxes / 12.0, 2)

    st.write(
        "Your gross yearly income is", salary, ","
        " after taxes your net yearly income is", salary_after_taxes, " and your "
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
        st.write(f"You have a monthly surplus of $ :green[{surplus_or_deficit}]")
    elif surplus_or_deficit < 0:
        st.write(f"You have a monthly deficit of $ :red[{surplus_or_deficit}]")

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
            color_discrete_sequence=["red", "green", "blue"],
            title="Remaining Funds Breakdown"
        )

        st.plotly_chart(remaining_funds)


elif option == "Investing":
    st.text("Here we are going to learn the basics about investing")

elif option == "Debt Management":
    st.title("Debt Management")
    st.text("Track and Manage Your Debts")

    if st.button("Add Debt"):
        debt_name = st.text_input("Debt Name", "")
        interest_rate = st.number_input("Interest Rate (%)", value=0.0, min_value=0.0)
        min_monthly_payment = st.number_input("Minimum Monthly Payment $", value=0.0, min_value=0.0)
        loan_length = st.number_input("Loan Length in Months", value=0.0, min_value=0.0)

        if "debts" not in st.session_state:
            st.session_state.debts = pd.DataFrame(columns=["Debt Name", "Interest Rate",
                                                           "Minimum Monthly Payment", "Loan Length"])

        if debt_name:
            st.session_state.debts = st.session_state.debts.append(
                {"Debt Name": debt_name, "Interest Rate (%)": interest_rate,
                 "Minimum Monthly Payment ($)": min_monthly_payment, "Loan Length (months)": loan_length}
                , ignore_index=True)

    st.write("Your Debts:")
    st.write(st.session_state.debts)

    total_debt = st.session_state.debts["Minimum Monthly Payment $"].sum()
    st.write(f"Total Debt Amount: ${total_debt:.2f}")