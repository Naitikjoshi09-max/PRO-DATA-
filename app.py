import streamlit as st
import pandas as pd
import numpy as np
import io

# Optional imports with fallbacks to prevent cloud deployment crashes
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_PLOTTING_LIBS = True
except ImportError:
    HAS_PLOTTING_LIBS = False

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Universal Analytics Studio Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4f46e5, #06b6d4, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #6366f1;
    }
    .metric-card-2 { border-left-color: #ec4899; }
    .metric-card-3 { border-left-color: #10b981; }
    .metric-card-4 { border-left-color: #f59e0b; }
    .metric-label { font-size: 0.8rem; font-weight: 700; color: #64748b; text-transform: uppercase; }
    .metric-val { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Password Protection System
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 License Key Verification")
    st.markdown("Please enter your active customer license key to unlock the studio.")
    
    user_key = st.text_input("License Key:", type="password")
    if st.button("Unlock Application", type="primary"):
        if user_key.strip() in ["VIP-2026-PASS", "DEMO123", "ADMIN"]:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Invalid key. Please check your purchase receipt.")
    st.stop()

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
@st.cache_data
def generate_demo_data():
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", periods=100, freq="D")
    categories = ["Technology", "Healthcare", "Retail", "Finance"]
    regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
    
    return pd.DataFrame({
        "Date": np.random.choice(dates, 300),
        "Category": np.random.choice(categories, 300),
        "Region": np.random.choice(regions, 300),
        "Sales": np.random.uniform(100.0, 5000.0, 300).round(2),
        "Units": np.random.randint(1, 50, 300),
        "Profit_Margin": np.random.uniform(0.05, 0.45, 300).round(2)
    })

def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)
    return buf

# ---------------------------------------------------------
# Sidebar & Data Engine
# ---------------------------------------------------------
st.sidebar.title("⚡ Control Center")
if st.sidebar.button("🔒 Lock Application"):
    st.session_state["authenticated"] = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("📂 Data Source")

data_mode = st.sidebar.radio("Mode:", ["Upload CSV", "Demo Sample Data"])

if data_mode == "Upload CSV":
    file = st.sidebar.file_uploader("Drop CSV file here", type=["csv"])
    if file is not None:
        try:
            df = pd.read_csv(file)
            st.sidebar.success(f"Loaded: {len(df):,} rows")
        except Exception as e:
            st.sidebar.error(f"File Error: {e}")
            df = generate_demo_data()
    else:
        st.sidebar.info("Upload a file above or switch to Demo Mode.")
        df = generate_demo_data()
else:
    df = generate_demo_data()

# Auto-Detect Column Types
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
date_cols = []

for c in df.columns:
    if c not in numeric_cols:
        try:
            converted = pd.to_datetime(df[c], errors='coerce')
            if converted.notna().sum() > 0.5 * len(df):
                date_cols.append(c)
                df[c] = converted
                if c in categorical_cols:
                    categorical_cols.remove(c)
        except Exception:
            pass

# ---------------------------------------------------------
# Main Header & KPIs
# ---------------------------------------------------------
st.markdown('<div class="main-title">✨ Universal Business Analytics Studio</div>', unsafe_allow_html=True)
st.markdown("Automated insights, visual analytics, and exportable data tables.")

st.subheader("📌 Performance Overview")
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Total Records</div><div class="metric-val">{len(df):,}</div></div>', unsafe_allow_html=True)

with k2:
    val = f"{df[numeric_cols[0]].sum():,.2f}" if numeric_cols else "N/A"
    lbl = numeric_cols[0] if numeric_cols else "Metric"
    st.markdown(f'<div class="metric-card metric-card-2"><div class="metric-label">Total {lbl}</div><div class="metric-val">{val}</div></div>', unsafe_allow_html=True)

with k3:
    val = f"{df[numeric_cols[0]].mean():,.2f}" if numeric_cols else "N/A"
    st.markdown(f'<div class="metric-card metric-card-3"><div class="metric-label">Average {lbl}</div><div class="metric-val">{val}</div></div>', unsafe_allow_html=True)

with k4:
    st.markdown(f'<div class="metric-card metric-card-4"><div class="metric-label">Attributes</div><div class="metric-val">{len(df.columns)} Columns</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Visual Analytics (Interactive Native + Matplotlib Fallback)
# ---------------------------------------------------------
st.subheader("📊 Interactive Visual Studio")

if numeric_cols:
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("##### 🏷️ Category Aggregation")
        cat_field = st.selectbox("Group By", options=categorical_cols if categorical_cols else df.columns)
        num_field = st.selectbox("Metric", options=numeric_cols, key="num1")

        grouped = df.groupby(cat_field)[num_field].sum().reset_index().sort_values(by=num_field, ascending=False).head(10)

        if HAS_PLOTTING_LIBS:
            fig, ax = plt.subplots(figsize=(7, 4.2))
            sns.barplot(data=grouped, x=num_field, y=cat_field, palette="Blues_r", ax=ax)
            ax.set_title(f"Top {cat_field} by {num_field}", fontweight="bold")
            st.pyplot(fig)
            st.download_button("📷 Download PNG Chart", data=fig_to_bytes(fig), file_name="chart.png", mime="image/png")
        else:
            st.bar_chart(grouped.set_index(cat_field))

    with col_r:
        st.markdown("##### 📈 Distribution Analysis")
        dist_col = st.selectbox("Variable", options=numeric_cols, key="num2")

        if HAS_PLOTTING_LIBS:
            fig, ax = plt.subplots(figsize=(7, 4.2))
            sns.histplot(df[dist_col].dropna(), kde=True, color="#2b5c8f", ax=ax)
            ax.set_title(f"Distribution of {dist_col}", fontweight="bold")
            st.pyplot(fig)
        else:
            st.line_chart(df[dist_col].value_counts().sort_index())

    if date_cols:
        st.markdown("---")
        st.subheader("📅 Time Series Trends")
        dt_col = date_cols[0]
        ts_metric = st.selectbox("Select Trend Metric", options=numeric_cols, key="ts")
        
        ts_data = df.groupby(df[dt_col].dt.date)[ts_metric].sum()
        st.line_chart(ts_data)

st.markdown("---")

# ---------------------------------------------------------
# Raw Data Explorer
# ---------------------------------------------------------
st.subheader("📋 Dataset Explorer")
st.dataframe(df, use_container_width=True)

csv_export = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="💾 Export Processed CSV Data",
    data=csv_export,
    file_name="processed_data.file.csv",
    mime="text/csv"
)
