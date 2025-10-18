import os
import json
import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(graph_json_path, findings=None, output_path="data/graphs/graph.png"):
    """
    Visualizes the Solidity call graph.
    - findings: optional list of vulnerability dicts [{function_name, risk_score}, ...]
    - Saves PNG at output_path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(graph_json_path) as f:
        data = json.load(f)
    G = nx.node_link_graph(data)

    # color-code nodes by risk level
    color_map = []
    for node in G.nodes():
        risk = 0
        if findings:
            for fnd in findings:
                if fnd.get("function_name") and fnd["function_name"].lower() in node.lower():
                    risk = fnd.get("risk_score", 0)
                    break
        # risk color scaling
        if risk > 70:
            color_map.append("red")
        elif risk > 30:
            color_map.append("orange")
        else:
            color_map.append("lightgreen")

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G, pos,
        with_labels=True,
        node_color=color_map,
        node_size=2500,
        font_size=9,
        font_weight="bold",
        edge_color="#555",
        alpha=0.9,
    )
    plt.title("SentinelAI Function Call Graph", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"📊 Graph visualization saved to: {output_path}")
    return output_path
