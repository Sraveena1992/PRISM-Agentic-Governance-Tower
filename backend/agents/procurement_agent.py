import os

# Free LLM - No billing needed - WINNER FACTS
try:
    import google.generativeai as genai
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_KEY:
        genai.configure(api_key=GEMINI_KEY)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        gemini_model = None
except:
    gemini_model = None

def get_procurement_reasoning(vendor_id, esg_score, gst_fraud_flag, sanctions_flag, financial=75):
    base_reason = f"As Procurement Agent, I received vendor {vendor_id} with ESG:{esg_score}, financial_stability:{financial}, GST_fraud:{gst_fraud_flag}, Sanctions:{sanctions_flag}. Data completeness: sufficient. Plan: 1) Call policy_retriever for ESG threshold & fraud policy, 2) Call ml_risk_scorer for risk signal, 3) Handoff enriched payload to GovernanceAgent. Tools: policy_retriever.retrieve, risk_scorer.predict_risk"
    if gemini_model:
        try:
            prompt = f"You are PRISM Procurement Agent. Vendor {vendor_id} ESG:{esg_score} Fraud:{gst_fraud_flag} Sanctions:{sanctions_flag}. Write 2-line factual plan using tools: policy_retriever.retrieve, risk_scorer.predict_risk, governance_decision."
            resp = gemini_model.generate_content(prompt)
            return resp.text
        except:
            return base_reason
    return base_reason

# FIX for orchestrator - enrich method added
class ProcurementAgent:
    def enrich(self, vendor_id, esg_score, gst_fraud_flag, sanctions_flag, financial=75):
        reasoning = get_procurement_reasoning(vendor_id, esg_score, gst_fraud_flag, sanctions_flag, financial)
        return {
            "vendor_id": vendor_id,
            "esg_score": esg_score,
            "gst_fraud_flag": gst_fraud_flag,
            "sanctions_flag": sanctions_flag,
            "reasoning_trace": reasoning,
            "financial_stability": financial
        }
    
    def run(self, vendor_id, esg_score, gst_fraud_flag, sanctions_flag, financial=75):
        return self.enrich(vendor_id, esg_score, gst_fraud_flag, sanctions_flag, financial)
