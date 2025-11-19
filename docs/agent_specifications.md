 
# Agent Specifications

It contains:

    ✔ Official agent names
    ✔ Roles, responsibilities, prompts
    ✔ Inputs & outputs
    ✔ Tools used
    ✔ Example queries
    ✔ Integration notes

---

# 🧠 **Agent Specifications – AkSalesAgentIntelligence**

This document describes the roles, responsibilities, logic, tools, and interaction flow for each agent in the **Akij Resource Multi-Agent Sales Intelligence System**.

The system consists of four analytical agents and two operational agents, designed to work together to answer sales queries, generate insights, and trigger business workflows.

✅ Final Combined Architecture + Agent Mapping

    ┌──────────────────────────────────────────────────────────────────────────────┐
│                      MULTI-AGENT SYSTEM ARCHITECTURE                         │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐         │
│   │   Agent 1        │   │   Agent 2        │   │   Agent 3        │         │
│   │ Descriptive      │──▶│ Diagnostic       │──▶│ Predictive       │         │
│   │ (What happened?) │   │ (Why happened?)  │   │ (Future trends)  │         │
│   └──────────────────┘   └──────────────────┘   └──────────────────┘         │
│            │                    │                    │                       │
│            └────────────────────┴────────────────────┘                       │
│                                 │                                            │
│                                 ▼                                            │
│                        ┌──────────────────┐                                   │
│                        │   Agent 4        │                                   │
│                        │ Prescriptive     │                                   │
│                        │ (What to do?)    │                                   │
│                        └──────────────────┘                                   │
│                                 │                                            │
│             ┌───────────────────┴──────────────────────┐                     │
│             │                                           │                     │
│             ▼                                           ▼                     │
│   ┌──────────────────┐                      ┌────────────────────┐            │
│   │  Chatbot Agent   │                      │ n8n Workflow Agent │            │
│   │ (Conversational) │                      │ (Automation Engine)│            │
│   └──────────────────┘                      └────────────────────┘            │
│             │                                           │                     │
│             ▼                                           ▼                     │
│   ┌──────────────────────────────────────────────────────────────────────┐    │
│   │                     Streamlit Dashboard UI                           │    │
│   │           (Interactive Visualizations & Analytics)                   │    │
│   └──────────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────────┘


  ┌──────────────────────────────────────────────────────────────────────────────┐
  │                    MULTI-AGENT SYSTEM ARCHITECTURE                           │
  ├──────────────────────────────────────────────────────────────────────────────┤
  │                                                                              │
  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                   │
  │   │   Agent 1    │    │   Agent 2    │    │   Agent 3    │                   │
  │   │ Descriptive  │───▶│ Diagnostic   │───▶│ Predictive   │                   │
  │   │ (What happened?) ││(Why happened?) ││ (What will     │                   │
  │   └──────────────┘    └──────────────┘    │ happen?)     │                   │
  │                                           └──────────────┘                   │
  │          │                     │                     │                       │
  │          └─────────────────────┴─────────────────────┘                       │
  │                                │                                             │
  │                                ▼                                             │
  │                      ┌─────────────────────┐                                 │
  │                      │      Agent 4        │                                 │
  │                      │  Prescriptive       │                                 │
  │                      │ (What to do?)       │                                 │
  │                      └─────────────────────┘                                 │
  │                                │                                             │
  │       ┌────────────────────────┴─────────────────────────┐                   │
  │       │                                                  │                   │
  │       ▼                                                  ▼                   │
  │  ┌─────────────────┐                         ┌────────────────────────┐      │
  │  │  Chatbot Agent  │                         │ n8n Workflow Builder   │      │
  │  │ (Conversational)│                         │ (Automation Engine)    │      │
  │  └─────────────────┘                         └────────────────────────┘      │
  │       │                                                  │                   │
  │       ▼                                                  ▼                   │
  │   ┌───────────────────────────────────────────────────────────────────────┐  │
  │   │                 Streamlit Dashboard UI                                │  │
  │   │      (Interactive Visualizations & Analytics)                         │  │
  │   └───────────────────────────────────────────────────────────────────────┘  │
  └──────────────────────────────────────────────────────────────────────────────┘



📘 Agent Mapping — Required by the AI Agent & Agentic Intelligence Specialist Role

 | Stage   | Agent Name                       | Task                  |
 | ------- | -------------------------------- | --------------------- |
 | **1**   | **Descriptive Analytics Agent**  | What happened?        |
 | **2**   | **Diagnostic Analytics Agent**   | Why it happened?      |
 | **3**   | **Predictive Analytics Agent**   | What will happen?     |
 | **4**   | **Prescriptive Analytics Agent** | What to do?           |
 | **Ops** | **Chatbot Agent**                | Conversational engine |
 | **Ops** | **n8n Workflow Builder Agent**   | Automation engine     |


# 🔍 **1. Descriptive Analytics Agent**

### **“What has happened?”**

---

### **Purpose**

Processes the sales dataset and provides historical summaries, KPIs, and factual observations across:

* Product categories
* Customer segments
* Regions (BD Divisions)
* Sales channels
* Monthly/quarterly performance

---

### **Responsibilities**

* Compute sales totals (revenue, profit, units)
* Generate performance breakdowns
* Identify top/bottom products, regions, customers
* Trend comparison (MoM, QoQ, YoY)
* Provide clean, structured summary

---

### **Inputs**

* Filtered dataset (based on user query)
* Query intent extracted by controller agent

---

### **Outputs**

JSON containing:

```json
{
  "summary": "...",
  "top_performers": {...},
  "low_performers": {...},
  "regional_breakdown": {...},
  "channel_breakdown": {...},
  "insights": [...]
}
```

