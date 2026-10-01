# LangGraph Orchestrator - Breaks problem into 5 steps
from backend.governance.governance_engine import evaluate_request

workflow = {
 "step1_data_extraction": "Data Agent extracts structured vendor data",
 "step2_policy_retrieval": "RAG retrieves procurement policies",
 "step3_risk_scoring": "ML model scores risk 0.05/0.65/0.99",
 "step4_human_gate": "REVIEW cases -> Human approval dashboard",
 "step5_execution": "Action Agent executes with audit trail"
}

def run_prism_workflow(vendor_input, task):
    result = evaluate_request(vendor_input, task)
    return {"workflow": workflow, "result": result, "human_in_loop": result.get("human_required")}
