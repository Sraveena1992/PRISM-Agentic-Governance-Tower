import logging
from typing import Dict, Any

logger = logging.getLogger("GovernanceAgent")

class GovernanceAgent:
    """Agent 2: Policy RAG + ML Risk + Statutory Rules + Fail-Closed Recovery"""

    def __init__(self):
        try:
            # FIXED IMPORTS - Canonical paths
            from backend.rag.retriever import policy_retriever
            from backend.ml_models.risk_scorer import risk_scorer
            self.retriever = policy_retriever
            self.scorer = risk_scorer
            logger.info("GovernanceAgent: RAG + ML loaded successfully")
        except Exception as e:
            logger.error(f"GovernanceAgent FAILED to load RAG/ML: {e}")
            self.retriever = None
            self.scorer = None

    def evaluate(self, enriched_data: Dict[str, Any]) -> Dict[str, Any]:
        # P0 FIX: Fail-Closed if RAG/ML unavailable - DO NOT fallback to []
        if self.retriever is None or self.scorer is None:
            logger.error("Governance subsystem unavailable -> SAFE HOLD")
            return {
                "risk_score": 0.99,
                "decision": "REJECTED",
                "requires_human_approval": False,
                "gate_reason": "SAFE HOLD: Governance subsystem (RAG/ML) unavailable - No policy authority",
                "retrieved_policies": [],
                "action": "NO_ACTION",
                "po_generated": False,
                "failure_mode": "SUBSYSTEM_UNAVAILABLE"
            }

        # Tool 1: Policy Retrieval
        try:
            policies = self.retriever.retrieve(enriched_data.get("document_text", ""), top_k=3)
        except Exception as e:
            logger.error(f"Policy retrieval failed -> SAFE HOLD: {e}")
            return {
                "risk_score": 0.99,
                "decision": "REJECTED",
                "requires_human_approval": False,
                "gate_reason": f"SAFE HOLD: Policy retrieval failed - {e}",
                "retrieved_policies": [],
                "action": "NO_ACTION",
                "po_generated": False,
                "failure_mode": "RAG_FAILURE"
            }

        # Tool 2: ML Risk
        try:
            risk_score = self.scorer.predict_risk(enriched_data)
        except Exception as e:
            logger.error(f"ML risk scoring failed -> SAFE HOLD: {e}")
            return {
                "risk_score": 0.99,
                "decision": "REJECTED",
                "requires_human_approval": False,
                "gate_reason": f"SAFE HOLD: Risk scoring failed - {e}",
                "retrieved_policies": policies,
                "action": "NO_ACTION",
                "po_generated": False,
                "failure_mode": "ML_FAILURE"
            }

        # Statutory Fail-Closed
        if enriched_data.get("gst_fraud_flag") == 1 or enriched_data.get("sanctions_match") == 1:
            return {
                "risk_score": 0.99,
                "decision": "REJECTED",
                "requires_human_approval": False,
                "gate_reason": "Statutory auto-REJECT: GST fraud / Sanctions",
                "retrieved_policies": policies,
                "risk_score_ml": risk_score,
                "action": "BLOCKED",
                "po_generated": False
            }

        # Normal governance logic
        if risk_score >= 0.8:
            decision = "REJECTED"
            requires_approval = False
        elif risk_score >= 0.5:
            decision = "REVIEW"
            requires_approval = True
        else:
            decision = "APPROVED"
            requires_approval = False

        return {
            "risk_score": risk_score,
            "decision": decision,
            "requires_human_approval": requires_approval,
            "gate_reason": f"Policy + ML evaluation - Risk {risk_score}",
            "retrieved_policies": policies,
            "action": "PENDING" if decision == "REVIEW" else ("EXECUTE" if decision == "APPROVED" else "BLOCKED"),
            "po_generated": False
        }

    def recover_with_safe_defaults(self):
        """Fail-closed recovery"""
        return {
            "risk_score": 0.99,
            "decision": "REJECTED",
            "requires_human_approval": False,
            "gate_reason": "SAFE HOLD: recover_with_safe_defaults() invoked",
            "retrieved_policies": [],
            "action": "NO_ACTION",
            "po_generated": False
        }
