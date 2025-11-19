
#!/usr/bin/env python3
# Compact Multi-Agent Sales Intelligence - Akij Resource (v2)
# Author: Abdul Matin
# Generates synthetic sales data, runs 4 analytics agents, and exports n8n payload + workflow.

from datetime import datetime, timedelta
import json, os
import numpy as np
import pandas as pd

# -------------------------
# Data generator
# -------------------------
def generate_sales_data(n=4000, seed=42):
    np.random.seed(seed)
    akij = {
        'Beverages & Food': ['Mojo','Frutika','Speed','Clemon','Twing','Lemu','Spa Drinking Water'],
        'Building & Construction': ['Akij Cement','Akij Tiles','Akij Rebar','Akij Pipes'],
        'FMCG & Household': ['Max Wash','Dish Master','H&H Hand Wash','Mum Mum Diaper'],
        'Industrial & Other': ['Akij Jute Yarn','Akij Textile','Akij Motors','Akij BIAX Films']
    }
    prod, div_map = [], {}
    for d, ps in akij.items():
        prod += ps
        for p in ps: div_map[p] = d
    div_weights = {'Beverages & Food':0.40,'Building & Construction':0.30,'FMCG & Household':0.20,'Industrial & Other':0.10}
    p_weights = np.array([div_weights[div_map[p]]/len(akij[div_map[p]]) for p in prod])
    p_weights /= p_weights.sum()
    segments = ['Enterprise','SMB','Individual','Government','Retail Distributor','Wholesaler']
    regions = ['Dhaka','Chittagong','Rangpur','Khulna','Mymensingh','Rajshahi','Sylhet','Barisal']
    channels = ['Online','Retail Store','Wholesale','Direct Sales','Distributor Network']
    end, start = datetime.now(), datetime.now()-timedelta(days=730)
    dates = [start+timedelta(days=i) for i in range((end-start).days+1)]
    df = pd.DataFrame({
        'transaction_id':[f'AKJ{str(i).zfill(7)}' for i in range(1,n+1)],
        'date':np.random.choice(dates,n),
        'product':np.random.choice(prod,n,p=p_weights),
        'customer_segment':np.random.choice(segments,n,p=[0.20,0.25,0.25,0.08,0.12,0.10]),
        'region':np.random.choice(regions,n,p=[0.28,0.20,0.10,0.12,0.08,0.10,0.07,0.05]),
        'sales_channel':np.random.choice(channels,n,p=[0.25,0.25,0.20,0.15,0.15])
    })
    df['business_division'] = df['product'].map(div_map)
    base_rev = np.random.uniform(500,50000,n)
    rev = base_rev.copy()
    rev *= np.where(df['business_division']=='Building & Construction', np.random.uniform(2.0,3.5,n), 1.0)
    rev *= np.where(df['business_division']=='Industrial & Other', np.random.uniform(1.5,2.5,n), 1.0)
    rev *= np.where(df['business_division']=='Beverages & Food', np.random.uniform(0.6,1.2,n), 1.0)
    rev *= np.where(df['business_division']=='FMCG & Household', np.random.uniform(0.5,1.0,n), 1.0)
    rev *= np.where(df['customer_segment']=='Enterprise',1.5,1.0)
    rev *= np.where(df['customer_segment']=='Government',1.4,1.0)
    rev *= np.where(df['customer_segment']=='Wholesaler',1.3,1.0)
    rev *= np.where(df['region'].isin(['Dhaka','Chittagong']),1.3,1.0)
    qty = np.where(df['business_division'].isin(['Beverages & Food','FMCG & Household']),
                   np.random.randint(100,1000,n), np.random.randint(1,100,n))
    qty = np.where(df['business_division']=='Building & Construction', np.random.randint(10,200,n), qty)
    df['quantity']=qty
    df['revenue']=rev
    df['unit_price']=df['revenue']/df['quantity']
    cost = df['revenue'] * np.where(df['business_division']=='Beverages & Food', np.random.uniform(0.65,0.75,n),
            np.random.uniform(0.50,0.70,n))
    cost = np.where(df['business_division']=='Building & Construction', df['revenue']*np.random.uniform(0.60,0.70,n), cost)
    cost = np.where(df['business_division']=='FMCG & Household', df['revenue']*np.random.uniform(0.70,0.80,n), cost)
    cost = np.where(df['business_division']=='Industrial & Other', df['revenue']*np.random.uniform(0.55,0.65,n), cost)
    df['cost']=cost
    df['profit']=df['revenue']-df['cost']
    df['profit_margin']=(df['profit']/df['revenue'])*100
    df['month']=pd.to_datetime(df['date']).dt.month
    df['quarter']=pd.to_datetime(df['date']).dt.quarter
    df['year']=pd.to_datetime(df['date']).dt.year
    df=df.sort_values('date').reset_index(drop=True)
    return df

