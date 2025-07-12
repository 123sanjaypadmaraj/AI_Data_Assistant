from flask import Flask, render_template, request, redirect
import pandas as pd
import requests
import re
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

df = None  # Global DataFrame to persist across requests

def build_prompt(columns, question):
    return f"""
You're a helpful data assistant. A DataFrame called 'df' is already loaded with the following columns:
{', '.join(columns)}

The user wants to know: "{question}"

Write Python pandas code to answer this.
Only return clean code inside a Python code block.
Assign the result to a variable called 'result'. No extra explanations.
"""

def ask_llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "deepseek-r1", "prompt": prompt, "stream": False}
    )
    return response.json()["response"]

def extract_code(response):
    match = re.search(r"```python(.*?)```", response, re.DOTALL)
    return match.group(1).strip() if match else response.strip()

def run_generated_code(code, df):
    try:
        local_vars = {"df": df}
        exec(code, {}, local_vars)
        result = local_vars.get("result")
        return result, None
    except Exception as e:
        return None, str(e)

@app.route("/", methods=["GET", "POST"])
def index():
    global df
    message = ""
    code = ""
    result = None

    if request.method == "POST":
        # Handle file upload
        if "file" in request.files:
            file = request.files["file"]
            if file.filename != "":
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                try:
                    if filename.endswith(".csv"):
                        df = pd.read_csv(path)
                    elif filename.endswith(".xlsx"):
                        df = pd.read_excel(path)
                    else:
                        message = "Unsupported file type."
                        return render_template("index.html", message=message)
                    message = f"File loaded with {df.shape[0]} rows and {df.shape[1]} columns."
                except Exception as e:
                    message = f"Error loading file: {e}"

        # Handle question
        if df is not None and "question" in request.form:
            question = request.form["question"]
            if question.strip():
                prompt = build_prompt(df.columns, question)
                llm_response = ask_llm(prompt)
                code = extract_code(llm_response)
                result, error = run_generated_code(code, df)
                if error:
                    message = f"Error running code: {error}"

    return render_template("index.html", message=message, code=code, result=result)

if __name__ == "__main__":
    app.run(debug=True)
