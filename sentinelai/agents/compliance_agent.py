from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def compliance_agent(audit_output):
    prompt = f"""
You are a compliance analyst.
Check if this contract adheres to common DeFi and ERC standards.
Return a JSON list like:
[
  {{
    "standard": "ERC20 / ERC721 / ERC4626 / Custom",
    "issue": "Non-compliance detail",
    "severity": "High | Medium | Low",
    "recommendation": "How to fix or comply"
  }}
]
Input: {audit_output}
"""

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content
