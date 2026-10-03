import logging
from datetime import datetime
from typing import Dict, Any
from backend.agents.procurement_agent import ProcurementAgent
from backend.agents.governance_agent import GovernanceAgent
from backend.agents.action_agent import ActionAgent
from backend.governance.audit import audit_store

logger = logging.getLogger("PRISM-Orchestrator")

class AgenticGovernanceOrchestrator:
    """
    PRISM Control Plane: Procurement Agent -> Governance Agent -> Action Agent
    Each agent reasons independently, uses tools, and audit is the verification layer.
    """
    def __init__(self):
        self.procurement_agent = ProcurementAgent()
        self.governance_agent = GovernanceAgent()
        self.action_agent = ActionAgent()

    def run_agentic_workflow(self, vendor_payload: Dict[str, Any], simulate_failure: str = None) -> Dict[str, Any]:
        audit_id = vendor_payload.get("audit_id") or f"AUDIT-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

        # Step 1: Procurement Agent - Reasoning & Tool Selection
        enriched_data, agent_plan = self.procurement_agent.plan_and_enrich(vendor_payload)

        # Step 2: Governance Agent - RAG + ML + Rules + Self-Correction
        try:
            if simulate_failure == "policy_unavailable":
                raise ConnectionError("Policy Vector Store unavailable - simulating failure")
            gov_result = self.governance_agent.evaluate(enriched_data)
        except Exception as e:
            logger.error(f"Governance failure: {e} -> Triggering autonomous recovery")
            gov_result = self.governance_agent.recover_with_safe_defaults(enriched_data, error=str(e))

        # Step 3: Action Agent - Fail-Closed Execution
        action_result = self.action_agent.execute_action(
            audit_id=audit_id,
            decision=gov_result["decision"],
            vendor_id=enriched_data.get("vendor_id", vendor_payload.get("vendor_id")),
            requires_human_approval=gov_result["requires_human_approval"]
        )

        # Step 4: Tamper-evident Audit
        audit_entry = audit_store.log_event(
            audit_id=audit_id,
            action=f"AGENT_WORKFLOW_{gov_result['decision']}",
            details={
                "audit_id": audit_id,
                "vendor_id": enriched_data.get("vendor_id"),
                "pipeline_stages_completed": 5,
                "agent_plan": agent_plan,
                "governance_evaluation": gov_result,
                "downstream_action": action_result,
                "fail_closed_active": True
            }
        )

        return {
            "audit_id": audit_id,
            "pipeline_stages_completed": 5,
            "agent_plan": agent_plan,
            "risk_score": gov_result["risk_score"],
            "decision": gov_result["decision"],
            "gate_reason": gov_result.get("gate_reason"),
            "requires_human_approval": gov_result["requires_human_approval"],
            "retrieved_policies": gov_result.get("retrieved_policies", []),
            "action_status": action_result["status"],
            "downstream_po_id": action_result.get("po_id"),
            "current_hash": audit_entry["current_hash"],
            "previous_hash": audit_entry["previous_hash"],
            "fail_closed_active": True
        }

orchestrator = AgenticGovernanceOrchestrator()
