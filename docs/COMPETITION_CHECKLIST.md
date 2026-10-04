# PRISM - ET AI Hackathon Competition Checklist

## Architecture - FINAL TRUTH
- **3 Decoupled Python Agents** (NOT LangGraph):
    1. ProcurementAgent - AI-assisted planning & enrichment (GPT-4o-mini)
    2. GovernanceAgent - Deterministic governance + Policy Gate + Risk Scoring
    3. ActionAgent - Governed execution (PO/ERP only if APPROVED)

- **Core Principle:** AI can plan the action. PRISM decides whether that action is allowed to execute.

## File Paths - VERIFIED
- Orchestrator: `backend/orchestrator.py`
- Governance: `backend/agents/governance_agent.py`
- Procurement: `backend/agents/procurement_agent.py`
- Action: `backend/agents/action_agent.py`
- ML Model Training: `backend/ml_models/train.py` (NOT train_model.py)
- RAG Retriever: `backend/rag/retriever.py` or `backend/governance/retriever.py`
- Audit Chain: `backend/governance/audit.py`

## API Contracts - VERIFIED
- `GET /` - PRISM Running + agents listed
- `GET /health` - RAG READY, ML READY, ml_model: random_forest_risk_model.joblib, LLM configured
- `POST /process-vendor` - Main workflow
- `POST /human-approval/{audit_id}` - Human approval (NOT /approve)
- `GET /audit/trail` - Full audit trail
- `GET /audits` - Alias for /audit/trail (dashboard compatibility)
- `GET /audit/verify` - Returns: verified, records_checked, algorithm: SHA-256, chain_status: INTACT, message + backward compat is_valid, count
- `POST /simulate-failure` - Fail-closed proof: 200, 0.99, REJECTED, NO_ACTION, fail_closed_proof:true, SUBSYSTEM_FAILURE

## P0 Checks - ALL GREEN
- [x] P0 #1 Fail-closed recovery signature: recover_with_safe_defaults(enriched_data=None, error_message=None) -> 0.99 REJECTED NO_ACTION
- [x] P0 #2 Human approval: 5 args (audit_id, vendor_id, approved_by, approved, comments) + vendor from audit trail
- [x] P0 #3 Audit verify: verified true + SHA-256 + INTACT + records_checked
- [x] P0 #4 Dashboard /audits alias
- [x] P0 #5 Render build: pip install -r requirements.txt && python -m backend.ml_models.train
- [x] P0 #6 Health check inspects RAG, ML model, Audit, LLM

## Technical Claims - DEFENSIBLE LANGUAGE
- RAG: "TF-IDF policy vector retrieval (lightweight RAG prototype) - 5 policy corpus, cosine similarity, extensible to enterprise repos"
- ML: "ML-assisted procurement risk scoring trained on synthetic prototype data - RandomForest 100 trees, 5 features, 1500 samples"
- Audit: "Tamper-evident SHA-256 audit chain - canonical JSON + previous_hash -> current_hash, NOT blockchain, NOT tamper-proof"
- Governance: "AI-assisted planning. Deterministic governance. Governed execution. LLM does NOT control downstream tool execution."

## 5 LIVE PROOFS FOR JUDGE
A - APPROVE: vendor -> APPROVED -> PO_CREATED -> audit
B - REVIEW: medium risk -> REVIEW -> NO PO -> human approval -> PO_CREATED
C - REJECT: gst_fraud/sanctions -> 0.99 -> REJECTED -> NO PO
D - FAILURE: /simulate-failure -> SAFE HOLD 0.99 REJECTED NO_ACTION audit
E - TAMPER: /audit/verify INTACT -> modify 1 char -> TAMPERED -> restore -> INTACT
