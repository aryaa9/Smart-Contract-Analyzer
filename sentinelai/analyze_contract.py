import os
import json
from dotenv import load_dotenv

# core imports
from core.graph_builder import build_graph
from core.risk_engine import calculate_overall_risk
from core.visualizer import visualize_graph

# agent system
from agents.coordinator_agent import coordinator

load_dotenv()


def run_analysis(file_path: str):
    """Run a full SentinelAI analysis pipeline for a single Solidity contract."""
    print(f"\n🔍 Running SentinelAI 2.1 analysis on: {file_path}")

    # 1️⃣ Build function call graph
    print("🧠 Building contract graph...")
    graph_path = build_graph(file_path)

    with open(graph_path) as g:
        graph_data = json.load(g)

    # 2️⃣ Run AI audit via multi-agent system
    print("🤖 Running AI audit with agents (Auditor, Critic, Compliance)...")
    report = coordinator(json.dumps(graph_data))

    # 3️⃣ Compute overall risk score
    gnn_score = 75  # placeholder for Phase 2 (GNN model)
    agent_confidences = [80, 60, 70]  # simulated confidences
    overall_risk = calculate_overall_risk(gnn_score, agent_confidences)

    # 4️⃣ Combine and save final report
    final_report = {
        "file_analyzed": os.path.basename(file_path),
        "overall_risk_score": overall_risk,
        "full_report": report,
    }

    os.makedirs("data/reports", exist_ok=True)
    output_path = f"data/reports/{os.path.basename(file_path).replace('.sol','')}_report.json"

    with open(output_path, "w") as f:
        json.dump(final_report, f, indent=2)

    # 5️⃣ Visualize function-call graph with risk overlays
    try:
        findings = []
        if isinstance(report, dict) and "audit_findings" in report:
            findings = report["audit_findings"]
        elif isinstance(report, list):
            findings = report
        visualize_graph(graph_path, findings=findings)
    except Exception as e:
        print(f"⚠️ Visualization skipped: {e}")

    print("\n✅ Audit completed! Report saved at:", output_path)
    print(f"📊 Overall Contract Risk Score: {overall_risk}\n")

    return final_report


if __name__ == "__main__":
    contract_path = "data/contracts/sample.sol"
    if not os.path.exists(contract_path):
        print("❌ Contract not found. Please place one in data/contracts/")
    else:
        run_analysis(contract_path)
