import streamlit as st
from datetime import datetime
from utils.db import init_db, add_expense, get_expenses, delete_expense
from utils.visuals import plot_category_pie, show_category_totals
import pandas as pd
import altair as alt


# --- Init ---
init_db()
st.set_page_config(page_title="House Expense Tracker", layout="wide")
st.title("🏠 House Budget Tracker")


# --- Form: Add Transaction ---
with st.form("add_transaction"):
    col1, col2 = st.columns(2)
    bank_name = col1.text_input("Bank Name")
    months = (
        pd.date_range("2025-01-01", periods=12, freq="MS").strftime("%Y-%m").tolist()
    )
    current_month = datetime.now().strftime("%Y-%m")
    month = col2.selectbox(
        "Month",
        months,
        index=months.index(current_month) if current_month in months else 0,
    )

    receiver = st.text_input("Receiver / Source")
    category = st.text_input("Category")
    amount = st.number_input("Amount (€)", format="%.2f")
    st.caption("💡 Use negative numbers for expenses, positive for income.")
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        add_expense(bank_name, month, receiver, category, amount)
        st.success("Transaction added!")
        st.rerun()


# --- Load data ---
df = get_expenses()
if df.empty:
    st.info("No transactions yet.")
    st.stop()


# --- Display Entries ---
st.subheader("📄 All Entries")

df["type"] = df["amount"].apply(lambda x: "Income" if x >= 0 else "Expense")

# Detect and mark transfers
df["transfer_key"] = df.apply(
    lambda r: frozenset([r["bank_name"], r["receiver"]]), axis=1
)
df["abs_amount"] = df["amount"].abs()
grouped = df.groupby(["transfer_key", "abs_amount"])

transfer_ids = set()
for _, group in grouped:
    if group["amount"].sum() == 0 and group["amount"].nunique() > 1:
        transfer_ids.update(group["id"].tolist())

df["type"] = df.apply(
    lambda row: (
        "Transfer"
        if row["id"] in transfer_ids
        else ("Income" if row["amount"] >= 0 else "Expense")
    ),
    axis=1,
)
df.drop(columns=["transfer_key", "abs_amount"], inplace=True)

df_without_transfer = df[df["type"] != "Transfer"].copy()

# Show entries
view_df = df_without_transfer.copy()
view_df["Amount (€)"] = view_df["amount"].map(lambda x: f"{x:.2f}")
st.dataframe(
    view_df[["id", "bank_name", "month", "receiver", "category", "Amount (€)", "type"]],
    use_container_width=True,
)

# --- Delete Entry ---
with st.expander("🗑 Delete Entry"):
    selected_id = st.selectbox("Select entry to delete (by ID)", df["id"])
    if st.button("Delete selected entry"):
        delete_expense(selected_id)
        st.success("Entry deleted.")
        st.rerun()


st.markdown("## 📅 Select a Month to Analyze")
available_months = sorted(df["month"].unique(), reverse=True)
available_months = pd.to_datetime(available_months).strftime("%Y-%m")

today = datetime.today()
first_of_this_month = today.replace(day=1)
prev_month = (first_of_this_month - pd.DateOffset(months=1)).strftime("%Y-%m")

default_index = (
    available_months.index(prev_month) if prev_month in available_months else 0
)

selected_month = st.selectbox(
    "",  # hide label since we added it manually
    options=available_months,
    index=default_index,
)
df_month = df[df["month"] == selected_month]
df_without_transfer = df_month[df_month["type"] != "Transfer"].copy()

# --- Summary ---
st.subheader("📋 Monthly Summary")
summary = (
    df_without_transfer.groupby(["month", "type"])["amount"].sum().unstack().fillna(0)
)
summary["Net"] = summary.get("Income", 0) + summary.get("Expense", 0)
# styled_summary = summary.style.applymap(highlight_net, subset=["Net"])
st.dataframe(summary)

st.subheader("📊 Monthly Income vs Expenses")
melted = (
    summary[["Income", "Expense", "Net"]]
    .reset_index()
    .melt(id_vars="month", var_name="type", value_name="Amount")
)

# Plot: grouped bars for each month
bar_chart = (
    alt.Chart(melted)
    .mark_bar()
    .encode(
        x=alt.X("month:N", title="Month", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("Amount:Q", title="Amount (€)"),
        color=alt.Color(
            "type:N",
            scale=alt.Scale(
                domain=["Income", "Net", "Expense"], range=["green", "blue", "red"]
            ),
        ),
        tooltip=["month", "type", "Amount"],
    )
    .properties(height=400)
)

st.altair_chart(bar_chart, use_container_width=True)


# --- Expense breakdown ---
expenses = df_without_transfer[df_without_transfer["amount"] < 0].copy()
incomes = df_without_transfer[df_without_transfer["amount"] > 0].copy()
expenses_with_savings = pd.concat(
    [
        expenses,
        pd.DataFrame(
            [
                {
                    "id": None,
                    "bank_name": "Generated",
                    "month": selected_month,
                    "receiver": "Myself",
                    "category": "Savings",
                    "amount": -summary["Net"].values[
                        0
                    ],  # Treat savings like an expense
                    "type": "Savings",
                }
            ]
        ),
    ],
    ignore_index=True,
)

if not expenses.empty:
    expenses["abs_amount"] = expenses["amount"].abs()
    st.subheader("📈 Expense Breakdown by Category (with Savings)")
    plot_category_pie(expenses_with_savings)
    show_category_totals(expenses_with_savings, title="Total Expenses by Category")
    show_category_totals(incomes, title="Total Income by Category")
