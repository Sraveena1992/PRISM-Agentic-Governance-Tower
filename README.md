# PRISM — Agentic Enterprise Governance Tower
ET AI Hackathon 2026 | Accenture

![Live](https://img.shields.io/badge/Live-200%20OK-brightgreen) ![Agents](https://img.shields.io/badge/Pipeline-5--Stage-blue) ![Audit](https://img.shields.io/badge/Audit-SHA256%20Chained-black) ![RAG](https://img.shields.io/badge/RAG-TF--IDF%20%2B%20Cosine-orange) ![Build](https://img.shields.io/badge/Build-3.0.0%20Enterprise-success)

**PRISM - Agentic Governance Tower addresses enterprise vendor compliance and risk controls.**
Single-agent automation carries fraud risks, while manual validations create operational bottlenecks. PRISM uses a 5-Stage Deterministic Orchestration Pipeline + Scikit-Learn ML Scorer + TF-IDF Policy Vector RAG + Human-in-the-Loop Gate + Tamper-Evident SHA-256 Chained Audit Trail.
— *Automated execution. Human oversight. Tamper-evident, hash-chained audit.*

---

## 🚀 Live Demo 🌐
- **API Live:** https://prism-agentic-governance-tower.onrender.com
- **Swagger Docs:** https://prism-agentic-governance-tower.onrender.com/docs
- **Health Check:** https://prism-agentic-governance-tower.onrender.com/health

---

## 🎯 Executive Summary
- **Problem:** Enterprise procurement teams spend significant resources on manual vendor risk validations, while unconstrained automation can miss statutory fraud signals.
- **Solution:** PRISM — A 5-Stage Governance Tower that ingests compliance documents, retrieves policy clauses via TF-IDF Vector Space Search, scores risk using a trained ML model, enforces human override gates, and records hash-linked audit records.
- **Impact:** Automated risk screening with measured ML precision (see eval.py), with every human approval linked to hash-chained audit record..

---

## 🏆 PRISM - 3.0.0 Enterprise Hackathon Prototype - LIVE PROOF

### 1. Live Status & Pipeline Telemetry
![Live Status]
`https://prism-agentic-governance-tower.onrender.com/health`
<img width="1600" height="856" alt="prism_health_rich_details" src="https://github.com/user-attachments/assets/d986b33c-f21d-4dff-851b-218b9c70bfd5" />

### 2. Swagger Interactive Documentation
![Swagger Endpoints]
`https://prism-agentic-governance-tower.onrender.com/docs`
<img width="1600" height="859" alt="prism_docs_10_apis" src="https://github.com/user-attachments/assets/890b26f9-7bf9-4348-9e23-bc132e47dba0" />

**Key Active Endpoints:**
- `POST /ingest-document` -> Document Metadata Ingestion
- `POST /evaluate` -> Complete 5-Stage Authoritative Risk & Policy Pipeline
- `POST /policy/search` -> TF-IDF Vector Space & Cosine Similarity Clause Search
- `POST /simulate` -> Dynamic Risk Threshold Shift Impact Simulation
- `POST /approve/{audit_id}` -> Fail-Closed Human-in-the-Loop Approval Gate
- `GET /audit/verify` -> Full SHA-256 Hash Chain Integrity Recalculation
- `GET /health` -> Real-time System Metrics & Telemetry

---

## 📸 Live API Demonstration & Governance Workflows

PRISM automatically routes vendor evaluation based on risk profiles, ML scoring, and policy mapping. Below are live Swagger UI test results from our deployed Render instance:

### Scenario 1: Low-Risk Vendor Auto-Approval (`200 OK`)
High ESG score (`85`) and clean GST status (`gst_fraud_flag: 0`) trigger low risk score (`0.05`) and instant `APPROVED` decision.

<img width="1600" height="867" alt="evaluate_approved" src="https://github.com/user-attachments/assets/fe6931b2-c7cb-471a-bfa3-ad3a3397eeaa" />

---

### Scenario 2: High-Risk Fraud Vendor Rejection (`200 OK`)
Fraud flag detected (`gst_fraud_flag: 1`) triggers fail-closed governance rules, raising risk score to `0.99` with `REJECTED` decision and policy citations.

<img width="1600" height="856" alt="doc_sassets_evaluate_demo" src="https://github.com/user-attachments/assets/edd58f65-1189-4e2a-ac49-12db98ffb607" />

---

## 🔥 LIVE EVALUATION PIPELINE FLOW

**Live API Endpoint:** `POST /evaluate`

**Pipeline Execution Workflow:**
1. **Stage 1 (Data Ingestion):** Ingests vendor payload and extracts structured compliance metadata.
2. **Stage 2 (Policy RAG):** Retrieves relevant compliance clauses using TF-IDF Vectorizer + Cosine Similarity (<5ms latency).
3. **Stage 3 (Risk Scorer):** Generates ML risk scores via Scikit-Learn RandomForest classifier.
4. **Stage 4 (Human Gate):** Enforces fail-closed rules (High Risk triggers mandatory human review gate).
5. **Stage 5 (Audit Ledger):** Appends execution record hash to persistent `audit_trail.jsonl` using SHA-256 chaining.

---

## 🏗️️ Architecture Breakdown

- **ML Risk Engine:** `backend/ml_models/` -> Scikit-Learn RandomForest model trained on synthetic vendor risk profiles (`eval.py` generates model performance metrics).
- **Orchestrator:** `backend/agents/orchestrator.py` -> Authoritative state machine routing execution through all governance stages.
- **Vector RAG Engine:** `backend/rag/retriever.py` -> Vector Space Retrieval using TF-IDF + Cosine Similarity.
- **Audit & Cryptography:** `backend/governance/audit.py` -> Tamper-evident, SHA-256 hash-linked append-only ledger.
- **API Layer:** `backend/api/main.py` -> FastAPI high-performance RESTful API with OpenAPI documentation.

---

## 🛠 Local Setup & Execution

```bash
# Clone and install dependencies
pip install -r requirements.txt

# Run ML model training & benchmark evaluation
python backend/ml_models/train.py
python backend/ml_models/eval.py

# Launch FastAPI server locally
uvicorn backend.api.main:app --reload
