 
# Agent Specifications

It contains:

    ✔ Official agent names
    ✔ Roles, responsibilities, prompts
    ✔ Inputs & outputs
    ✔ Tools used
    ✔ Example queries
    ✔ Integration notes

 

# 🧠 **Agent Specifications – AkSalesAgentIntelligence**

This document describes the roles, responsibilities, logic, tools, and interaction flow for each agent in the **Akij Resource Multi-Agent Sales Intelligence System**.

The system consists of four analytical agents and two operational agents, designed to work together to answer sales queries, generate insights, and trigger business workflows.


# ✅ **Architecture Diagram**

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                      MULTI-AGENT SYSTEM ARCHITECTURE                         │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                 │
│   │   Agent 1    │     │   Agent 2    │     │   Agent 3    │                 │
│   │ Descriptive  │ ───▶│ Diagnostic   │ ───▶│ Predictive   │                 │
│   │ (What happened?)│  │ (Why happened?)│   │ (What will    │                 │
│   └──────────────┘     └──────────────┘     │ happen?)      │                │
│                                              └──────────────┘                │
│            │                     │                     │                     │
│            └─────────────────────┴─────────────────────┘                     │
│                                 │                                            │
│                                 ▼                                            │
│                        ┌─────────────────────┐                               │
│                        │      Agent 4        │                               │
│                        │    Prescriptive     │                               │
│                        │    (What to do?)    │                               │
│                        └─────────────────────┘                               │
│                                 │                                            │
│       ┌─────────────────────────┴──────────────────────────┐                 │
│       │                                                    │                 │
│       ▼                                                    ▼                 │
│   ┌─────────────────┐                          ┌────────────────────────┐    │
│   │  Chatbot Agent  │                          │ n8n Workflow Builder   │    │
│   │ (Conversational)│                          │  (Automation Engine)   │    │
│   └─────────────────┘                          └────────────────────────┘    │
│       │                                                    │                 │
│       ▼                                                    ▼                 │
│   ┌───────────────────────────────────────────────────────────────────────┐  │
│   │                       Streamlit Dashboard UI                          │  │
│   │            (Interactive Visualizations & Analytics)                   │  │
│   └───────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

# 📘 **Agent Specification (As Required by Job Description)**

| Stage   | Agent Name                       | Task                  |
| ------- | -------------------------------- | --------------------- |
| **1**   | **Descriptive Analytics Agent**  | What happened?        |
| **2**   | **Diagnostic Analytics Agent**   | Why it happened?      |
| **3**   | **Predictive Analytics Agent**   | What will happen?     |
| **4**   | **Prescriptive Analytics Agent** | What to do?           |
| **Ops** | **Chatbot Agent**                | Conversational engine |
| **Ops** | **n8n Workflow Builder Agent**   | Automation engine     |

---
 
  

# 🧠 **Detailed Agent Specifications**

This section expands each agent with **internal logic**, **reasoning patterns**, **data flow**, and **decision responsibilities**—exactly what interview panels look for when evaluating an AI Agentic Architecture.

---

# 1️⃣ **Descriptive Analytics Agent (Stage 1)**

### 🏷 **Question Answered:** *“What has happened?”*

### 🎯 **Primary Goal:** Summarize past sales performance with factual, data-driven metrics.

---

## ✅ **Responsibilities**

* Clean and preprocess raw data
* Generate KPIs (revenue, volume, margin)
* Trend extraction (daily, weekly, monthly, quarterly)
* Regional comparison (Dhaka vs Chattogram vs Khulna etc.)
* Product/category-level summaries
* Customer segmentation analysis
* Channel-based performance (Retail, Wholesale, Modern Trade)

---

## 🔍 **Internal Logic**

* Uses **Pandas** for groupby operations
* Performs **rolling averages** for smoothed trends
* Detects top/bottom performers using rank functions
* Handles missing or inconsistent data
* Normalizes numeric fields (min-max)

---

## 🔢 **Output Format**

```json
{
  "kpis": {...},
  "top_products": [...],
  "bottom_regions": [...],
  "channel_summary": {...},
  "timeline_trends": [...],
  "raw_summary_text": "..."
}
```

---

## 🧪 **Examples of Questions Routed to This Agent**

* “Show sales performance for last quarter”
* “Top 5 channels last month”
* "Give me summary of product category A"

---

---

# 2️⃣ **Diagnostic Analytics Agent (Stage 2)**

