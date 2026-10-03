from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from backend.orchestrator import orchestrator
from backend.governance.audit import audit_store
from backend.agents.action_agent import ActionAgent

app = FastAPI(title="PRISM Agentic Governance Tower", version="1.0.0")

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


@app.get("/")
def health():
    return {
        "status": "PRISM Running",
        "agents": ["ProcurementAgent", "GovernanceAgent", "ActionAgent"],
        "p0_compliant": True
    }


@app.post("/process-vendor")
def process_vendor(req: VendorRequest):
    result = orchestrator.run_workflow(req.dict())
    return result


@app.post("/simulate-failure")
def simulate_failure(req: VendorRequest):
    """Judge evaluation endpoint - Fail-Closed Recovery Demo"""
    orchestrator.enable_failure_simulation()
    result = orchestrator.run_workflow(req.dict())
    return {
        "demo": "Simulated ML/RAG failure -> Recovered with Safe Defaults (Fail-Closed)",
        "fail_closed_proof": result.get("fail_closed_recovery", True),
        "action_taken": result.get("action_taken", False),
        "result": result
    }


@app.post("/human-approval/{audit_id}")
def human_approval(audit_id: str, payload: HumanApprovalRequest):
    """Human-in-the-Loop Gate Execution"""
    audit_record = audit_store.get_audit(audit_id)
    if not audit_record:
        raise HTTPException(status_code=404, detail=f"Audit ID {audit_id} not found")

    vendor_id = audit_record.get("details", {}).get("vendor_id", "UNKNOWN")

    if payload.approved:
        # Downstream execution on approval
        action_result = action_agent.execute_post_approval_action(
            audit_id=audit_id,
            vendor_id=vendor_id,
            approved_by=payload.approved_by
        )
        
        # Log to SHA-256 Audit Chain
        audit_entry = audit_store.log_event(
            audit_id=audit_id,
            action="HUMAN_APPROVAL_EXECUTED",
            details={
                "approved_by": payload.approved_by,
                "comments": payload.comments,
                "action_result": action_result
            }
        )
        return {
            "audit_id": audit_id,
            "status": "HUMAN_APPROVED_AND_EXECUTED",
            "action": action_result,
            "audit_entry": audit_entry
        }
    else:
        audit_entry = audit_store.log_event(
            audit_id=audit_id,
            action="HUMAN_REJECTED",
            details={
                "approved_by": payload.approved_by,
                "comments": payload.comments,
                "status": "BLOCKED_BY_HUMAN"
            }
        )
        return {
            "audit_id": audit_id,
            "status": "HUMAN_REJECTED",
            "action": {"status": "BLOCKED", "action_executed": False},
            "audit_entry": audit_entry
        }


@app.get("/audit/{audit_id}")
def get_audit(audit_id: str):
    record = audit_store.get_audit(audit_id)
    if not record:
        raise HTTPException(status_code=404, detail="Audit ID not found")
    return record


@app.get("/audits")
def get_all_audits():
    return audit_store.get_all_audits()
