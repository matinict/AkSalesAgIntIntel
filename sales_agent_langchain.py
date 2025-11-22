“””
LangChain Multi-Agent Sales Intelligence System
Converts the original custom agent architecture to LangChain-based implementation
“””

# ======================================================================

# SECTION 1: DEPENDENCIES

# ======================================================================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import warnings
warnings.filterwarnings(‘ignore’)

# LangChain Core

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool, StructuredTool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough

# For multi-agent orchestration

from langchain.agents import AgentType, initialize_agent

print(“✅ LangChain dependencies loaded successfully”)

# ======================================================================

# SECTION 2: DATA GENERATION (Same as original)

# ======================================================================

class SalesDataGenerator:
“”“Generate realistic sales dataset with complete Akij Resource product portfolio”””

```
@staticmethod
def generate_sales_data(num_records: int = 4000) -> pd.DataFrame:
    np.random.seed(42)
    
    # Complete Akij Resource Product Portfolio
    akij_products = {
        'Beverages & Food': [
            'Mojo', 'Frutika (Juice)', 'Speed (Energy Drink)', 'Clemon', 'Twing', 'Lemu',
            'Royal Tiger', 'Spa Drinking Water', 'Yummy Lassi', 'Farm Fresh Milk (UHT)',
            'Farm Fresh Ghee', 'Akij Daily Spices', 'Akij Daily Edible Oil', 'Akij Tea',
            'Aafi Snacks (Chanachur)', "O'Potato Chips", 'Happy Times Jam',
            "Bakeman's Biscuits", 'Funtastic Chocolate', 'Akij Flour (Atta)',
            'Akij Maida', 'Akij Suji', 'Akij Muri (Puffed Rice)', 'Essential Chinigura Rice',
            'Akij Bakers Bread', 'Akij Bakers Bun', 'Akij Bakers Cake'
        ],
        'Building & Construction': [
            'Akij Cement (PCC/CEM-I)', 'Akij Ceramics Tiles (Wall/Floor/Stair)',
            'Kathena Tiles', 'Sierra Tiles', 'Espacio Tiles', 'Rosa Sanitaryware',
            'Akij Board (Particle Board/MDF)', 'Akij Door (Laminated)', 'Akij Door (Solid)',
            'Akij Pipes & Fittings', 'Akij Buildtech', 'Akij Rebar (TMT)'
        ],
        'FMCG & Household': [
            'Max Wash Detergent Powder', 'Dish Master (Liquid)', 'Dish Master (Bar)',
            'Fantastik Air Freshener', 'H&H Hand Wash', 'Mum Mum Baby Diaper',
            'Akij Daily Home Care Products', 'Akij Plastics Furniture',
            'Akij Plastics Household Items'
        ],
        'Industrial & Other': [
            'Akij Jute Yarn', 'Akij Jute Sacks', 'Akij Textile Woven Fabric',
            'Akij Textile Denim', 'Akij Tableware (Porcelain)',
            'Akij Motors Electric Bike', 'Akij Motors Three-Wheeler',
            'AKIJ Power Light LED Bulb', 'AKIJ Fan (Ceiling Fan)',
            'AKIJ AURA Switch', 'AKIJ DELIGHT Socket', 'Akij Electrical Cables',
            'AKIJ Circuit Breaker (MCB)', 'Akij BIAX Films (BOPET)',
            'Akij BIAX Films (CPP)', 'Akij Printing & Packaging',
            'Akij Pharma Medicine', 'Akij Footwear', 'BONN Bicycle', "B'FIRE Bicycle"
        ]
    }
    
    regions = ['Dhaka', 'Chittagong', 'Sylhet', 'Rajshahi', 'Khulna', 'Barisal', 'Rangpur', 'Mymensingh']
    customer_segments = ['Retail', 'Wholesale', 'Corporate', 'E-commerce']
    sales_channels = ['Direct Sales', 'Distributor', 'Online', 'Retail Partner']
    
    # Flatten products with division mapping
    all_products = []
    product_to_division = {}
    for division, products in akij_products.items():
        all_products.extend(products)
        for product in products:
            product_to_division[product] = division
    
    # Generate dates (2 years)
    start_date = datetime.now() - timedelta(days=730)
    dates = [start_date + timedelta(days=x) for x in range(730)]
    
    records = []
    for i in range(num_records):
        product = np.random.choice(all_products)
        division = product_to_division[product]
        date = np.random.choice(dates)
        quantity = np.random.randint(1, 100)
        unit_price = np.random.uniform(50, 5000)
        revenue = quantity * unit_price
        cost = revenue * np.random.uniform(0.5, 0.8)
        profit = revenue - cost
        profit_margin = (profit / revenue) * 100
        
        records.append({
            'transaction_id': f'TXN{i+1:06d}',
            'date': date,
            'product': product,
            'business_division': division,
            'region': np.random.choice(regions),
            'customer_segment': np.random.choice(customer_segments),
            'sales_channel': np.random.choice(sales_channels),
            'quantity': quantity,
            'unit_price': round(unit_price, 2),
            'revenue': round(revenue, 2),
            'cost': round(cost, 2),
            'profit': round(profit, 2),
            'profit_margin': round(profit_margin, 2),
            'month': date.strftime('%Y-%m'),
            'quarter': f"Q{(date.month-1)//3 + 1}-{date.year}",
            'year': date.year
        })
    
    return pd.DataFrame(records)
```

