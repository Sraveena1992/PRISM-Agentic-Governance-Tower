import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger("ActionAgent")


class ActionAgent:
    """Agent 3: Executes consequential enterprise action - gated by governance"""

    def execute_action(self, audit_id: str, decision: str, vendor_id: str, requires_human_approval: bool) -> Dict[str, Any]:
        if decision == "REJECTED":
            return {
                "status": "BLOCKED",
                "po_id": None,
                "erp_response": f"Vendor {vendor_id} BLOCKED - No PO created",
                "action_executed": False,
                "timestamp": datetime.utcnow().isoformat()
            }

        if decision == "REVIEW" and requires_human_approval:
            return {
                "status": "PENDING_APPROVAL",
                "po_id": None,
                "erp_response": "Awaiting HUMAN_APPROVAL - Fail-Closed, NO downstream action",
                "action_executed": False,
                "timestamp": datetime.utcnow().isoformat()
            }

        if decision == "APPROVED":
            po_id = f"PO-{audit_id}"
            return {
                "status": "APPROVED_AND_EXECUTED",
                "po_id": po_id,
                "erp_response": f"ERP Simulator: Procurement Order {po_id} CREATED for vendor {vendor_id}",
                "action_executed": True,
                "timestamp": datetime.utcnow().isoformat()
            }

        return {
            "status": "HOLD",
            "po_id": None,
            "action_executed": False,
            "timestamp": datetime.utcnow().isoformat()
        }

    def execute_post_approval_action(self, audit_id: str, vendor_id: str, approved_by: str = "Admin") -> Dict[str, Any]:
        """Triggered upon human approval from API endpoint /human-approval/{audit_id}"""
        po_id = f"PO-{audit_id}-HUMAN"
        return {
            "status": "APPROVED_VIA_HUMAN_AND_EXECUTED",
            "po_id": po_id,
            "erp_response": f"ERP Simulator: PO {po_id} CREATED post human approval by {approved_by} for vendor {vendor_id}",
            "action_executed": True,
            "approved_by": approved_by,
            "timestamp": datetime.utcnow().isoformat()
        }