### 🏷 **Question:** *“Why did it happen?”*

### 🎯 **Goal:** Uncover root causes behind trends.

---

## ✅ **Responsibilities**

* Drill down into anomalies detected by the descriptive agent
* Compare metrics with historical baselines
* Identify region/product/channel bottlenecks
* Perform correlation analysis
* Generate causal reasoning using LLM
* Detect seasonality or demand shocks (festivals, weather, market events)

---

## 🔍 **Internal Logic**

* Computes:

  * **Δ (%) change month-over-month**
  * **Z-score** to detect anomalies
  * **Correlation matrices** (Pearson/Spearman)
* Runs **LLM causal reasoning** over its findings
* Links cause → effect → business impact

---

## 🔢 **Output Format**

```json
{
  "causes": [...],
  "correlations": {...},
  "anomaly_explanations": [...],
  "business_reasoning": "..."
}
```

---

## 🧪 **Examples**

* “Why sales dropped in Rajshahi division?”
* “Why did SKU-104 spike suddenly?”
* “Why Modern Trade underperformed this period?”

---

---

# 3️⃣ **Predictive Analytics Agent (Stage 3)**

### 🏷 **Question:** *“What will happen?”*

### 🎯 **Goal:** Forecast near-term and long-term outcomes.

---

## ✅ **Responsibilities**

* Short-term sales forecasting (7-day, 30-day)
* Seasonal trend prediction
* Future top/bottom products
* Market opportunity identification
* Customer churn prediction (if modeled)

---

## 🔍 **Internal Logic**

* Uses:

  * Linear regression
  * Moving averages
  * Seasonal index
  * LLM-based pattern projection
* Applies **Holt-Winters** when time-series patterns detected
* Estimates **confidence score (0-1)**

---

## 🔢 **Output Format**

```json
{
  "forecast": {...},
  "growth_opportunities": [...],
  "risk_segments": [...],
  "future_trends_text": "..."
}
```

---

## 🧪 **Example Queries**

* “Predict next month revenue for Dhaka region”
* “What will happen to category B this quarter?”
* “Forecast sales for top customers”

---

---

# 4️⃣ **Prescriptive Analytics Agent (Stage 4)**

### 🏷 **Question:** *“What should we do now?”*

### 🎯 **Goal:** Provide actionable, strategic recommendations.

---

## ✅ **Responsibilities**

* Convert diagnostic + predictive insights into actions
* Build strategies like:

  * Discount optimization
  * Supply chain adjustment
  * Sales team reinforcement
  * Stock reallocation
* Prioritize actions by:

  * Impact
  * Urgency
  * Effort

---

## 🔍 **Internal Logic**

* Uses:

  * Decision trees
  * Priority scoring matrix
  * LLM-based reasoning
* Generates **SMART actions**:

  * S → Specific
  * M → Measurable
  * A → Achievable
  * R → Relevant
  * T → Time-bound

---

## 🔢 **Output (Human + Machine Combined)**

```json
{
  "priority_actions": [...],
  "impact_score": "high",
  "business_plan": "...",
  "n8n_payload": {...}
}
```

---

## 🧪 **Example Queries**

* “How do we improve sales in Chattogram?”
* “What actions should be taken for low-performing SKUs?”
* “Give me action items based on forecast.”

---

---

# 🔧 **Operational Agents**

These are not analytical agents but **control and automation agents**.

---

# 🗣️ **Chatbot Agent (Ops)**

### 🎯 **Goal:** Natural language interface to the entire system.

## Responsibilities

* Understand user query
* Map query → correct agent(s)
* Chain multi-agent calls
* Generate a combined response
* Provide follow-up questions

---

# ⚙️ **n8n Workflow Builder Agent (Ops)**

### 🎯 **Goal:** Turn insights into automated workflow triggers.

## Responsibilities

* Build actionable JSON payloads
* Trigger n8n webhooks
* Assign tasks to teams
* Send alerts (critical / high / medium)
* Automate repetitive decision loops

---

# 🔄 **Full Interaction Example**

User asks:

> “Why did Chattogram sales drop and what should we do?”

**Flow:**

1. Chatbot Agent → determines MULTI-AGENT query
2. Descriptive → fetches Chattogram summary
3. Diagnostic → finds drop causes
4. Predictive → forecasts future impact
5. Prescriptive → generates actions + n8n trigger
6. Chatbot → returns unified answer

---
 