---

### **Tools Used**

* Pandas
* NumPy
* Internal metrics calculator

---

### **Example Queries**

* “Show sales in Dhaka division last month”
* “Top performing product categories this quarter”
* “Give me overall sales summary”

---

---

# 🧠 **2. Diagnostic Analytics Agent**

### **“Why did it happen?”**

---

### **Purpose**

Identifies factors influencing sales performance, including:

* Underperforming products/regions
* Market behavior
* Correlations between variables
* Operational bottlenecks
* Seasonal impacts

---

### **Responsibilities**

* Compare performance vs expected trends
* Find root causes behind revenue decline/growth
* Analyze anomalies
* Attribute sales changes to specific factors
* Provide cause-effect reasoning

---

### **Inputs**

* Descriptive agent output
* User query context
* Relevant filtered dataset

---

### **Outputs**

JSON containing:

```json
{
  "root_causes": [...],
  "performance_gaps": {...},
  "unexpected_trends": [...],
  "explanations": "..."
}
```

---

### **Tools Used**

* Correlation engine
* Trend deviation detector
* Agent reasoning prompts

---

### **Example Queries**

* “Why did Rajshahi region decline in September?”
* “Why did channel sales drop in modern trade?”
* “What caused spike in category A revenue?”

---

---

# 🔮 **3. Predictive Analytics Agent**

### **“What is likely to happen?”**

---

### **Purpose**

Forecasts future performance using:

* Historical patterns
* Seasonality
* Trend projections
* LLM-assisted predictive reasoning

---

### **Responsibilities**

* Forecast revenue for next month/quarter
* Predict best/worst performing products
* Identify early warning signals
* Estimate growth or decline

---

### **Inputs**

* Descriptive agent metrics
* Filtered data
* Forecast horizon from user

---

### **Outputs**

JSON format:

```json
{
  "forecast_summary": "...",
  "predicted_growth": {...},
  "declining_segments": [...],
  "future_opportunities": [...],
  "confidence_level": "high|medium|low"
}
```

---

### **Tools Used**

* Statistical trend model (moving avg, seasonal index)
* LLM forecasting logic
* Pattern recognition scripts

---

### **Example Queries**

* “Predict next quarter sales in Chattogram”
* “What will happen to category B next month?”
* “Show forecast for top 5 SKUs”

---

---

# 🎯 **4. Prescriptive Analytics Agent**

### **“What actions should be taken?”**

---

### **Purpose**

Converts analytical insights into:

* Strategic recommendations
* Immediate actions
* Resource allocation decisions
* Sales improvement techniques

---

### **Responsibilities**

* Recommend actionable sales strategy
* Prioritize actions by impact level
* Suggest targeted interventions
* Create business rules for automation
* Produce n8n workflow payload

---

### **Inputs**

* Descriptive output
* Diagnostic insights
* Predictive forecast
* Business conditions

---

### **Outputs**

### **A. Human-readable Recommendations**

```json
{
  "action_items": [...],
  "priority": "critical | high | medium | low",
  "expected_impact": "..."
}
```

### **B. n8n Automation Payload**

```json
{
  "workflow_trigger": true,
  "alert_level": "critical",
  "assigned_team": "Sales Regional Manager",
  "actions": [...]
}
```

---

### **Tools Used**

* LLM action formulation
* Weighted priority scoring
* n8n workflow schema generator

---

### **Example Queries**

* “What actions should we take to boost Dhaka region sales?”
* “Recommend strategies for low performance SKUs”
* “Give me a plan to improve modern trade channel revenue”

---

---

# 🤖 **5. Chatbot Agent (Operational)**

### **“Conversational interface for all insights”**

---

### **Purpose**

Serves as the front-end assistant that:

* Receives user queries
* Identifies intent
* Decides which agent(s) to trigger
* Combines multi-agent outputs into final response

---

### **Responsibilities**

* Query parsing
* Intent classification
* Agent orchestration
* Streaming responses
* Dynamic filtering (region, product, segment)

---

### **Inputs**

* User text input
* Optional filters from dashboard

---

### **Outputs**

* Natural language replies
* Structured summaries
* Visual-ready data

---

---

# ⚙️ **6. n8n Workflow Builder Agent (Operational)**

### **“Automation trigger and workflow generator”**

---

### **Purpose**

Builds n8n-compatible automation flows using Prescriptive output.

---

### **Responsibilities**

* Validate JSON structure
* Assign workflow severity
* Build webhook payload
* Trigger actual n8n workflows

---

### **Inputs**

* Prescriptive agent output

---

### **Outputs**

```json
{
  "n8n_workflow": {
    "trigger": "webhook",
    "alert_level": "critical",
    "actions": [...],
    "assigned_to": "..."
  }
}
```

---

# 🔗 **Inter-Agent Communication Protocol**

Each agent communicates via a **shared context object**, enabling:

* Data passing between analytical stages
* Causality linking (what → why → future → action)
* Structured JSON standardization
* Controller-agent managed execution

---

# 🧩 **Summary**

This specification defines all agents required by the **AI Agent & Agentic Intelligence Specialist** role:

| Stage | Agent Name                   | Task                  |
| ----- | ---------------------------- | --------------------- |
| 1     | Descriptive Analytics Agent  | What happened?        |
| 2     | Diagnostic Analytics Agent   | Why it happened?      |
| 3     | Predictive Analytics Agent   | What will happen?     |
| 4     | Prescriptive Analytics Agent | What to do?           |
| Ops   | Chatbot Agent                | Conversational engine |
| Ops   | n8n Workflow Builder Agent   | Automation engine     |

--- 