# AI_Data_Assistant

This is a conversational **AI-powered data assistant** that uses **Pandas** and **Mistral LLM (via Ollama)** to help you explore and analyze your Excel or CSV datasets.

With just natural language queries like _"Which department has the highest average salary?"_, the tool automatically:
- Loads your dataset
- Generates clean Python Pandas code using Mistral
- Executes the code
- Displays the result — instantly and interactively!

---

## 🚀 Features

- 📂 Load `.xlsx` or `.csv` files easily  
- 💬 Ask natural language questions about your dataset  
- 🧠 Get real-time responses from the Mistral language model  
- 🐼 Uses Pandas under the hood to manipulate and analyze your data  
- ⚡ Automatically executes the generated Python code

---

## 🔧 Requirements

- Python 3.8+
- Required Python packages:
  - `pandas`
  - `requests`

Install them using:

```bash
pip install pandas requests
