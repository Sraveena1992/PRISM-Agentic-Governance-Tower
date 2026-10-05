# PRISM - Agentic Governance Tower - Pitch Deck

## Winning Line
> **"AI can plan the action. PRISM decides whether that action is allowed to execute."**

---

## 1. Title
**PRISM - Agents that work. Humans who lead.**

---

## 2. Problem
40 hrs/week vendor validation + fraud + compliance risk in procurement. AI agents can act fast but need governance.

---

## 3. Solution: Governance Tower

```text
BUSINESS REQUEST
      ↓
PROCUREMENT AGENT (AI PLANNING - GPT-4o-mini)
      ↓
GOVERNANCE AGENT
  ┌───────┼────────┐
  ↓       ↓        ↓
 RAG      ML   STATUTORY
  └───────┼────────┘
          ↓
     POLICY GATE
     /    |     \
 APPROVED REVIEW REJECTED
    ↓      ↓       ↓
  ACTION  HUMAN   BLOCK
    │      ↓
    │   APPROVE
    └──────┘
         ↓
   ACTION AGENT (PO/ERP only if APPROVED)
         ↓
 SHA-256 AUDIT -> VERIFICATION

       ---

## 4. Agentic Workflow
- **3 Decoupled Python Agents** (NOT LangGraph)
- **AI-assisted planning. Deterministic governance. Governed execution.**
- LLM does **NOT** control downstream tool execution

---

## 5. 5 Live Proofs (Fail-Closed + Tamper-Evident)

A. Clean Vendor (VEND-001) → AI PLAN → GOVERNANCE → APPROVED → PO_CREATED
B. Risky Vendor (VEND-002, 5L, ESG 45) → REVIEW → NO_ACTION → HUMAN → PO_CREATED
C. Fraud Vendor (VEND-003, gst_fraud_flag=1) → STATUTORY GATE → 0.99 → REJECTED → NO_ACTION
D. System Failure (/simulate-failure) → SAFE HOLD → 0.99 → REJECTED → NO_ACTION → SUBSYSTEM_FAILURE
E. Audit (/audit/verify) → SHA-256 INTACT → mutate backend/audit/audit_chain.json → TAMPERED → restore → INTACT

---

## 6. Demo (Live) - 5 Proofs
- **A - APPROVE:** Clean vendor $\rightarrow$ `APPROVED` $\rightarrow$ `PO_CREATED` $\rightarrow$ Audit Logged
- **B - REVIEW:** Medium risk $\rightarrow$ `REVIEW` $\rightarrow$ `NO PO` $\rightarrow$ Human Approval $\rightarrow$ `PO_CREATED`
- **C - REJECT:** GST fraud/sanctions $\rightarrow$ `Risk: 0.99` $\rightarrow$ `REJECTED` $\rightarrow$ `NO PO`
- **D - FAILURE:** `/simulate-failure` $\rightarrow$ `SAFE HOLD (0.99 REJECTED NO_ACTION)` (Fail-closed proof)
- **E - TAMPER:** `/audit/verify` $\rightarrow$ `INTACT` $\rightarrow$ Modify file $\rightarrow$ `TAMPERED` $\rightarrow$ Restore $\rightarrow$ `INTACT`

---

## 7. Business Value (Defensible)
- Measurable governance boundary for consequential AI actions
- Human-in-the-loop for uncertain cases
- Tamper-evident audit for compliance
- Architecture extensible to enterprise policy repos & ERP
- Prototype demonstrates fail-closed safety

---

## 8. Tech Stack
FastAPI, Python, OpenAI GPT-4o-mini, scikit-learn RandomForest, TF-IDF, SHA-256, Render, Streamlit
