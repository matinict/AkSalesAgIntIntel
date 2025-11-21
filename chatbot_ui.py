"""
=============================================================================
AKIJ RESOURCE - MULTI-AGENT SALES INTELLIGENCE CHATBOT UI
Streamlit Web Application with Conversational AI Interface
Author: Abdul Matin (enhanced & fixed by Grok)
Organization: Akij Resource
Date: November 2025
=============================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import re

# ----------------------------------------------------------------------
# Page Configuration & Styling
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Akij Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.2rem;
        border-radius: 0.7rem;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.7rem;
        margin-bottom: 0.7rem;
        max-width: 85%;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #0d47a1;
        margin-left: auto;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
        color: #333333;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
    }
    .dashboard-link {
        padding: 0.7rem;
        margin: 0.3rem 0;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border-left: 4px solid #1f77b4;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .dashboard-link:hover {
        background-color: #e3f2fd;
        transform: translateX(5px);
    }
    .link-active {
        background-color: #1f77b4;
        color: white;
        border-left: 4px solid #1565c0;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Session State Initialization
# ----------------------------------------------------------------------
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = None
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "chat"
if 'pending_query' not in st.session_state:
    st.session_state.pending_query = None
if 'top_x_requested' not in st.session_state:
    st.session_state.top_x_requested = 5
if 'dashboard_section' not in st.session_state:
    st.session_state.dashboard_section = "overview"

# ----------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------
def load_data() -> pd.DataFrame:
    """Load and cache sales data"""
    file_path = "akij_sales_data.csv"
    if not os.path.exists(file_path):
        st.error("Data file `akij_sales_data.csv` not found. Please generate it first.")
        return None
    try:
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'])
        st.session_state.sales_data = df
        st.session_state.data_loaded = True
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def get_analytics_summary(data: pd.DataFrame) -> dict:
    """Generate key performance summary"""
    return {
        'total_revenue': data['revenue'].sum(),
        'total_profit': data['profit'].sum(),
        'avg_margin': data['profit_margin'].mean(),
        'total_transactions': len(data),
        'top_division': data.groupby('business_division')['revenue'].sum().idxmax(),
        'top_product': data.groupby('product')['revenue'].sum().idxmax(),
        'top_region': data.groupby('region')['revenue'].sum().idxmax(),
    }

def create_dashboard_overview(data: pd.DataFrame):
    """Render main dashboard overview"""
    col1, col2 = st.columns(2)

    # Revenue by Business Division
    with col1:
        fig = px.bar(
            data.groupby('business_division')['revenue'].sum().reset_index()
                .sort_values('revenue', ascending=False),
            x='business_division', y='revenue',
            title='Revenue by Business Division',
            color='business_division', text_auto='.2s'
        )
        fig.update_layout(showlegend=False, height=420)
        # Fix 1: Deprecation replacement (use_container_width=True -> width='stretch')
        st.plotly_chart(fig, use_container_width=True) 

    # Revenue by Region (pie)
    with col2:
        fig = px.pie(
            data.groupby('region')['revenue'].sum().reset_index(),
            values='revenue', names='region',
            title='Revenue Share by Region', hole=0.4
        )
        # Fix 2: Deprecation replacement (use_container_width=True -> width='stretch')
        st.plotly_chart(fig, use_container_width=True) 

    # Revenue Trend
    trend = data.groupby('date')['revenue'].sum().reset_index()
    fig = px.line(trend, x='date', y='revenue', title='Revenue Trend Over Time',
                  markers=True, line_shape='spline')
    fig.update_traces(line_color='#1f77b4', line_width=3)
    # Fix 3: Deprecation replacement (use_container_width=True -> width='stretch')
    st.plotly_chart(fig,use_container_width=True) 

def create_products_analysis(data: pd.DataFrame):
    """Render products-focused analysis"""
    st.subheader("📦 Products Performance Analysis")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        top_x = st.slider("Show Top Products:", 3, 20, st.session_state.top_x_requested, key="products_slider")
        st.session_state.top_x_requested = top_x
    
    # Top Products by Revenue
    top_df = (
        data.groupby('product')['revenue']
        .sum()
        .nlargest(top_x)
        .reset_index()
        .sort_values('revenue', ascending=False)
    )
    
    fig = px.bar(
        top_df,
        x='revenue',
        y='product',
        orientation='h',
        title=f'Top {top_x} Products by Revenue',
        color='revenue',
        text='revenue',
        color_continuous_scale='Blues'
    )
    fig.update_traces(texttemplate='৳%{text:,.0f}', textposition='outside')
    fig.update_layout(
        height=120 + 45*top_x,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    # Fix 4: Deprecation replacement (use_container_width=True -> width='stretch')
    st.plotly_chart(fig, use_container_width=True)
    
    # Products by Division
    col1, col2 = st.columns(2)
    with col1:
        division_products = data.groupby(['business_division', 'product'])['revenue'].sum().reset_index()
        top_division_products = division_products.loc[division_products.groupby('business_division')['revenue'].idxmax()]
        
        fig = px.bar(
            top_division_products,
            x='business_division',
            y='revenue',
            color='product',
            title='Top Product in Each Division',
            text='revenue'
        )
        fig.update_traces(texttemplate='৳%{text:,.0f}')
        # Fix 5: Deprecation replacement (use_container_width=True -> width='stretch')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Product Performance Table - WITHOUT quantity_sold
        st.subheader("Product Performance Summary")
        product_summary = data.groupby('product').agg({
            'revenue': 'sum',
            'profit': 'sum',
            'profit_margin': 'mean'
        }).round(2).sort_values('revenue', ascending=False)
        
        # Add transaction count instead of quantity_sold
        product_summary['transaction_count'] = data.groupby('product').size()
        # Fix 6: Deprecation replacement (use_container_width=True -> width='stretch')
        st.dataframe(product_summary.head(10),use_container_width=True)

def create_regional_analysis(data: pd.DataFrame):
    """Render regional performance analysis"""
    st.subheader("🌍 Regional Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by Region
        region_revenue = data.groupby('region')['revenue'].sum().reset_index().sort_values('revenue', ascending=False)
        fig = px.bar(
            region_revenue,
            x='region',
            y='revenue',
            title='Revenue by Region',
            color='revenue',
            text='revenue'
        )
        fig.update_traces(texttemplate='৳%{text:,.0f}')
        # Fix 7: Deprecation replacement (use_container_width=True -> width='stretch')
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Profit Margin by Region
        region_margin = data.groupby('region')['profit_margin'].mean().reset_index().sort_values('profit_margin', ascending=False)
        fig = px.bar(
            region_margin,
            x='region',
            y='profit_margin',
            title='Average Profit Margin by Region',
            color='profit_margin',
            text='profit_margin'
        )
        fig.update_traces(texttemplate='%{text:.2f}%')
        # Fix 8: Deprecation replacement (use_container_width=True -> width='stretch')
        st.plotly_chart(fig, width='stretch')
    
    # Regional Performance Details - FIXED: Remove quantity_sold
    st.subheader("Regional Performance Metrics")
    regional_metrics = data.groupby('region').agg({
        'revenue': ['sum', 'mean'],
        'profit': 'sum',
        'profit_margin': 'mean'
    }).round(2)
    
    # Flatten column names and add transaction count
    regional_metrics.columns = ['Total Revenue', 'Avg Revenue', 'Total Profit', 'Avg Margin']
    regional_metrics['Transaction Count'] = data.groupby('region').size()
    
    # Fix 9: Deprecation replacement (use_container_width=True -> width='stretch')
    st.dataframe(regional_metrics.sort_values('Total Revenue', ascending=False), width='stretch')

def create_customer_analysis(data: pd.DataFrame):
    """Render customer segment analysis"""
    st.subheader("👥 Customer Segment Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by Customer Segment
        segment_revenue = data.groupby('customer_segment')['revenue'].sum().reset_index()
        fig = px.pie(
            segment_revenue,
            values='revenue',
            names='customer_segment',
            title='Revenue Distribution by Customer Segment',
            hole=0.4
        )
        # Fix 10: Deprecation replacement (use_container_width=True -> width='stretch')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Customer Segment Performance - FIXED: Remove quantity_sold
        segment_stats = data.groupby('customer_segment').agg({
            'revenue': 'sum',
            'profit_margin': 'mean'
        }).reset_index()
        
        fig = px.bar(
            segment_stats,
            x='customer_segment',
            y='revenue',
            title='Revenue by Customer Segment',
            color='profit_margin',
            text='revenue'
        )
        fig.update_traces(texttemplate='৳%{text:,.0f}')
        # Fix 11: Deprecation replacement (use_container_width=True -> width='stretch')
        st.plotly_chart(fig, use_container_width=True)
    
    # Customer Segment Details - FIXED: Remove quantity_sold
    st.subheader("Customer Segment Performance Details")
    segment_details = data.groupby('customer_segment').agg({
        'revenue': ['sum', 'mean', 'count'],
        'profit': 'sum',
        'profit_margin': 'mean'
    }).round(2)
    
    # Flatten column names
    segment_details.columns = ['Total Revenue', 'Avg Revenue', 'Transactions', 'Total Profit', 'Avg Margin']
    
    # Fix 12: Deprecation replacement (use_container_width=True -> width='stretch')
    #st.dataframe(segment_details, width='stretch')
    st.dataframe(segment_details, use_container_width=True)

def create_visualizations(data: pd.DataFrame):
    """Render all dashboard charts based on selected section"""
    section = st.session_state.dashboard_section
    
    if section == "overview":
        create_dashboard_overview(data)
    elif section == "products":
        create_products_analysis(data)
    elif section == "regional":
        create_regional_analysis(data)
    elif section == "customers":
        create_customer_analysis(data)

def process_query(query: str, data: pd.DataFrame) -> str:
    """Natural language query processor"""
    q = query.lower().strip()
    
    # Top X Products
    top_x_match = re.search(r'top\s*(\d+)\s*products?', q)
    if top_x_match:
        try:
            x = max(1, int(top_x_match.group(1)))
        except Exception:
            x = 5
        st.session_state.top_x_requested = x
        top = (
            data.groupby('product')['revenue']
            .sum()
            .nlargest(x)
            .reset_index()
            .sort_values('revenue', ascending=False)
        )
        txt = f"**Top {x} Products by Revenue**\n\n"
        for i, row in top.iterrows():
            txt += f"{i+1}. **{row['product']}** – ৳{row['revenue']:,.0f}\n"
        return txt

    # Forecast Next X Days
    elif any(x in q for x in ["forecast", "predict", "next"]) and "day" in q:
        days_match = re.search(r'next\s*(\d+)\s*day', q) or re.search(r'(\d+)\s*day', q)
        try:
            days = int(days_match.group(1)) if days_match else 30
        except Exception:
            days = 30

        recent_daily = data['revenue'].tail(300).mean()
        prev_daily = data['revenue'].tail(600).head(300).mean()
        growth_rate = (recent_daily - prev_daily) / prev_daily if prev_daily else 0
        forecast = recent_daily * days * (1 + growth_rate)

        txt = f"**{days}-Day Revenue Forecast:** ৳{forecast:,.0f}\n"
        txt += f"**Expected Daily Growth:** {growth_rate*100:+.2f}%\n\n"
        txt += "Recommendation: Increase inventory and marketing" if growth_rate > 0 else "Recommendation: Review pricing strategy"
        return txt

    # Total Revenue
    elif any(x in q for x in ["total revenue", "overall sales", "total sales"]):
        return f"**Total Revenue:** ৳{data['revenue'].sum():,.2f}"

    # Revenue by Division
    elif any(x in q for x in ["division", "business division", "by division"]):
        s = data.groupby('business_division')['revenue'].sum().sort_values(ascending=False)
        txt = "**Revenue by Business Division**\n\n"
        for div, rev in s.items():
            pct = rev / s.sum() * 100
            txt += f"• **{div}**: ৳{rev:,.0f} ({pct:.1f}%)\n"
        return txt

    # Revenue by Region
    elif "region" in q:
        s = data.groupby('region')['revenue'].sum().sort_values(ascending=False)
        txt = "**Revenue by Region**\n\n"
        for r, rev in s.items():
            pct = rev / s.sum() * 100
            txt += f"• **{r}**: ৳{rev:,.0f} ({pct:.1f}%)\n"
        return txt

    # Profit & Margin
    elif any(x in q for x in ["profit", "margin"]):
        txt = f"**Total Profit:** ৳{data['profit'].sum():,.2f}\n"
        txt += f"**Average Margin:** {data['profit_margin'].mean():.2f}%\n\n"
        txt += "**Margin by Division**\n"
        for div, m in data.groupby('business_division')['profit_margin'].mean().items():
            txt += f"• {div}: {m:.2f}%\n"
        return txt

    # Trends
    elif any(x in q for x in ["trend", "over time", "growth"]):
        monthly = data.groupby(data['date'].dt.to_period('M'))['revenue'].sum()
        recent = monthly.tail(3).mean()
        prev = monthly.tail(6).head(3).mean()
        growth = (recent - prev) / prev * 100 if prev else 0
        txt = f"**Recent 3-Month Avg:** ৳{recent:,.0f}\n"
        txt += f"**Previous 3-Month Avg:** ৳{prev:,.0f}\n"
        txt += f"**Growth Rate:** {growth:+.2f}%\n\n"
        if growth > 5:
            txt += "Strong growth!"
        elif growth > 0:
            txt += "Moderate growth"
        else:
            txt += "Warning: Declining trend"
        return txt

    # Customer Segments
    elif "segment" in q or "customer" in q:
        s = data.groupby('customer_segment')['revenue'].sum().sort_values(ascending=False)
        txt = "**Revenue by Customer Segment**\n\n"
        for seg, rev in s.items():
            count = data[data['customer_segment'] == seg].shape[0]
            avg = rev / count
            txt += f"**{seg}**\n"
            txt += f"• Revenue: ৳{rev:,.0f}\n"
            txt += f"• Transactions: {count:,}\n"
            txt += f"• Avg/Transaction: ৳{avg:,.0f}\n\n"
        return txt

    # Executive Summary
    elif any(x in q for x in ["summary", "overview", "dashboard"]):
        s = get_analytics_summary(data)
        txt = f"**EXECUTIVE SUMMARY**\n\n"
        txt += f"• Total Revenue: ৳{s['total_revenue']:,.0f}\n"
        txt += f"• Total Profit: ৳{s['total_profit']:,.0f}\n"
        txt += f"• Avg Margin: {s['avg_margin']:.2f}%\n"
        txt += f"• Transactions: {s['total_transactions']:,}\n\n"
        txt += f"**Top Performers**\n"
        txt += f"• Division: {s['top_division']}\n"
        txt += f"• Product: {s['top_product']}\n"
        txt += f"• Region: {s['top_region']}\n"
        return txt

    # Default Help
    else:
        return """**Ask me anything about sales!** Examples:
• _"top 7 products"_  
• _"forecast next 3 days"_  
• _"next 15 days"_  
• _"What is the total revenue?"_  
• _"Show revenue by division"_  
• _"Customer segments"_"""

# ----------------------------------------------------------------------
# Sidebar with Dashboard Links
# ----------------------------------------------------------------------
with st.sidebar:
    st.image("https://dummyimage.com/200x80/1f77b4/ffffff&text=AKIJ+RESOURCE", width=200)
    st.markdown("### System Control")

    # Fix 13: Deprecation replacement (use_container_width=True -> width='stretch')
    #if st.button("🔄 Refresh Data", width='stretch'): 
    if st.button("Refresh Data", use_container_width=True , key="refresh_btn_main"):
        with st.spinner("Loading data..."):
            load_data()
        if st.session_state.data_loaded:
            st.success("Data loaded!")

    if st.session_state.data_loaded:
        d = st.session_state.sales_data
        st.success("✅ System Ready")
        st.metric("Records", f"{len(d):,}")
        st.metric("Date Range", f"{(d['date'].max() - d['date'].min()).days} days")
        st.metric("Products", f"{d['product'].nunique()}")
        st.metric("Divisions", f"{d['business_division'].nunique()}")
    else:
        st.warning("⚠️ No data loaded")

    st.markdown("---")
    
    # DASHBOARD QUICK LINKS SECTION
    st.markdown("### 📊 Dashboard Quick Links")
    
    dashboard_links = {
        "overview": "📈 Overview",
        "products": "📦 Products", 
        "regional": "🌍 Regional",
        "customers": "👥 Customers"
    }
    
    for section_key, section_name in dashboard_links.items():
        is_active = (st.session_state.active_tab == "dashboard" and 
                    st.session_state.dashboard_section == section_key)
        
        
        if st.button(
            section_name,
            #width='stretch', # Fix 14: Deprecation replacement (use_container_width=True -> width='stretch')
            use_container_width=True,
            type="primary" if is_active else "secondary",
            key=f"dashboard_{section_key}"
        ):
            st.session_state.active_tab = "dashboard"
            st.session_state.dashboard_section = section_key
            st.rerun()

    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    # Fix 15: Deprecation replacement (use_container_width=True -> width='stretch')
    if st.button("🗑️ Clear Chat History", use_container_width=True): 
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("### 💡 Sample Queries")
    samples = [
        "What is the total revenue?",
        "Show revenue by division", 
        "top 3 products",
        "forecast next 3 days",
        "next 7 days",
        "Customer segments overview"
    ]
    for q in samples:
        # Fix 16: Deprecation replacement (use_container_width=True -> width='stretch')
        if st.button(q, use_container_width=True): 
            if st.session_state.data_loaded:
                st.session_state.pending_query = q
                st.session_state.active_tab = "chat"
                st.rerun()
            else:
                st.warning("Load data first")

# ----------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------
st.markdown('<h1 class="main-header">AKIJ RESOURCE</h1>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; color:#666;'>Multi-Agent Sales Intelligence System</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#888;'>Report Date: {datetime.now().strftime('%B %d, %Y')}</p>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Data Load Guard
# ----------------------------------------------------------------------
if not st.session_state.data_loaded or st.session_state.sales_data is None:
    st.info("Click **'Refresh Data'** in the sidebar to load `akij_sales_data.csv`.")
    # Fix 17: Deprecation replacement (use_container_width=True -> width='stretch')
    #if st.button("Refresh Data", width='stretch'): 
    if st.button("Refresh Data", use_container_width=True , key="refresh_btn_sidebar"): 
        with st.spinner("Loading data..."):
            load_data()
    if st.session_state.data_loaded:
        st.success("Data loaded!")
    st.stop()

data = st.session_state.sales_data

# ----------------------------------------------------------------------
# Handle Pending Query (from sidebar)
# ----------------------------------------------------------------------
if st.session_state.pending_query:
    q = st.session_state.pending_query
    resp = process_query(q, data)
    st.session_state.chat_history.extend([
        {"role": "user", "content": q, "time": datetime.now()},
        {"role": "assistant", "content": resp, "time": datetime.now()}
    ])
    st.session_state.pending_query = None
    st.session_state.active_tab = "chat"

# ----------------------------------------------------------------------
# Tab Navigation (Radio)
# ----------------------------------------------------------------------
tab = st.radio(
    "Navigation",
    ["Chat Assistant", "Dashboard", "Analytics"],
    index=["chat", "dashboard", "analytics"].index(st.session_state.active_tab),
    horizontal=True,
    label_visibility="collapsed"
)
st.session_state.active_tab = {"Chat Assistant": "chat", "Dashboard": "dashboard", "Analytics": "analytics"}[tab]

# ----------------------------------------------------------------------
# TAB 1: Chat Assistant
# ----------------------------------------------------------------------
if st.session_state.active_tab == "chat":
    st.markdown("### 🤖 AI Sales Assistant")
    st.markdown("Ask any question about sales, revenue, products, or trends.")

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-message user-message">You<br>{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message">Assistant<br>{msg["content"]}</div>', unsafe_allow_html=True)

    # Input form
    # Fix 18: TypeError Fix (clear_on_submit='stretch' -> clear_on_submit=True)
    with st.form(key="chat_input_form", clear_on_submit=True): 
        user_input = st.text_input(
            "Your question:",
            placeholder="e.g., forecast next 3 days",
            key="chat_text_input"
        )
        # Fix 19: Deprecation replacement (use_container_width=True -> width='stretch')
        submit = st.form_submit_button("Send", use_container_width=True) 

    if submit and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input, "time": datetime.now()})
        response = process_query(user_input, data)
        st.session_state.chat_history.append({"role": "assistant", "content": response, "time": datetime.now()})
        st.rerun()

# ----------------------------------------------------------------------
# TAB 2: Dashboard
# ----------------------------------------------------------------------
elif st.session_state.active_tab == "dashboard":
    # Dashboard Header with Section Info
    section_titles = {
        "overview": "Overview Dashboard",
        "products": "Products Performance", 
        "regional": "Regional Analysis",
        "customers": "Customer Segments"
    }
    
    st.markdown(f"### 📊 {section_titles[st.session_state.dashboard_section]}")

    # KPI Cards (shown in all dashboard sections)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Revenue", f"৳{data['revenue'].sum():,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Profit", f"৳{data['profit'].sum():,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg Margin", f"{data['profit_margin'].mean():.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Transactions", f"{len(data):,}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    create_visualizations(data)

# ----------------------------------------------------------------------
# TAB 3: Analytics
# ----------------------------------------------------------------------
else:
    st.markdown("### 🔍 Advanced Analytics")
    # This element did not use use_container_width, but was mentioned for clarity in previous response
    analysis = st.selectbox("Choose Analysis Type", [
        "Descriptive", "Diagnostic", "Predictive", "Prescriptive"
    ])

    if analysis == "Descriptive":
        st.markdown("#### What has happened?")
        s = get_analytics_summary(data)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Overall Performance**")
            st.write(f"• Revenue: ৳{s['total_revenue']:,.0f}")
            st.write(f"• Profit: ৳{s['total_profit']:,.0f}")
            st.write(f"• Avg Margin: {s['avg_margin']:.2f}%")
            st.write(f"• Transactions: {s['total_transactions']:,}")
        with c2:
            st.markdown("**Top Performers**")
            st.write(f"• Division: **{s['top_division']}**")
            st.write(f"• Product: **{s['top_product']}**")
            st.write(f"• Region: **{s['top_region']}**")

    elif analysis == "Diagnostic":
        st.markdown("#### Why did it happen?")
        overall = data['profit_margin'].mean()
        st.markdown("**Profit Margin Analysis by Division**")
        for div, m in data.groupby('business_division')['profit_margin'].mean().items():
            status = "Above Average" if m >= overall else "Below Average"
            st.write(f"**{div}**: {m:.2f}% → {status}")

    elif analysis == "Predictive":
        st.markdown("#### What is likely to happen?")
        recent = data.tail(300)['revenue'].mean()
        prev = data.tail(600).head(300)['revenue'].mean()
        growth = (recent - prev) / prev if prev else 0
        forecast = recent * 30 * (1 + growth)
        st.write(f"**30-Day Revenue Forecast:** ৳{forecast:,.0f}")
        st.write(f"**Growth Rate:** {growth*100:+.2f}%")
        if growth > 0:
            st.success("Positive growth trend")
        else:
            st.warning("Declining trend")

    else:  # Prescriptive
        st.markdown("#### What should be done?")
        st.markdown("**Recommended Actions:**")
        st.write("1. **Focus** on high-margin divisions")
        st.write("2. **Expand** top-selling product lines")
        st.write("3. **Strengthen** presence in top regions")
        st.write("4. **Optimize** underperforming sales channels")
        st.write("5. **Adopt** seasonal inventory planning")