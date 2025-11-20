"""
Multi-Agent Sales Intelligence System - Akij Resource
Author: Abdul Matin | Date: November 2025
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# DATA GENERATOR
# ============================================================================

class SalesDataGenerator:
    """Generate synthetic sales data with Akij product portfolio"""
    
    PRODUCTS = {
        'Beverages & Food': ['Mojo', 'Frutika (Juice)', 'Speed (Energy Drink)', 'Clemon', 
                             'Spa Drinking Water', 'Farm Fresh Milk (UHT)', 'Akij Tea', 
                             'Akij Flour (Atta)', 'Essential Chinigura Rice'],
        'Building & Construction': ['Akij Cement (PCC/CEM-I)', 'Akij Ceramics Tiles', 
                                    'Rosa Sanitaryware', 'Akij Door (Laminated)', 
                                    'Akij Pipes & Fittings'],
        'FMCG & Household': ['Max Wash Detergent', 'Dish Master', 'Fantastik Air Freshener', 
                             'H&H Hand Wash', 'Akij Plastics Furniture'],
        'Industrial & Other': ['Akij Jute Yarn', 'Akij Textile Fabric', 'Akij Motors Electric Bike', 
                               'AKIJ Power Light LED', 'Akij Pharma Medicine']
    }
    
    SEGMENTS = ['Enterprise', 'SMB', 'Individual', 'Government', 'Retail Distributor', 'Wholesaler']
    REGIONS = ['Dhaka', 'Chittagong', 'Rangpur', 'Khulna', 'Mymensingh', 'Rajshahi', 'Sylhet', 'Barisal']
    CHANNELS = ['Online', 'Retail Store', 'Wholesale', 'Direct Sales', 'Distributor Network']
    
    @classmethod
    def generate_sales_data(cls, num_records: int = 4000) -> pd.DataFrame:
        """Generate synthetic sales data"""
        np.random.seed(42)
        
        # Flatten products
        all_products = [p for products in cls.PRODUCTS.values() for p in products]
        product_to_division = {p: div for div, products in cls.PRODUCTS.items() for p in products}
        
        # Weights
        div_weights = {'Beverages & Food': 0.40, 'Building & Construction': 0.30, 
                      'FMCG & Household': 0.20, 'Industrial & Other': 0.10}
        product_weights = np.array([div_weights[product_to_division[p]] / len(cls.PRODUCTS[product_to_division[p]]) 
                                   for p in all_products])
        product_weights /= product_weights.sum()
        
        # Generate dates
        end_date = datetime.now()
        dates = [end_date - timedelta(days=x) for x in range(730)]
        
        # Base dataframe
        df = pd.DataFrame({
            'transaction_id': [f'AKJ{i:07d}' for i in range(1, num_records + 1)],
            'date': np.random.choice(dates, num_records),
            'product': np.random.choice(all_products, num_records, p=product_weights),
            'customer_segment': np.random.choice(cls.SEGMENTS, num_records, p=[0.20, 0.25, 0.25, 0.08, 0.12, 0.10]),
            'region': np.random.choice(cls.REGIONS, num_records, p=[0.28, 0.20, 0.10, 0.12, 0.08, 0.10, 0.07, 0.05]),
            'sales_channel': np.random.choice(cls.CHANNELS, num_records, p=[0.25, 0.25, 0.20, 0.15, 0.15])
        })
        
        df['business_division'] = df['product'].map(product_to_division)
        
        # Revenue calculation
        base_revenue = np.random.uniform(500, 50000, num_records)
        multipliers = {'Building & Construction': 2.75, 'Industrial & Other': 2.0, 
                      'Beverages & Food': 0.9, 'FMCG & Household': 0.75}
        df['revenue'] = base_revenue * df['business_division'].map(multipliers)
        
        # Adjust for segments and regions
        df.loc[df['customer_segment'] == 'Enterprise', 'revenue'] *= 1.5
        df.loc[df['customer_segment'] == 'Government', 'revenue'] *= 1.4
        df.loc[df['region'].isin(['Dhaka', 'Chittagong']), 'revenue'] *= 1.3
        
        # Quantity and pricing
        df['quantity'] = np.where(df['business_division'].isin(['Beverages & Food', 'FMCG & Household']),
                                 np.random.randint(100, 1000, num_records),
                                 np.random.randint(1, 100, num_records))
        df['unit_price'] = df['revenue'] / df['quantity']
        
        # Cost and profit
        margins = {'Beverages & Food': 0.70, 'Building & Construction': 0.65, 
                  'FMCG & Household': 0.75, 'Industrial & Other': 0.60}
        df['cost'] = df['revenue'] * df['business_division'].map(margins)
        df['profit'] = df['revenue'] - df['cost']
        df['profit_margin'] = (df['profit'] / df['revenue']) * 100
        
        # Temporal dimensions
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['year'] = df['date'].dt.year
        
        return df.sort_values('date').reset_index(drop=True)

# ============================================================================
# ANALYTICAL AGENTS
# ============================================================================

class DescriptiveAgent:
    """What has happened? - Historical analysis"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.data['date'] = pd.to_datetime(self.data['date'])
    
    def analyze(self) -> Dict[str, Any]:
        """Perform descriptive analysis"""
        agg_funcs = {'revenue': ['sum', 'mean'], 'profit': 'sum', 
                    'profit_margin': 'mean', 'transaction_id': 'count'}
        
        division_stats = self.data.groupby('business_division').agg(agg_funcs).round(2)
        region_stats = self.data.groupby('region')['revenue'].sum().round(2)
        
        return {
            "agent_name": "Descriptive Analytics",
            "timestamp": datetime.now().isoformat(),
            "overall_metrics": {
                "total_revenue": float(self.data['revenue'].sum()),
                "total_profit": float(self.data['profit'].sum()),
                "total_transactions": len(self.data),
                "avg_profit_margin": float(self.data['profit_margin'].mean())
            },
            "top_performers": {
                "division": self.data.groupby('business_division')['revenue'].sum().idxmax(),
                "product": self.data.groupby('product')['revenue'].sum().idxmax(),
                "region": region_stats.idxmax()
            },
            "hierarchical_breakdown": {
                "by_division": division_stats.to_dict(),
                "by_region": region_stats.to_dict()
            }
        }

