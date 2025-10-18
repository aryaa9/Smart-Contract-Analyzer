import json
from .auditor_agent import auditor_agent
from .critic_agent import critic_agent
from .compliance_agent import compliance_agent

def safe_json_loads(text):
    """Try parsing JSON, even if model response includes code blocks or text."""
    if not text or not text.strip():
        return []
    text = text.strip()
    # Remove code fences if present
    if text.startswith("```"):
        text = text.strip("` \n")
        if text.startswith("json"):
            text = text[4:]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # If it's not valid JSON, return as raw text
        return [{"raw_text": text}]

def coordinator(contract_summary: str):
    """Run all agents and aggregate their reports safely."""
    print("🤖 [Coordinator] Running Auditor Agent...")
    audit_response = auditor_agent(contract_summary)
    audit = safe_json_loads(audit_response)

    print("🧐 [Coordinator] Running Critic Agent...")
    critic_response = critic_agent(json.dumps(audit))
    critique = safe_json_loads(critic_response)

    print("📋 [Coordinator] Running Compliance Agent...")
    compliance_response = compliance_agent(json.dumps(audit))
    compliance = safe_json_loads(compliance_response)

    final = {
        "audit_findings": audit,
        "critic_review": critique,
        "compliance_map": compliance
    }

    # Save report
    import os
    os.makedirs("data/reports", exist_ok=True)
    with open("data/reports/final_report.json", "w") as f:
        json.dump(final, f, indent=2)

    print("✅ [Coordinator] All agents completed successfully.")
    return final
