import os
import sys
import streamlit as st
from PIL import Image

# ensure root in import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analyze_contract import run_analysis

# ----- Streamlit Page Config -----
st.set_page_config(page_title="SentinelAI Dashboard", page_icon="🧠", layout="wide")

# ----- Header -----
st.markdown(
    """
    <h1 style='text-align:center; color:#2E86C1;'>🧠 SentinelAI Smart Contract Auditor</h1>
    <p style='text-align:center; color:gray;'>
    AI + Multi-Agent + Graph Neural Network powered security analysis for Ethereum smart contracts.
    </p>
    """,
    unsafe_allow_html=True
)

# ----- Upload -----
uploaded_file = st.file_uploader("📂 Upload a Solidity contract", type=["sol"])

if uploaded_file is not None:
    os.makedirs("data/contracts", exist_ok=True)
    file_path = os.path.join("data/contracts", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Running AI-powered audit... please wait ⏳"):
        report = run_analysis(file_path)

    st.success("✅ Audit complete!")

    # ===== SUMMARY =====
    st.markdown("## 📊 Risk Overview")
    st.markdown(
        f"""
        <div style='padding:12px; border-radius:8px; background-color:#F8F9F9; border-left:6px solid #2E86C1;'>
            <b>Overall Contract Risk Score:</b> <span style='font-size:20px; color:#2E86C1;'>{round(report["overall_risk_score"], 2)}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ===== FINDINGS =====
    st.markdown("## 🔍 Vulnerability Findings")

    findings = []
    if isinstance(report["full_report"], dict):
        findings = report["full_report"].get("audit_findings", [])
    elif isinstance(report["full_report"], list):
        findings = report["full_report"]

    if not findings:
        st.markdown("> ✅ No vulnerabilities detected.")
    else:
        for fnd in findings:
            severity = fnd.get("severity", "Info")
            issue = fnd.get("issue", "Unnamed Issue")
            suggestion = fnd.get("suggested_fix", "No suggestion provided.")
            func = fnd.get("function_name", "N/A")

            color = {
                "Critical": "#E74C3C",
                "High": "#E67E22",
                "Medium": "#F1C40F",
                "Low": "#2ECC71",
                "Info": "#5DADE2"
            }.get(severity, "#5DADE2")

            st.markdown(
                f"""
                <div style='background-color:{color}15; border-left:6px solid {color}; border-radius:6px; padding:12px; margin-bottom:12px;'>
                    <b style='color:{color};'>Severity:</b> {severity}<br>
                    <b>Function:</b> `{func}`<br>
                    <b>Issue:</b> {issue}<br>
                    <b>Suggested Fix:</b> <i>{suggestion}</i>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ===== AGENT INSIGHTS =====
    st.markdown("## 🤖 Agent Insights")

    agent_labels = {
        "audit_findings": "🧩 Auditor Agent Findings",
        "critic_review": "🔍 Critic Agent Review",
        "compliance_map": "📋 Compliance Agent Observations"
    }

    for key, label in agent_labels.items():
        if key in report["full_report"]:
            with st.expander(label):
                section = report["full_report"][key]
                if isinstance(section, list) and section and isinstance(section[0], dict):
                    for i, entry in enumerate(section, 1):
                        st.markdown(
                            f"""
                            **Finding {i}:**  
                            - **Comment:** {entry.get('comment', 'N/A')}  
                            - **Confidence Drop:** {entry.get('confidence_drop', 'N/A')}  
                            """
                        )
                else:
                    st.markdown(f"```markdown\n{section}\n```")

    # ===== GRAPH =====
    graph_path = "data/graphs/graph.png"
    if os.path.exists(graph_path):
        st.markdown("## 🕸️ Function Call Graph")
        st.image(Image.open(graph_path), caption="Smart Contract Function Structure", use_column_width=True)

else:
    st.info("Upload a `.sol` file to begin analysis.")
