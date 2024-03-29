import json
import math
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from alpha_vantage.timeseries import TimeSeries

st.set_page_config(
    page_title="WealthPath Finder",
    layout="wide",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug': 'https://www.google.com/',
        'About': '# Welcome to WealthPath Finder. Developed by Rodney Graham'
    }
)

# Add a sidebar with the select box
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


def calculate_debt_over_time(initial_debt, interest_rate, monthly_payment, max_months=120):
    monthly_interest_rate = interest_rate / 12 / 100
    debt_remaining = initial_debt
    monthly_debt_progress = []

    for month in range(max_months):
        if debt_remaining <= 0:
            break

        interest_for_month = debt_remaining * monthly_interest_rate
        debt_remaining = debt_remaining + interest_for_month - monthly_payment
        monthly_debt_progress.append(max(debt_remaining, 0))  # Ensure debt doesn't go below zero

    return monthly_debt_progress


if option == "Home":
    st.title("WealthPath Finder")
    st.subheader("Created by Rodney Graham")
    st.text("Welcome to WealthPath Finder")

    st.subheader("Learn the Basics of Financial Literacy")
    st.text("Watch this short video to understand some fundamental concepts of financial literacy. "
            "Video by NYU StudentLink")

    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        financial_literacy_video_url = 'https://youtu.be/swXHv0khiWY?si=oiZ7ItY5BSBm5jY2'
        st.video(financial_literacy_video_url)


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

    error_flag = False

    with colExpenses1:
        st.subheader("Monthly Rent")
        monthly_rent = st.number_input("Enter your monthly rent($): ", min_value=0.0, format='%f')
        if monthly_rent < 0:
            st.error("Monthly rent cannot be negative.")
            error_flag = True

        st.subheader("Monthly Utilities")
        monthly_utilities = st.number_input(
            "Enter your monthly expenses on utilities ($): ", min_value=0.0, format='%f')
        if monthly_utilities < 0:
            st.error("Monthly utilities cannot be negative.")
            error_flag = True

        st.subheader("Savings")
        monthly_savings = st.number_input(
            "Enter your monthly contributions towards savings: ", min_value=0.0, format='%f')
        if monthly_savings < 0:
            st.error("Monthly savings cannot be negative.")
            error_flag = True

        st.subheader("Monthly Bills")
        st.text("Include here one time bills such as, Car Insurance, Streaming subscriptions, etc")
        monthly_bills = st.number_input(
            "Enter the total that goes towards bills: ", min_value=0.0, format='%f')
        if monthly_bills < 0:
            st.error("Monthly bills cannot be negative.")
            error_flag = True

    with colExpenses2:

        st.subheader("Groceries")
        weekly_groceries = st.number_input(
            "Enter your weekly expenses on groceries: ", min_value=0.0, format='%f')
        weekly_groceries = weekly_groceries * 4
        if weekly_groceries < 0:
            st.error("Weekly groceries cannot be negative.")
            error_flag = True

        st.subheader("Entertainment")
        weekly_entertainment = st.number_input(
            "Enter your weekly expenses on entertainment: ", min_value=0.0, format='%f')
        weekly_entertainment = weekly_entertainment * 4
        if weekly_entertainment < 0:
            st.error("Weekly entertainment cannot be negative.")
            error_flag = True

        st.subheader("Transportation")
        weekly_transport = st.number_input(
            "Enter your weekly expenses on transportation: ", min_value=0.0, format='%f')
        if weekly_transport < 0:
            st.error("Weekly transport cannot be negative.")
            error_flag = True

        st.subheader("Buffer")
        weekly_buffer = st.number_input(
            "Enter a weekly buffer for unexpected expenses: ", min_value=0.0, format='%f')
        if weekly_buffer < 0:
            st.error("Weekly buffer cannot be negative.")
            error_flag = True

    if not error_flag:
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
    st.title("Investing")
    st.text("Explore Stocks, Index Funds, and ETFs for Investing")

    st.subheader("Learn the Importance of Investing!")

    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        importance_of_investing_video_url = 'https://youtu.be/x7msE3tx8QI?si=1y72OHGfLPGsSrfy'
        st.video(importance_of_investing_video_url)

    # Load API key and create TimeSeries object
    file = open("api_key.json")
    json_file = json.load(file)
    api_key = json_file["vantage_api"]
    ts = TimeSeries(key=api_key, output_format='pandas')

    ticker_symbol = st.text_input("Enter a Ticker Symbol (e.g., AAPL, MSFT, SPY):")

    if ticker_symbol:
        try:
            # Fetch data using Alpha Vantage
            data, meta_data = ts.get_daily(symbol=ticker_symbol, outputsize='compact')

            st.subheader(f"Displaying Stock Information for {ticker_symbol.upper()}")
            st.write(data.tail())  # Display the last few rows of the data

            # Plotting the stock's closing price using Plotly
            fig = px.line(data, y='4. close', title=f'Closing Prices for {ticker_symbol.upper()}')
            fig.update_xaxes(title_text='Date')
            fig.update_yaxes(title_text='Closing Price (USD)')
            st.plotly_chart(fig)

        except Exception as e:
            st.error(f"Failed to retrieve data for {ticker_symbol}: {e}")


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
        line_color = st.color_picker("Pick a Color for the Debt Line", '#00f900')  # Default color as an example

        if add_debt:
            error_flag = False

            # Input validation
            if initial_debt < 0:
                st.error("Initial debt amount cannot be negative.")
                error_flag = True
            if min_monthly_payment < 0:
                st.error("Minimum monthly payment cannot be negative.")
                error_flag = True
            if interest_rate < 0 or interest_rate > 100:
                st.error("Interest rate must be between 0% and 100%.")
                error_flag = True

            if not error_flag and debt_name:
                new_debt = {"Debt Name": debt_name, "Interest Rate": interest_rate,
                            "Minimum Monthly Payment": min_monthly_payment, "Loan Length": loan_length,
                            "Initial Debt": initial_debt, 'Line Color': line_color}
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

    if st.session_state.debts:
        st.subheader("Debt Repayment Progress Over Time")

        debt_progress_data = {}  # Dictionary to hold progress data for each debt
        debt_colors = {}

        for debt in st.session_state.debts:
            debt_name = debt["Debt Name"]
            initial_debt = debt["Initial Debt"]
            interest_rate = debt["Interest Rate"]
            monthly_payment = debt["Minimum Monthly Payment"]
            line_color = debt["Line Color"]

            monthly_progress = calculate_debt_over_time(initial_debt, interest_rate, monthly_payment)
            debt_progress_data[debt_name] = monthly_progress
            debt_colors[debt_name] = line_color

        # Plotting all debts on the same graph
        fig = go.Figure()
        for debt_name, progress in debt_progress_data.items():
            fig.add_trace(go.Scatter(
                x=list(range(1, len(progress) + 1)),
                y=progress,
                mode='lines',
                name=debt_name,
                line=dict(color=debt_colors[debt_name]),
                hovertemplate='Month: %{x}<br>Remaining Debt: $%{y:.2f}<extra></extra>'  # Custom hover label
            ))

        fig.update_layout(
            title="Debt Repayment Progress Over Time",
            xaxis_title="Month",
            yaxis_title="Remaining Debt ($)",
            legend_title="Debts"
        )

        st.plotly_chart(fig)

    st.header("Additional Payments to Pay Off Debts Faster")
    with st.form("extra_payment_form"):
        extra_payment = st.number_input("Enter Extra Monthly Payment Amount $", value=0.0, min_value=0.0)
        add_extra_payment = st.form_submit_button("Add Extra Payment")

        if add_extra_payment:
            if extra_payment > 0:
                st.session_state.total_debt -= extra_payment
                st.write(f"New Total Debt Amount After Extra Monthly Payments: ${st.session_state.total_debt:.2f}")

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
                st.write(f"It will take {total_time_to_pay_off} months to pay everything with the additional payments!")