class DiagnosticAgent:
    """Why did it happen? - Root cause analysis"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
    
    def analyze(self) -> Dict[str, Any]:
        """Perform diagnostic analysis"""
        overall_margin = self.data['profit_margin'].mean()
        division_margins = self.data.groupby('business_division')['profit_margin'].mean()
        underperformers = division_margins[division_margins < overall_margin].to_dict()
        
        regional_revenue = self.data.groupby('region')['revenue'].sum()
        regional_disparity = float(regional_revenue.std() / regional_revenue.mean())
        
        monthly_revenue = self.data.groupby('month')['revenue'].mean()
        seasonality = float((monthly_revenue.max() - monthly_revenue.min()) / monthly_revenue.mean())
        
        insights = []
        if underperformers:
            insights.append(f"⚠️ {len(underperformers)} divisions below avg margin: {', '.join(underperformers.keys())}")
        if regional_disparity > 0.3:
            insights.append(f"🌍 High regional disparity ({regional_disparity:.2f})")
        if seasonality > 0.3:
            insights.append(f"📅 Strong seasonality ({seasonality:.2f})")
        
        return {
            "agent_name": "Diagnostic Analytics",
            "timestamp": datetime.now().isoformat(),
            "underperforming_divisions": underperformers,
            "regional_disparity_score": round(regional_disparity, 3),
            "seasonality_strength": round(seasonality, 3),
            "peak_month": int(monthly_revenue.idxmax()),
            "key_insights": insights
        }

class PredictiveAgent:
    """What will happen? - Forecasting"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
    
    def analyze(self, forecast_days: int = 30) -> Dict[str, Any]:
        """Perform predictive analysis"""
        recent = self.data.tail(300)['revenue'].mean()
        previous = self.data.tail(600).head(300)['revenue'].mean()
        growth_rate = ((recent - previous) / previous) if previous > 0 else 0
        
        forecast_revenue = self.data.tail(70)['revenue'].mean() * (1 + growth_rate) * forecast_days
        
        return {
            "agent_name": "Predictive Analytics",
            "timestamp": datetime.now().isoformat(),
            "forecast_period": f"{forecast_days} days",
            "overall_forecast": {
                "predicted_total_revenue": round(float(forecast_revenue), 2),
                "growth_rate_pct": round(float(growth_rate * 100), 2)
            }
        }

class PrescriptiveAgent:
    """What should we do? - Actionable recommendations"""
    
    def __init__(self, descriptive: Dict, diagnostic: Dict, predictive: Dict):
        self.desc = descriptive
        self.diag = diagnostic
        self.pred = predictive
    
    def analyze(self) -> Dict[str, Any]:
        """Generate prescriptive recommendations"""
        recommendations = []
        
        if self.pred['overall_forecast']['growth_rate_pct'] < 0:
            recommendations.append({
                "priority": "Critical",
                "action": "Implement revenue recovery plan",
                "timeline": "1-2 weeks",
                "reason": f"Negative growth ({self.pred['overall_forecast']['growth_rate_pct']:.1f}%)"
            })
        
        if self.diag['underperforming_divisions']:
            recommendations.append({
                "priority": "High",
                "action": "Optimize underperforming divisions",
                "timeline": "2-4 weeks",
                "reason": f"{len(self.diag['underperforming_divisions'])} divisions below average"
            })
        
        recommendations.append({
            "priority": "Strategic",
            "action": f"Invest in {self.desc['top_performers']['division']}",
            "timeline": "Ongoing",
            "reason": "Highest performing division"
        })
        
        return {
            "agent_name": "Prescriptive Analytics",
            "timestamp": datetime.now().isoformat(),
            "total_recommendations": len(recommendations),
            "recommendations": recommendations,
            "immediate_actions": recommendations[:2] if len(recommendations) >= 2 else recommendations
        }

# ============================================================================
# N8N WORKFLOW GENERATOR (Proper Format)
# ============================================================================

