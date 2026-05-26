import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
import os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="A Comparative Analysis of Energy Sources for Sustainable Growth in India",
    page_icon="⚡",
    layout="wide",
)

# ── Custom CSS for professional buttons & styling ─────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Hero header ── */
.hero {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
    color: white;
}
.hero h1 {
    font-size: 1.9rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    line-height: 1.3;
}
.hero p {
    font-size: 1rem;
    opacity: 0.82;
    margin: 0;
}

/* ── Nav button bar ── */
.nav-bar {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}
.nav-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 0.88rem;
    font-weight: 600;
    cursor: pointer;
    border: none;
    text-decoration: none;
    transition: all 0.2s ease;
    letter-spacing: 0.3px;
}
.nav-btn-primary {
    background: linear-gradient(135deg, #1a73e8, #0d47a1);
    color: white !important;
    box-shadow: 0 3px 10px rgba(26,115,232,0.35);
}
.nav-btn-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(26,115,232,0.45); }

.nav-btn-success {
    background: linear-gradient(135deg, #2e7d32, #1b5e20);
    color: white !important;
    box-shadow: 0 3px 10px rgba(46,125,50,0.35);
}
.nav-btn-success:hover { transform: translateY(-2px); }

.nav-btn-warning {
    background: linear-gradient(135deg, #f57c00, #e65100);
    color: white !important;
    box-shadow: 0 3px 10px rgba(245,124,0,0.35);
}
.nav-btn-warning:hover { transform: translateY(-2px); }

.nav-btn-info {
    background: linear-gradient(135deg, #00838f, #006064);
    color: white !important;
    box-shadow: 0 3px 10px rgba(0,131,143,0.35);
}
.nav-btn-info:hover { transform: translateY(-2px); }

.nav-btn-purple {
    background: linear-gradient(135deg, #6a1b9a, #4a148c);
    color: white !important;
    box-shadow: 0 3px 10px rgba(106,27,154,0.35);
}
.nav-btn-purple:hover { transform: translateY(-2px); }

/* ── Section card ── */
.section-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}

/* ── KPI metric override ── */
[data-testid="metric-container"] {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* ── Download button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #1a73e8, #0d47a1) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 22px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    box-shadow: 0 3px 10px rgba(26,115,232,0.35) !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(26,115,232,0.45) !important;
}

/* ── Streamlit default button ── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 10px 22px !important;
    transition: all 0.2s ease !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f2027 !important;
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stMultiSelect label {
    color: #cbd5e0 !important;
    font-weight: 600;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 0.8rem;
    padding: 1.5rem 0 0.5rem 0;
    border-top: 1px solid #e2e8f0;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

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
st.sidebar.markdown("## ⚡ Dashboard Controls")
st.sidebar.markdown("---")

energy_types = st.sidebar.multiselect(
    "🔋 Energy Type",
    options=df["Energy Type"].unique().tolist(),
    default=df["Energy Type"].unique().tolist(),
)
energy_sources = st.sidebar.multiselect(
    "🌱 Energy Source",
    options=df["Energy Source"].unique().tolist(),
    default=df["Energy Source"].unique().tolist(),
)

filtered_df = df[
    df["Energy Type"].isin(energy_types) & df["Energy Source"].isin(energy_sources)
]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**{len(filtered_df)}** records selected")

# Reset filters button
if st.sidebar.button("🔄 Reset Filters"):
    st.rerun()


# ── Hero Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>⚡ A Comparative Analysis of Energy Sources<br>for Sustainable Growth in India</h1>
    <p>Exploring Renewable vs Non-Renewable energy — Cost, Emissions, Employment & Sustainability</p>
</div>
""", unsafe_allow_html=True)


# ── Navigation Buttons ────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
    <a class="nav-btn nav-btn-primary" href="#key-metrics">📊 Key Metrics</a>
    <a class="nav-btn nav-btn-success" href="#emissions-cost">🌿 Emissions & Cost</a>
    <a class="nav-btn nav-btn-warning" href="#generation-analysis">⚡ Generation Analysis</a>
    <a class="nav-btn nav-btn-info" href="#correlation">🔗 Correlation</a>
    <a class="nav-btn nav-btn-purple" href="#data-table">📋 Data Table</a>
</div>
""", unsafe_allow_html=True)


# ── KPI Cards ─────────────────────────────────────────────────────────────────
st.markdown('<a name="key-metrics"></a>', unsafe_allow_html=True)
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🗂️ Total Records", len(filtered_df))
col2.metric("💰 Avg Installation Cost",
            f"₹{filtered_df['Installation Cost (INR per kW)'].mean():,.0f} /kW")
col3.metric("🌫️ Avg CO₂ Emission",
            f"{filtered_df['CO2 Emission (kg per kWh)'].mean():.3f} kg/kWh")
col4.metric("⚙️ Avg Generation Cost",
            f"₹{filtered_df['Generation Cost (INR per unit)'].mean():.2f} /unit")

st.divider()


# ── Charts Row 1 ─────────────────────────────────────────────────────────────
st.markdown('<a name="emissions-cost"></a>', unsafe_allow_html=True)
st.subheader("🌿 Emissions & Installation Cost")
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    co2_data = (filtered_df.groupby("Energy Source")["CO2 Emission (kg per kWh)"]
                .mean().sort_values(ascending=False).reset_index())
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ["#d62728" if s == "Fossil Fuel" else "#2ca02c" for s in co2_data["Energy Source"]]
    ax.barh(co2_data["Energy Source"], co2_data["CO2 Emission (kg per kWh)"], color=colors)
    ax.set_xlabel("CO₂ Emission (kg per kWh)")
    ax.set_title("Avg CO₂ Emission by Energy Source")
    plt.tight_layout()
    st.pyplot(fig); plt.close()

with row1_col2:
    cost_data = (filtered_df.groupby("Energy Source")["Installation Cost (INR per kW)"]
                 .mean().sort_values(ascending=False).reset_index())
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(cost_data["Energy Source"], cost_data["Installation Cost (INR per kW)"],
            color=sns.color_palette("Blues_r", len(cost_data)))
    ax.set_xlabel("Installation Cost (INR per kW)")
    ax.set_title("Avg Installation Cost by Energy Source")
    plt.tight_layout()
    st.pyplot(fig); plt.close()

st.divider()

# ── Charts Row 2 ─────────────────────────────────────────────────────────────
st.markdown('<a name="generation-analysis"></a>', unsafe_allow_html=True)
st.subheader("⚡ Generation & Pricing Analysis")
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    gen_data = (filtered_df.groupby("Energy Source")["Percentage of Generation (India)"]
                .mean().reset_index())
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(gen_data["Percentage of Generation (India)"],
           labels=gen_data["Energy Source"], autopct="%1.1f%%", startangle=140,
           colors=sns.color_palette("tab10", len(gen_data)))
    ax.set_title("🇮🇳 Share of Electricity Generation in India")
    plt.tight_layout()
    st.pyplot(fig); plt.close()

with row2_col2:
    avg_costs = (filtered_df.groupby("Energy Source")[
        ["Generation Cost (INR per unit)", "Selling Price per Unit (INR)"]].mean().reset_index())
    x = np.arange(len(avg_costs)); width = 0.35
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(x - width/2, avg_costs["Generation Cost (INR per unit)"],
           width, label="Gen Cost", color="#1f77b4")
    ax.bar(x + width/2, avg_costs["Selling Price per Unit (INR)"],
           width, label="Selling Price", color="#ff7f0e")
    ax.set_xticks(x)
    ax.set_xticklabels(avg_costs["Energy Source"], rotation=30, ha="right")
    ax.set_ylabel("INR per Unit")
    ax.set_title("Generation Cost vs Selling Price")
    ax.legend(); plt.tight_layout()
    st.pyplot(fig); plt.close()

st.divider()

# ── Correlation Heatmap ───────────────────────────────────────────────────────
st.markdown('<a name="correlation"></a>', unsafe_allow_html=True)
st.subheader("🔗 Correlation Heatmap")
numeric_cols = filtered_df.select_dtypes(include=np.number).columns.tolist()
corr = filtered_df[numeric_cols].corr()
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax, linewidths=0.5)
ax.set_title("Correlation Between Numeric Features")
plt.tight_layout()
st.pyplot(fig); plt.close()

st.divider()

# ── Summary Table + Download ──────────────────────────────────────────────────
st.markdown('<a name="data-table"></a>', unsafe_allow_html=True)
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
    ).reset_index().round(2)
)
st.dataframe(summary, use_container_width=True)

# Download buttons row
dl_col1, dl_col2, dl_col3 = st.columns([1, 1, 4])

with dl_col1:
    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered CSV",
        data=csv_bytes,
        file_name="filtered_energy_data.csv",
        mime="text/csv",
    )

with dl_col2:
    summary_csv = summary.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Summary CSV",
        data=summary_csv,
        file_name="energy_summary.csv",
        mime="text/csv",
    )

st.divider()

# ── Raw Data Expander ─────────────────────────────────────────────────────────
with st.expander("🗂️ View Full Raw Data"):
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ⚡ A Comparative Analysis of Energy Sources for Sustainable Growth in India &nbsp;|&nbsp;
    Built with Streamlit &nbsp;|&nbsp; Data: CAPSTONE_PROJECT.csv
</div>
""", unsafe_allow_html=True)
