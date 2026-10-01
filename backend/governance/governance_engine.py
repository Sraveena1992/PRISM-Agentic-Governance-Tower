import hashlib, time, uuid
from backend.ml_models.risk_scorer import score_risk
from backend.rag.retriever import retrieve_policies

def evaluate_request(vendor_data, task_prompt):
    policies = retrieve_policies(task_prompt)
    try:
        risk = score_risk(vendor_data.get('esg_score',50), vendor_data.get('gst_fraud_flag',0), vendor_data.get('sanctions_match',0), vendor_data.get('invoice_anomaly',0.1))
    except:
        risk = 0.99
    if risk >= 0.8: decision="BLOCK"
    elif risk >= 0.4: decision="REVIEW"
    else: decision="ALLOW"
    audit_id = hashlib.sha256(f"{time.time()}{uuid.uuid4()}".encode()).hexdigest()[:16]
    return {"risk_score": risk, "decision": decision, "policies_applied": policies, "audit_id": audit_id, "human_required": decision=="REVIEW"}
