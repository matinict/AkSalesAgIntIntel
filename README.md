# AkSalesAgIntIntel: Multi-Agent Sales Intelligence System

 

[![Python](https://img.shields.io/badge/Language-Python%203.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-LangChain-04C4A4?logo=chainlink)](https://www.langchain.com/)
[![Agentic AI](https://img.shields.io/badge/Architecture-Multi--Agent-007bff)](https://www.langchain.com/)
[![Orchestration](https://img.shields.io/badge/Workflow-n8n%20Integration-FF6200?logo=n8n)](https://n8n.io/)
[![UI](https://img.shields.io/badge/Interface-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io/)

A comprehensive **Agentic Intelligence system** built to provide deep, real-time sales analytics and generate **prescriptive actions** for Akij Resource. This project was developed as a submission for the **AI Agent & Agentic Intelligence Specialist** position.

---

## 📦 Project Submission and Downloadable Components

| Artifact | File/Content | Access Link |
|---------|--------------|-------------|
| **GitHub Repository** |All Updated source code + documentation | [Github](https://github.com/matinict/AkSalesAgIntIntel)|
| **Complete Project Package** | All source code |  [GDrive](https://drive.google.com/file/d/1-shjTXeVWoM2e8KS-MdWnHfvfMomhpCL/view) |
| **Video Walkthrough** | Full demo | [Youtube Video](https://youtu.be/ahtN0UOX_vQ) | 
| **Full Documentation** | `Download Pdf` | [AMASIS.pdf](docs/AkijMulti-AgentSalesIntelligenceSystem-CompleteDocumentation.pdf) |
| **Full Documentation** | `Updated documentation` | [AMASIS](docs/AMASIS_CompleteDocumentation.md) |
| **Core Agent Logic** | `sales_agents system` | [1.ipynb](sales_agents.ipynb) [2.py Format](docs/sales_agents.ipynb)|
| **Interactive Prototype UI** | `chatbot_ui.py interface` | [chatbot_ui](chatbot_ui.py) |

---

 

## 📖 Project Structure
    AkSalesAgIntIntel/
    │
    ├── README.md                          # This file - Complete documentation
    ├── sales_agents.ipynb/.py             # Core: Multi-agent system (Jupyter Notebook)
    ├── chatbot_ui.py                      # Streamlit conversational interface
    ├── akij_sales_data_complete.csv       # Generated sales dataset (4000+ records)
    ├── n8n_akij_payload_*.json           # AI payload for n8n integration
    ├── n8n_akij_workflow_*.json          # Importable n8n workflow
    │
    ├── requirements.txt                   # Python dependencies
    ├── .env.example                       # Environment configuration template
    └── docs/
        ├── architecture.md                # System architecture details
        ├── agent_specifications.md        # Individual agent capabilities
        └── deployment_guide.md            # Production deployment guide

 
---

 


# 🛠️ **Setup & Execution Guide**

Follow the steps below to run the **AkSalesAgIntIntel – Multi-Agent Sales Intelligence System** on your local machine.

---

## **1️⃣ Clone the Repository**

```bash
git clone https://github.com/matinict/AkSalesAgIntIntel.git
cd AkSalesAgIntIntel
```

---

## **2️⃣ Create & Activate Virtual Environment**

```bash
python3 -m venv sales-env
source sales-env/bin/activate
```

> 💡 **Note:** Ensure Python 3.10+ is installed.

---

## **3️⃣ Install Required Dependencies**

```bash
pip install -r requirements.txt
```
> 💡 **Note:** Fresh Install [If  Virtual Environmentctivation Activate Not Worked].

---

## **4️⃣ Run the Analytical Engine**

You can run the analytical logic in three different modes:

### **A. Jupyter Notebook (Recommended for Reviewers)**

```bash
jupyter notebook
```

Then open:

```
sales_agents.ipynb
```

> 👉 Click **Run All** inside Jupyter Notebook to execute the entire analytical pipeline.

---

### **B. Full Python Script (Complete Multi-Agent Logic)**

```bash
python3 sales_agents.py
```

---

### **C. Minimal Version (Lightweight Execution)**

```bash
python3 sales_agents_min.py
```

---

## **5️⃣ Launch the Chatbot Interface & Dashboard**

The UI combines:

* Chat-based assistant
* Insights visualizations
* KPI dashboard

Run the Streamlit app:

```bash
streamlit run chatbot_ui.py
```

Once it starts, open the interface:

👉 **[http://localhost:8501/](http://localhost:8501/)**

---

## **6️⃣ Load Dataset & Enable Interactive Tools**

Inside the Streamlit sidebar:

### ✔ Click **“Refresh Data”**

Loads: `akij_sales_data_complete.csv`

### ✔ Select Features to Activate:

* **Chat Assistant**
* **Dashboard**
* **Analytics Insights**

This will unlock:

* Multi-Agent query processing
* Trends, KPIs, charts
* Region/Product/Channel explorations
* Automated prescriptive recommendations

--- 
