from fastapi import FastAPI
from backend.agents.orchestrator import orchestrator
from backend.governance.audit import audit_store
from backend.ml_models.risk_scorer import score_risk
from backend.rag.retriever import get_relevant_policies

app = FastAPI(title="PRISM - Enterprise Governance")

@app.get("/")
def home():
    return {"status": "PRISM Running - 5 Agents Active"}

@app.post("/evaluate")
async def evaluate_vendor(payload: dict):
    # Orchestrator runs the complete 5-agent pipeline
    result = orchestrator.run_pipeline(
        payload=payload,
        risk_scorer_fn=score_risk
    )
    return {
        "status": "success",
        "audit_id": result["audit_id"],
        "vendor_id": result["vendor_id"],
        "risk_score": result["risk_score"],
        "decision": result["decision"],
        "retrieved_policies": result["policies"]
    }

@app.get("/audit/verify")
async def verify_audit():
    ok, msg = audit_store.verify_chain()
    return {"immutable": ok, "message": msg}

@app.post("/policy/search")
async def search_policy(query: dict):
    hits = get_relevant_policies(query.get("q", "ESG GST"))
    return {"retriever": "FAISS + MiniLM", "results": hits}
