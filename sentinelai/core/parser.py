from slither.slither import Slither
import networkx as nx

def parse_contract(file_path):
    """Parse Solidity contract and build a function call graph safely."""
    sl = Slither(file_path)
    G = nx.DiGraph()

    for contract in sl.contracts:
        for func in contract.functions:
            G.add_node(func.name, visibility=func.visibility)

            for call in func.all_internal_calls():
                callee_name = None

                # Try different possible attributes
                if hasattr(call, "name") and isinstance(call.name, str):
                    callee_name = call.name
                elif hasattr(call, "function_name") and isinstance(call.function_name, str):
                    callee_name = call.function_name
                elif hasattr(call, "names"):
                    names_attr = call.names
                    if isinstance(names_attr, (list, tuple)):
                        callee_name = ", ".join(map(str, names_attr))
                    elif isinstance(names_attr, str):
                        callee_name = names_attr
                else:
                    callee_name = str(call)

                # Clean and validate name
                if callee_name:
                    callee_name = callee_name.strip()
                    if callee_name and callee_name != func.name:
                        G.add_edge(func.name, callee_name)

    print(f"✅ Parsed {len(G.nodes)} functions and {len(G.edges)} calls from {file_path}")
    return G
