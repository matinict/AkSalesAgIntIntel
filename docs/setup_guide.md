# 🛠️ **Setup & Installation Guide - AkSalesAgIntIntel**

## 📋 **Multi-Agent Sales Intelligence System**

Follow this comprehensive guide to set up and run the **AkSalesAgIntIntel – Multi-Agent Sales Intelligence System** on your local machine.

---

## 🚀 **Quick Start (3 Steps)**

### **Step 1: Clone Repository & Setup Environment**

```bash
# Clone the repository
git clone https://github.com/matinict/AkSalesAgIntIntel.git
cd AkSalesAgIntIntel

# Create virtual environment
python3 -m venv sales-env

# Activate environment (Linux/Mac)
source sales-env/bin/activate

# Activate environment (Windows)
sales-env\Scripts\activate
```

> 💡 **Note:** Ensure Python 3.9+ is installed. Check with `python --version`

### **Step 2: Install Dependencies**

Choose one installation option:

**Option A: Core System Only (Minimal)**
```bash
pip install -r requirements-minimal.txt
```

**Option B: Complete System (Recommended)**
```bash
pip install -r requirements.txt
```

**Option C: Full Stack (Everything)**
```bash
pip install -r requirements-complete.txt
```

### **Step 3: Run the System**

```bash
# Run analytics engine
python3 sales_agents.py

# Launch chatbot interface
streamlit run chatbot_ui.py
```

---

## 📦 **What Each Requirements File Includes**

### **requirements-minimal.txt** (Core Only)
- ✅ pandas, numpy, plotly
- ✅ Basic analytics and visualization
- ✅ No web interface, no LangChain
- ⚡ Fastest installation

### **requirements.txt** (Standard)
- ✅ Everything in minimal
- ✅ Streamlit web interface
- ✅ LangChain framework
- ✅ Environment management
- 🎯 **Recommended for most users**

### **requirements-complete.txt** (Full Stack)
- ✅ Everything in standard
- ✅ Vector databases support
- ✅ Testing frameworks
- ✅ Code quality tools
- 🚀 For advanced users/development

---

## 🔧 **Execution Methods**

### **A. Jupyter Notebook (Recommended for Reviewers)**

```bash
jupyter notebook
```
Then open: `sales_agents.ipynb` and click **Run All**

### **B. Full Python Script (Complete Multi-Agent Logic)**

```bash
python3 sales_agents.py
```

### **C. Minimal Version (Lightweight Execution)**

```bash
python3 sales_agents_min.py
```

### **D. Chatbot Interface & Dashboard**

```bash
streamlit run chatbot_ui.py
```
Once started, open: 👉 **[http://localhost:8501/](http://localhost:8501/)**

---

## ⚙️ **System Configuration**

### **Prerequisites**
- **Python**: 3.9 or higher
- **Operating System**: Linux, macOS, or Windows
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: ~500MB for dependencies

### **Optional: API Keys Setup**
Create `.env` file for LLM features:

```bash
# OpenAI (Optional)
OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-4

# Anthropic Claude (Optional) 
ANTHROPIC_API_KEY=sk-ant-your-key

# n8n (Optional)
N8N_WEBHOOK_URL=https://your-n8n.com/webhook
```

---

## 🎯 **Getting Started with the Interface**

### **Load Dataset & Enable Interactive Tools**

Inside the Streamlit sidebar:

1. ✔ Click **"Refresh Data"** - Loads `akij_sales_data_complete.csv`
2. ✔ Select Features to Activate:
   - **Chat Assistant**
   - **Dashboard** 
   - **Analytics Insights**

This unlocks:
- Multi-Agent query processing
- Trends, KPIs, charts
- Region/Product/Channel explorations
- Automated prescriptive recommendations

---

## ⚠️ **Troubleshooting Common Issues**

### **Issue 1: "externally-managed-environment" Error**
```bash
# Solution: Always use virtual environment
python3 -m venv sales-env
source sales-env/bin/activate
pip install -r requirements.txt
```

### **Issue 2: Permission Denied**
```bash
# Check file permissions
chmod 644 akij_sales_data_complete.csv
```

### **Issue 3: Module Not Found**
```bash
# Reactivate virtual environment
source sales-env/bin/activate
pip install -r requirements.txt
```

### **Issue 4: Streamlit Port Already in Use**
```bash
# Use different port
streamlit run chatbot_ui.py --server.port 8502
```

---

## ✅ **Verification Steps**

After installation, verify everything works:

### **Test 1: Core Dependencies**
```bash
python -c "import pandas, numpy, plotly; print('✅ Core OK')"
```

### **Test 2: Streamlit**
```bash
python -c "import streamlit; print('✅ Streamlit OK')"
```

### **Test 3: Run Analytics**
```bash
python sales_agents.py
```
Should output:
```
================================================================================
GENERATING HIERARCHICAL SALES DATA - AKIJ RESOURCE
================================================================================
📦 Total Akij Products: 80+
✅ Generated 4,000 sales transactions
...
```

### **Test 4: Run Chatbot**
```bash
streamlit run chatbot_ui.py
```
Should open browser at: http://localhost:8501

---

## 📊 **System Requirements by Use Case**

### **Basic Analytics (sales_agents.py only)**
- RAM: 2GB
- CPU: 1 core  
- Disk: 100MB
- Install: `requirements-minimal.txt`

### **Chatbot Interface (Streamlit)**
- RAM: 4GB
- CPU: 2 cores
- Disk: 300MB
- Install: `requirements.txt`

### **Full Development (All Features)**
- RAM: 8GB
- CPU: 4 cores
- Disk: 500MB
- Install: `requirements-complete.txt`

---

## 📁 **Project Structure**

```
AkSalesAgIntIntel/
├── sales_agents.py                    # Main analytics engine
├── chatbot_ui.py                      # Streamlit web interface
├── sales_agents_min.py                # Lightweight version
├── sales_agents.ipynb                 # Jupyter notebook
├── requirements.txt                   # Standard dependencies
├── requirements-minimal.txt           # Core only
├── requirements-complete.txt          # Full stack
├── akij_sales_data_complete.csv       # Generated data
├── n8n_akij_workflow_*.json           # n8n workflows
└── n8n_akij_payload_*.json            # n8n payloads
```

---

## 🆘 **Getting Help**

If you encounter issues:

1. **Check Python version:** `python --version` (need 3.9+)
2. **Verify virtual env is active:** Should see `(sales-env)` in prompt
3. **Check installation:** `pip list | grep pandas`
4. **Read error messages carefully**
5. **Contact:** matinict@gmail.com

---

## ✨ **Quick Commands Reference**

```bash
# Setup
git clone https://github.com/matinict/AkSalesAgIntIntel.git
cd AkSalesAgIntIntel
python3 -m venv sales-env
source sales-env/bin/activate
pip install -r requirements.txt

# Run Analytics
python sales_agents.py

# Run Chatbot Interface  
streamlit run chatbot_ui.py

# Verify Installation
python -c "import pandas; print('OK')"

# Cleanup
deactivate
rm -rf sales-env
```

---

## 🎯 **Next Steps After Installation**

1. ✅ Run `python sales_agents.py` to generate data
2. ✅ Check `akij_sales_data_complete.csv` is created  
3. ✅ Run `streamlit run chatbot_ui.py`
4. ✅ Test the chatbot with sample queries
5. ✅ Review generated n8n workflow files

**You're all set! Start exploring your sales intelligence system!** 🚀

---

**Guide Created by Abdul Matin**  
**AkSalesAgIntIntel - Multi-Agent Sales Intelligence System**

---
 