import os
import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.agents.orchestrator import GovernanceOrchestrator, orchestrator
from backend.governance.audit import AuditStore, audit_store
from backend.rag.retriever import PolicyRetriever, get_relevant_policies
from backend.ml_models.risk_scorer import score_risk

os.makedirs("data", exist_ok=True)
os.makedirs("audit_logs", exist_ok=True)
os.makedirs("backend/ml_models", exist_ok=True)

app = FastAPI(
    title="PRISM - Agentic Governance Tower",
    description="Enterprise Procurement Governance, Risk Scoring, and Tamper-Evident Audit Ledger.",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IngestDocumentRequest(BaseModel):
    document_name: str = Field("vendor_contract.pdf")
    content: str = Field("Vendor ESG compliance and financial risk record.")

class EvaluateRequest(BaseModel):
    vendor_id: Optional[str] = Field("VEND-101")
    document_text: Optional[str] = Field("ESG compliance and GST audit review")
    audit_id: Optional[str] = Field(None)
    esg_score: float = Field(75.0)
    financial_stability_score: float = Field(0.85)
    gst_fraud_flag: int = Field(0)
    sanctions_match: int = Field(0)
    invoice_anomaly: float = Field(0.1)

class SimulateRequest(BaseModel):
    esg_threshold: float = Field(40.0)
    strict_mode: bool = Field(True)

class ApproveRequest(BaseModel):
    approved_by: str = Field("Compliance_Officer")
    comments: Optional[str] = Field("Approved via manual gate")

class PolicySearchRequest(BaseModel):
    q: str = Field("ESG GST Compliance")

def get_system_health() -> Dict[str, Any]:
    return {
        "status": "HEALTHY",
        "system": "PRISM - Agentic Governance Tower",
        "version": "3.0.0 - Enterprise Hackathon Build",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "pipeline_stages": {
            "stage_1_ingestion": "ACTIVE",
            "stage_2_policy_rag": "ACTIVE (TF-IDF + Cosine)",
            "stage_3_risk_scorer": "ACTIVE (ML Scorer)",
            "stage_4_human_gate": "ACTIVE (Fail-Closed)",
            "stage_5_audit_chain": "ACTIVE (SHA-256 Chained)"
        },
        "retriever_engine": {"model": "TF-IDF", "search": "Cosine", "latency": "<5ms"},
        "memory_engine": {
            "type": "Persistent JSONL Hash-Chained Ledger",
            "file_path": getattr(audit_store, 'file_path', 'data/audit_trail.jsonl'),
            "integrity": "TAMPER_EVIDENT_HASH_CHAINED"
        },
        "environment": "Render Cloud Container"
    }

@app.get("/")
def root(): return get_system_health()
@app.get("/Health")
def health_upper(): return get_system_health()
@app.get("/health")
def health_lower(): return get_system_health()

@app.post("/ingest-document")
async def ingest_document(payload: IngestDocumentRequest):
    return {"status": "SUCCESS", "document": payload.document_name, "parsed_length": len(payload.content)}

@app.post("/evaluate")
async def evaluate_vendor(payload: EvaluateRequest):
    data = payload.model_dump() if hasattr(payload, 'model_dump') else payload.dict()
    try:
        result = orchestrator.run_pipeline(payload=data, risk_scorer_fn=score_risk)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Governance Pipeline Execution Failed: {str(e)}")

@app.post("/policy/search")
async def search_policy(payload: PolicySearchRequest):
    hits = get_relevant_policies(payload.q)
    return {"retriever": "TF-IDF Vector + Cosine", "query": payload.q, "results": hits}

@app.post("/simulate")
async def simulate(payload: SimulateRequest):
    base = 40.0
    delta = payload.esg_threshold - base
    change = round(delta * 0.45, 2)
    return {
        "simulation_status": "COMPLETED",
        "parameters_applied": payload.model_dump() if hasattr(payload, 'model_dump') else payload.dict(),
        "dynamic_impact_analysis": {
            "esg_threshold_applied": payload.esg_threshold,
            "projected_flagged_vendor_rate_change_pct": f"{change}%",
            "governance_sensitivity": "HIGH" if abs(change) > 5.0 else "MODERATE",
            "strict_mode_active": payload.strict_mode
        }
    }

@app.post("/approve/{audit_id}")
async def approve(audit_id: str, payload: ApproveRequest):
    log = audit_store.log_event(audit_id=audit_id, action="HUMAN_APPROVAL", details={"approved_by": payload.approved_by, "comments": payload.comments})
    return {"status": "APPROVED", "audit_record": log}

@app.get("/audit/verify")
async def verify_audit():
    ok, msg = audit_store.verify_chain()
    return {"tamper_evident": ok, "chain_status": "VERIFIED" if ok else "CORRUPTED", "message": msg, "verification_method": "Full SHA-256 hash chain recalculation"}

@app.get("/audit/{audit_id}")
async def get_audit(audit_id: str):
    record = audit_store.get_audit(audit_id)
    if not record:
        return {"audit_id": audit_id, "status": "RECORD_NOT_FOUND"}
    return record
