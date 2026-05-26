import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India Energy Sources Dashboard",
    page_icon="⚡",
    layout="wide",
)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

import os
CSV_PATH = "CAPSTONE_PROJECT.csv"

if os.path.exists(CSV_PATH):
    df = load_data(CSV_PATH)
else:
    st.warning("📂 CSV file not found. Please upload your `CAPSTONE_PROJECT.csv` below.")
    uploaded_file = st.file_uploader("Upload CAPSTONE_PROJECT.csv", type=["csv"])
    if uploaded_file is None:
        st.stop()
    df = load_data(uploaded_file)

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.title("🔍 Filters")

energy_types = st.sidebar.multiselect(
    "Energy Type",
    options=df["Energy Type"].unique().tolist(),
    default=df["Energy Type"].unique().tolist(),
)

energy_sources = st.sidebar.multiselect(
    "Energy Source",
    options=df["Energy Source"].unique().tolist(),
    default=df["Energy Source"].unique().tolist(),
)

filtered_df = df[
    df["Energy Type"].isin(energy_types) & df["Energy Source"].isin(energy_sources)
]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("⚡ India Energy Sources Dashboard")
st.markdown("Comparative analysis of **Renewable vs Non-Renewable** energy sources in India.")

# ── KPI Cards ─────────────────────────────────────────────────────────────────
st.subheader("📊 Key Metrics (Filtered Data)")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(filtered_df))
col2.metric(
    "Avg Installation Cost (INR/kW)",
    f"₹{filtered_df['Installation Cost (INR per kW)'].mean():,.0f}",
)
col3.metric(
    "Avg CO₂ Emission (kg/kWh)",
    f"{filtered_df['CO2 Emission (kg per kWh)'].mean():.3f}",
)
col4.metric(
    "Avg Generation Cost (INR/unit)",
    f"₹{filtered_df['Generation Cost (INR per unit)'].mean():.2f}",
)

st.divider()

# ── Charts ────────────────────────────────────────────────────────────────────
row1_col1, row1_col2 = st.columns(2)

# 1. Average CO2 Emission by Energy Source
with row1_col1:
    st.subheader("🌿 Avg CO₂ Emission by Energy Source")
    co2_data = (
        filtered_df.groupby("Energy Source")["CO2 Emission (kg per kWh)"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ["#d62728" if src == "Fossil Fuel" else "#2ca02c" for src in co2_data["Energy Source"]]
    ax.barh(co2_data["Energy Source"], co2_data["CO2 Emission (kg per kWh)"], color=colors)
    ax.set_xlabel("CO₂ Emission (kg per kWh)")
    ax.set_title("CO₂ Emission by Energy Source")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# 2. Average Installation Cost by Energy Source
with row1_col2:
    st.subheader("💰 Avg Installation Cost by Energy Source")
    cost_data = (
        filtered_df.groupby("Energy Source")["Installation Cost (INR per kW)"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(cost_data["Energy Source"], cost_data["Installation Cost (INR per kW)"],
            color=sns.color_palette("Blues_r", len(cost_data)))
    ax.set_xlabel("Installation Cost (INR per kW)")
    ax.set_title("Installation Cost by Energy Source")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

row2_col1, row2_col2 = st.columns(2)

# 3. Percentage of Generation in India (Pie Chart)
with row2_col1:
    st.subheader("🇮🇳 % of Electricity Generation in India")
    gen_data = (
        filtered_df.groupby("Energy Source")["Percentage of Generation (India)"]
        .mean()
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(
        gen_data["Percentage of Generation (India)"],
        labels=gen_data["Energy Source"],
        autopct="%1.1f%%",
        startangle=140,
        colors=sns.color_palette("tab10", len(gen_data)),
    )
    ax.set_title("Share of Electricity Generation")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# 4. Generation Cost vs Selling Price
with row2_col2:
    st.subheader("📈 Generation Cost vs Selling Price")
    avg_costs = (
        filtered_df.groupby("Energy Source")[
            ["Generation Cost (INR per unit)", "Selling Price per Unit (INR)"]
        ]
        .mean()
        .reset_index()
    )
    x = np.arange(len(avg_costs))
    width = 0.35
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(x - width / 2, avg_costs["Generation Cost (INR per unit)"], width, label="Gen Cost", color="#1f77b4")
    ax.bar(x + width / 2, avg_costs["Selling Price per Unit (INR)"], width, label="Selling Price", color="#ff7f0e")
    ax.set_xticks(x)
    ax.set_xticklabels(avg_costs["Energy Source"], rotation=30, ha="right")
    ax.set_ylabel("INR per Unit")
    ax.set_title("Generation Cost vs Selling Price")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.divider()

# 5. Correlation Heatmap
st.subheader("🔗 Correlation Heatmap (Numeric Features)")
numeric_cols = filtered_df.select_dtypes(include=np.number).columns.tolist()
corr = filtered_df[numeric_cols].corr()
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax, linewidths=0.5)
ax.set_title("Correlation Between Numeric Features")
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.divider()

# ── Summary Table ─────────────────────────────────────────────────────────────
st.subheader("📋 Aggregated Summary by Energy Source")
summary = (
    filtered_df.groupby(["Energy Source", "Energy Type"])
    .agg(
        Count=("Energy Source", "count"),
        Avg_Installation_Cost=("Installation Cost (INR per kW)", "mean"),
        Avg_Generation_Cost=("Generation Cost (INR per unit)", "mean"),
        Avg_CO2=("CO2 Emission (kg per kWh)", "mean"),
        Avg_Selling_Price=("Selling Price per Unit (INR)", "mean"),
        Avg_Generation_pct=("Percentage of Generation (India)", "mean"),
    )
    .reset_index()
    .round(2)
)
st.dataframe(summary, use_container_width=True)

# ── Raw Data Viewer ───────────────────────────────────────────────────────────
with st.expander("🗂️ View Raw Data"):
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

st.caption("Data: CAPSTONE_PROJECT.csv | Dashboard built with Streamlit")
