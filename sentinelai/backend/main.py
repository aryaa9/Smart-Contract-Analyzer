from fastapi import FastAPI, UploadFile, File
from core.graph_builder import build_graph
from agents.coordinator_agent import coordinator
import json

app = FastAPI(title="SentinelAI 2.0")

@app.post("/analyze")
async def analyze_contract(file: UploadFile = File(...)):
    contents = await file.read()
    path = f"data/contracts/{file.filename}"
    with open(path, "wb") as f:
        f.write(contents)

    graph_path = build_graph(path)
    with open(graph_path) as g:
        graph_summary = json.load(g)

    report = coordinator(json.dumps(graph_summary))
    return {"message": "Analysis complete", "report": report}
