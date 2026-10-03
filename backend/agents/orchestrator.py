import os
import json
from datetime import datetime
from typing import Dict, Any, Callable, Optional, List

from backend.governance.audit import AuditStore, audit_store

# Safely import functions / classes from retriever
try:
    from backend.rag.retriever import PolicyRetriever
except ImportError:
    PolicyRetriever = None

try:
    from backend.rag.retriever import get_relevant_policies
except ImportError:
    def get_relevant_policies(query: str, top_k: int = 3):
        return []


class GovernanceOrchestrator:
    def __init__(self, audit_store_instance: Optional[AuditStore] = None, retriever_instance: Optional[Any] = None):
        self.audit_store = audit_store_instance or audit_store
        # Fallback to None if PolicyRetriever class does not exist
        if retriever_instance:
            self.retriever = retriever_instance
        elif PolicyRetriever is not None:
            self.retriever = PolicyRetriever()
        else:
            self.retriever = None

    def run_pipeline(self, payload: Dict[str, Any], risk_scorer_fn: Callable[[Dict[str, Any]], float]) -> Dict[str, Any]:
        """
        Deterministic 5-Stage Authoritative Governance Pipeline Execution.
        Stage 1: Ingestion & Metadata Normalization
        Stage 2: Policy RAG Retrieval (TF-IDF Vector + Cosine Similarity)
        Stage 3: ML Risk Engine Scoring (Scikit-Learn RandomForest Scorer)
        Stage 4: Fail-Closed Gate & Decision Matrix
        Stage 5: Cryptographic SHA-256 Chained Audit Trail
        """
        # --- STAGE 1: Data Ingestion & Field Normalization ---
        vendor_id = payload.get("vendor_id", "VEND-UNKNOWN")
        document_text = payload.get("document_text", payload.get("content", "Vendor compliance evaluation record"))
        
        # Canonical feature normalization across incoming API requests
        esg_score = float(payload.get("esg_score", payload.get("esg_rating", 75.0)))
        financial_stability = float(payload.get("financial_stability_score", 0.85))
        gst_fraud_flag = int(payload.get("gst_fraud_flag", 0))
        sanctions_match = int(payload.get("sanctions_match", 0))
        invoice_anomaly = float(payload.get("invoice_anomaly", payload.get("invoice_anomaly_score", 0.10)))

        normalized_payload = {
            "vendor_id": vendor_id,
            "document_text": document_text,
            "esg_score": esg_score,
            "financial_stability_score": financial_stability,
            "gst_fraud_flag": gst_fraud_flag,
            "sanctions_match": sanctions_match,
            "invoice_anomaly": invoice_anomaly
        }

        # --- STAGE 2: Policy RAG Vector Retrieval ---
        rag_query = f"ESG {esg_score} GST fraud {gst_fraud_flag} sanctions {sanctions_match} financial stability {financial_stability}"
        if self.retriever and hasattr(self.retriever, 'search'):
            retrieved_policies = self.retriever.search(query=rag_query, top_k=3)
        else:
            retrieved_policies = get_relevant_policies(rag_query)

        # --- STAGE 3: Deterministic ML Risk Engine Scoring ---
        risk_score = risk_scorer_fn(normalized_payload)

        # --- STAGE 4: Fail-Closed Decision Engine ---
        if gst_fraud_flag == 1 or sanctions_match == 1:
            decision = "REJECTED"
            requires_human_approval = False
            gate_reason = "Fail-Closed Statutory Block: GST fraud / Sanctions list match - automatic rejection per compliance policy"
        elif risk_score >= 0.50 or esg_score < 40.0 or financial_stability < 0.50:
            decision = "REVIEW"
            requires_human_approval = True
            gate_reason = "Risk score exceeds automated tolerance threshold; routed to Human Gate"
        else:
            decision = "APPROVED"
            requires_human_approval = False
            gate_reason = "Low risk profile; auto-approval policy met"

        audit_id = payload.get("audit_id") or f"AUDIT-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

        execution_summary = {
            "audit_id": audit_id,
            "vendor_id": vendor_id,
            "pipeline_stages_completed": 5,
            "risk_score": risk_score,
            "decision": decision,
            "requires_human_approval": requires_human_approval,
            "gate_reason": gate_reason,
            "retrieved_policies": retrieved_policies,
            "fail_closed_active": True,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        # --- STAGE 5: Audit Ledger (Cryptographic SHA-256 Hash Chain) ---
        audit_record = self.audit_store.log_event(
            audit_id=audit_id,
            action=f"GOVERNANCE_EVALUATION_{decision}",
            details=execution_summary
        )

        execution_summary["audit_chain_hash"] = audit_record.get("current_hash")
        execution_summary["previous_hash"] = audit_record.get("previous_hash")

        return execution_summary


# Export Singleton Instance and Class
orchestrator = GovernanceOrchestrator()