# -------------------------
# Agents
# -------------------------
class DescriptiveAgent:
    def __init__(self, df): self.df=df.copy(); self.df['date']=pd.to_datetime(self.df['date'])
    def analyze(self):
        total_revenue=float(self.df['revenue'].sum()); total_profit=float(self.df['profit'].sum())
        top_div=self.df.groupby('business_division')['revenue'].sum().idxmax()
        top_prod=self.df.groupby('product')['revenue'].sum().idxmax()
        return {'total_revenue':round(total_revenue,2),'total_profit':round(total_profit,2),
                'transactions':len(self.df),'top_division':top_div,'top_product':top_prod}
class DiagnosticAgent:
    def __init__(self, df): self.df=df.copy()
    def analyze(self):
        overall=self.df['profit_margin'].mean()
        div_margin=self.df.groupby('business_division')['profit_margin'].mean().round(2).to_dict()
        disp=float(self.df.groupby('region')['revenue'].sum().std()/self.df.groupby('region')['revenue'].sum().mean())
        return {'overall_margin':round(float(overall),2),'division_margins':div_margin,'regional_disparity_score':round(disp,3)}
class PredictiveAgent:
    def __init__(self, df): self.df=df.copy()
    def analyze(self,days=30):
        recent=self.df.tail(300)['revenue'].mean(); prev=self.df.tail(600).head(300)['revenue'].mean()
        g=((recent-prev)/prev) if prev>0 else 0; forecast=recent*(1+g)*days
        return {'predicted_total':round(float(forecast),2),'growth_pct':round(float(g*100),2)}
class PrescriptiveAgent:
    def __init__(self, desc, diag, pred): self.desc=desc; self.diag=diag; self.pred=pred
    def analyze(self):
        return {'actions':[{'priority':'High','action':'Optimize underperforming divisions','timeline':'1-4 weeks'},
                           {'priority':'Medium','action':'Expand high-growth channels','timeline':'1-3 months'}]}

# -------------------------
# N8N Workflow Generator
# -------------------------
class N8NWorkflowGenerator:
    def __init__(self, desc, diag, pred, presc, raw):
        self.desc, self.diag, self.pred, self.presc, self.raw = desc, diag, pred, presc, raw
    def generate_payload(self):
        growth=self.pred['growth_pct']
        priority="CRITICAL" if growth<-5 else "HIGH" if growth<0 else "NORMAL"
        return {
            "workflow_metadata":{"workflow_name":"akij_sales_intel_compact_v2","report_date":datetime.now().strftime('%Y-%m-%d')},
            "data_summary":{"total_records":len(self.raw),"total_revenue":float(self.raw['revenue'].sum())},
            "analytics_results":{"descriptive":self.desc,"diagnostic":self.diag,"predictive":self.pred,"prescriptive":self.presc},
            "alert_configuration":{"priority":priority},
            "timestamp":datetime.now().isoformat()
        }
    def generate_workflow(self, payload):
        p=payload
        return {
            "name":f"{p['workflow_metadata']['workflow_name']} (Auto Generated)",
            "nodes":[
                {"id":"Webhook_1","name":"AI Report Webhook","type":"n8n-nodes-base.webhook","typeVersion":1,
                 "parameters":{"path":"akij-sales-intelligence"},"position":[250,300]},
                {"id":"Function_1","name":"Process AI Report","type":"n8n-nodes-base.function","typeVersion":1,
                 "parameters":{"functionCode":"const payload = $json; console.log('Payload received'); return [{json: payload}];"},"position":[550,300]},
                {"id":"Slack_1","name":"Notify Slack","type":"n8n-nodes-base.httpRequest","typeVersion":1,
                 "parameters":{"url":"https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK","method":"POST",
                               "sendBody":True,"bodyParametersUi":{"parameter":[{"name":"text","value":"📊 Workflow processed successfully!"}]} },
                 "position":[850,300]}
            ],
            "connections":{"AI Report Webhook":{"main":[[{"node":"Process AI Report","type":"main","index":0}]]},
                           "Process AI Report":{"main":[[{"node":"Notify Slack","type":"main","index":0}]]}},
            "active":False,"settings":{},"id":str(int(datetime.now().timestamp()))
        }
    def auto_generate(self):
        payload=self.generate_payload()
        workflow=self.generate_workflow(payload)
        pf, wf='n8n_akij_payload_compact.json','n8n_akij_workflow_compact.json'
        with open(pf,'w',encoding='utf-8') as f: json.dump(payload,f,indent=2,ensure_ascii=False)
        with open(wf,'w',encoding='utf-8') as f: json.dump(workflow,f,indent=2,ensure_ascii=False)
        print("✅ Payload saved:",pf); print("✅ Workflow saved:",wf)
        return {'payload_file':pf,'workflow_file':wf}

# -------------------------
# Runner
# -------------------------
def main(n=4000):
    print("Generating data...")
    df=generate_sales_data(n); df.to_csv('akij_sales_data_complete.csv',index=False)
    print("Data generated:",len(df))
    desc, diag, pred = DescriptiveAgent(df).analyze(), DiagnosticAgent(df).analyze(), PredictiveAgent(df).analyze()
    presc=PrescriptiveAgent(desc,diag,pred).analyze()
    gen=N8NWorkflowGenerator(desc,diag,pred,presc,df)
    gen.auto_generate()
    print("All tasks complete. Ready for n8n import!")

if __name__=="__main__":
    main()
