import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from backend.agents.procurement_agent import ProcurementAgent
from backend.agents.governance_agent import GovernanceAgent
from backend.agents.action_agent import ActionAgent
from backend.governance.audit import audit_store

logger = logging.getLogger("Orchestrator")

class Orchestrator:
    """PRISM Workflow: Procurement -> Governance -> Human Gate -> Action (Fail-Closed)"""

    def __init__(self):
        self.procurement = ProcurementAgent()
        self.governance = GovernanceAgent()
        self.action = ActionAgent()
        self.fail_next = False

    def enable_failure_simulation(self):
        self.fail_next = True

    def run_workflow(self, vendor_data: Dict[str, Any], audit_id: Optional[str] = None) -> Dict[str, Any]:
        audit_id = audit_id or f"AUD-{uuid.uuid4().hex[:6].upper()}"

        try:
            # AGENT 1 - Procurement Planning & Data Enrichment
            if hasattr(self.procurement, "plan_and_enrich"):
                enriched, agent_plan = self.procurement.plan_and_enrich(vendor_data)
            else:
                enriched = self.procurement.enrich(vendor_data)
                agent_plan = {"agent": "ProcurementAgent", "status": "enriched"}

            # AGENT 2 - Governance Evaluation with Fail-Closed Recovery
            try:
                if self.fail_next:
                    self.fail_next = False
                    raise RuntimeError("Simulated ML/RAG subsystem failure")
                gov_result = self.governance.evaluate(enriched)
                recovery_used = False
            except Exception as e:
                logger.error(f"Governance failure -> Safe defaults: {e}")
                gov_result = self.governance.recover_with_safe_defaults(enriched, str(e))
                recovery_used = True

            # AGENT 3 - Action Execution Gated by Governance
            # IMPORTANT: This is workflow action, NOT human approval action
            if gov_result["decision"] == "REJECTED" or gov_result.get("requires_human_approval"):
                action_result = self.action.execute_action(
                    audit_id,
                    gov_result["decision"],
                    vendor_data.get("vendor_id", "UNKNOWN"),
                    gov_result.get("requires_human_approval", False)
                )
                action_taken = False
            else:
                action_result = self.action.execute_action(
                    audit_id,
                    "APPROVED",
                    vendor_data.get("vendor_id", "UNKNOWN"),
                    False
                )
                action_taken = action_result.get("action_executed", False)

            # Log to Tamper-Evident SHA-256 Ledger
            audit_entry = audit_store.log_event(
                audit_id=audit_id,
                action=f"AGENT_WORKFLOW_{gov_result['decision']}",
                details={
                    "audit_id": audit_id,
                    "vendor_id": vendor_data.get("vendor_id"),
                    "agent_plan": agent_plan,
                    "governance": gov_result,
                    "action": action_result
                }
            )

            return {
                "audit_id": audit_id,
                "vendor_id": vendor_data.get("vendor_id"),
                "agent_plan": agent_plan,
                "procurement_enriched": enriched,
                "governance": gov_result,
                "action": action_result,
                "action_taken": action_taken,
                "fail_closed_recovery": recovery_used,
                "current_hash": audit_entry.get("current_hash"),
                "previous_hash": audit_entry.get("previous_hash"),
                "timestamp": datetime.utcnow().isoformat(),
                "compliant_with_p0": True
            }

        except Exception as e:
            logger.error(f"Critical workflow error: {e}")
            return {
                "audit_id": audit_id,
                "error": str(e),
                "action_taken": False,
                "fail_closed_recovery": True,
                "timestamp": datetime.utcnow().isoformat()
            }

orchestrator = Orchestrator()
