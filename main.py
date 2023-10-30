import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go


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
    colAnnualSal, colTax = st.columns(2)

    with colAnnualSal:
        salary = st.number_input("Enter your annual salary($): ", min_value=0.0, format='%f')
    with colTax:
        tax_rate = st.number_input("Enter your tax rate(%): ", min_value=0.0, format='%f')

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
        monthly_rent = st.number_input("Enter your monthly rent($): ", min_value=0.0, format='%f')

        st.subheader("Groceries")
        weekly_groceries = st.number_input("Enter your weekly expenses on groceries: ", min_value=0.0, format='%f')


elif option == "Investing":
    st.text("Here we are going to learn the basics about investing")

elif option == "Debt Management":
    st.text("Here we are going to learn the basics on debt management")