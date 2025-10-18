import json
import os
import networkx as nx
from core.parser import parse_contract

def build_graph(file_path, output_path="data/graphs/graph.json"):
    """Build a contract graph and export it as JSON."""
    G = parse_contract(file_path)

    # 🧩 Make sure the output folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # ⚙️ Convert to node-link format
    data = nx.node_link_data(G, edges="edges")  # forward-compatible syntax
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"📁 Graph JSON saved to: {output_path}")
    return output_path
