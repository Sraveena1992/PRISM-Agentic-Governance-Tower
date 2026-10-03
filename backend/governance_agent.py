from typing import Dict, Any
import logging

logger = logging.getLogger("GovernanceAgent")

class GovernanceAgent:
    """Agent 2: Policy RAG + ML Risk + Statutory Rules + Fail-Closed Recovery"""
    
    def __init__(self):
        try:
            from backend.rag.policy_retriever import policy_retriever
            from backend.ml_models.risk_model import risk_scorer
            self.retriever = policy_retriever
            self.scorer = risk_scorer
        except Exception as e:
            logger.warning(f"Using fallback retriever/scorer: {e}")
            self.retriever = None
            self.scorer = None

    def evaluate(self, enriched_data: Dict[str, Any]) -> Dict[str, Any]:
        # Tool 1: Policy Retrieval
        try:
            policies = self.retriever.retrieve(enriched_data.get("document_text",""), top_k=3) if self.retriever else []
        except:
            policies = []

        # Tool 2: ML Risk
        try:
            risk_score = self.scorer.predict_risk(enriched_data) if self.scorer else 0.5
        except:
            risk_score = 0.5

        # Statutory Fail-Closed
        if enriched_data.get("gst_fraud_flag") == 1 or enriched_data.get("sanctions_match") == 1:
            return {
                "risk_score": 0.99, "decision": "REJECTED",
                "requires_human_approval": False,
                "gate_reason": "Statutory auto-REJECT: GST fraud / Sanctions",
                "retrieved_policies": policies
            }
        
        if float(enriched_data.get("esg_score", 100)) < 40:
            return {
                "risk_score": 0.85, "decision": "REVIEW",
                "requires_human_approval": True,
                "gate_reason": "Low ESG (<40) triggers human gate",
                "retrieved_policies": policies
            }

        if risk_score < 0.35:
            decision = "APPROVED"
        elif risk_score < 0.70:
            decision = "REVIEW"
        else:
            decision = "REJECTED"

        return {
            "risk_score": risk_score, "decision": decision,
            "requires_human_approval": decision == "REVIEW",
            "gate_reason": f"ML risk {risk_score:.2f} -> {decision}",
            "retrieved_policies": policies
        }

    def recover_with_safe_defaults(self, enriched_data: Dict[str, Any], error: str) -> Dict[str, Any]:
        return {
            "risk_score": 0.99, "decision": "REJECTED",
            "requires_human_approval": False,
            "gate_reason": f"Subsystem failure: {error} -> SAFE HOLD (Fail-Closed, No Action)",
            "retrieved_policies": [],
            "recovery_attempted": True
        }
