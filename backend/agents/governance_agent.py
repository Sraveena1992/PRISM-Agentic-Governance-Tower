import logging
from typing import Dict, Any, List

logger = logging.getLogger("GovernanceAgent")

class GovernanceAgent:
    """Deterministic Governance Gate - NOT autonomous"""

    def evaluate(self, enriched_data: Dict[str, Any]) -> Dict[str, Any]:
        # Your existing logic - ML + RAG + Rules
        # Keep as is, just ensure it can raise on ML failure
        from backend.ml_models.risk_scorer import risk_scorer
        from backend.rag.retriever import policy_retriever

        try:
            risk_score = risk_scorer.predict_risk(enriched_data)
        except Exception as e:
            # P1 FIX: Don't swallow - propagate to fail-closed
            logger.error(f"ML inference failed, propagating to fail-closed: {e}")
            raise RuntimeError(f"ML subsystem failure: {e}")

        policies = []
        try:
            policies = policy_retriever.retrieve(enriched_data.get("document_text", ""))
        except Exception as e:
            logger.warning(f"RAG failure: {e}")
            raise RuntimeError(f"RAG subsystem failure: {e}")

        # Statutory gates
        if enriched_data.get("gst_fraud_flag") == 1 or enriched_data.get("sanctions_match") == 1:
            return {
                "risk_score": 0.99,
                "decision": "REJECTED",
                "requires_human_approval": False,
                "gate_reason": "STATUTORY GATE: Fraud/Sanctions",
                "retrieved_policies": policies,
                "action": "NO_ACTION"
            }

        if risk_score > 0.8 or enriched_data.get("amount", 0) > 400000:
            return {
                "risk_score": risk_score,
                "decision": "REVIEW",
                "requires_human_approval": True,
                "gate_reason": f"High risk/amount: {risk_score}",
                "retrieved_policies": policies,
                "action": "NO_ACTION"
            }

        return {
            "risk_score": risk_score,
            "decision": "APPROVED",
            "requires_human_approval": False,
            "gate_reason": "All gates passed",
            "retrieved_policies": policies,
            "action": "PO_CREATED"
        }

    # --- P0 #1 FINAL FIX: Correct Signature ---
    def recover_with_safe_defaults(
        self,
        enriched_data=None,
        error_message=None
    ) -> Dict[str, Any]:
        """
        Fail-Closed Recovery - Signature FIXED
        Called by orchestrator and /simulate-failure
        """
        return {
            "risk_score": 0.99,
            "decision": "REJECTED",
            "requires_human_approval": False,
            "gate_reason": (
                "SAFE HOLD: Governance subsystem failure"
                + (f" - {error_message}" if error_message else "")
            ),
            "retrieved_policies": [],
            "action": "NO_ACTION",
            "po_generated": False,
            "failure_mode": "SUBSYSTEM_FAILURE"
        }

governance_agent = GovernanceAgent()