# Generate data

print(”\n🔄 Generating sales data…”)
sales_data = SalesDataGenerator.generate_sales_data(num_records=4000)
print(f”✅ Generated {len(sales_data):,} sales transactions”)

# ======================================================================

# SECTION 3: LANGCHAIN TOOLS (Analytics Functions as Tools)

# ======================================================================

@tool
def descriptive_analytics(query: str) -> str:
“””
Analyzes historical sales data to answer: ‘What happened?’
Provides overall metrics, trends, top performers, and hierarchical breakdowns.
Use this for queries about past performance, revenue totals, top products, regional performance, etc.

```
Args:
    query: User's question about historical performance

Returns:
    Comprehensive descriptive analysis in JSON format
"""
data = sales_data.copy()
data['date'] = pd.to_datetime(data['date'])

# Overall metrics
total_revenue = float(data['revenue'].sum())
total_profit = float(data['profit'].sum())
total_transactions = len(data)
avg_transaction_value = float(data['revenue'].mean())
avg_profit_margin = float(data['profit_margin'].mean())

# Top performers
top_division = data.groupby('business_division')['revenue'].sum().idxmax()
top_product = data.groupby('product')['revenue'].sum().idxmax()
top_region = data.groupby('region')['revenue'].sum().idxmax()

# Division breakdown
division_revenue = data.groupby('business_division')['revenue'].sum().to_dict()

# Monthly trends
monthly_revenue = data.groupby('month')['revenue'].sum().sort_index().tail(6).to_dict()

result = {
    "type": "descriptive_analytics",
    "overall_metrics": {
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2),
        "total_transactions": total_transactions,
        "avg_transaction_value": round(avg_transaction_value, 2),
        "avg_profit_margin": round(avg_profit_margin, 2)
    },
    "top_performers": {
        "division": top_division,
        "product": top_product,
        "region": top_region
    },
    "division_breakdown": {k: round(v, 2) for k, v in division_revenue.items()},
    "monthly_trends_last_6": {k: round(v, 2) for k, v in monthly_revenue.items()}
}

return json.dumps(result, indent=2)
```

@tool
def diagnostic_analytics(query: str) -> str:
“””
Explains WHY performance changed. Performs root-cause analysis.
Identifies underperforming divisions, channel efficiency issues, regional disparities, and correlations.
Use this for queries about reasons for changes, performance drops, or comparative analysis.

```
Args:
    query: User's question about why something happened

Returns:
    Diagnostic analysis with root causes and insights
"""
data = sales_data.copy()

# Overall margin
overall_margin = data['profit_margin'].mean()

# Division performance
division_margins = data.groupby('business_division')['profit_margin'].mean()
underperforming = division_margins[division_margins < overall_margin].to_dict()

# Channel efficiency
channel_stats = data.groupby('sales_channel').agg({
    'revenue': 'sum',
    'profit': 'sum',
    'profit_margin': 'mean',
    'transaction_id': 'count'
}).to_dict()

# Regional disparity
region_revenue = data.groupby('region')['revenue'].sum()
disparity_score = region_revenue.std() / region_revenue.mean()

# Correlations
numeric_cols = ['revenue', 'profit', 'quantity', 'unit_price', 'profit_margin']
correlations = data[numeric_cols].corr()['revenue'].drop('revenue').to_dict()

result = {
    "type": "diagnostic_analytics",
    "underperforming_divisions": {k: round(v, 2) for k, v in underperforming.items()},
    "overall_margin": round(overall_margin, 2),
    "channel_efficiency": channel_stats,
    "regional_disparity_score": round(disparity_score, 3),
    "key_correlations": {k: round(v, 3) for k, v in correlations.items()},
    "insights": [
        f"Regional disparity score: {disparity_score:.3f} ({'High' if disparity_score > 0.3 else 'Moderate'})",
        f"{len(underperforming)} divisions underperforming vs overall margin"
    ]
}

return json.dumps(result, indent=2)
```

