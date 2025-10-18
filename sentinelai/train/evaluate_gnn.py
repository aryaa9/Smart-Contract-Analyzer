import torch
from core.gnn_model import VulnerabilityGNN

def evaluate_gnn(x_test, edge_index_test, y_test):
    model = VulnerabilityGNN(in_channels=x_test.size(1), hidden=16, out_channels=2)
    model.load_state_dict(torch.load("data/models/gnn_v1.pt"))
    model.eval()
    preds = model(x_test, edge_index_test).argmax(dim=1)
    acc = (preds == y_test).sum().item() / y_test.size(0)
    print(f"✅ GNN accuracy: {acc*100:.2f}%")
