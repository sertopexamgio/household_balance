import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt


def highlight_net(val):
    color = "green" if val >= 0 else "red"
    return f"color: {color}"


def plot_category_pie(expenses_df, threshold_cut=0.01):
    expenses_df["abs_amount"] = expenses_df["amount"].abs()

    cat_sum = expenses_df.groupby("category")["abs_amount"].sum()
    total = cat_sum.sum()

    threshold = threshold_cut * total
    major_cats = cat_sum[cat_sum >= threshold]
    other_sum = cat_sum[cat_sum < threshold].sum()

    if other_sum > 0:
        major_cats["Other"] = other_sum

    sort_major_cats = major_cats.sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(6, 6))
    explode = [threshold_cut] * len(major_cats)

    wedges, texts, autotexts = ax.pie(
        sort_major_cats,
        autopct="%1.1f%%",
        startangle=140,
        explode=explode,
        textprops={"color": "w"},
    )
    ax.axis("equal")
    ax.legend(
        wedges,
        sort_major_cats.index,
        title="Category",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )
    st.pyplot(fig)


def show_category_totals(df, title="Total by Category"):
    df = df.copy()
    df["abs_amount"] = df["amount"].abs()

    category_totals = (
        df.groupby("category")["abs_amount"]
        .sum()
        .reset_index()
        .sort_values("abs_amount", ascending=False)
    )

    if category_totals.empty:
        st.info("No data to display.")
        return

    st.markdown(f"### 📊 {title}")

    chart = (
        alt.Chart(category_totals)
        .mark_bar()
        .encode(
            x=alt.X("category:N", sort="-y", title="Category"),
            y=alt.Y("abs_amount:Q", title="Total (€)"),
            color=alt.Color("category:N", legend=None),
            tooltip=["category", "abs_amount"],
        )
        .properties(height=400)
    )

    st.altair_chart(chart, use_container_width=True)
