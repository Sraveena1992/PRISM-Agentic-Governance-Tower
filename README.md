# PRISM — Agentic Governance Tower
**ET AI Hackathon 2026 | Accenture**

![Live](https://img.shields.io/badge/Live-200%20OK-brightgreen) ![Agents](https://img.shields.io/badge/Agents-3--Agent%20Decoupled-blue) ![Audit](https://img.shields.io/badge/Audit-SHA256%20Evident-black) ![RAG](https://img.shields.io/badge/RAG-TF--IDF%20%2B%20Cosine-orange) ![LLM](https://img.shields.io/badge/LLM-Gemini%201.5%20Flash%20FREE-success) ![Build](https://img.shields.io/badge/Build-3.0.0%20Prototype-success)

**PRISM addresses enterprise vendor compliance risk.** Single-agent automation carries fraud risks, while manual validation creates operational bottlenecks. PRISM decouples governance into a **3-Agent Architecture** (Procurement Data Agent, Governance & Risk Agent, Action Execution Agent) with ML Risk Scoring, TF-IDF Policy Vector RAG, Human-in-the-Loop Gate, Fail-Closed Recovery, and Tamper-Evident SHA-256 Audit Chaining.

> *Automated planning. Autonomous governance. Fail-closed action execution. Tamper-evident audit. Zero billing — 100% FACTS.*

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

1.  **`ProcurementAgent` (Data & Tool Planning):** Validates payload, executes soft type-casting, plans tools, outputs auditable reasoning trace via `Gemini 1.5 Flash FREE` + deterministic fallback: `As Procurement Agent, received {vendor_id} ESG:{esg_score}... Plan: 1) policy_retriever.retrieve 2) ml_risk_scorer.predict_risk 3) handoff to GovernanceAgent`.
2.  **`GovernanceAgent` (RAG + ML + Fail-Closed Gate):** Runs TF-IDF Policy Vector RAG via `policy_retriever.retrieve()`, Scikit-Learn ML `risk_scorer.predict_risk()` → float 0-1, statutory rules (`gst_fraud_flag`, `sanctions_flag`), fail-closed SAFE HOLD.
3.  **`ActionAgent` (Gated Execution):** Generates `PO-<audit_id>` for `APPROVED`, enforces fail-closed hold for `REVIEW`/`REJECTED`, executes `/human-approval/{audit_id}`.

**Startup Health Log:** `PRISM STARTUP CHECK -> RAG: READY, ML: READY, LLM: CONFIGURED (Gemini FREE), AUDIT: READY`

---
## 📸 Live Production Proof - HAT-TRICK COMPLETE ✅

| 1️⃣ VEND-001 APPROVED (0.05) | 2️⃣ VEND-002 REJECTED (0.99) | 3️⃣ VEND-003 REVIEW (1.0) |
| :---: | :---: | :---: |
| ESG 85, clean → `APPROVED` | ESG 45, GST fraud=1 → `REJECTED` | ESG 30, Sanctions=1, Amount 2L → `REVIEW` |
| `risk_score: 0.05` <br> `decision: APPROVED` <br> `retriever: TF-IDF Vector + Cosine` | `risk_score: 0.99` <br> `decision: REJECTED` <br> `gate_reason: STATUTORY GATE: Fraud/Sanctions` | `risk_score: 1.0` <br> `decision: REVIEW` <br> `requires_human_approval: true` |
| `reasoning_trace: Procurement Agent received... policy_retriever.retrieve... risk_scorer.predict_risk` | Same clean trace — NO credits error | Same clean trace — fail-closed human gate |

**Verdict:** 3 different governance paths proven LIVE — no mock, no billing.

### 4️⃣ SHA-256 Audit Verification
**Endpoint:** `GET /audit/verify` → `{"verified": true, "chain_status": "INTACT", "algorithm": "SHA-256"}`

---
## 🧠 ML Model - Honest Reporting
- **Algorithm:** `RandomForestClassifier` (100 trees) - prototype
- **Features:** `["esg_score", "financial_stability_score", "gst_fraud_flag", "sanctions_match", "invoice_anomaly"]`
- **Interface:** `risk_scorer.predict_risk(payload)` → 0-1
- **Fail-Closed:** statutory flags → 0.99 safe high risk

## 📚 RAG - Honest Reporting
- **Retriever:** TF-IDF Vector + Cosine Similarity (Render 512MB friendly)
- **Interface:** `policy_retriever.retrieve(query, top_k)`
- **Corpus:** 5 policies in `retriever.py`

---
## 🧪 Test Endpoints (LIVE - Judge Copy-Paste)

**1. GOOD Vendor - APPROVED**

curl -X POST https://prism-agentic-governance-tower.onrender.com/process-vendor \
-H "Content-Type: application/json" \
-d '{"vendor_id":"VEND-001","amount":50000,"esg_score":85,"gst_fraud_flag":0,"sanctions_flag":0}'

**2. 🚨 FRAUD Vendor - REJECTED**

curl -X POST https://prism-agentic-governance-tower.onrender.com/process-vendor \
-H "Content-Type: application/json" \
-d '{"vendor_id":"VEND-002","amount":100000,"esg_score":45,"gst_fraud_flag":1,"sanctions_flag":0}'

**3. ⚠️ SANCTIONS Vendor - REVIEW (Human Gate)**

curl -X POST https://prism-agentic-governance-tower.onrender.com/process-vendor \
-H "Content-Type: application/json" \
-d '{"vendor_id":"VEND-003","amount":200000,"esg_score":30,"gst_fraud_flag":0,"sanctions_flag":1}'

**4. 🔐 Verify Audit Chain**

curl https://prism-agentic-governance-tower.onrender.com/audit/verify

curl https://prism-agentic-governance-tower.onrender.com/health

**💻 Local Run**

pip install -r requirements.txt

# 🔑 Set GEMINI_API_KEY in .env (FREE - no billing)
uvicorn backend.api.main:app --reload --port 8000

# 📚 Docs: http://localhost:8000/docs
