import time
import json
import uuid
import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from detector import analyze_input, check_rate_limit
from config import CONFIG
from app.utils.logging_util import save_audit_log

app = FastAPI(title="LLM Security Gateway - CSC262")

LOG_FILE = "results/audit_log.jsonl"
os.makedirs("results", exist_ok=True)

def read_audit_log(limit: int = 20):
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    entries = []
    for line in lines[-limit:]:
        try:
            entries.append(json.loads(line))
        except:
            pass
    return entries

class UserMessage(BaseModel):
    user_id: str = "anonymous"
    input_id: Optional[str] = None
    text: str

@app.get("/")
def home():
    return {"status": "LLM Security Gateway Running", "version": "2.0-final"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": time.time(),
        "languages_supported": ["en", "ur", "ko"],
        "model": "TF-IDF + Logistic Regression"
    }

@app.post("/analyze")
def analyze(message: UserMessage):
    if check_rate_limit(message.user_id):
        return {
            "input_id": message.input_id or "N/A",
            "user_id": message.user_id,
            "decision": "BLOCK",
            "reason_codes": ["RATE_LIMIT_EXCEEDED"],
            "latency_ms": 0
        }

    input_id = message.input_id or str(uuid.uuid4())[:8]

    result = analyze_input(
        text=message.text,
        input_id=input_id,
        user_id=message.user_id
    )

    save_audit_log(result)

    return result

@app.get("/audit")
def audit_log(limit: int = 20):
    entries = read_audit_log(limit=limit)
    return {
        "total_returned": len(entries),
        "entries": entries
    }

@app.get("/stats")
def stats():
    entries = read_audit_log(limit=1000)
    if not entries:
        return {"message": "No logs yet"}
    decisions = [e.get("decision") for e in entries]
    return {
        "total_requests": len(entries),
        "blocked": decisions.count("BLOCK"),
        "masked": decisions.count("MASK"),
        "allowed": decisions.count("ALLOW"),
    }