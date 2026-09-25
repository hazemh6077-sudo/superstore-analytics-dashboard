import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="SuperStore Sales & Profit Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling (Sunset Vibrant / Luxury Purple Palette)
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --bg-dark: #150729;
    --panel-bg: rgba(44, 15, 87, 0.72);
    --panel-border: rgba(139, 107, 216, 0.35);
    --accent-pink: #fb7185;
    --accent-gold: #f7c948;
    --accent-purple: #c084fc;
    --accent-cyan: #22d3ee;
    --accent-green: #4ade80;
    --text-primary: #fdf4ff;
    --text-dim: #c4b5fd;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', 'Cairo', sans-serif;
}

/* Background gradient */
.stApp {
    background: radial-gradient(circle at 15% 15%, #2a0845 0%, #17072b 45%, #0f031d 100%) !important;
    color: var(--text-primary);
}

/* Header Banner */
.header-container {
    background: linear-gradient(135deg, rgba(76, 29, 149, 0.5) 0%, rgba(46, 16, 101, 0.6) 100%);
    border: 1px solid rgba(251, 113, 133, 0.28);
    border-radius: 16px;
    padding: 22px 28px;
    margin-bottom: 22px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(12px);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
}

.header-title-box h1 {
    color: #fdf4ff;
    font-size: 26px;
    font-weight: 800;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.header-title-box p {
    color: var(--text-dim);
    font-size: 13px;
    margin: 0;
}

.header-badge {
    background: linear-gradient(135deg, #fb7185 0%, #c084fc 100%);
    color: #150729;
    font-weight: 800;
    font-size: 11px;
    padding: 6px 14px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 14px;
    margin-bottom: 22px;
}

.kpi-card {
    background: linear-gradient(145deg, rgba(59, 7, 100, 0.65) 0%, rgba(30, 11, 61, 0.8) 100%);
    border: 1px solid var(--panel-border);
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.28);
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.kpi-card:hover {
    transform: translateY(-3px);
    border-color: rgba(251, 113, 133, 0.6);
    box-shadow: 0 12px 28px rgba(251, 113, 133, 0.18);
}

.kpi-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
}

.kpi-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.kpi-icon {
    font-size: 16px;
    opacity: 0.85;
}

.kpi-value {
    font-size: 26px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin: 4px 0 2px 0;
}

.kpi-sub {
    font-size: 11px;
    color: var(--accent-gold);
    font-weight: 500;
}

/* Chart Container Cards */
.chart-card {
    background: linear-gradient(145deg, rgba(46, 16, 101, 0.55) 0%, rgba(26, 7, 56, 0.75) 100%);
    border: 1px solid var(--panel-border);
    border-radius: 16px;
    padding: 20px 20px 14px 20px;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.3);
    margin-bottom: 18px;
    backdrop-filter: blur(8px);
}

.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 14px;
    border-bottom: 1px solid rgba(139, 107, 216, 0.18);
    padding-bottom: 8px;
}

.chart-title {
    font-size: 15px;
    font-weight: 700;
    color: #fdf4ff;
    margin: 0;
}

.chart-subtitle {
    font-size: 11px;
    color: var(--text-dim);
    margin: 0;
}

/* Slicer Card */
.slicer-card {
    background: linear-gradient(145deg, rgba(59, 7, 100, 0.75) 0%, rgba(30, 11, 61, 0.85) 100%);
    border: 1px solid rgba(247, 201, 72, 0.35);
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 14px;
}

/* Custom Pills / Region buttons */
div[data-testid="stRadio"] > div {
    display: flex;
    flex-direction: row;
    gap: 8px;
}

/* Clean tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(30, 11, 61, 0.7);
    padding: 6px;
    border-radius: 12px;
    border: 1px solid rgba(139, 107, 216, 0.25);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 20px;
    color: #c4b5fd !important;
    font-weight: 600;
    font-size: 13px;
    border: none !important;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #ffffff !important;
    background: rgba(139, 107, 216, 0.2);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(251, 113, 133, 0.35) 0%, rgba(192, 132, 252, 0.35) 100%) !important;
    color: #ffffff !important;
    border: 1px solid var(--accent-pink) !important;
    box-shadow: 0 4px 12px rgba(251, 113, 133, 0.2);
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1b0736 0%, #120324 100%) !important;
    border-right: 1px solid rgba(139, 107, 216, 0.25);
}

/* Filter Summary Pill */
.active-filter-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(251, 113, 133, 0.15);
    border: 1px solid rgba(251, 113, 133, 0.4);
    color: #fbcfe8;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
    margin: 2px 4px 2px 0;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Loading & Preprocessing
