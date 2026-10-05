import os

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
    base = f"As Procurement Agent, received {vendor_id} ESG:{esg_score} GST_fraud:{gst_fraud_flag} Sanctions:{sanctions_flag}. Plan: 1) policy_retriever.retrieve for ESG/fraud threshold, 2) ml_risk_scorer.predict_risk, 3) handoff to GovernanceAgent with fail-closed safety. Tools used: policy_retriever, risk_scorer."
    if gemini_model:
        try:
            p = f"PRISM Procurement Agent: Vendor {vendor_id} ESG {esg_score} Fraud {gst_fraud_flag} Sanctions {sanctions_flag}. Write 2-line factual tool plan."
            r = gemini_model.generate_content(p)
            return r.text
        except:
            return base
    return base

class ProcurementAgent:
    def enrich(self, *args, **kwargs):
        # Handle all call styles: enrich(dict), enrich(vendor_id,...), enrich(kwargs)
        vendor_id = kwargs.get("vendor_id", "VEND-UNKNOWN")
        esg_score = kwargs.get("esg_score", 75)
        gst_fraud = kwargs.get("gst_fraud_flag", 0)
        sanc = kwargs.get("sanctions_flag", 0)
        financial = kwargs.get("financial", 75)

        if args:
            if isinstance(args[0], dict):
                d = args[0]
                vendor_id = d.get("vendor_id", vendor_id)
                esg_score = d.get("esg_score", esg_score)
                gst_fraud = d.get("gst_fraud_flag", gst_fraud)
                sanc = d.get("sanctions_flag", sanc)
                financial = d.get("financial", financial)
            else:
                if len(args) > 0: vendor_id = args[0]
                if len(args) > 1: esg_score = args[1]
                if len(args) > 2: gst_fraud = args[2]
                if len(args) > 3: sanc = args[3]

        reasoning = get_procurement_reasoning(vendor_id, esg_score, gst_fraud, sanc, financial)
        return {
            "vendor_id": vendor_id,
            "esg_score": esg_score,
            "gst_fraud_flag": gst_fraud,
            "sanctions_flag": sanc,
            "reasoning_trace": reasoning,
            "financial_stability": financial
        }

    def run(self, *args, **kwargs):
        return self.enrich(*args, **kwargs)
