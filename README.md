# PRISM — Agentic Enterprise Governance Tower
**ET AI Hackathon 2026 | Accenture**

![Live](https://img.shields.io/badge/Live-200%20OK-brightgreen) ![Pipeline](https://img.shields.io/badge/Pipeline-5--Stage-blue) ![Audit](https://img.shields.io/badge/Audit-SHA256%20Chained-black) ![RAG](https://img.shields.io/badge/RAG-TF--IDF%20%2B%20Cosine-orange) ![Build](https://img.shields.io/badge/Build-3.0.0%20Enterprise-success)

**PRISM addresses enterprise vendor compliance risk.** Single-agent automation carries fraud risks, while manual validation creates operational bottlenecks. PRISM uses a 5-Stage Deterministic Orchestration Pipeline + Scikit-Learn ML Scorer + TF-IDF Policy Vector RAG + Human-in-the-Loop Gate + Tamper-Evident SHA-256 Audit Chain.
> *Automated execution. Human oversight. Tamper-evident, hash-chained audit.*

---

## 🚀 Live Demo
- **API Live:** https://prism-agentic-governance-tower.onrender.com
- **Swagger Docs:** https://prism-agentic-governance-tower.onrender.com/docs
- **Health Check:** https://prism-agentic-governance-tower.onrender.com/health

---

## 📸 Live Production Proof - 3 Stages Verified (JUDGE READY)

| 1️⃣ APPROVED (Risk 0.2) | 2️⃣ REJECTED (Fail-Closed 0.99) | 3️⃣ Render Live Deploy |
| :---: | :---: | :---: |
| <img width="100%" alt="APPROVED" src="https://github.com/user-attachments/assets/52d13b0e-5e2b-4e31-8222-5e69fe78454f" /> | <img width="100%" alt="REJECTED" src="https://github.com/user-attachments/assets/159590bc-d80b-4f26-9745-e1806bbc85e5" /> | <img width="100%" alt="Render Live" src="https://github.com/user-attachments/assets/be617dc6-5a4d-4dbc-a777-46e8bd3d4c7c" /> |
| `risk_score: 0.2` → `APPROVED`<br>`pipeline_stages: 5`<br>`TF-IDF + Cosine: 0.4221` | `gst_fraud_flag=1` → `risk: 0.99` → `REJECTED`<br>`gate_reason: GST fraud / Sanctions`<br>`requires_human_approval: false` | `Service: PRISM-Agentic-Governance-Tower`<br>`Status: Live` + `Deploy succeeded 1m14s`<br>`Commit: PolicyRetriever class` |

**Verified Highlights:**
- `pipeline_stages_completed: 5` | `retriever: TF-IDF Vector + Cosine Matrix` | `audit_id: SHA-256 Chained`
- **Fail-Closed Proven:** Fraud=1 → Auto REJECTED, No Human Bypass
- **Pipeline:** Ingestion → Policy RAG → ML Risk → Fail-Closed Gate → SHA-256 Audit

---

#### Test it yourself (cURL):
```bash
curl -X POST https://prism-agentic-governance-tower.onrender.com/evaluate \
-H "Content-Type: application/json" \
-d '{
  "vendor_id": "VEND-APPROVED-001",
  "esg_score": 85,
  "financial_stability_score": 0.92,
  "gst_fraud_flag": 0,
  "sanctions_match": 0,
  "invoice_anomaly": 0.05,
  "document_text": "Clean vendor with strong ESG compliance"
}'

# Clone and install dependencies
pip install -r requirements.txt

# Run ML model training & benchmark evaluation
python backend/ml_models/train.py
python backend/ml_models/eval.py

# Launch FastAPI server locally
uvicorn backend.api.main:app --reload
