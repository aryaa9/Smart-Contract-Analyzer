import torch
import torch.optim as optim
from torch_geometric.data import Data
from core.gnn_model import VulnerabilityGNN

def train_gnn(x, edge_index, y):
    model = VulnerabilityGNN(in_channels=x.size(1), hidden=16, out_channels=2)
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    loss_fn = torch.nn.CrossEntropyLoss()

    for epoch in range(100):
        optimizer.zero_grad()
        out = model(x, edge_index)
        loss = loss_fn(out, y)
        loss.backward()
        optimizer.step()
        if epoch % 10 == 0:
            print(f"Epoch {epoch}: loss {loss.item():.4f}")
    torch.save(model.state_dict(), "data/models/gnn_v1.pt")
    print("✅ GNN model trained & saved.")
