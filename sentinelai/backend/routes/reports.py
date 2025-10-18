from fastapi import APIRouter
import json, os

router = APIRouter()

@router.get("/report/{filename}")
async def get_report(filename: str):
    path = f"data/reports/{filename}"
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"error": "Report not found."}
