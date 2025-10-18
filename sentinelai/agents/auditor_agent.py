from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def auditor_agent(contract_summary: str):
    """
    Analyzes smart contract data and produces structured vulnerability findings.
    Always outputs a valid JSON list.
    """
    prompt = f"""
    You are a professional smart contract auditor specializing in Solidity security.

    Analyze the given contract structure and static analysis output below.
    Identify all possible vulnerabilities or design flaws.

    Return ONLY a valid JSON list with the following format:
    [
      {{
        "issue": "Short, clear title of the problem",
        "severity": "Critical | High | Medium | Low | Info",
        "function_name": "Name of affected function, if any",
        "risk_score": 0-100,
        "suggested_fix": "Actionable short fix suggestion"
      }}
    ]

    Contract Data:
    {contract_summary}
    """

    models = [
        "llama-3.3-70b-versatile",
        "llama-3.2-70b-versatile",
        "llama-3.2-8b-preview"
    ]

    for model in models:
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            print(f"✅ [Auditor Agent] Using model: {model}")
            return resp.choices[0].message.content
        except Exception as e:
            if "model_not_found" in str(e):
                print(f"⚠️ [Auditor Agent] Model {model} unavailable, trying next...")
                continue
            raise e

    return "[]"