@tool
def predictive_analytics(query: str) -> str:
“””
Forecasts future performance. Predicts revenue trends and growth rates.
Use this for queries about future expectations, forecasts, predictions, or ‘what will happen’.

```
Args:
    query: User's question about future performance

Returns:
    Predictive forecast with growth rates and trends
"""
data = sales_data.copy()
data = data.sort_values('date')

# Calculate growth rate
recent_avg = data.tail(300)['revenue'].mean()
previous_avg = data.head(300)['revenue'].mean()
growth_rate = (recent_avg - previous_avg) / previous_avg

# Overall forecast (30 days)
last_week_avg = data.tail(70)['revenue'].mean()
predicted_daily = last_week_avg * (1 + growth_rate)
forecast_30days = predicted_daily * 30

# Division forecasts
division_forecasts = {}
for division in data['business_division'].unique():
    div_data = data[data['business_division'] == division]
    div_recent = div_data.tail(200)['revenue'].mean()
    div_previous = div_data.head(200)['revenue'].mean()
    div_growth = (div_recent - div_previous) / div_previous if div_previous > 0 else 0
    
    trend = "Growing" if div_growth > 0.05 else "Declining" if div_growth < -0.05 else "Stable"
    division_forecasts[division] = {
        "growth_rate": round(div_growth * 100, 2),
        "trend": trend
    }

result = {
    "type": "predictive_analytics",
    "overall_forecast": {
        "predicted_30day_revenue": round(forecast_30days, 2),
        "predicted_daily_revenue": round(predicted_daily, 2),
        "growth_rate_percent": round(growth_rate * 100, 2)
    },
    "division_forecasts": division_forecasts
}

return json.dumps(result, indent=2)
```

@tool
def prescriptive_analytics(query: str) -> str:
“””
Recommends actions based on all analytics. Provides immediate actions and strategic initiatives.
Use this for queries about what to do, recommendations, action plans, or strategy.

```
Args:
    query: User's question about what actions to take

Returns:
    Actionable recommendations with priorities and timelines
"""
# Run other analytics first
desc_result = json.loads(descriptive_analytics._run("summary"))
diag_result = json.loads(diagnostic_analytics._run("issues"))
pred_result = json.loads(predictive_analytics._run("forecast"))

immediate_actions = []
strategic_initiatives = []

# Generate actions based on insights
if diag_result.get('underperforming_divisions'):
    immediate_actions.append({
        "priority": "🔴 Critical",
        "action": f"Optimize {len(diag_result['underperforming_divisions'])} underperforming divisions",
        "timeline": "1-2 weeks",
        "expected_impact": "5-10% margin improvement"
    })

growth_rate = pred_result['overall_forecast']['growth_rate_percent']
if growth_rate > 5:
    immediate_actions.append({
        "priority": "🟢 High",
        "action": "Scale operations to meet growing demand",
        "timeline": "2-4 weeks",
        "expected_impact": "15-20% revenue capture"
    })
elif growth_rate < -5:
    immediate_actions.append({
        "priority": "🔴 Critical",
        "action": "Address declining sales trend immediately",
        "timeline": "Immediate",
        "expected_impact": "Prevent further decline"
    })

# Strategic initiatives
strategic_initiatives.append({
    "initiative": "Digital transformation of sales channels",
    "timeline": "6-12 months",
    "expected_impact": "25-30% efficiency gain"
})

if diag_result['regional_disparity_score'] > 0.3:
    strategic_initiatives.append({
        "initiative": "Market expansion in underserved regions",
        "timeline": "6-9 months",
        "expected_impact": "20% geographic diversification"
    })

result = {
    "type": "prescriptive_analytics",
    "immediate_actions": immediate_actions,
    "strategic_initiatives": strategic_initiatives
}

return json.dumps(result, indent=2)
```

@tool
def get_sales_summary(query: str) -> str:
“””
Quick summary of current sales status. Use for general questions or conversation starters.

