# PRISM — Agentic Enterprise Governance Tower
**ET AI Hackathon 2026 | Accenture**

![Live](https://img.shields.io/badge/Live-200%20OK-brightgreen) ![Agents](https://img.shields.io/badge/Agents-3--Agent%20Decoupled-blue) ![Audit](https://img.shields.io/badge/Audit-SHA256%20Chained-black) ![RAG](https://img.shields.io/badge/RAG-TF--IDF%20%2B%20Cosine-orange) ![Build](https://img.shields.io/badge/Build-3.0.0%20Enterprise-success)

**PRISM addresses enterprise vendor compliance risk.** Single-agent automation carries fraud risks, while manual validation creates operational bottlenecks. PRISM decouples governance into a **3-Agent Architecture** (Procurement Data Agent, Governance & Risk Agent, Action Execution Agent) with ML Risk Scoring, TF-IDF Policy Vector RAG, Human-in-the-Loop Gate, Fail-Closed Recovery, and Tamper-Evident SHA-256 Audit Chaining.

> *Automated planning. Autonomous governance. Fail-closed action execution. Tamper-evident audit.*

---

## 🚀 Live Demo
- **API Live:** https://prism-agentic-governance-tower.onrender.com
- **Swagger Docs:** https://prism-agentic-governance-tower.onrender.com/docs
- **Health Check:** https://prism-agentic-governance-tower.onrender.com/health
- **Live Verify Proof:** https://prism-agentic-governance-tower.onrender.com/audit/verify
- **GitHub:** https://github.com/Sraveena1992/PRISM-Agentic-Governance-Tower

---

## 🤖 3-Agent Decoupled Architecture

1. **`ProcurementAgent` (Data & Tool Planning):** Validates incoming payload completeness, executes soft type-casting, plans tool selection, and outputs an auditable LLM reasoning trace (`gpt-4o-mini` with deterministic fallbacks).
2. **`GovernanceAgent` (RAG + ML + Fail-Closed Gate):** Runs TF-IDF Policy Vector RAG, Scikit-Learn ML risk scoring, statutory compliance rules (`gst_fraud_flag`, `sanctions_match`), and handles subsystem degradation with safe defaults.
3. **`ActionAgent` (Gated Downstream Execution):** Carries real action ownership. Generates downstream Purchase Orders (`PO-<audit_id>`) for `APPROVED` states, enforces a fail-closed hold for `REVIEW` / `REJECTED`, and executes post-human-approval actions via `/human-approval/{audit_id}`.

---

## 📸 Live Production Proof - 3 Stages Verified (JUDGE READY)

| 1️⃣ APPROVED (Risk 0.2) | 2️⃣ REJECTED (Fail-Closed 0.99) | 3️⃣ Render Live Deploy |
| :---: | :---: | :---: |
| <img width="100%" alt="APPROVED" src="https://github.com/user-attachments/assets/52d13b0e-5e2b-4e31-8222-5e69fe78454f" /> | <img width="100%" alt="REJECTED" src="https://github.com/user-attachments/assets/159590bc-d80b-4f26-9745-e1806bbc85e5" /> | <img width="100%" alt="Render Live" src="https://github.com/user-attachments/assets/be617dc6-5a4d-4dbc-a777-46e8bd3d4c7c" /> |
| `risk_score: 0.2` → `APPROVED`<br>`agents: 3` (`Procurement` → `Governance` → `Action`) | `gst_fraud_flag=1` → `risk: 0.99` → `REJECTED`<br>`gate_reason: Statutory auto-REJECT` | `Service: PRISM-Agentic-Governance-Tower`<br>`Status: Live` + `Deploy succeeded` |

---

### 4️⃣ SHA-256 Audit Verification - Tamper-Proof Ledger
<img width="1600" height="865" alt="SHA-256_Audit_Verification" src="https://github.com/user-attachments/assets/9e9c1c88-283a-4e73-8293-e2fddd3751ec" />

**Live Proof Endpoint:** `GET /audits` or `GET /audit/{audit_id}`
- **Hash Chain Linkage:** `previous_hash` → `current_hash`
- **Deterministic Record:** Complete trace of agent plan, governance decision, and downstream action output.

---

## 🧪 Test Endpoints (cURL)

### 1. GOOD Vendor - APPROVED (200 OK)
```bash
curl -X POST https://prism-agentic-governance-tower.onrender.com/process-vendor \
-H "Content-Type: application/json" \
-d '{"vendor_id": "VEND-GOOD-01","gstin": "07AABCU1234A1Z5","document_text": "MSME certified clean vendor","esg_score": 92,"gst_fraud_flag": 0,"sanctions_match": 0}'
```

### 2. **FRAUD Vendor - Fail-Closed REJECTED (200 OK - AUD-AS01BF)**
```bash
curl -X POST https://prism-agentic-governance-tower.onrender.com/process-vendor \
-H "Content-Type: application/json" \
-d '{"vendor_id": "VEND-FRAUD-01","gstin": "07AABCU1234A1Z5","document_text": "sanctions hit GST fraud","esg_score": 20,"gst_fraud_flag": 1,"sanctions_match": 1}'
```

### 3. **Simulate Subsystem Failure (Fail-Closed Proof)**
```bash
curl -X POST https://prism-agentic-governance-tower.onrender.com/simulate-failure \
-H "Content-Type: application/json" \
-d '{"vendor_id": "VEND-FAILSAFE-002","esg_score": 80}'
```

### 4. **Verify SHA-256 Audit Ledger & Health**
```bash
curl https://prism-agentic-governance-tower.onrender.com/audits
curl https://prism-agentic-governance-tower.onrender.com/audit/AUD-AS01BF
curl https://prism-agentic-governance-tower.onrender.com/health
```

## 💻 **Local Run**
```bash
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
# Docs: http://localhost:8000/docs
```
