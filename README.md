# AkSalesAgIntIntel: Multi-Agent Sales Intelligence System

**GitHub Repository:** [https://github.com/matinict/AkSalesAgIntIntel](https://github.com/matinict/AkSalesAgIntIntel)

[![Python](https://img.shields.io/badge/Language-Python%203.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-LangChain-04C4A4?logo=chainlink)](https://www.langchain.com/)
[![Agentic AI](https://img.shields.io/badge/Architecture-Multi--Agent-007bff)](https://www.langchain.com/)
[![Orchestration](https://img.shields.io/badge/Workflow-n8n%20Integration-FF6200?logo=n8n)](https://n8n.io/)
[![UI](https://img.shields.io/badge/Interface-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io/)

A comprehensive **Agentic Intelligence system** built to provide deep, real-time sales analytics and generate **prescriptive actions** for Akij Resource. This project was developed as a submission for the **AI Agent & Agentic Intelligence Specialist** position.

It demonstrates expertise in constructing scalable, multi-agent architectures integrated with external workflow automation tools like n8n, built on a LangChain foundation.

---

## 📦 Project Submission and Downloadable Components

This section outlines the key deliverables of the submission, including the code, documentation, and demonstration resources.

| Artifact | File/Content | Access Link |
| :--- | :--- | :--- |
| **Complete Project Package** | All source code, documentation, and setup files. | [https://drive.google.com/file/d/1-shjTXeVWoM2e8KS-MdWnHfvfMomhpCL/view?usp=sharing](https://drive.google.com/file/d/1-shjTXeVWoM2e8KS-MdWnHfvfMomhpCL/view?usp=sharing) |
| **Video Walkthrough** | Complete demonstration of system functionality. | [https://youtu.be/ahtN0UOX_vQ](https://youtu.be/ahtN0UOX_vQ) |
| **Core Agent Logic** | Python source file (previously Jupyter Notebook). | `sales_agents.py` |
| **Interactive Prototype** | Streamlit web application interface. | `chatbot_ui.py` |

### 📖 Project Structure

AkSalesAgIntIntel/
│
├── [README.md](README.md)                          # Complete documentation
├── [sales_agents.py](sales_agents.py)              # Core: Multi-agent system
├── [chatbot_ui.py](chatbot_ui.py)                  # Streamlit conversational interface
├── [akij_sales_data_complete.csv](akij_sales_data_complete.csv)   # Sales dataset
├── [n8n_akij_payload_*.json](n8n_akij_payload_*.json)             # n8n AI payload
├── [n8n_akij_workflow_*.json](n8n_akij_workflow_*.json)           # n8n workflow
│
├── [requirements.txt](requirements.txt)            # Python dependencies
├── [.env.example](.env.example)                    # Environment config template
└── docs/
    ├── [architecture.md](docs/architecture.md)     # System architecture details
    ├── [agent_specifications.md](docs/agent_specifications.md)    # Agent capabilities
    └── [deployment_guide.md](docs/deployment_guide.md)            # Deployment guide
 

---

## 🔑 Key Agentic & Analytical Features

### A. Four Analytical Frameworks

The system responds to natural language queries by executing a complete, four-stage analytical cycle, leveraging separate LLM tools and agents for each stage:

1.  **Descriptive Analytics:** *What has happened?*
2.  **Diagnostic Analytics:** *Why did it happen?*
3.  **Predictive Analytics:** *What is likely to happen?*
4.  **Prescriptive Analytics:** *What actions should be taken?*

### B. Agentic Intelligence & Orchestration

* **Multi-Agent Coordination:** Implemented autonomous agents using **LangChain** for complex query decomposition, tool execution (data querying), and response synthesis.
* **n8n Workflow Integration:** Includes structured JSON payload generation capability within the Prescriptive Agent, enabling a direct path from insight to automated business action via an **n8n workflow webhook**.
* **Conversational Interface:** The Streamlit UI (`chatbot_ui.py`) acts as the front-end **AI Assistant**, interpreting queries and routing them to the appropriate analytical agent.

### C. Data Hierarchy and Scope

The system is built to handle analysis across the required hierarchical data layers:

* **Product Category**
* **Customer Segment**
* **Region** (Bangladesh Divisions)
* **Sales Channel**

---

## 🛠️ Setup and Execution

To run the project, ensure you have your LLM API keys configured in a local `.env` file.

### 1. Clone the Repository

```bash
git clone [https://github.com/matinict/AkSalesAgIntIntel.git](https://github.com/matinict/AkSalesAgIntIntel.git)
cd AkSalesAgIntIntel
