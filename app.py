import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import date

# Page setup
st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")
st.title("💰 Personal Expense Tracker & Analytics")

FILE_PATH = "expenses.csv"

# Data load ya nayi CSV file create karein
if os.path.exists(FILE_PATH):
    df = pd.read_csv(FILE_PATH)
else:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

# Left Sidebar: Naya Kharcha Add Karne Ka Form
st.sidebar.header("➕ add a new expense")
with st.sidebar.form("expense_form", clear_on_submit=True):
    exp_date = st.date_input("Date", date.today())
    category = st.selectbox(
        "Category", 
        ["Food & Dining", "Travel & Transport", "Shopping", "Bills & Utilities", "Entertainment", "Health", "Other"]
    )
    amount = st.number_input("Amount (₹)", min_value=1.0, step=10.0)
    desc = st.text_input("Description (e.g., Lunch, Metro, Recharge)")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_data = pd.DataFrame([[str(exp_date), category, amount, desc]], columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(FILE_PATH, index=False)
        st.sidebar.success("✅ Expense successfully added!")

# Main Dashboard Area
if not df.empty:
    # Top Metrics (Summary Cards)
    total_spent = df["Amount"].sum()
    highest_category = df.groupby("Category")["Amount"].sum().idxmax()
    total_transactions = len(df)

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Kharcha", f"₹{total_spent:,.2f}")
    m2.metric("Sabse Zyada Kharcha", highest_category)
    m3.metric("Total Transactions", total_transactions)

    st.divider()

    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Category ke Hisab se Kharcha")
        fig_pie = px.pie(df, values="Amount", names="Category", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("📈 Category-wise Comparison")
        cat_summary = df.groupby("Category")["Amount"].sum().reset_index()
        fig_bar = px.bar(cat_summary, x="Category", y="Amount", color="Category", text_auto=True)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # Recent Transactions Table & Download Option
    st.subheader("🧾 Recent Expenses")
    st.dataframe(df.iloc[::-1], use_container_width=True)

    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Report (CSV)",
        data=csv_data,
        file_name="my_expenses.csv",
        mime="text/csv"
    )
else:
    st.info("👈 Abhi koi data nahi hai. Left sidebar se apna pehla kharcha add karein!")