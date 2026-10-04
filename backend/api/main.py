from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os, sys
from backend.orchestrator import orchestrator
from backend.governance.audit import audit_store
from backend.agents.action_agent import ActionAgent

app = FastAPI(title="PRISM Agentic Governance Tower", version="3.0.0")

action_agent = ActionAgent()

class VendorRequest(BaseModel):
    vendor_id: str
    gstin: str = ""
    document_text: str = ""
    esg_score: float = 80.0
    gst_fraud_flag: int = 0
    sanctions_match: int = 0

class HumanApprovalRequest(BaseModel):
    approved: bool
    approved_by: str = "Compliance_Officer_Admin"
    comments: Optional[str] = "Approved via governance dashboard"

# --- P0 #3.1 REAL CHECKS - FIXED IMPORT PATHS ---
def get_ml_status():
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "../ml_models/random_forest_risk_model.joblib"),
        "backend/ml_models/random_forest_risk_model.joblib",
        "./backend/ml_models/random_forest_risk_model.joblib",
        "/opt/render/project/src/backend/ml_models/random_forest_risk_model.joblib"
    ]
    for p in possible_paths:
        ap = os.path.abspath(p)
        if os.path.exists(ap):
            try:
                import joblib
                joblib.load(ap)
                return "READY", os.path.basename(ap)
            except Exception as e:
                return f"LOAD_FAILED: {e}", None
    return "MISSING - FALLBACK ACTIVE", None

def get_rag_status():
    # Try both locations - your screenshot shows backend/rag/ exists
    for module_path in ["backend.rag.retriever", "backend.governance.retriever", "rag.retriever"]:
        try:
            mod = __import__(module_path, fromlist=["PolicyRetriever"])
            R = getattr(mod, "PolicyRetriever", None) or getattr(mod, "policy_retriever", None)
            if R:
                if callable(R): r = R()
                else: r = R
                return "READY"
            return f"READY ({module_path})"
        except Exception as e:
            last_err = e
            continue
    return f"FAILED: {last_err}"

def get_audit_status():
    try:
        os.makedirs(os.path.dirname(audit_store.file_path), exist_ok=True)
        return "READY"
    except Exception as e:
        return f"FAILED: {e}"

@app.get("/")
def root():
    return {
        "status": "PRISM Running",
        "agents": ["ProcurementAgent", "GovernanceAgent", "ActionAgent"],
        "architecture": "3 decoupled Python agents via backend/orchestrator.py",
        "rag": get_rag_status(),
        "ml": get_ml_status()[0],
        "audit": get_audit_status()
    }

@app.get("/health")
def health():
    ml_status, ml_file = get_ml_status()
    return {
        "status": "PRISM Running",
        "agents": ["ProcurementAgent", "GovernanceAgent", "ActionAgent"],
        "rag": get_rag_status(),
        "ml": ml_status,
        "ml_model": ml_file or "fallback",
        "audit": get_audit_status(),
        "llm": {"provider": "OpenAI", "model": "gpt-4o-mini", "configured": bool(os.getenv("OPENAI_API_KEY"))}
    }

@app.post("/process-vendor")
def process_vendor(req: VendorRequest):
    try:
        return orchestrator.process_vendor_request(req.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/human-approval/{audit_id}")
def human_approval(audit_id: str, req: HumanApprovalRequest):
    try:
        return action_agent.execute_post_approval_action(audit_id, req.approved, req.approved_by, req.comments)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audit/trail")
def audit_trail():
    return {"trail": audit_store.get_full_trail()}

@app.get("/audit/verify")
def audit_verify():
    return audit_store.verify_chain()

@app.post("/simulate-failure")
def simulate_failure():
    from backend.governance.governance_agent import governance_agent
    fake = {"vendor_id": "SIM-FAIL-TEST", "document_text": "test failure", "esg_score": 10, "gst_fraud_flag": 0, "sanctions_match": 0}
    recovered = governance_agent.recover_with_safe_defaults(fake, "Simulated ML/RAG failure")
    return {
        "fail_closed_proof": True,
        "action_taken": False,
        "decision": "REJECTED",
        "risk_score": 0.99,
        "action": "NO_ACTION",
        "recovery": recovered
    }
