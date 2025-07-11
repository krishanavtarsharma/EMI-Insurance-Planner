import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Page Setup ---
st.set_page_config(page_title="💼 EMI & Insurance Planner", layout="centered")

# --- CSS ---
st.markdown("""
    <style>
        .main-title { text-align: center; font-size: 40px; color: #2874A6; font-weight: bold; }
        .sub-title { text-align: center; font-size: 20px; color: #555; }
        .result-box {
            background-color: #D6EAF8; padding: 20px; border-radius: 10px;
            text-align: center; font-size: 24px; color: #154360; border: 2px solid #AED6F1; margin-top: 20px;
        }
        .safe-box {
            padding: 10px; border-radius: 8px; margin-top: 10px;
            text-align: center; font-size: 20px; font-weight: bold;
        }
        .safe { background-color: #D5F5E3; color: #1E8449; border: 2px solid #ABEBC6; }
        .risky { background-color: #FADBD8; color: #C0392B; border: 2px solid #F5B7B1; }
        .footer { text-align: center; color: #999; margin-top: 50px; }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="main-title">💼 EMI & Insurance Planner</div>', unsafe_allow_html=True)

# --- User Choice ---
st.sidebar.header("🔘 Choose Your Tool")
mode = st.sidebar.radio("What would you like to use?", ["Loan EMI Calculator", "Insurance Planner"])

# ------------------------------------------------------------------------
# 1️⃣ Loan EMI Calculator
# ------------------------------------------------------------------------
if mode == "Loan EMI Calculator":

    st.markdown('<div class="sub-title">🏦 Smart Loan EMI Analysis</div>', unsafe_allow_html=True)

    loan_type = st.sidebar.selectbox("Loan Type", ["Home Loan", "Car Loan", "Personal Loan"])
    default_interest = {"Home Loan": 8.5, "Car Loan": 9.5, "Personal Loan": 12.5}
    interest_rate = default_interest[loan_type]

    loan_amount = st.sidebar.number_input("Loan Amount (₹)", min_value=10000, max_value=10000000, value=500000, step=1000)
    user_rate = st.sidebar.number_input("Annual Interest Rate (%)", min_value=1.0, max_value=25.0, value=interest_rate, step=0.1)
    tenure_years = st.sidebar.slider("Loan Tenure (Years)", 1, 30, 5)
    monthly_income = st.sidebar.number_input("Monthly Income (₹)", min_value=5000, max_value=1000000, value=40000, step=1000)

    tenure_months = tenure_years * 12
    monthly_interest = user_rate / (12 * 100)

    try:
        emi = loan_amount * monthly_interest * (1 + monthly_interest) ** tenure_months
        emi /= ((1 + monthly_interest) ** tenure_months - 1)
        emi = np.round(emi, 2)
    except ZeroDivisionError:
        emi = 0.0

    emi_ratio = emi / monthly_income
    safe = emi_ratio < 0.4

    # Display EMI
    st.markdown(f"""<div class="result-box">💰 Monthly EMI for <strong>{loan_type}</strong>: <strong>₹{emi:,.2f}</strong></div>""", unsafe_allow_html=True)

    # Risk Suggestion
    if safe:
        st.markdown('<div class="safe-box safe">✅ EMI is Affordable. Loan likely to be approved.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="safe-box risky">⚠ EMI is High Compared to Income. Risk of Rejection.</div>', unsafe_allow_html=True)

    # Loan Type Suggestion
    st.subheader("📊 Loan Suggestion Based on Your EMI")
    if emi < 5000:
        st.success("✔ You can easily go for **Personal Loan or Used Car Loan**.")
    elif emi < 15000:
        st.info("ℹ You may consider a **New Car Loan or Home Renovation Loan**.")
    else:
        st.warning("💡 Based on EMI, a **Home Loan** is most suitable for this amount.")

    # Amortization Table
    st.subheader("📆 EMI Amortization Table")
    balance = loan_amount
    amort_data = []
    for i in range(1, tenure_months + 1):
        interest = balance * monthly_interest
        principal = emi - interest
        balance -= principal
        amort_data.append([i, emi, round(principal, 2), round(interest, 2), max(round(balance, 2), 0)])
    df_amort = pd.DataFrame(amort_data, columns=["Month", "EMI", "Principal", "Interest", "Balance"])
    st.dataframe(df_amort.style.format({"EMI": "₹{:.2f}", "Principal": "₹{:.2f}", "Interest": "₹{:.2f}", "Balance": "₹{:.2f}"}), use_container_width=True)

    # EMI Chart
    st.subheader("📉 EMI Breakdown Over Time")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df_amort["Month"], df_amort["Principal"], label="Principal Paid", color="#28B463")
    ax.plot(df_amort["Month"], df_amort["Interest"], label="Interest Paid", color="#E74C3C")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount (₹)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# ------------------------------------------------------------------------
# 2️⃣ Insurance Planner
# ------------------------------------------------------------------------
elif mode == "Insurance Planner":

    st.markdown('<div class="sub-title">🛡️ Smart Insurance Estimator</div>', unsafe_allow_html=True)

    # Insurance Input
    insurance_type = st.selectbox("Insurance Type", ["Health Insurance", "Life Insurance", "Vehicle Insurance"])
    age = st.number_input("Enter Your Age", min_value=18, max_value=100, value=30)
    sum_insured = st.number_input("Sum Insured (₹)", min_value=100000, max_value=10000000, value=500000, step=100000)
    tenure = st.slider("Policy Tenure (Years)", 1, 30, 10)
    smoker = st.radio("Are you a smoker?", ["No", "Yes"])
    critical_illness = st.checkbox("Add Critical Illness Cover")

    # Premium Estimation Logic
    base_rate = 0.0008 if insurance_type == "Life Insurance" else 0.0012
    risk_factor = 1.5 if smoker == "Yes" else 1.0
    illness_factor = 1.2 if critical_illness else 1.0
    age_factor = 1.0 + ((age - 30) * 0.02) if age > 30 else 1.0

    annual_premium = sum_insured * base_rate * risk_factor * illness_factor * age_factor
    total_premium = annual_premium * tenure

    st.subheader("📋 Estimated Insurance Details")
    st.success(f"📌 Annual Premium: ₹{annual_premium:,.2f}")
    st.info(f"💰 Total Cost over {tenure} years: ₹{total_premium:,.2f}")

    # Insurance Tips
    if insurance_type == "Health Insurance" and age > 45:
        st.warning("🩺 Tip: Consider a plan with pre-existing disease coverage.")
    elif insurance_type == "Vehicle Insurance":
        st.info("🚗 Tip: Don't forget to include zero-depreciation add-on for new vehicles.")

# --- Footer ---
st.markdown('<div class="footer">Made with ❤ using Streamlit | EMI & Insurance Planner</div>', unsafe_allow_html=True)
