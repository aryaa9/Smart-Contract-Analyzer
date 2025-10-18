from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def critic_agent(audit_output: str):
    prompt = f"""
You are a Solidity security critic.
Given these audit findings, point out questionable assumptions or missed issues.
Return a valid JSON list of objects like:
[
  {{
    "finding": "Issue reference",
    "comment": "Critic's reasoning or doubt",
    "confidence_drop": 0.0-1.0
  }}
]
Audit Findings:
{audit_output}"""
    resp = client.chat.completions.create(
        # ✅ Updated model name
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content