class N8NWorkflowGenerator:
    """Generate n8n-compatible workflow"""
    
    def __init__(self, desc: Dict, diag: Dict, pred: Dict, presc: Dict, data: pd.DataFrame):
        self.desc = desc
        self.diag = diag
        self.pred = pred
        self.presc = presc
        self.data = data
    
    def generate_workflow_payload(self) -> Dict[str, Any]:
        """Generate proper n8n workflow format"""
        growth_rate = self.pred['overall_forecast']['growth_rate_pct']
        priority = "CRITICAL" if growth_rate < -5 else "HIGH" if growth_rate < 0 else "NORMAL"
        
        data_summary = {
            "totalRevenue": float(self.data['revenue'].sum()),
            "totalProfit": float(self.data['profit'].sum()),
            "avgMargin": float(self.data['profit_margin'].mean()),
            "growthRate": growth_rate,
            "priority": priority
        }
        
        return {
            "name": "Akij Sales Intelligence Multi-Agent",
            "nodes": [
                {
                    "parameters": {"rule": {"interval": [{"field": "cronExpression", "expression": "0 9 * * *"}]}},
                    "name": "Schedule Trigger",
                    "type": "n8n-nodes-base.scheduleTrigger",
                    "typeVersion": 1,
                    "position": [250, 300],
                    "id": "schedule-trigger"
                },
                {
                    "parameters": {
                        "jsCode": f"""
const data = {{
  totalRevenue: {data_summary['totalRevenue']},
  growthRate: {data_summary['growthRate']},
  priority: "{priority}",
  topDivision: "{self.desc['top_performers']['division']}"
}};
return {{json: {{agent: "Multi-Agent", data: data}}}};
"""
                    },
                    "name": "Process Analytics",
                    "type": "n8n-nodes-base.code",
                    "typeVersion": 2,
                    "position": [450, 300],
                    "id": "process-analytics"
                },
                {
                    "parameters": {
                        "url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
                        "bodyParametersJson": """={
  "text": "🤖 Akij Sales Report",
  "blocks": [{
    "type": "section",
    "fields": [
      {"type": "mrkdwn", "text": "*Revenue:* ৳" + $json.data.totalRevenue.toLocaleString()},
      {"type": "mrkdwn", "text": "*Growth:* " + $json.data.growthRate + "%"}
    ]
  }]
}"""
                    },
                    "name": "Send Slack",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 4.1,
                    "position": [650, 300],
                    "id": "send-slack"
                }
            ],
            "connections": {
                "Schedule Trigger": {"main": [[{"node": "Process Analytics", "type": "main", "index": 0}]]},
                "Process Analytics": {"main": [[{"node": "Send Slack", "type": "main", "index": 0}]]}
            },
            "settings": {"executionOrder": "v1"},
            "active": False,
            "id": "akij-sales-workflow"
        }
    
    def save_workflow(self, filename: str = None) -> str:
        """Save workflow to file"""
        filename = filename or f"n8n_workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        workflow = self.generate_workflow_payload()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, indent=2, ensure_ascii=False)
        return filename

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Generate data
    print("="*80)
    print("AKIJ RESOURCE - MULTI-AGENT SALES INTELLIGENCE SYSTEM")
    print("="*80)
    
    sales_data = SalesDataGenerator.generate_sales_data(4000)
    print(f"\n✅ Generated {len(sales_data):,} transactions")
    print(f"📅 Period: {sales_data['date'].min().date()} to {sales_data['date'].max().date()}")
    print(f"💰 Revenue: ৳{sales_data['revenue'].sum():,.2f}")
    
    # Run agents
    desc_agent = DescriptiveAgent(sales_data)
    diag_agent = DiagnosticAgent(sales_data)
    pred_agent = PredictiveAgent(sales_data)
    
    desc_analysis = desc_agent.analyze()
    diag_analysis = diag_agent.analyze()
    pred_analysis = pred_agent.analyze()
    
    presc_agent = PrescriptiveAgent(desc_analysis, diag_analysis, pred_analysis)
    presc_analysis = presc_agent.analyze()
    
    # Display results
    print(f"\n📊 DESCRIPTIVE: Revenue ৳{desc_analysis['overall_metrics']['total_revenue']:,.0f}")
    print(f"🔍 DIAGNOSTIC: {len(diag_analysis['key_insights'])} insights identified")
    print(f"🔮 PREDICTIVE: {pred_analysis['overall_forecast']['growth_rate_pct']:+.1f}% growth forecast")
    print(f"💡 PRESCRIPTIVE: {presc_analysis['total_recommendations']} recommendations")
    
    # Generate n8n workflow
    n8n_gen = N8NWorkflowGenerator(desc_analysis, diag_analysis, pred_analysis, presc_analysis, sales_data)
    workflow_file = n8n_gen.save_workflow()
    print(f"\n⚡ n8n Workflow: {workflow_file}")
    
    # Save data
    sales_data.to_csv('akij_sales_data_complete.csv', index=False)
    print(f"💾 Data saved: akij_sales_data_complete.csv")
    
    print("\n" + "="*80)
    print("✅ SYSTEM READY FOR DEPLOYMENT")
    print("="*80)