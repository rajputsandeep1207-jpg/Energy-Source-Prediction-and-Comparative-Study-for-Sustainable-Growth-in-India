import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="A Comparative Analysis of Energy Sources for Sustainable Growth in India",
    page_icon="⚡",
    layout="wide",
)

# ── Dark Theme CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0e0e0e !important;
    color: #e2e8f0 !important;
}

/* ── App background ── */
.stApp {
    background-color: #0e0e0e !important;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
    border: 1px solid #2d2d2d;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 0;
    text-align: center;
    color: white;
}
.hero h1 {
    font-size: 1.9rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    line-height: 1.3;
    color: #e2e8f0;
}
.hero p { font-size: 1rem; opacity: 0.75; margin: 0; color: #a0aec0; }

/* ── Tab bar ── */
.tab-bar {
    display: flex;
    gap: 0;
    flex-wrap: nowrap;
    margin-bottom: 1.8rem;
    border-bottom: 3px solid #4f8ef7;
    overflow-x: auto;
}
.tab-btn {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 12px 22px;
    font-size: 0.88rem;
    font-weight: 600;
    cursor: pointer;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    text-decoration: none !important;
    transition: all 0.18s ease;
    letter-spacing: 0.2px;
    white-space: nowrap;
    background: #1a1a1a;
    color: #94a3b8 !important;
    border: 1px solid #2d2d2d;
    border-bottom: 3px solid transparent;
    margin-bottom: -3px;
}
.tab-btn:hover {
    background: #1e2a3a;
    color: #4f8ef7 !important;
    border-bottom: 3px solid #4f8ef7;
}
.tab-btn.active {
    background: #111827;
    color: #4f8ef7 !important;
    border-bottom: 3px solid #4f8ef7;
    box-shadow: 0 -2px 8px rgba(79,142,247,0.15);
}

/* ── KPI cards ── */
[data-testid="metric-container"] {
    background: #1a1a1a !important;
    border: 1px solid #2d2d2d !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.4) !important;
}
[data-testid="metric-container"] label,
[data-testid="metric-container"] div {
    color: #e2e8f0 !important;
}

/* ── Dataframe ── */
.stDataFrame { background: #1a1a1a !important; border-radius: 10px; }

/* ── Divider ── */
hr { border-color: #2d2d2d !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #1a1a1a !important;
    color: #e2e8f0 !important;
    border: 1px solid #2d2d2d !important;
    border-radius: 8px !important;
}

/* ── Download buttons ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #4f8ef7, #1a56db) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 22px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    box-shadow: 0 3px 10px rgba(79,142,247,0.3) !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(79,142,247,0.5) !important;
}

/* ── Streamlit tab buttons ── */
.stButton > button {
    background: #1a1a1a !important;
    color: #94a3b8 !important;
    border: 1px solid #2d2d2d !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stButton > button:hover {
    background: #1e2a3a !important;
    color: #4f8ef7 !important;
    border-color: #4f8ef7 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: #111111 !important; border-right: 1px solid #2d2d2d; }
[data-testid="stSidebar"] * { color: #cbd5e0 !important; }
[data-testid="stSidebar"] .stButton > button {
    background: #1e2a3a !important;
    border-color: #4f8ef7 !important;
    color: #4f8ef7 !important;
}

/* ── Subheaders ── */
h2, h3 { color: #e2e8f0 !important; }

/* ── Footer ── */
.footer {
    text-align: center;
    color: #4a5568;
    font-size: 0.8rem;
    padding: 1.5rem 0 0.5rem 0;
    border-top: 1px solid #2d2d2d;
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


# ── Sidebar ───────────────────────────────────────────────────────────────────
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
filtered_df = df[df["Energy Type"].isin(energy_types) & df["Energy Source"].isin(energy_sources)]
st.sidebar.markdown("---")
st.sidebar.markdown(f"**{len(filtered_df)}** records selected")
if st.sidebar.button("🔄 Reset Filters"):
    st.rerun()


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>⚡ A Comparative Analysis of Energy Sources<br>for Sustainable Growth in India</h1>
    <p>Exploring Renewable vs Non-Renewable energy — Cost, Emissions, Employment & Sustainability</p>
</div>
""", unsafe_allow_html=True)


# ── Tab Navigation ────────────────────────────────────────────────────────────
TABS = {
    "📊 Key Metrics":         "key-metrics",
    "🌿 Emissions & Cost":    "emissions-cost",
    "⚡ Generation Analysis": "generation-analysis",
    "🔗 Correlation":         "correlation",
    "📋 Data Table":          "data-table",
}

if "active_tab" not in st.session_state:
    st.session_state.active_tab = list(TABS.keys())[0]

tab_html = '<div class="tab-bar">'
for label in TABS:
    active_class = "active" if st.session_state.active_tab == label else ""
    tab_html += f'<a class="tab-btn {active_class}" href="#{TABS[label]}">{label}</a>'
tab_html += "</div>"
st.markdown(tab_html, unsafe_allow_html=True)

tab_cols = st.columns(len(TABS))
for i, label in enumerate(TABS):
    with tab_cols[i]:
        if st.button(label, key=f"tab_{i}", use_container_width=True):
            st.session_state.active_tab = label
            st.rerun()


# ── Dark matplotlib style ─────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#1a1a1a",
    "axes.facecolor":    "#1a1a1a",
    "axes.edgecolor":    "#3d3d3d",
    "axes.labelcolor":   "#e2e8f0",
    "xtick.color":       "#94a3b8",
    "ytick.color":       "#94a3b8",
    "text.color":        "#e2e8f0",
    "grid.color":        "#2d2d2d",
    "legend.facecolor":  "#1a1a1a",
    "legend.edgecolor":  "#3d3d3d",
})


# ── Section: Key Metrics ──────────────────────────────────────────────────────
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


# ── Section: Emissions & Cost ─────────────────────────────────────────────────
st.markdown('<a name="emissions-cost"></a>', unsafe_allow_html=True)
st.subheader("🌿 Emissions & Installation Cost")
r1c1, r1c2 = st.columns(2)

with r1c1:
    co2_data = (filtered_df.groupby("Energy Source")["CO2 Emission (kg per kWh)"]
                .mean().sort_values(ascending=False).reset_index())
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ["#ef4444" if s == "Fossil Fuel" else "#22c55e" for s in co2_data["Energy Source"]]
    ax.barh(co2_data["Energy Source"], co2_data["CO2 Emission (kg per kWh)"], color=colors)
    ax.set_xlabel("CO₂ Emission (kg per kWh)")
    ax.set_title("Avg CO₂ Emission by Energy Source")
    plt.tight_layout(); st.pyplot(fig); plt.close()

with r1c2:
    cost_data = (filtered_df.groupby("Energy Source")["Installation Cost (INR per kW)"]
                 .mean().sort_values(ascending=False).reset_index())
    fig, ax = plt.subplots(figsize=(7, 4))
    blues = ["#1e3a5f", "#1e4976", "#1a5f9e", "#1a73c4", "#2186e0", "#4f9ef8", "#74b3fc", "#a8d0ff"]
    ax.barh(cost_data["Energy Source"], cost_data["Installation Cost (INR per kW)"],
            color=blues[:len(cost_data)])
    ax.set_xlabel("Installation Cost (INR per kW)")
    ax.set_title("Avg Installation Cost by Energy Source")
    plt.tight_layout(); st.pyplot(fig); plt.close()

st.divider()


# ── Section: Generation Analysis ──────────────────────────────────────────────
st.markdown('<a name="generation-analysis"></a>', unsafe_allow_html=True)
st.subheader("⚡ Generation & Pricing Analysis")
r2c1, r2c2 = st.columns(2)

with r2c1:
    gen_data = (filtered_df.groupby("Energy Source")["Percentage of Generation (India)"]
                .mean().reset_index())
    fig, ax = plt.subplots(figsize=(6, 5))
    dark_palette = ["#4f8ef7","#22c55e","#f59e0b","#ef4444","#a855f7","#14b8a6","#f97316","#ec4899"]
    ax.pie(gen_data["Percentage of Generation (India)"],
           labels=gen_data["Energy Source"], autopct="%1.1f%%", startangle=140,
           colors=dark_palette[:len(gen_data)],
           textprops={"color": "#e2e8f0"})
    ax.set_title("🇮🇳 Share of Electricity Generation in India")
    plt.tight_layout(); st.pyplot(fig); plt.close()

with r2c2:
    avg_costs = (filtered_df.groupby("Energy Source")[
        ["Generation Cost (INR per unit)", "Selling Price per Unit (INR)"]].mean().reset_index())
    x = np.arange(len(avg_costs)); width = 0.35
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(x - width/2, avg_costs["Generation Cost (INR per unit)"],
           width, label="Gen Cost", color="#4f8ef7")
    ax.bar(x + width/2, avg_costs["Selling Price per Unit (INR)"],
           width, label="Selling Price", color="#f59e0b")
    ax.set_xticks(x)
    ax.set_xticklabels(avg_costs["Energy Source"], rotation=30, ha="right")
    ax.set_ylabel("INR per Unit")
    ax.set_title("Generation Cost vs Selling Price")
    ax.legend(); plt.tight_layout(); st.pyplot(fig); plt.close()

st.divider()


# ── Section: Correlation ──────────────────────────────────────────────────────
st.markdown('<a name="correlation"></a>', unsafe_allow_html=True)
st.subheader("🔗 Correlation Heatmap")
numeric_cols = filtered_df.select_dtypes(include=np.number).columns.tolist()
corr = filtered_df[numeric_cols].corr()
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax,
            linewidths=0.5, linecolor="#2d2d2d",
            annot_kws={"color": "#e2e8f0"})
ax.set_title("Correlation Between Numeric Features")
plt.tight_layout(); st.pyplot(fig); plt.close()

st.divider()


# ── Section: Data Table ───────────────────────────────────────────────────────
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

dl1, dl2, _ = st.columns([1, 1, 4])
with dl1:
    st.download_button("⬇️ Download Filtered CSV",
                       filtered_df.to_csv(index=False).encode("utf-8"),
                       "filtered_energy_data.csv", "text/csv")
with dl2:
    st.download_button("⬇️ Download Summary CSV",
                       summary.to_csv(index=False).encode("utf-8"),
                       "energy_summary.csv", "text/csv")

with st.expander("🗂️ View Full Raw Data"):
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ⚡ A Comparative Analysis of Energy Sources for Sustainable Growth in India &nbsp;|&nbsp;
    Built with Streamlit &nbsp;|&nbsp; Data: CAPSTONE_PROJECT.csv
</div>
""", unsafe_allow_html=True)
