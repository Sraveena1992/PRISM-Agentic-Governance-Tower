from typing import Dict, Any, TypedDict
from backend.rag.retriever import get_relevant_policies
from backend.governance.audit import audit_store

class GovernanceState(TypedDict):
    vendor_id: str
    document_text: str
    policies: list
    risk_score: float
    decision: str
    audit_id: str

class AgenticGovernanceOrchestrator:
    def __init__(self):
        pass

    def data_ingestion_agent(self, state: GovernanceState) -> GovernanceState:
        """Step 1: Parse input payload & extract regulatory obligations"""
        state["policies"] = get_relevant_policies(state.get("document_text", "ESG GST Compliance"))
        return state

    def risk_assessment_agent(self, state: GovernanceState, risk_scorer_fn) -> GovernanceState:
        """Step 2: ML Model prediction & Policy rule evaluation"""
        score, decision = risk_scorer_fn(state)
        state["risk_score"] = score
        state["decision"] = decision
        return state

    def human_gate_agent(self, state: GovernanceState) -> GovernanceState:
        """Step 3: Route high-risk cases to fail-closed approval gate"""
        if state["risk_score"] >= 0.60 or state["decision"] == "REVIEW":
            state["decision"] = "PENDING_HUMAN_APPROVAL"
        return state

    def audit_execution_agent(self, state: GovernanceState) -> GovernanceState:
        """Step 4: Persist event in SHA-256 hashed audit log"""
        log_entry = audit_store.log_event(
            audit_id=state["audit_id"],
            action="GOVERNANCE_EVALUATION",
            details={
                "vendor_id": state.get("vendor_id"),
                "risk_score": state["risk_score"],
                "decision": state["decision"]
            }
        )
        return state

    def run_pipeline(self, payload: Dict[str, Any], risk_scorer_fn) -> Dict[str, Any]:
        """Executes the complete Agentic State Workflow"""
        state: GovernanceState = {
            "vendor_id": payload.get("vendor_id", "VEND-UNKNOWN"),
            "document_text": payload.get("document_text", "ESG GST Compliance"),
            "policies": [],
            "risk_score": 0.0,
            "decision": "UNKNOWN",
            "audit_id": payload.get("audit_id", "AUDIT-INIT")
        }
        
        # Sequentially execute state transitions
        state = self.data_ingestion_agent(state)
        state = self.risk_assessment_agent(state, risk_scorer_fn)
        state = self.human_gate_agent(state)
        state = self.audit_execution_agent(state)
        
        return state

orchestrator = AgenticGovernanceOrchestrator()
