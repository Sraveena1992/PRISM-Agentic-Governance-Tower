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
                "action": "NO_ACTION",
                "po_generated": False,
                "timestamp": datetime.utcnow().isoformat()
            }

        if decision == "REVIEW" and requires_human_approval:
            return {
                "status": "PENDING_APPROVAL",
                "po_id": None,
                "erp_response": "Awaiting HUMAN_APPROVAL - Fail-Closed, NO downstream action",
                "action_executed": False,
                "action": "NO_ACTION",
                "po_generated": False,
                "timestamp": datetime.utcnow().isoformat()
            }

        if decision == "APPROVED":
            po_id = f"PO-{audit_id}"
            return {
                "status": "APPROVED_AND_EXECUTED",
                "po_id": po_id,
                "erp_response": f"ERP Simulator: Procurement Order {po_id} CREATED for vendor {vendor_id}",
                "action_executed": True,
                "action": "PO_CREATED",
                "po_generated": True,
                "timestamp": datetime.utcnow().isoformat()
            }

        return {
            "status": "HOLD",
            "po_id": None,
            "action_executed": False,
            "action": "NO_ACTION",
            "po_generated": False,
            "timestamp": datetime.utcnow().isoformat()
        }

    def execute_post_approval_action(
        self, 
        audit_id: str, 
        vendor_id: str, 
        approved_by: str = "Admin",
        approved: bool = True,
        comments: str = ""
    ) -> Dict[str, Any]:
        """
        P0 #2 FIX - FINAL CONTRACT
        Handles both APPROVE and REJECT from human
        Signature now accepts: audit_id, vendor_id, approved_by, approved, comments
        This fixes the 4-args vs 3-args bug
        """
        if not approved:
            logger.info(f"Human REJECTED audit {audit_id} by {approved_by}: {comments}")
            return {
                "status": "REJECTED_BY_HUMAN",
                "audit_id": audit_id,
                "vendor_id": vendor_id,
                "po_id": None,
                "erp_response": f"Human rejection by {approved_by} - NO PO for vendor {vendor_id}. Reason: {comments}",
                "action_executed": False,
                "action": "NO_ACTION",
                "po_generated": False,
                "approved_by": approved_by,
                "approved": False,
                "comments": comments,
                "timestamp": datetime.utcnow().isoformat()
            }

        # APPROVED path
        po_id = f"PO-{audit_id}-HUMAN"
        logger.info(f"Human APPROVED audit {audit_id} by {approved_by}")
        return {
            "status": "APPROVED_VIA_HUMAN_AND_EXECUTED",
            "audit_id": audit_id,
            "vendor_id": vendor_id,
            "po_id": po_id,
            "erp_response": f"ERP Simulator: PO {po_id} CREATED post human approval by {approved_by} for vendor {vendor_id}",
            "action_executed": True,
            "action": "PO_CREATED",
            "po_generated": True,
            "approved_by": approved_by,
            "approved": True,
            "comments": comments,
            "timestamp": datetime.utcnow().isoformat()
        }
