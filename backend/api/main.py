from fastapi import FastAPI

# Import orchestrator - pro pattern
try:
    from backend.agents.orchestrator import run_prism_workflow
except:
    def run_prism_workflow(vendor, task):
        return {"mock": True, "vendor": vendor, "task": task}

app = FastAPI(title="PRISM Governance Tower - ET Hackathon 2026")

@app.get("/health")
def health(): 
    return {"status":"ok","service":"PRISM","version":"1.0"}

@app.post("/evaluate")
def evaluate(vendor: dict, task: str):
    return run_prism_workflow(vendor, task)

@app.post("/approve/{audit_id}")
def approve(audit_id: str, approved: bool):
    return {"audit_id": audit_id, "approved": approved, "final": "EXECUTED" if approved else "BLOCKED"}
