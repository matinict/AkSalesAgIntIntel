# AkSalesAgIntIntel: Multi-Agent Sales Intelligence System

**GitHub Repository:** https://github.com/matinict/AkSalesAgIntIntel

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
| **Complete Project Package** | All source code + documentation | https://drive.google.com/file/d/1-shjTXeVWoM2e8KS-MdWnHfvfMomhpCL/view |
| **Video Walkthrough** | Full demo | https://youtu.be/ahtN0UOX_vQ |
| **Core Agent Logic** | `sales_agents.py` | [sales_agents.py](sales_agents.py) |
| **Interactive Prototype UI** | `chatbot_ui.py` | [chatbot_ui.py](chatbot_ui.py) |

---

## 📖 Project Structure
    AkSalesAgIntIntel/
    │
    ├── README.md                          # This file - Complete documentation
    ├── sales_agents.py                    # Core: Multi-agent system (Jupyter Notebook)
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

- [sales_agents.py](sales_agents.py) — Core multi-agent system  
- [chatbot_ui.py](chatbot_ui.py) — Streamlit UI  
- [akij_sales_data_complete.csv](akij_sales_data_complete.csv) — Sales dataset  
- [n8n_akij_payload_*.json](n8n_akij_payload_*.json) — n8n payload  
- [n8n_akij_workflow_*.json](n8n_akij_workflow_*.json) — n8n workflow  
- [requirements.txt](requirements.txt)  
- [.env.example](.env.example)  

 
---

## 📖 Project Documentation

| Document | Path | Description |
|----------|------|-------------|
| **README.md** | [README.md](README.md) | Summary documentation |
| **System Architecture** | [docs/architecture.md](docs/architecture.md) | Multi-agent + LangChain workflow architecture |
| **Agent Specifications** | [docs/agent_specifications.md](docs/agent_specifications.md) | Roles, prompts, tools |
| **Deployment Guide** | [docs/deployment_guide.md](docs/deployment_guide.md) | Local/cloud deployment |

---

## 🔑 Key Agentic & Analytical Features

### A. Four Analytical Frameworks
1. **Descriptive Analytics** — What happened  
2. **Diagnostic Analytics** — Why it happened  
3. **Predictive Analytics** — What will happen  
4. **Prescriptive Analytics** — What to do next  

### B. Main System Features
- Multi-agent orchestration with LangChain  
- n8n workflow integration  
- Streamlit conversational UI  
- Structured JSON output for automation  

---

## 🛠️ Setup and Execution

### 1. Clone the Repository

```bash
git clone https://github.com/matinict/AkSalesAgIntIntel.git
cd AkSalesAgIntIntel
