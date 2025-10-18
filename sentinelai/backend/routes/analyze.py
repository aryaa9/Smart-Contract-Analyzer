from fastapi import APIRouter, UploadFile, File
from core.graph_builder import build_graph
from agents.coordinator_agent import coordinator
import json, os

router = APIRouter()

@router.post("/analyze")
async def analyze_contract(file: UploadFile = File(...)):
    contents = await file.read()
    os.makedirs("data/contracts", exist_ok=True)
    path = f"data/contracts/{file.filename}"
    with open(path, "wb") as f:
        f.write(contents)

    graph_path = build_graph(path)
    with open(graph_path) as g:
        summary = json.load(g)

    report = coordinator(json.dumps(summary))
    return {"message": "Analysis complete", "report": report}