# ---------------------------------------------------------
@st.cache_data
def load_data():
    csv_path = "SuperStore_Sales_Dataset.csv"
    df = pd.read_csv(csv_path)

    # Clean & Format Dates
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y", errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y", errors="coerce")

    # Shipping Days
    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df["Shipping Days"] = df["Shipping Days"].fillna(0).clip(lower=0)

    # Returns Indicator: 1 if returned, 0 otherwise
    df["Is_Returned"] = df["Returns"].notna().astype(int)

    # Date hierarchy
    df["Year"] = df["Order Date"].dt.year
    df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)

    return df

df_raw = load_data()

# ---------------------------------------------------------
# State abbreviations for US Map
# ---------------------------------------------------------
US_STATE_ABBR = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
    'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
    'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
    'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA',
    'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# ---------------------------------------------------------
# Sidebar Controls & Global Filters
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ التحكم والتصفية | Controls")
    
    # Language toggle
    lang = st.radio("اللغة / Language", ["العربية (Arabic)", "English"], horizontal=True)
    is_ar = "العربية" in lang

    st.markdown("---")
    
    # Region Filter
    regions = sorted(df_raw["Region"].dropna().unique().tolist())
    selected_region = st.selectbox(
        "المنطقة (Region)" if is_ar else "Region",
        options=["All Regions (الكل)"] + regions,
        index=0,
        key="sidebar_region_select"
    )

    # Category Filter
    categories = sorted(df_raw["Category"].dropna().unique().tolist())
    selected_categories = st.multiselect(
        "الفئة (Category)" if is_ar else "Category",
        options=categories,
        default=categories
    )

    # Segment Filter
    segments = sorted(df_raw["Segment"].dropna().unique().tolist())
    selected_segments = st.multiselect(
        "قطاع العملاء (Segment)" if is_ar else "Customer Segment",
        options=segments,
        default=segments
    )

    # Ship Mode Filter
    ship_modes = sorted(df_raw["Ship Mode"].dropna().unique().tolist())
    selected_ship_modes = st.multiselect(
        "طريقة الشحن (Ship Mode)" if is_ar else "Ship Mode",
        options=ship_modes,
        default=ship_modes
    )

    # Payment Mode Filter
    pay_modes = sorted(df_raw["Payment Mode"].dropna().unique().tolist())
    selected_pay_modes = st.multiselect(
        "طريقة الدفع (Payment Mode)" if is_ar else "Payment Mode",
        options=pay_modes,
        default=pay_modes
    )

    # Date Range Filter
    min_date = df_raw["Order Date"].min().date()
    max_date = df_raw["Order Date"].max().date()
    date_range = st.date_input(
        "الفترة الزمنية (Order Date)" if is_ar else "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    st.markdown("---")
    if st.button("🔄 إعادة ضبط الفلاتر (Reset All)" if is_ar else "🔄 Reset Filters", use_container_width=True):
        st.session_state["sidebar_region_select"] = "All Regions (الكل)"
        st.rerun()

# ---------------------------------------------------------
# Apply Filters to Dataset
# ---------------------------------------------------------
df = df_raw.copy()

if selected_region != "All Regions (الكل)":
    df = df[df["Region"] == selected_region]

if selected_categories:
    df = df[df["Category"].isin(selected_categories)]

if selected_segments:
    df = df[df["Segment"].isin(selected_segments)]

if selected_ship_modes:
    df = df[df["Ship Mode"].isin(selected_ship_modes)]

if selected_pay_modes:
    df = df[df["Payment Mode"].isin(selected_pay_modes)]

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_d, end_d = date_range
    df = df[(df["Order Date"].dt.date >= start_d) & (df["Order Date"].dt.date <= end_d)]

# ---------------------------------------------------------
# Core Metrics (DAX Equivalents)
# ---------------------------------------------------------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
profit_margin = (total_profit / total_sales) if total_sales > 0 else 0.0
order_count = df["Order ID"].nunique()
returned_orders_count = df["Is_Returned"].sum()
return_rate = (returned_orders_count / len(df)) if len(df) > 0 else 0.0
avg_profit_per_order = (total_profit / order_count) if order_count > 0 else 0.0
avg_shipping_days = df["Shipping Days"].mean() if len(df) > 0 else 0.0

# ---------------------------------------------------------
# Header Bar
# ---------------------------------------------------------
st.markdown(
    f"""
    <div class="header-container" dir="{'rtl' if is_ar else 'ltr'}">
        <div class="header-title-box">
            <h1>
                <span>💎 SuperStore Analytics</span>
                <span class="header-badge">Power BI Enterprise Replica</span>
            </h1>
            <p>
                {"لوحة تحكم تفاعلية متطورة للمبيعات، الأرباح، مرتجعات الطلبات وعمليات الشحن عبر الفروع والولايات" if is_ar else
                 "Executive interactive dashboard for Sales, Profit, Order Returns, and Shipping Operations across US regions"}
            </p>
        </div>
        <div style="text-align:{'left' if is_ar else 'right'}; font-size:12px; color:#c4b5fd;">
            <div>📅 <b>{df['Order Date'].min().strftime('%d %b %Y') if len(df) else ''}</b> — <b>{df['Order Date'].max().strftime('%d %b %Y') if len(df) else ''}</b></div>
            <div>📦 <b>{len(df):,}</b> {"سجل متطابق" if is_ar else "Matching Records"}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# KPI Cards Component Function
# ---------------------------------------------------------
def render_kpis():
    st.markdown(
        f"""
        <div class="kpi-grid" dir="{'rtl' if is_ar else 'ltr'}">
            <div class="kpi-card">
                <div class="kpi-top">
                    <span class="kpi-label">{"متوسط ربح الطلب" if is_ar else "Avg Profit / Order"}</span>
                    <span class="kpi-icon">💰</span>
                </div>
                <div class="kpi-value">${avg_profit_per_order:,.2f}</div>
                <div class="kpi-sub">{"لكل طلب مكتمل" if is_ar else "Per unique order"}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-top">
                    <span class="kpi-label">{"إجمالي الأرباح" if is_ar else "Sum of Profit"}</span>
                    <span class="kpi-icon">📈</span>
                </div>
                <div class="kpi-value">${total_profit:,.0f}</div>
                <div class="kpi-sub">{"صافي الربح التراكمي" if is_ar else "Total net profit"}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-top">
                    <span class="kpi-label">{"هامش الربح" if is_ar else "Profit Margin"}</span>
                    <span class="kpi-icon">🎯</span>
                </div>
                <div class="kpi-value">{profit_margin * 100:.2f}%</div>
                <div class="kpi-sub">{"الأرباح ÷ المبيعات" if is_ar else "Profit / Sales ratio"}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-top">
                    <span class="kpi-label">{"معدل المرتجعات" if is_ar else "Return Rate"}</span>
                    <span class="kpi-icon">🔄</span>
                </div>
                <div class="kpi-value">{return_rate * 100:.2f}%</div>
                <div class="kpi-sub">{"من إجمالي العمليات" if is_ar else "Of all line items"}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-top">
                    <span class="kpi-label">{"الطلبات المرتجعة" if is_ar else "Returned Orders"}</span>
                    <span class="kpi-icon">⚠️</span>
                </div>
                <div class="kpi-value">{returned_orders_count:,}</div>
                <div class="kpi-sub">{"طلب تم إرجاعه" if is_ar else "Returned items"}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-top">
                    <span class="kpi-label">{"إجمالي المبيعات" if is_ar else "Total Sales"}</span>
                    <span class="kpi-icon">💳</span>
                </div>
                <div class="kpi-value">${total_sales:,.0f}</div>
                <div class="kpi-sub">{"حجم الإيرادات" if is_ar else "Gross Revenue"}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# Plotly Dark Sunset Theme Helper
# ---------------------------------------------------------
def apply_chart_theme(fig, height=300):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, Cairo, sans-serif", color="#fdf4ff", size=12),
        margin=dict(l=15, r=15, t=30, b=25),
        height=height,
        hoverlabel=dict(
            bgcolor="#250d47",
            font_size=12,
            font_family="Plus Jakarta Sans",
            bordercolor="#fb7185"
        )
    )
    fig.update_xaxes(
        gridcolor="rgba(139, 107, 216, 0.15)",
        tickfont=dict(color="#c4b5fd", size=11),
        showline=False
    )
    fig.update_yaxes(
        gridcolor="rgba(139, 107, 216, 0.15)",
        tickfont=dict(color="#c4b5fd", size=11),
        showline=False
    )
    return fig

# ---------------------------------------------------------
# Main Tabs Navigation
# ---------------------------------------------------------
tab_titles = [
    "📑 الصفحة 1: نظرة عامة والمرتجعات" if is_ar else "📑 Page 1: Sales & Returns Overview",
    "📈 الصفحة 2: العمليات والقطاعات" if is_ar else "📈 Page 2: Operations & Segments",
    "🗺️ الخريطة الجغرافية للولايات" if is_ar else "🗺️ US Geographic Analysis",
    "🔍 مستكشف البيانات الكامل" if is_ar else "🔍 Data Explorer & Export"
]

tab1, tab2, tab3, tab4 = st.tabs(tab_titles)

# =========================================================
# TAB 1: Page 1 (Exact Power BI Replica + Upgrades)
# =========================================================
with tab1:
    render_kpis()

    # Layout Row 1: Profit Margin by Category (1.3fr) | Region Slicer (0.8fr) | Returned Orders Count (1.3fr)
    col1, col2, col3 = st.columns([1.3, 0.85, 1.3])

    with col1:
        st.markdown(
            f"""
            <div class="chart-card">
                <div class="chart-header">
                    <h3 class="chart-title">{"هامش الربح حسب الفئة" if is_ar else "Profit Margin"}</h3>
                    <span class="chart-subtitle">{"by Category" if not is_ar else "حسب فئة المنتج"}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Calculate Margin by Category
        cat_stats = df.groupby("Category").agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        ).reset_index()
        cat_stats["Margin"] = cat_stats["Profit"] / cat_stats["Sales"]
        cat_stats = cat_stats.sort_values("Margin", ascending=True)

        fig_margin = go.Figure(go.Bar(
            x=cat_stats["Margin"],
            y=cat_stats["Category"],
            orientation="h",
            marker=dict(
                color=["#c084fc", "#f7c948", "#fb7185"][:len(cat_stats)],
                line=dict(color="rgba(255,255,255,0.2)", width=1)
            ),
            text=[f"{m * 100:.2f}%" for m in cat_stats["Margin"]],
            textposition="auto",
            textfont=dict(color="#ffffff", size=12, family="Plus Jakarta Sans", weight="bold"),
            hovertemplate="<b>%{y}</b><br>Profit Margin: %{x:.2%}<br>Sales: $%{customdata[0]:,.0f}<br>Profit: $%{customdata[1]:,.0f}<extra></extra>",
            customdata=cat_stats[["Sales", "Profit"]]
        ))
        fig_margin.update_xaxes(tickformat=".0%")
        apply_chart_theme(fig_margin, height=240)
        st.plotly_chart(fig_margin, use_container_width=True)

    with col2:
        st.markdown(
            f"""
            <div class="chart-card">
                <div class="chart-header">
                    <h3 class="chart-title">{"محدد المنطقة" if is_ar else "Region Slicer"}</h3>
                    <span class="chart-subtitle">{"سريع وتفاعلي" if is_ar else "Quick Slicer"}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Interactive Region Quick Selector
        st.write("اختر المنطقة للتصفية الفورية:" if is_ar else "Select region to cross-filter:")
        reg_cols = st.columns(2)
        all_reg_options = ["Central", "East", "South", "West"]
        
        for idx, r in enumerate(all_reg_options):
            col_target = reg_cols[idx % 2]
            is_active = (selected_region == r)
            btn_label = f"{'⭐ ' if is_active else ''}{r}"
            if col_target.button(btn_label, key=f"slicer_btn_{r}", use_container_width=True):
                if selected_region == r:
                    st.session_state["sidebar_region_select"] = "All Regions (الكل)"
                else:
                    st.session_state["sidebar_region_select"] = r
                st.rerun()

        # Mini Region Summary
        st.markdown(
            f"""
            <div style="background:rgba(21,7,41,0.6); padding:10px; border-radius:10px; margin-top:12px; font-size:12px; border:1px solid rgba(139,107,216,0.2);">
                <div style="color:#c4b5fd;">{"المنطقة النشطة:" if is_ar else "Active Region:"} <b style="color:#f7c948;">{selected_region}</b></div>
                <div style="color:#c4b5fd; margin-top:4px;">{"مبيعات المنطقة:" if is_ar else "Region Sales:"} <b style="color:#ffffff;">${df['Sales'].sum():,.0f}</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="chart-card">
                <div class="chart-header">
                    <h3 class="chart-title">{"عدد الطلبات المرتجعة" if is_ar else "Returned Orders Count"}</h3>
                    <span class="chart-subtitle">{"by Category" if not is_ar else "حسب فئة المنتج"}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Returned Orders by Category
        ret_stats = df[df["Is_Returned"] == 1].groupby("Category")["Order ID"].count().reset_index()
        # Ensure all categories appear
        all_cats_df = pd.DataFrame({"Category": ["Furniture", "Office Supplies", "Technology"]})
        ret_stats = all_cats_df.merge(ret_stats, on="Category", how="left").fillna(0)
        ret_stats = ret_stats.sort_values("Order ID", ascending=True)

        fig_ret = go.Figure(go.Bar(
            x=ret_stats["Order ID"],
            y=ret_stats["Category"],
            orientation="h",
            marker=dict(
                color=["#f7c948", "#fb7185", "#c084fc"][:len(ret_stats)],
                line=dict(color="rgba(255,255,255,0.2)", width=1)
            ),
            text=[f"{int(v):,}" for v in ret_stats["Order ID"]],
            textposition="auto",
            textfont=dict(color="#ffffff", size=12, weight="bold"),
            hovertemplate="<b>%{y}</b><br>Returns Count: %{x:,}<extra></extra>"
        ))
        apply_chart_theme(fig_ret, height=240)
        st.plotly_chart(fig_ret, use_container_width=True)

    # Layout Row 2: Donut (Orders vs Returns) | Top 15 States by Profit
    r2_col1, r2_col2 = st.columns([1, 1.3])

    with r2_col1:
        st.markdown(
            f"""
            <div class="chart-card">
                <div class="chart-header">
                    <h3 class="chart-title">{"إجمالي الطلبات مقابل المرتجعات" if is_ar else "Order Count vs Returns Count"}</h3>
                    <span class="chart-subtitle">{"Donut Ratio" if not is_ar else "نسبة المرتجع من الإجمالي"}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Donut Chart
        non_returned = max(order_count - returned_orders_count, 0)
        labels_pie = ["الطلبات الناجحة (Orders)" if is_ar else "Orders Kept", "الطلبات المرتجعة (Returns)" if is_ar else "Returned Orders"]
        values_pie = [non_returned, returned_orders_count]
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels_pie,
            values=values_pie,
            hole=0.62,
            marker=dict(colors=["#c084fc", "#fb7185"], line=dict(color="#150729", width=2)),
            textinfo="percent+value",
            textfont=dict(size=12, color="#ffffff", weight="bold"),
            hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Ratio: %{percent}<extra></extra>"
        )])
        fig_pie.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(color="#c4b5fd", size=11)),
            annotations=[dict(text=f"<b>{return_rate*100:.1f}%</b><br><span style='font-size:10px; color:#c4b5fd;'>Return Rate</span>", x=0.5, y=0.5, font_size=18, font_color="#fb7185", showarrow=False)]
        )
        apply_chart_theme(fig_pie, height=310)
        st.plotly_chart(fig_pie, use_container_width=True)

    with r2_col2:
        st.markdown(
            f"""
            <div class="chart-card">
                <div class="chart-header">
                    <h3 class="chart-title">{"إجمالي الأرباح حسب الولاية (أعلى 15 ولاية)" if is_ar else "Sum of Profit by State (Top 15)"}</h3>
                    <span class="chart-subtitle">{"Top 15 States" if not is_ar else "أكثر الولايات تحقيقاً للأرباح"}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Top 15 States by Profit
        state_profit = df.groupby("State")["Profit"].sum().reset_index()
        top_15_states = state_profit.sort_values("Profit", ascending=False).head(15).sort_values("Profit", ascending=True)

        fig_state = go.Figure(go.Bar(
            x=top_15_states["Profit"],
            y=top_15_states["State"],
            orientation="h",
            marker=dict(
                color=top_15_states["Profit"],
                colorscale=[[0, "#5b21b6"], [0.5, "#9333ea"], [1, "#fb7185"]],
                line=dict(color="rgba(255,255,255,0.15)", width=1)
            ),
            text=[f"${p:,.0f}" for p in top_15_states["Profit"]],
            textposition="auto",
            textfont=dict(color="#ffffff", size=11, weight="bold"),
            hovertemplate="<b>%{y}</b><br>Profit: $%{x:,.2f}<extra></extra>"
        ))
        apply_chart_theme(fig_state, height=310)
        st.plotly_chart(fig_state, use_container_width=True)

# =========================================================
# TAB 2: Page 2 (Operations, Shipping & Segments)
# =========================================================
with tab2:
    render_kpis()

    # Row 1: Sum of Profit by Segment (Area / Curve)
    st.markdown(
        f"""
        <div class="chart-card">
            <div class="chart-header">
                <h3 class="chart-title">{"إجمالي الأرباح حسب قطاع العملاء" if is_ar else "Sum of Profit by Segment"}</h3>
                <span class="chart-subtitle">{"by Segment" if not is_ar else "Consumer vs Corporate vs Home Office"}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    seg_profit = df.groupby("Segment")["Profit"].sum().reset_index()
    # Ensure ordered segments
    desired_order = ["Consumer", "Corporate", "Home Office"]
    seg_profit["Segment"] = pd.Categorical(seg_profit["Segment"], categories=desired_order, ordered=True)
    seg_profit = seg_profit.sort_values("Segment")

    fig_seg = go.Figure()
    fig_seg.add_trace(go.Scatter(
        x=seg_profit["Segment"],
        y=seg_profit["Profit"],
        mode="lines+markers+text",
        text=[f"${p:,.0f}" for p in seg_profit["Profit"]],
        textposition="top center",
        textfont=dict(color="#ffffff", size=13, weight="bold"),
        line=dict(color="#fb7185", width=4, shape="spline"),
        marker=dict(size=12, color="#ffffff", line=dict(color="#fb7185", width=3)),
        fill="tozeroy",
        fillcolor="rgba(251, 113, 133, 0.22)",
        hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.2f}<extra></extra>"
    ))
    apply_chart_theme(fig_seg, height=270)
    st.plotly_chart(fig_seg, use_container_width=True)

    # Row 2: Average Shipping Days by Ship Mode | Order Count by Payment Mode
    p2_col1, p2_col2 = st.columns(2)

    with p2_col1:
        st.markdown(
            f"""
            <div class="chart-card">
                <div class="chart-header">
                    <h3 class="chart-title">{"متوسط أيام الشحن حسب طريقة الشحن" if is_ar else "Average Shipping Days by Ship Mode"}</h3>
                    <span class="chart-subtitle">{"by Ship Mode" if not is_ar else "مؤشر سرعة التوصيل بالأيام"}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        ship_stats = df.groupby("Ship Mode")["Shipping Days"].mean().reset_index()
        # Sort in standard order
        ship_order = ["Standard Class", "Second Class", "First Class", "Same Day"]
        ship_stats["Ship Mode"] = pd.Categorical(ship_stats["Ship Mode"], categories=ship_order, ordered=True)
        ship_stats = ship_stats.sort_values("Ship Mode")

        fig_ship = go.Figure(go.Bar(
            x=ship_stats["Ship Mode"],
            y=ship_stats["Shipping Days"],
            marker=dict(
                color=["#fb7185", "#f7c948", "#c084fc", "#22d3ee"][:len(ship_stats)],
                line=dict(color="rgba(255,255,255,0.2)", width=1)
            ),
            text=[f"{d:.1f} days" for d in ship_stats["Shipping Days"]],
            textposition="auto",
            textfont=dict(color="#ffffff", size=12, weight="bold"),
            hovertemplate="<b>%{x}</b><br>Average Days: %{y:.2f} days<extra></extra>"
        ))
        # Add target line
        fig_ship.add_hline(y=3.0, line_dash="dash", line_color="#22d3ee", annotation_text="Benchmark (3d)", annotation_position="top right", annotation_font_color="#22d3ee")
        apply_chart_theme(fig_ship, height=280)
        st.plotly_chart(fig_ship, use_container_width=True)

    with p2_col2:
        st.markdown(
            f"""
            <div class="chart-card">
                <div class="chart-header">
                    <h3 class="chart-title">{"عدد الطلبات حسب طريقة الدفع" if is_ar else "Order Count by Payment Mode"}</h3>
                    <span class="chart-subtitle">{"by Payment Mode" if not is_ar else "COD vs Online vs Cards"}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        pay_stats = df.groupby("Payment Mode")["Order ID"].nunique().reset_index()
        fig_pay = go.Figure(data=[go.Pie(
            labels=pay_stats["Payment Mode"],
            values=pay_stats["Order ID"],
            hole=0.6,
            marker=dict(colors=["#8b6bd8", "#fb7185", "#f7c948"], line=dict(color="#150729", width=2)),
            textinfo="percent+label",
            textfont=dict(size=12, color="#ffffff", weight="bold"),
            hovertemplate="<b>%{label}</b><br>Orders: %{value:,}<br>Share: %{percent}<extra></extra>"
        )])
        fig_pay.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color="#c4b5fd", size=11))
        )
        apply_chart_theme(fig_pay, height=280)
        st.plotly_chart(fig_pay, use_container_width=True)

    # Bonus Executive Chart: Monthly Sales & Profit Performance
    st.markdown(
        f"""
        <div class="chart-card">
            <div class="chart-header">
                <h3 class="chart-title">{"المسار الزمني الشهري للمبيعات والأرباح" if is_ar else "Monthly Revenue & Profit Growth Trend"}</h3>
                <span class="chart-subtitle">{"2019 - 2020 Performance" if not is_ar else "أداء المبيعات والأرباح شهرياً"}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    monthly_df = df.groupby("YearMonth").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    ).reset_index().sort_values("YearMonth")

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(
        x=monthly_df["YearMonth"],
        y=monthly_df["Sales"],
        name="Sales ($)",
        marker_color="rgba(192, 132, 252, 0.45)",
        marker_line_color="#c084fc",
        marker_line_width=1,
        hovertemplate="Sales: $%{y:,.0f}<extra></extra>"
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly_df["YearMonth"],
        y=monthly_df["Profit"],
        name="Profit ($)",
        mode="lines+markers",
        line=dict(color="#fb7185", width=3),
        marker=dict(size=8, color="#fb7185"),
        hovertemplate="Profit: $%{y:,.0f}<extra></extra>"
    ))
    fig_trend.update_layout(
        barmode="overlay",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#c4b5fd")),
    )
    apply_chart_theme(fig_trend, height=280)
    st.plotly_chart(fig_trend, use_container_width=True)

# =========================================================
# TAB 3: Geographic Map (Original Power BI Filled Map)
# =========================================================
with tab3:
    st.markdown(
        f"""
        <div class="chart-card">
            <div class="chart-header">
                <h3 class="chart-title">{"الخريطة التفاعلية لأرباح ومبيعات الولايات الأمريكية (Filled Map)" if is_ar else "US States Interactive Map (Profit & Sales Density)"}</h3>
                <span class="chart-subtitle">{"Choropleth Analytics" if not is_ar else "تحليل جغرافي متكامل بمطابقة Power BI"}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Aggregate by State
    state_geo = df.groupby("State").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Returns=("Is_Returned", "sum"),
        TotalItems=("Row ID+O6G3A1:R6", "count")
    ).reset_index()

    state_geo["State_Code"] = state_geo["State"].map(US_STATE_ABBR)
    state_geo["Profit_Margin"] = state_geo["Profit"] / state_geo["Sales"]
    state_geo["Return_Rate"] = state_geo["Returns"] / state_geo["TotalItems"]

    map_metric = st.radio(
        "المقياس المعروض على الخريطة / Display Metric on Map:" if is_ar else "Select Metric on Map:",
        ["Sum of Profit (الأرباح)", "Total Sales (المبيعات)", "Return Rate (معدل المرتجعات)"],
        horizontal=True
    )

    metric_col = "Profit" if "Profit" in map_metric else ("Sales" if "Sales" in map_metric else "Return_Rate")
    metric_label = "Profit ($)" if "Profit" in map_metric else ("Sales ($)" if "Sales" in map_metric else "Return Rate (%)")

    fig_map = px.choropleth(
        state_geo.dropna(subset=["State_Code"]),
        locations="State_Code",
        locationmode="USA-states",
        color=metric_col,
        scope="usa",
        color_continuous_scale=[[0, "#2c0f57"], [0.35, "#8b6bd8"], [0.7, "#f7c948"], [1, "#fb7185"]],
        hover_name="State",
        hover_data={
            "State_Code": False,
            "Sales": ":$,.0f",
            "Profit": ":$,.0f",
            "Profit_Margin": ":.2%",
            "Orders": ":,",
            "Returns": ":,"
        }
    )
    fig_map.update_layout(
        geo=dict(
            bgcolor="rgba(0,0,0,0)",
            lakecolor="#150729",
            landcolor="#250d47",
            subunitcolor="rgba(139, 107, 216, 0.4)",
            showlakes=True,
            showsubunits=True
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=10),
        height=520,
        coloraxis_colorbar=dict(
            title=dict(text=metric_label, font=dict(color="#fdf4ff")),
            tickfont=dict(color="#fdf4ff"),
            thickness=14
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Detailed Table for States
    with st.expander("📊 جدول أداء الولايات التفصيلي | State Performance Breakdown"):
        st.dataframe(
            state_geo[["State", "Sales", "Profit", "Profit_Margin", "Orders", "Returns", "Return_Rate"]]
            .sort_values("Profit", ascending=False)
            .style.format({
                "Sales": "${:,.2f}",
                "Profit": "${:,.2f}",
                "Profit_Margin": "{:.2%}",
                "Orders": "{:,}",
                "Returns": "{:,}",
                "Return_Rate": "{:.2%}"
            }),
            use_container_width=True,
            height=320
        )

# =========================================================
# TAB 4: Data Explorer & CSV Export
# =========================================================
with tab4:
    st.markdown(
        f"""
        <div class="chart-card">
            <div class="chart-header">
                <h3 class="chart-title">{"مستكشف البيانات وعمليات التصدير" if is_ar else "Data Explorer & Export Center"}</h3>
                <span class="chart-subtitle">{"Filtered Dataset" if not is_ar else "تصفية وفحص البيانات الخام وتنزيلها"}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    search_query = st.text_input("🔍 ابحث في المنتجات، العملاء، المدن أو معرف الطلب:" if is_ar else "🔍 Search Product, Customer, City, or Order ID:")
    
    display_df = df.copy()
    if search_query:
        mask = (
            display_df["Order ID"].astype(str).str.contains(search_query, case=False, na=False) |
            display_df["Customer Name"].astype(str).str.contains(search_query, case=False, na=False) |
            display_df["Product Name"].astype(str).str.contains(search_query, case=False, na=False) |
            display_df["City"].astype(str).str.contains(search_query, case=False, na=False) |
            display_df["State"].astype(str).str.contains(search_query, case=False, na=False)
        )
        display_df = display_df[mask]

    cols_to_show = [
        "Order ID", "Order Date", "Ship Date", "Shipping Days", "Ship Mode",
        "Customer Name", "Segment", "City", "State", "Region",
        "Category", "Sub-Category", "Product Name", "Sales", "Quantity",
        "Profit", "Is_Returned", "Payment Mode"
    ]
    
    st.dataframe(
        display_df[cols_to_show].head(1000).style.format({
            "Sales": "${:,.2f}",
            "Profit": "${:,.2f}",
            "Order Date": lambda t: t.strftime("%Y-%m-%d") if pd.notna(t) else "",
            "Ship Date": lambda t: t.strftime("%Y-%m-%d") if pd.notna(t) else ""
        }),
        use_container_width=True,
        height=450
    )
    
    # Download Button
    csv_bytes = display_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥 تحميل البيانات المفلترة كملف CSV" if is_ar else "📥 Download Filtered Data as CSV",
        data=csv_bytes,
        file_name=f"superstore_analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown(
    f"""
    <div style="text-align:center; padding:24px 0 10px 0; color:#c4b5fd; font-size:12px; border-top:1px solid rgba(139,107,216,0.2); margin-top:30px;" dir="{'rtl' if is_ar else 'ltr'}">
        ✨ <b>SuperStore Intelligence Platform</b> — {"تم تطويره بواسطة Streamlit & Plotly بمطابقة كاملة لتقرير Power BI" if is_ar else "Built with Streamlit & Plotly matching Power BI Sunset Vibrant theme specifications"}
    </div>
    """,
    unsafe_allow_html=True
)
