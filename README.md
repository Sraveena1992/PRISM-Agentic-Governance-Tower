# PRISM — Agentic Governance Tower
**ET AI Hackathon 2026 | Accenture**

![Live](https://img.shields.io/badge/Live-200%20OK-brightgreen) ![Agents](https://img.shields.io/badge/Agents-3--Agent%20Decoupled-blue) ![Audit](https://img.shields.io/badge/Audit-SHA256%20Evident-black) ![RAG](https://img.shields.io/badge/RAG-TF--IDF%20%2B%20Cosine-orange) ![LLM](https://img.shields.io/badge/LLM-Gemini%201.5%20Flash-blue) ![Build](https://img.shields.io/badge/Build-3.0.0%20Prototype-success)

**PRISM addresses enterprise vendor compliance risk.** Single-agent automation carries fraud risks, while manual validation creates operational bottlenecks. PRISM decouples governance into a **3-Agent Architecture** (Procurement Data Agent, Governance & Risk Agent, Action Execution Agent) with ML Risk Scoring, TF-IDF Policy Vector RAG, Human-in-the-Loop Gate, Fail-Closed Recovery, and Tamper-Evident SHA-256 Audit Chaining.

> *Automated planning. Autonomous governance. Fail-closed action execution. Tamper-evident audit.*

---
## 🚀 Live Demo
- **API Live:** https://prism-agentic-governance-tower.onrender.com
- **Swagger Docs:** https://prism-agentic-governance-tower.onrender.com/docs
- **Health Check:** https://prism-agentic-governance-tower.onrender.com/health
- **Audit Verify:** https://prism-agentic-governance-tower.onrender.com/audit/verify
- **GitHub:** https://github.com/Sraveena1992/PRISM-Agentic-Governance-Tower

---
## 🤖 3-Agent Decoupled Architecture
**Not LangGraph. 3 decoupled Python agents orchestrated via `backend/orchestrator.py`.**

1.  **`ProcurementAgent` (Data & Tool Planning):** Validates payload, executes soft type-casting, plans tools, outputs auditable reasoning trace via `Gemini 1.5 Flash` + deterministic fallback: `As Procurement Agent, received {vendor_id} ESG:{esg_score}... Plan: 1) policy_retriever.retrieve 2) ml_risk_scorer.predict_risk 3) handoff to GovernanceAgent`.
2.  **`GovernanceAgent` (RAG + ML + Fail-Closed Gate):** Runs TF-IDF Policy Vector RAG via `policy_retriever.retrieve()`, Scikit-Learn ML `risk_scorer.predict_risk()` → float 0-1, statutory rules (`gst_fraud_flag`, `sanctions_match`), fail-closed SAFE HOLD.
3.  **`ActionAgent` (Gated Execution):** Generates `PO-<audit_id>` for `APPROVED`, enforces fail-closed hold for `REVIEW`/`REJECTED`, executes `/human-approval/{audit_id}`.

**Startup Health Log:** `PRISM STARTUP CHECK -> RAG: READY, ML: READY, LLM: CONFIGURED (Gemini gemini-1.5-flash), AUDIT: READY`

**Winning Thesis:** *AI can plan the action. PRISM decides whether that action is allowed to execute.*

---
## 📸 Live Production Proof - HAT-TRICK COMPLETE ✅

| 1️⃣ VEND-001 APPROVED (0.05) | 2️⃣ VEND-002 REVIEW (0.75) | 3️⃣ VEND-003 REJECTED (0.99) |
| :---: | :---: | :---: |
| ESG 85, 50K, clean → `APPROVED` | ESG 30, 5L, clean → `REVIEW` | ESG 45, 100K, GST fraud=1 → `REJECTED` |
| `risk_score: 0.05` <br> `decision: APPROVED` <br> `action: PO_CREATED` <br> `retriever: TF-IDF Vector + Cosine` | `risk_score: 0.75` <br> `decision: REVIEW` <br> `action: NO_ACTION` <br> `requires_human_approval: true` | `risk_score: 0.99` <br> `decision: REJECTED` <br> `action: NO_ACTION` <br> `gate_reason: STATUTORY GATE` |
| `reasoning_trace: Procurement Agent received... policy_retriever.retrieve... risk_scorer.predict_risk` | HITL Proof: Human approval → PO_CREATED | Fail-closed Proof: Statutory block |

**Verdict:** 3 different governance paths proven LIVE.

### 4️⃣ SHA-256 Audit Verification
**Endpoint:** `GET /audit/verify` → `{"verified": true, "records_checked": int, "algorithm": "SHA-256", "chain_status": "INTACT"}`

**Verification Contract:** Recalculates record SHA-256 + verifies `previous_hash` linkage. Tamper 1 char in `audit_trail.jsonl` → `TAMPERED` → Restore → `INTACT`.

---
## 🧠 ML Model - Honest Reporting
- **Algorithm:** `RandomForestClassifier` (100 trees) - prototype
- **Training:** `backend/ml_models/train_model.py` generates synthetic vendor data
- **Features:** `["esg_score", "financial_stability_score", "gst_fraud_flag", "sanctions_match", "invoice_anomaly"]`
- **Interface:** `risk_scorer.predict_risk(payload)` → 0-1
- **Fail-Closed:** model missing/inference failure → raises → Governance → `SAFE HOLD` 0.99 `REJECTED`

## 📚 RAG - Honest Reporting
- **Retriever:** TF-IDF Vector + Cosine Similarity (512MB Render-friendly)
- **Interface:** `policy_retriever.retrieve(query, top_k)` → list of `{id, text, similarity_score}`
- **Corpus:** 5 policies in `retriever.py`

---
## 🧪 Test Endpoints (LIVE - Judge Copy-Paste)

### 1. 🟢 GOOD Vendor - APPROVED

curl -X POST https://prism-agentic-governance-tower.onrender.com/process-vendor \
-H "Content-Type: application/json" \
-d '{"vendor_id":"VEND-001","amount":50000,"esg_score":85,"gst_fraud_flag":0,"sanctions_match":0}'

**2. 🟠 HIGH-RISK Vendor - REVIEW (Human-in-the-Loop)**

curl -X POST https://prism-agentic-governance-tower.onrender.com/process-vendor \
-H "Content-Type: application/json" \
-d '{"vendor_id":"VEND-002","amount":500000,"esg_score":30,"gst_fraud_flag":0,"sanctions_match":0}'

**3. 🔴 FRAUD Vendor - REJECTED (Statutory Gate)**

curl -X POST https://prism-agentic-governance-tower.onrender.com/process-vendor \
-H "Content-Type: application/json" \
-d '{"vendor_id":"VEND-003","amount":100000,"esg_score":45,"gst_fraud_flag":1,"sanctions_match":0}'

**Alternate Sanctions Test:**

curl -X POST https://prism-agentic-governance-tower.onrender.com/process-vendor \
-H "Content-Type: application/json" \
-d '{"vendor_id":"VEND-003-SANCTIONS","amount":100000,"esg_score":45,"gst_fraud_flag":0,"sanctions_match":1}'

**4. 🔐 Verify Audit Chain**

curl https://prism-agentic-governance-tower.onrender.com/audit/verify

curl https://prism-agentic-governance-tower.onrender.com/health

**💻 Local Run**
bash
pip install -r requirements.txt
python -m backend.ml_models.train_model

### Set GEMINI_API_KEY in .env
bash
uvicorn backend.api.main:app --reload --port 8000

### Docs: http://localhost:8000/docser.onrender.com/process-vendor \
-H "Content-Type: application/json" \
-d '{"vendor_id":"VEND-001","amount":50000,"esg_score":85,"gst_fraud_flag":0,"sanctions_match":0}'
