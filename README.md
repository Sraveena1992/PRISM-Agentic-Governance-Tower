# PRISM — Agentic Enterprise Governance Tower
ET AI Hackathon 2026 | Accenture

**PRISM - Agentic Governance Tower solves Accenture's real vendor risk problem.**
Single agent = fraud risk. Manual checks = 40 hrs/week waste. PRISM uses Orchestrator + 3 GenAI Agents + ML Risk Scorer (0.05/0.65/0.99) + RAG Policies + Human Approval + Fail-Closed Audit.
— Agents that work. Humans who lead. Audit that never lies.


## 🚀 Live Demo 🌐
- **API Live:** https://prism-agentic-governance-tower.onrender.com
- **Swagger Docs:** https://prism-agentic-governance-tower.onrender.com/docs
- **Health Check:** https://prism-agentic-governance-tower.onrender.com/health

- **Problem:** Enterprises lose millions due to manual vendor risk checks.

- **Solution:** PRISM - Agentic Tower that auto-evaluates, scores, and governs vendors with AI agents.

- **Impact:** 90% faster audits, 100% traceable decisions.

<img width="1600" height="856" alt="PRISM_LIVE_PROOF" src="https://github.com/user-attachments/assets/352f4321-f36a-4a23-91f4-6dc0672a3dda" />

## 🔥 LIVE DEMO PROOF - 200 OK

**Live API:** https://prism-agentic-governance-tower.onrender.com/docs

**Endpoint:** POST /evaluate?task=vendor_evaluation

**LIVE Result (01-10-2026):**
- Workflow: 5 Agents (Data -> RAG -> ML Risk 0.65 -> Human Gate -> Action)
- Decision: REVIEW
- Policies: "Vendor with ESG < 40 must go for REVIEW", "GST fraud flag = BLOCK"
- Audit ID: e5a14c69... (Fail-closed audit)
- Human-in-Loop: true

> Agents that work. Humans who lead. Audit that never lies.



## Why This Wins?
Enterprise procurement: 40 hrs/week vendor validation. Single autonomous agent = fraud risk.
PRISM = Orchestrator + 3 GenAI Agents + ML Risk Scorer (0.05/0.65/0.99) + RAG Policies + Human Approval + Fail-Closed Audit.

## Where is What?
- ML: backend/ml_models/train.py -> 2000 synthetic vendors, RandomForest
- GenAI: backend/agents/ -> Data/Risk/Action Agents (LangGraph)
- RAG: backend/rag/retriever.py -> Policy retrieval before every decision
- Train Data: backend/data/synthetic_vendors/vendors.csv
- Break into Steps: backend/agents/orchestrator.py -> 5-step workflow

## Run
pip install -r requirements.txt
python backend/ml_models/train.py
uvicorn backend.api.main:app --reload
