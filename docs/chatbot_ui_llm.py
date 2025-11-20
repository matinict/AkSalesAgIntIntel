"""
=============================================================================
AKIJ RESOURCE - MULTI-AGENT SALES INTELLIGENCE CHATBOT UI
Streamlit Web Application with Conversational AI Interface
Author: Abdul Matin
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
import ollama # <--- ADDED OLLAMA IMPORT

# --- OLLAMA CONFIGURATION ---
# Using 'gemma3:latest' as per your available models (ollama list)
OLLAMA_MODEL = "gemma3:latest" 
# ----------------------------

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
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #0d47a1;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
        color: #333333;
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
if 'dashboard_section' not in st.session_state:
    st.session_state.dashboard_section = "overview"

# ----------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------
def load_data() -> pd.DataFrame:
    """Load and cache sales data"""
    file_path = "akij_sales_data_complete.csv"
    if not os.path.exists(file_path):
        st.error(f"❌ Data file `{file_path}` not found. Please generate it first.")
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

    with col1:
        fig = px.bar(
            data.groupby('business_division')['revenue'].sum().reset_index().sort_values('revenue', ascending=False),
            x='business_division', y='revenue',
            title='Revenue by Business Division',
            color='business_division', text_auto='.2s'
        )
        fig.update_layout(showlegend=False, height=420)
        st.plotly_chart(fig, width='stretch') # REPLACED use_container_width
        
    with col2:
        fig = px.pie(
            data.groupby('region')['revenue'].sum().reset_index(),
            values='revenue', names='region',
            title='Revenue Share by Region', hole=0.4
        )
        st.plotly_chart(fig, width='stretch') # REPLACED use_container_width

    trend = data.groupby('date')['revenue'].sum().reset_index()
    fig = px.line(trend, x='date', y='revenue', title='Revenue Trend Over Time',
                  markers=True, line_shape='spline')
    fig.update_traces(line_color='#1f77b4', line_width=3)
    st.plotly_chart(fig, width='stretch') # REPLACED use_container_width

def create_products_analysis(data: pd.DataFrame):
    """Render products-focused analysis"""
    st.subheader("📦 Products Performance Analysis")
    
    top_x = st.slider("Show Top Products:", 3, 20, 10)
    
    top_df = data.groupby('product')['revenue'].sum().nlargest(top_x).reset_index().sort_values('revenue', ascending=False)
    
    fig = px.bar(
        top_df, x='revenue', y='product', orientation='h',
        title=f'Top {top_x} Products by Revenue',
        color='revenue', text='revenue',
        color_continuous_scale='Blues'
    )
    fig.update_traces(texttemplate='৳%{text:,.0f}', textposition='outside')
    fig.update_layout(height=120 + 45*top_x, showlegend=False, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, width='stretch') # REPLACED use_container_width
    
    col1, col2 = st.columns(2)
    
    with col1:
        division_products = data.groupby(['business_division', 'product'])['revenue'].sum().reset_index()
        top_division_products = division_products.loc[division_products.groupby('business_division')['revenue'].idxmax()]
        
        fig = px.bar(top_division_products, x='business_division', y='revenue',
                     color='product', title='Top Product in Each Division', text='revenue')
        fig.update_traces(texttemplate='৳%{text:,.0f}')
        st.plotly_chart(fig, width='stretch') # REPLACED use_container_width
    
    with col2:
        st.subheader("Product Performance")
        product_summary = data.groupby('product').agg({
            'revenue': 'sum',
            'profit': 'sum',
            'profit_margin': 'mean'
        }).round(2).sort_values('revenue', ascending=False)
        product_summary['transactions'] = data.groupby('product').size()
        st.dataframe(product_summary.head(10), width='stretch') # REPLACED use_container_width

def create_regional_analysis(data: pd.DataFrame):
    """Render regional performance analysis"""
    st.subheader("🌍 Regional Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        region_revenue = data.groupby('region')['revenue'].sum().reset_index().sort_values('revenue', ascending=False)
        fig = px.bar(region_revenue, x='region', y='revenue',
                     title='Revenue by Region', color='revenue', text='revenue')
        fig.update_traces(texttemplate='৳%{text:,.0f}')
        st.plotly_chart(fig, width='stretch') # REPLACED use_container_width
    
    with col2:
        region_margin = data.groupby('region')['profit_margin'].mean().reset_index().sort_values('profit_margin', ascending=False)
        fig = px.bar(region_margin, x='region', y='profit_margin',
                     title='Average Profit Margin by Region',
                     color='profit_margin', text='profit_margin')
        fig.update_traces(texttemplate='%{text:.2f}%')
        st.plotly_chart(fig, width='stretch') # REPLACED use_container_width
    
    st.subheader("Regional Metrics")
    regional_metrics = data.groupby('region').agg({
        'revenue': ['sum', 'mean'],
        'profit': 'sum',
        'profit_margin': 'mean'
    }).round(2)
    regional_metrics.columns = ['Total Revenue', 'Avg Revenue', 'Total Profit', 'Avg Margin']
    regional_metrics['Transactions'] = data.groupby('region').size()
    st.dataframe(regional_metrics.sort_values('Total Revenue', ascending=False), width='stretch') # REPLACED use_container_width

def create_customer_analysis(data: pd.DataFrame):
    """Render customer segment analysis"""
    st.subheader("👥 Customer Segment Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        segment_revenue = data.groupby('customer_segment')['revenue'].sum().reset_index()
        fig = px.pie(segment_revenue, values='revenue', names='customer_segment',
                     title='Revenue Distribution by Customer Segment', hole=0.4)
        st.plotly_chart(fig, width='stretch') # REPLACED use_container_width
    
    with col2:
        segment_stats = data.groupby('customer_segment').agg({
            'revenue': 'sum',
            'profit_margin': 'mean'
        }).reset_index()
        fig = px.bar(segment_stats, x='customer_segment', y='revenue',
                     title='Revenue by Customer Segment',
                     color='profit_margin', text='revenue')
        fig.update_traces(texttemplate='৳%{text:,.0f}')
        st.plotly_chart(fig, width='stretch') # REPLACED use_container_width
    
    st.subheader("Segment Details")
    segment_details = data.groupby('customer_segment').agg({
        'revenue': ['sum', 'mean', 'count'],
        'profit': 'sum',
        'profit_margin': 'mean'
    }).round(2)
    segment_details.columns = ['Total Revenue', 'Avg Revenue', 'Transactions', 'Total Profit', 'Avg Margin']
    st.dataframe(segment_details, width='stretch') # REPLACED use_container_width

def create_visualizations(data: pd.DataFrame):
    """Render dashboard based on selected section"""
    section = st.session_state.dashboard_section
    
    if section == "overview":
        create_dashboard_overview(data)
    elif section == "products":
        create_products_analysis(data)
    elif section == "regional":
        create_regional_analysis(data)
    elif section == "customers":
        create_customer_analysis(data)

# ----------------------------------------------------------------------
# OLLAMA LLM INTEGRATION FUNCTION (Replaced old rule-based function)
# ----------------------------------------------------------------------
def process_query(query: str, history: list) -> str:
    """
    Sends query to Ollama LLM with system context and chat history 
    for contextual and generative responses.
    """

    # 1. System Prompt to provide context and define the LLM persona/role
    system_prompt = (
        "You are an expert Sales Intelligence Assistant for AKIJ RESOURCE. "
        "Your role is to analyze sales data and answer user questions concisely and professionally. "
        "The current date is {current_date}. "
        "Do not invent facts or numbers. If you don't have the specific data, politely state that you cannot fulfill the request. "
        "Keep your responses focused on sales, revenue, profit, and trends."
    ).format(current_date=datetime.now().strftime('%Y-%m-%d'))

    # 2. Format messages for Ollama API
    messages = [{"role": "system", "content": system_prompt}]
    
    # Append existing chat history
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
        
    # Append the new user query
    messages.append({"role": "user", "content": query})
    
    # 3. Call Ollama API
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL, 
            messages=messages, 
            stream=False # Using non-streaming for simpler integration with current UI logic
        )
        
        # 4. Extract content
        return response['message']['content']

    except Exception as e:
        return f"🚨 **Ollama Error:** Could not connect to the model (`{OLLAMA_MODEL}`). Ensure Ollama is running (`ollama serve`) and the model is pulled (`ollama pull {OLLAMA_MODEL}`). Error: {e}"
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")

    if st.button("🔄 Load Data", width='stretch'): # REPLACED use_container_width
        with st.spinner("Loading..."):
            load_data()
        if st.session_state.data_loaded:
            st.success("✅ Data loaded!")

    if st.session_state.data_loaded:
        d = st.session_state.sales_data
        st.success("✅ System Ready (Ollama: " + OLLAMA_MODEL + ")") # Display model name
        st.metric("Records", f"{len(d):,}")
        st.metric("Date Range", f"{(d['date'].max() - d['date'].min()).days} days")
    else:
        st.warning("⚠️ No data loaded")

    st.markdown("---")
    st.markdown("### 📊 Dashboard Sections")
    
    sections = {
        "overview": "📈 Overview",
        "products": "📦 Products",
        "regional": "🌍 Regional",
        "customers": "👥 Customers"
    }
    
    for key, name in sections.items():
        is_active = (st.session_state.active_tab == "dashboard" and 
                    st.session_state.dashboard_section == key)
        
        if st.button(name, width='stretch', # REPLACED use_container_width
                    type="primary" if is_active else "secondary", key=f"sec_{key}"):
            st.session_state.active_tab = "dashboard"
            st.session_state.dashboard_section = key
            st.rerun()

    st.markdown("---")
    st.markdown("### 💡 Sample Queries")
    samples = [
        "What is the total revenue?",
        "top 5 products",
        "Explain the regional performance trends in Bangladesh.",
        "Give me a summary of the sales data"
    ]
    
    for q in samples:
        if st.button(q, width='stretch', key=f"sample_{q}"): # REPLACED use_container_width
            if st.session_state.data_loaded:
                st.session_state.pending_query = q
                st.session_state.active_tab = "chat"
                st.rerun()

# ----------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------
st.markdown('<h1 class="main-header">AKIJ RESOURCE</h1>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; color:#666;'>Multi-Agent Sales Intelligence</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#888;'>{datetime.now().strftime('%B %d, %Y')}</p>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Data Load Check
# ----------------------------------------------------------------------
if not st.session_state.data_loaded:
    st.info("👆 Click **'Load Data'** in sidebar to start")
    st.stop()

data = st.session_state.sales_data

# Handle pending query (e.g., from sidebar sample buttons)
if st.session_state.pending_query:
    q = st.session_state.pending_query
    
    # Use the existing chat history (before adding the pending query)
    history_for_llm = st.session_state.chat_history.copy()
    
    # NEW CALL SITE: Use the Ollama function
    with st.spinner(f"Querying {OLLAMA_MODEL}..."):
        # The new function only needs the query and the existing history
        resp = process_query(q, history_for_llm) 

    st.session_state.chat_history.extend([
        {"role": "user", "content": q},
        {"role": "assistant", "content": resp}
    ])
    st.session_state.pending_query = None

# ----------------------------------------------------------------------
# Tab Navigation
# ----------------------------------------------------------------------
tab = st.radio(
    "Navigation",
    ["💬 Chat", "📊 Dashboard", "📈 Analytics"],
    index=["chat", "dashboard", "analytics"].index(st.session_state.active_tab),
    horizontal=True,
    label_visibility="collapsed"
)
st.session_state.active_tab = {"💬 Chat": "chat", "📊 Dashboard": "dashboard", "📈 Analytics": "analytics"}[tab]

# ----------------------------------------------------------------------
# TAB 1: Chat
# ----------------------------------------------------------------------
if st.session_state.active_tab == "chat":
    st.markdown("### 🤖 AI Sales Assistant")

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">**You:** {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message">**Assistant:**\n\n{msg["content"]}</div>', unsafe_allow_html=True)

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask a question:", placeholder="e.g., top 5 products, Explain regional trends.")
        submit = st.form_submit_button("Send", width='stretch') # REPLACED use_container_width

    if submit and user_input.strip():
        # Append user message immediately
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # NEW CALL SITE: Use the Ollama function
        with st.spinner(f"Querying {OLLAMA_MODEL}..."):
            # Pass the new user input, and all messages *before* the latest one as history
            history_for_llm = st.session_state.chat_history[:-1]
            response = process_query(user_input, history_for_llm)
            
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

# ----------------------------------------------------------------------
# TAB 2: Dashboard
# ----------------------------------------------------------------------
elif st.session_state.active_tab == "dashboard":
    section_titles = {
        "overview": "Overview",
        "products": "Products Performance",
        "regional": "Regional Analysis",
        "customers": "Customer Segments"
    }
    
    st.markdown(f"### 📊 {section_titles[st.session_state.dashboard_section]}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Revenue", f"৳{data['revenue'].sum():,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Profit", f"৳{data['profit'].sum():,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Margin", f"{data['profit_margin'].mean():.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Records", f"{len(data):,}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    create_visualizations(data)

# ----------------------------------------------------------------------
# TAB 3: Analytics
# ----------------------------------------------------------------------
else:
    st.markdown("### 📈 Advanced Analytics")
    
    analysis = st.selectbox("Analysis Type", ["Descriptive", "Diagnostic", "Predictive", "Prescriptive"])

    if analysis == "Descriptive":
        st.markdown("#### What has happened?")
        s = get_analytics_summary(data)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Performance**")
            st.write(f"• Revenue: ৳{s['total_revenue']:,.0f}")
            st.write(f"• Profit: ৳{s['total_profit']:,.0f}")
            st.write(f"• Margin: {s['avg_margin']:.2f}%")
        
        with col2:
            st.markdown("**Top Performers**")
            st.write(f"• Division: **{s['top_division']}**")
            st.write(f"• Product: **{s['top_product']}**")
            st.write(f"• Region: **{s['top_region']}**")

    elif analysis == "Diagnostic":
        st.markdown("#### Why did it happen?")
        overall = data['profit_margin'].mean()
        st.markdown("**Margin Analysis**")
        for div, m in data.groupby('business_division')['profit_margin'].mean().items():
            status = "✅ Above Average" if m >= overall else "⚠️ Below Average"
            st.write(f"**{div}**: {m:.2f}% — {status}")

    elif analysis == "Predictive":
        st.markdown("#### What is likely to happen?")
        recent = data.tail(300)['revenue'].mean()
        prev = data.tail(600).head(300)['revenue'].mean()
        growth = (recent - prev) / prev if prev else 0
        forecast = recent * 30 * (1 + growth)
        
        st.write(f"**30-Day Forecast:** ৳{forecast:,.0f}")
        st.write(f"**Growth Rate:** {growth*100:+.2f}%")
        
        if growth > 0:
            st.success("📈 Positive growth trend")
        else:
            st.warning("📉 Declining trend")

    else:
        st.markdown("#### What should be done?")
        st.markdown("**Recommendations:**")
        st.write("1. Focus on high-margin divisions")
        st.write("2. Expand top-selling products")
        st.write("3. Strengthen top regions")
        st.write("4. Optimize underperforming channels")