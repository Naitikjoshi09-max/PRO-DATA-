import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io
from sklearn.linear_model import LinearRegression

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Universal Analytics Studio Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Ultra-Modern CSS & Glassmorphic Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Dark Gradient Base */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 70%, #020617 100%);
        color: #f8fafc;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Branding Header */
    .brand-logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 14px;
        margin-bottom: 20px;
    }
    .brand-logo-icon {
        width: 54px;
        height: 54px;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 30px rgba(168, 85, 247, 0.4);
    }
    .brand-logo-text {
        font-size: 2.3rem;
        font-weight: 900;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #818cf8, #c084fc, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 28px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }
    
    /* Interactive Metric KPI Cards with Hover Animation */
    .kpi-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(168, 85, 247, 0.4);
        box-shadow: 0 12px 25px rgba(168, 85, 247, 0.2);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: linear-gradient(180deg, #6366f1, #a855f7);
    }
    .kpi-card-2::before { background: linear-gradient(180deg, #ec4899, #f43f5e); }
    .kpi-card-3::before { background: linear-gradient(180deg, #10b981, #14b8a6); }
    .kpi-card-4::before { background: linear-gradient(180deg, #f59e0b, #eab308); }
    
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 6px;
    }
    
    /* Smart Insight Box */
    .insight-box {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.05) 100%);
        border: 1px solid rgba(168, 85, 247, 0.2);
        border-radius: 16px;
        padding: 18px 24px;
        margin-bottom: 24px;
    }
    
    /* Title Stylings */
    .main-title {
        font-size: 2.2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #a78bfa, #38bdf8, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)
# ---------------------------------------------------------
# Security Lock Screen (Password Authentication)
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Logo Header
        st.markdown("""
        <div class="brand-logo-container">
            <div class="brand-logo-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                </svg>
            </div>
            <div class="brand-logo-text">UNIVERSAL STUDIO</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Glassmorphism Lock Card
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h3 style="margin-bottom: 8px; font-weight: 800;">🔒 Enterprise License Lock</h3>
            <p style="color: #94a3b8; font-size: 0.9rem;">Enter your confidential password key to unlock the interactive studio.</p>
        </div>
        """, unsafe_allow_html=True)
        
        user_key = st.text_input("", type="password", placeholder="Enter license password...", key="pwd_field")
        
        if st.button("🚀 Unlock Interactive Studio", type="primary", use_container_width=True):
            if user_key.strip() == "UNIVERSAL$12346":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Invalid License Key. Access Denied.")
                
        st.markdown("<br><br>", unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------
# Helper Functions & Demo Dataset Generator
# ---------------------------------------------------------
@st.cache_data
def generate_demo_data():
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", periods=120, freq="D")
    categories = ["Software", "Hardware", "Consulting", "Cloud Services", "Support"]
    regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
    
    return pd.DataFrame({
        "Date": np.random.choice(dates, 400),
        "Category": np.random.choice(categories, 400),
        "Region": np.random.choice(regions, 400),
        "Revenue": np.random.uniform(200.0, 8000.0, 400).round(2),
        "Units_Sold": np.random.randint(1, 60, 400),
        "Satisfaction_Score": np.random.uniform(3.5, 5.0, 400).round(1)
    })

# Plotly Transparent Dark Theme Template
PLOTLY_THEME = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "#cbd5e1", "family": "Inter, sans-serif"},
        "xaxis": {"gridcolor": "#1e293b", "zerolinecolor": "#1e293b"},
        "yaxis": {"gridcolor": "#1e293b", "zerolinecolor": "#1e293b"}
    }
}

# ---------------------------------------------------------
# Sidebar Engine & Dynamic Data Filtering
# ---------------------------------------------------------
st.sidebar.markdown("""
<div class="brand-logo-container" style="justify-content: flex-start; margin-bottom: 10px;">
    <div class="brand-logo-icon" style="width:38px; height:38px; border-radius:12px;">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
        </svg>
    </div>
    <div class="brand-logo-text" style="font-size: 1.4rem;">UNIVERSAL</div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🔒 Lock Application", use_container_width=True):
    st.session_state["authenticated"] = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("📂 1. Data Source")

data_mode = st.sidebar.radio("Choose Input:", ["Upload Custom CSV", "Use Demo Dataset"])

if data_mode == "Upload Custom CSV":
    uploaded_file = st.sidebar.file_uploader("Drop CSV file here", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success(f"Loaded: {len(df):,} rows")
        except Exception as e:
            st.sidebar.error(f"Error loading file: {e}")
            df = generate_demo_data()
    else:
        st.sidebar.info("Upload CSV above or view Demo Data.")
        df = generate_demo_data()
else:
    df = generate_demo_data()

# Column Auto-Detection Engine
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
date_cols = []

for col in df.columns:
    if col not in numeric_cols:
        try:
            converted = pd.to_datetime(df[col], errors='coerce')
            if converted.notna().sum() > 0.5 * len(df):
                date_cols.append(col)
                df[col] = converted
                if col in categorical_cols:
                    categorical_cols.remove(col)
        except Exception:
            pass

# Sidebar Interactive Filters
st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ 2. Interactive Data Filters")

filtered_df = df.copy()

if categorical_cols:
    filter_col = st.sidebar.selectbox("Filter By Category Column:", options=["None"] + categorical_cols)
    if filter_col != "None":
        selected_vals = st.sidebar.multiselect(
            f"Select {filter_col} Values:",
            options=list(df[filter_col].unique()),
            default=list(df[filter_col].unique())[:3]
        )
        if selected_vals:
            filtered_df = filtered_df[filtered_df[filter_col].isin(selected_vals)]

if date_cols:
    dt_col = date_cols[0]
    min_date = filtered_df[dt_col].min().date()
    max_date = filtered_df[dt_col].max().date()
    date_range = st.sidebar.date_input("Date Range:", value=(min_date, max_date))
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df[dt_col].dt.date >= date_range[0]) & 
            (filtered_df[dt_col].dt.date <= date_range[1])
        ]

# ---------------------------------------------------------
# Dashboard Main UI
# ---------------------------------------------------------
st.markdown('<div class="main-title">✨ Universal Business Analytics Studio</div>', unsafe_allow_html=True)
st.markdown("Interactive dashboards, multi-variable Plotly visualizations, and real-time filtering.")
st.markdown("<br>", unsafe_allow_html=True)

# Executive Insights Banner
if numeric_cols and categorical_cols:
    primary_num = numeric_cols[0]
    primary_cat = categorical_cols[0]
    top_group = filtered_df.groupby(primary_cat)[primary_num].sum().idxmax()
    top_val = filtered_df.groupby(primary_cat)[primary_num].sum().max()
    
    st.markdown(f"""
    <div class="insight-box">
        💡 <b>Automated Insight:</b> The highest performing category in current filtered view is 
        <span style="color:#c084fc; font-weight:bold;">{top_group}</span> with a total <b>{primary_num}</b> of 
        <span style="color:#38bdf8; font-weight:bold;">{top_val:,.2f}</span> across <b>{len(filtered_df):,}</b> analyzed records.
    </div>
    """, unsafe_allow_html=True)

# KPI Metric Cards
st.subheader("📌 Key Metrics Overview")
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Active Records</div><div class="kpi-value">{len(filtered_df):,}</div></div>', unsafe_allow_html=True)

with k2:
    val = f"{filtered_df[numeric_cols[0]].sum():,.2f}" if numeric_cols else "N/A"
    lbl = numeric_cols[0] if numeric_cols else "Metric"
    st.markdown(f'<div class="kpi-card kpi-card-2"><div class="kpi-label">Total {lbl}</div><div class="kpi-value">{val}</div></div>', unsafe_allow_html=True)

with k3:
    val = f"{filtered_df[numeric_cols[0]].mean():,.2f}" if numeric_cols else "N/A"
    st.markdown(f'<div class="kpi-card kpi-card-3"><div class="kpi-label">Average {lbl}</div><div class="kpi-value">{val}</div></div>', unsafe_allow_html=True)

with k4:
    val = f"{filtered_df[numeric_cols[1]].sum():,.0f}" if len(numeric_cols) > 1 else f"{len(filtered_df.columns)} Cols"
    lbl = numeric_cols[1] if len(numeric_cols) > 1 else "Attributes"
    st.markdown(f'<div class="kpi-card kpi-card-4"><div class="kpi-label">{lbl}</div><div class="kpi-value">{val}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Interactive Plotly Visualizations Studio
# ---------------------------------------------------------
st.subheader("📊 Interactive Visual Studio")

if numeric_cols:
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Category Breakdown", 
        "📈 Time Series & Forecasting", 
        "🔥 Correlation Heatmap", 
        "🛠️ Custom Dynamic Builder"
    ])

    # TAB 1: Category Bar & Donut Charts
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            cat_field = st.selectbox("Group Category By:", options=categorical_cols if categorical_cols else filtered_df.columns, key="p_cat")
            num_field = st.selectbox("Aggregate Metric:", options=numeric_cols, key="p_num_1")

            grouped = filtered_df.groupby(cat_field)[num_field].sum().reset_index().sort_values(by=num_field, ascending=False).head(10)

            fig_bar = px.bar(
                grouped, x=num_field, y=cat_field, orientation='h',
                color=num_field, color_continuous_scale="Purples",
                title=f"Top 10 {cat_field} by {num_field}"
            )
            fig_bar.update_layout(PLOTLY_THEME["layout"], coloraxis_showscale=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        with c2:
            fig_pie = px.pie(
                grouped, names=cat_field, values=num_field, hole=0.5,
                color_discrete_sequence=px.colors.qualitative.Pastel,
                title=f"Proportion Share of {num_field}"
            )
            fig_pie.update_layout(PLOTLY_THEME["layout"])
            st.plotly_chart(fig_pie, use_container_width=True)

    # TAB 2: Time Series & Predictive Machine Learning Forecasting (ADDON 2)
    with tab2:
        c3, c4 = st.columns(2)
        with c3:
            dist_col = st.selectbox("Select Variable for Histogram:", options=numeric_cols, key="p_dist")
            fig_hist = px.histogram(
                filtered_df, x=dist_col, nbins=30, marginal="rug" if len(filtered_df) < 1000 else None,
                color_discrete_sequence=["#818cf8"], title=f"Distribution Frequency of {dist_col}"
            )
            fig_hist.update_layout(PLOTLY_THEME["layout"])
            st.plotly_chart(fig_hist, use_container_width=True)

        with c4:
            if date_cols:
                dt = date_cols[0]
                ts_metric = st.selectbox("Trend Metric:", options=numeric_cols, key="p_ts")
                ts_data = filtered_df.groupby(filtered_df[dt].dt.date)[ts_metric].sum().reset_index()
                
                fig_line = px.area(
                    ts_data, x=dt, y=ts_metric,
                    color_discrete_sequence=["#38bdf8"], title=f"Timeline Trend: {ts_metric}"
                )
                fig_line.update_layout(PLOTLY_THEME["layout"])
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.info("Upload data containing date columns to unlock automatic timeline trends.")

        # --- FEATURE 2: 30-Day Predictive Forecasting ---
        if date_cols and numeric_cols:
            st.markdown("---")
            st.markdown("##### 🔮 30-Day Machine Learning Trend Projection")
            dt_col = date_cols[0]
            fc_metric = st.selectbox("Target Metric to Forecast:", options=numeric_cols, key="fc_select")
            
            ts_data_fc = filtered_df.groupby(filtered_df[dt_col].dt.date)[fc_metric].sum().reset_index().sort_values(by=dt_col)
            ts_data_fc[dt_col] = pd.to_datetime(ts_data_fc[dt_col])
            
            if len(ts_data_fc) > 3:
                ts_data_fc['Day_Index'] = np.arange(len(ts_data_fc))
                
                # Linear Regression Fit
                X = ts_data_fc[['Day_Index']]
                y = ts_data_fc[fc_metric]
                model = LinearRegression().fit(X, y)
                
                # Predict Future 30 Days
                future_days = 30
                last_index = ts_data_fc['Day_Index'].max()
                future_indices = np.arange(last_index + 1, last_index + 1 + future_days).reshape(-1, 1)
                future_preds = model.predict(future_indices)
                
                last_date = ts_data_fc[dt_col].max()
                future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=future_days)
                
                forecast_df = pd.DataFrame({dt_col: future_dates, fc_metric: future_preds, "Type": "30-Day Forecast"})
                hist_df = ts_data_fc[[dt_col, fc_metric]].copy()
                hist_df["Type"] = "Historical Data"
                
                combined_df = pd.concat([hist_df, forecast_df])
                
                fig_forecast = px.line(
                    combined_df, x=dt_col, y=fc_metric, color="Type",
                    color_discrete_map={"Historical Data": "#38bdf8", "30-Day Forecast": "#ec4899"},
                    title=f"Projected 30-Day Trend Model for {fc_metric}"
                )
                fig_forecast.update_layout(PLOTLY_THEME["layout"])
                st.plotly_chart(fig_forecast, use_container_width=True)

    # TAB 3: Correlation Heatmap
    with tab3:
        if len(numeric_cols) > 1:
            corr_matrix = filtered_df[numeric_cols].corr().round(2)
            fig_corr = px.imshow(
                corr_matrix, text_auto=True, color_continuous_scale="Plasma",
                title="Numerical Correlation Matrix"
            )
            fig_corr.update_layout(PLOTLY_THEME["layout"])
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info("Correlation heatmaps require at least two numeric columns.")

    # TAB 4: Custom Interactive Chart Builder (ADDON 1)
    with tab4:
        st.markdown("##### 🛠️ Ad-Hoc Dynamic Chart Studio")
        col_x, col_y, col_type = st.columns(3)
        with col_x:
            x_axis = st.selectbox("Select X-Axis Column:", options=filtered_df.columns, key="builder_x")
        with col_y:
            y_axis = st.selectbox("Select Y-Axis Metric:", options=numeric_cols, key="builder_y")
        with col_type:
            chart_style = st.selectbox("Select Chart Style:", ["Scatter Plot", "Bar Chart", "Line Trend", "Box Plot"], key="builder_style")

        if chart_style == "Scatter Plot":
            fig_custom = px.scatter(
                filtered_df, x=x_axis, y=y_axis, 
                color=categorical_cols[0] if categorical_cols else None, 
                hover_data=filtered_df.columns
            )
        elif chart_style == "Bar Chart":
            fig_custom = px.bar(filtered_df, x=x_axis, y=y_axis, color_discrete_sequence=["#a855f7"])
        elif chart_style == "Line Trend":
            fig_custom = px.line(filtered_df, x=x_axis, y=y_axis, color_discrete_sequence=["#38bdf8"])
        else:
            fig_custom = px.box(filtered_df, x=x_axis, y=y_axis, color_discrete_sequence=["#ec4899"])

        fig_custom.update_layout(PLOTLY_THEME["layout"])
        st.plotly_chart(fig_custom, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------
# Interactive Data Table Explorer & Multi-Format Export (ADDON 5)
# ---------------------------------------------------------
st.subheader("📋 Dataset Explorer & Multi-Format Reports")

# Search Filter inside Data Table
search_term = st.text_input("🔍 Search rows by keyword:", placeholder="Type to filter data records...")
if search_term:
    mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
    display_df = filtered_df[mask]
else:
    display_df = filtered_df

st.dataframe(display_df, use_container_width=True)

# Generate Multi-Tab Excel Workbook
excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
    display_df.to_excel(writer, sheet_name='Filtered Records', index=False)
    if categorical_cols and numeric_cols:
        summary_tb = display_df.groupby(categorical_cols[0])[numeric_cols[0]].agg(['sum', 'mean', 'count']).reset_index()
        summary_tb.to_excel(writer, sheet_name='Category Summary', index=False)

csv_export = display_df.to_csv(index=False).encode('utf-8')

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    st.download_button(
        label="💾 Export Processed CSV Data",
        data=csv_export,
        file_name="universal_analytics_export.csv",
        mime="text/csv",
        use_container_width=True
    )

with col_exp2:
    st.download_button(
        label="📊 Export Multi-Tab Excel Workbook (.xlsx)",
        data=excel_buffer.getvalue(),
        file_name="Executive_Analytics_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
