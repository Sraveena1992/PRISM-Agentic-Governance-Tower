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