```
Args:
    query: Any general question about sales

Returns:
    Quick summary of key metrics
"""
data = sales_data

summary = f"""
📊 AKIJ RESOURCE SALES SUMMARY (as of {datetime.now().strftime('%Y-%m-%d')})

Total Revenue: ৳{data['revenue'].sum():,.2f}
Total Profit: ৳{data['profit'].sum():,.2f}
Total Transactions: {len(data):,}
Average Margin: {data['profit_margin'].mean():.2f}%

Top Division: {data.groupby('business_division')['revenue'].sum().idxmax()}
Top Product: {data.groupby('product')['revenue'].sum().idxmax()}
Top Region: {data.groupby('region')['revenue'].sum().idxmax()}
"""

return summary.strip()
```

# ======================================================================

# SECTION 4: LANGCHAIN AGENT CREATION

# ======================================================================

# Initialize LLM

llm = ChatOpenAI(
model=“gpt-4”,
temperature=0,
# api_key=“your-api-key-here”  # Add your OpenAI API key
)

# Create tools list

tools = [
descriptive_analytics,
diagnostic_analytics,
predictive_analytics,
prescriptive_analytics,
get_sales_summary
]

# Create system prompt

system_prompt = “”“You are an expert sales analytics AI assistant for Akij Resource, a leading Bangladeshi conglomerate.

You have access to comprehensive sales data across 4 business divisions:

1. Beverages & Food
1. Building & Construction
1. FMCG & Household
1. Industrial & Other

Your capabilities:

- Descriptive Analytics: Analyze what happened (historical performance, trends, KPIs)
- Diagnostic Analytics: Explain why it happened (root causes, correlations, variances)
- Predictive Analytics: Forecast what will happen (revenue predictions, growth trends)
- Prescriptive Analytics: Recommend what to do (action plans, strategies)

Guidelines:

- Choose the right tool based on the user’s question type
- Provide clear, actionable insights
- Use data-driven reasoning
- Format responses professionally with proper currency (৳ for BDT)
- Always explain your reasoning

When users ask about:

- “What happened?” or “Show me…” → Use descriptive_analytics
- “Why did…” or “What caused…” → Use diagnostic_analytics
- “What will…” or “Forecast…” → Use predictive_analytics
- “What should…” or “Recommend…” → Use prescriptive_analytics
- General questions → Use get_sales_summary first
  “””

# Create prompt template

prompt = ChatPromptTemplate.from_messages([
(“system”, system_prompt),
MessagesPlaceholder(variable_name=“chat_history”, optional=True),
(“human”, “{input}”),
MessagesPlaceholder(variable_name=“agent_scratchpad”)
])

# Create agent

agent = create_openai_tools_agent(
llm=llm,
tools=tools,
prompt=prompt
)

# Create agent executor with memory

memory = ConversationBufferMemory(
memory_key=“chat_history”,
return_messages=True
)

agent_executor = AgentExecutor(
agent=agent,
tools=tools,
memory=memory,
verbose=True,
handle_parsing_errors=True,
max_iterations=5
)

print(”\n✅ LangChain Multi-Agent System Initialized!”)

# ======================================================================

# SECTION 5: EXAMPLE USAGE & CHAT INTERFACE

# ======================================================================

def query_agent(question: str) -> str:
“”“Query the multi-agent system”””
try:
response = agent_executor.invoke({“input”: question})
return response[‘output’]
except Exception as e:
return f”Error: {str(e)}”

# Example queries

example_queries = [
“What were our total sales last month?”,
“Why did the Building & Construction division underperform?”,
“What’s the revenue forecast for next quarter?”,
“What actions should we take to improve profitability?”,
“Show me the top 5 performing products”
]

print(”\n” + “=”*80)
print(“LANGCHAIN MULTI-AGENT SALES INTELLIGENCE SYSTEM”)
print(”=”*80)

print(”\n📝 Example Queries You Can Ask:”)
for i, q in enumerate(example_queries, 1):
print(f”   {i}. {q}”)

print(”\n💬 Interactive Chat Interface Ready!”)
print(”   Call: query_agent(‘your question here’)”)
print(”\n” + “=”*80)

# Demo query

print(”\n🔍 DEMO QUERY: ‘Give me a summary of our sales performance’\n”)
demo_response = query_agent(“Give me a summary of our sales performance”)
print(”\n📊 Response:”)
print(demo_response)