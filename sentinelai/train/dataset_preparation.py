import os, json, networkx as nx
from core.parser import parse_contract

DATA_DIR = "data/contracts"
OUT_DIR = "data/graphs"

def prepare_dataset():
    os.makedirs(OUT_DIR, exist_ok=True)
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".sol"):
            G = parse_contract(os.path.join(DATA_DIR, fname))
            nx.write_gpickle(G, f"{OUT_DIR}/{fname.replace('.sol','.gpickle')}")
    print("✅ Dataset graphs saved.")
