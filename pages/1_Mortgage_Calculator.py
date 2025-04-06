import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Mortgage Calculator", page_icon="🏠")

def calculate_monthly_payment(principal, annual_interest_rate, years):
    """
    Calculates the fixed monthly mortgage payment.

    Args:
        principal (float): The total loan amount.
        annual_interest_rate (float): The annual interest rate (as a percentage).
        years (int): The loan term in years.

    Returns:
        float: The calculated monthly payment. Returns principal / number_of_payments if interest rate is 0.
               Returns float('inf') or raises error if inputs are invalid (handled by st.number_input).
    """
    if annual_interest_rate == 0:
        if years > 0:
            return principal / (years * 12)
        else:
            return float('inf')

    monthly_interest_rate = (annual_interest_rate / 100) / 12
    number_of_payments = years * 12

    try:
        monthly_payment = (
            principal
            * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
            / ((1 + monthly_interest_rate) ** number_of_payments - 1)
        )
        return monthly_payment
    except OverflowError:
        st.error("Calculation resulted in an overflow. Please check your input values.")
        return float('inf')
    except ZeroDivisionError:
        st.error("Calculation resulted in division by zero. This might happen with invalid inputs.")
        return float('inf')

st.title("🏠 Mortgage Repayments Calculator")
st.write("Enter your loan details to calculate monthly payments and see the amortization schedule.")

st.divider()

st.write("### Input Loan Details")
col1, col2 = st.columns(2)

with col1:
    home_value = st.number_input("Home Value (₹)", min_value=0, value=10000000, step=50000, help="Total value of the property.")
    deposit = st.number_input("Deposit (₹)", min_value=0, value=1000000, step=10000, help="Amount paid upfront.")

with col2:
    interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=5.50, step=0.05, format="%.2f", help="Annual interest rate.")
    loan_term = st.number_input("Loan Term (years)", min_value=1, max_value=50, value=30, step=1, help="Duration of the loan in years.")

st.divider()

loan_amount = home_value - deposit

if loan_amount < 0:
    st.error("Deposit cannot be greater than the Home Value.")
    st.stop()

monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)

if monthly_payment != float('inf') and loan_amount > 0:

    number_of_payments = loan_term * 12
    total_payments = monthly_payment * number_of_payments
    total_interest = total_payments - loan_amount

    st.write("### Summary of Repayments")
    res_col1, res_col2, res_col3 = st.columns(3)

    with res_col1:
        st.metric(label="Monthly Payment", value=f"₹{monthly_payment:,.2f}")
    with res_col2:
        st.metric(label="Total Payments", value=f"₹{total_payments:,.2f}")
    with res_col3:
        st.metric(label="Total Interest Paid", value=f"₹{total_interest:,.2f}")

    st.divider()

    st.write("### Amortization Schedule")

    schedule = []
    remaining_balance = loan_amount
    monthly_interest_rate_calc = (interest_rate / 100) / 12

    for i in range(1, number_of_payments + 1):
        interest_payment = remaining_balance * monthly_interest_rate_calc
        principal_payment = monthly_payment - interest_payment

        # Ensure principal payment doesn't exceed remaining balance (can happen in the last month due to rounding)
        if principal_payment > remaining_balance:
            principal_payment = remaining_balance
            # Adjust final month's payment if necessary due to rounding
            monthly_payment_adj = interest_payment + principal_payment
        else:
            monthly_payment_adj = monthly_payment

        remaining_balance -= principal_payment

        # Ensure remaining balance doesn't go below zero due to floating point inaccuracies
        if remaining_balance < 0:
            remaining_balance = 0

        year = math.ceil(i / 12)

        schedule.append(
            {
                "Month": i,
                "Year": year,
                "Payment": monthly_payment_adj, # Use adjusted payment for final month if needed
                "Principal Paid": principal_payment,
                "Interest Paid": interest_payment,
                "Remaining Balance": remaining_balance,
            }
        )

    schedule_df = pd.DataFrame(schedule)

    with st.expander("View Full Payment Schedule Table"):
        st.dataframe(schedule_df.style.format({
            "Payment": "₹{:,.2f}",
            "Principal Paid": "₹{:,.2f}",
            "Interest Paid": "₹{:,.2f}",
            "Remaining Balance": "₹{:,.2f}",
        }))

    st.write("### Remaining Loan Balance Over Time")

    # Group by year and take the minimum remaining balance for that year (end-of-year balance)
    balance_over_time_df = schedule_df[["Year", "Remaining Balance"]].groupby("Year").min().reset_index()

    st.line_chart(balance_over_time_df, x="Year", y="Remaining Balance")

elif loan_amount <= 0:
    st.info("Loan Amount is zero or negative. Please adjust Home Value and Deposit.")
