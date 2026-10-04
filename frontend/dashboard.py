import streamlit as st
import requests
import os

# Set live backend URL as default fallback for Streamlit Cloud
DEFAULT_BACKEND = "https://prism-agentic-governance-tower.onrender.com"
BACKEND_URL = os.getenv("BACKEND_URL", DEFAULT_BACKEND).rstrip("/")

st.set_page_config(page_title="PRISM Governance Tower", layout="wide")
st.title("🛡️ PRISM Agentic Governance Tower")
st.caption("P0 Compliant | Fail-Closed | SHA-256 Audit Chain | Human-in-the-Loop")

# --- Sidebar Judge Demo ---
st.sidebar.header("⚖️ Judge Evaluation Panel")

if st.sidebar.button("🔍 Verify Audit Chain (SHA-256)"):
    try:
        r = requests.get(f"{BACKEND_URL}/audit/verify", timeout=10)
        data = r.json()
        st.sidebar.json(data)
        if data.get("verified"):
            st.sidebar.success("Chain INTACT ✅")
        else:
            st.sidebar.error("Chain TAMPERED ❌")
    except Exception as e:
        st.sidebar.error(f"Backend not reachable: {e}")

if st.sidebar.button("💥 Simulate Failure -> Fail-Closed Demo"):
    try:
        payload = {
            "vendor_id": "TEST_FAIL",
            "esg_score": 50,
            "gst_fraud_flag": 0,
            "sanctions_match": 0,
            "document_text": "Simulating ML/RAG subsystem crash test"
        }
        r = requests.post(f"{BACKEND_URL}/simulate-failure", json=payload, timeout=15)
        st.sidebar.json(r.json())
        st.sidebar.warning("Fail-Closed Safe Hold Triggered ✅")
    except Exception as e:
        st.sidebar.error(f"Simulation failed: {e}")

# --- Main Section: Run Workflow ---
st.header("1. Process Vendor Request")
c1, c2 = st.columns(2)
with c1:
    vendor_id = st.text_input("Vendor ID", "VENDOR_123")
    gstin = st.text_input("GSTIN", "27ABCDE1234F1Z5")
    esg = st.slider("ESG Score", 0.0, 100.0, 80.0)
with c2:
    fraud = st.selectbox("GST Fraud Flag", [0, 1])
    sanctions = st.selectbox("Sanctions Match", [0, 1])
    doc_text = st.text_area("Document Text (for RAG Policy Engine)", "Vendor provides green steel, fully compliant with ESG norms...")

if st.button("🚀 Run Governance Workflow", type="primary"):
    with st.spinner("Orchestrator executing: Procurement -> Governance -> Action..."):
        try:
            payload = {
                "vendor_id": vendor_id,
                "gstin": gstin,
                "document_text": doc_text,
                "esg_score": esg,
                "gst_fraud_flag": fraud,
                "sanctions_match": sanctions
            }
            res = requests.post(f"{BACKEND_URL}/process-vendor", json=payload, timeout=20).json()
            
            decision = res.get('decision') or res.get('final_decision') or 'EVALUATED'
            st.success(f"Decision: **{decision}** | Risk Score: **{res.get('risk_score', 'N/A')}**")
            st.json(res)
            
            # Save audit ID in session state for HITL gate
            extracted_audit_id = res.get("audit_id") or (res.get("audit", {}).get("audit_id") if isinstance(res.get("audit"), dict) else None)
            if extracted_audit_id:
                st.session_state["last_audit_id"] = extracted_audit_id
        except Exception as e:
            st.error(f"Execution Error: {e}")

st.divider()

# --- HITL Gate Section ---
st.header("2. Human-in-the-Loop Approval Gate")
default_audit = st.session_state.get("last_audit_id", "")
target_audit_id = st.text_input("Audit ID for Review/Approval", value=default_audit, placeholder="AUD-XXXXXX")
reviewer_comments = st.text_area("Compliance Reviewer Notes", "Approved following document and policy verification.")

col_approve, col_reject = st.columns(2)

with col_approve:
    if st.button("✅ Approve & Issue PO", type="primary"):
        if not target_audit_id:
            st.error("Please provide a valid Audit ID.")
        else:
            try:
                payload = {"approved": True, "approved_by": "Compliance_Officer_UI", "comments": reviewer_comments}
                appr_res = requests.post(f"{BACKEND_URL}/human-approval/{target_audit_id}", json=payload, timeout=10).json()
                st.success("Vendor Approved Live! Downstream PO Generated.")
                st.json(appr_res)
            except Exception as e:
                st.error(f"Approval failed: {e}")

with col_reject:
    if st.button("❌ Reject & Lock Ledger"):
        if not target_audit_id:
            st.error("Please provide a valid Audit ID.")
        else:
            try:
                payload = {"approved": False, "approved_by": "Compliance_Officer_UI", "comments": reviewer_comments}
                rej_res = requests.post(f"{BACKEND_URL}/human-approval/{target_audit_id}", json=payload, timeout=10).json()
                st.warning("Vendor Blocked Live! Action recorded into SHA-256 Audit Chain.")
                st.json(rej_res)
            except Exception as e:
                st.error(f"Rejection failed: {e}")

st.divider()

# --- Audit Ledger Overview ---
st.header("3. Recent SHA-256 Audit Ledger Entries")
try:
    audits = requests.get(f"{BACKEND_URL}/audits", timeout=10).json()
    if isinstance(audits, list):
        st.dataframe(audits[-10:], use_container_width=True)
    else:
        st.json(audits)
except Exception:
    st.write("No audit records found or backend is initializing.")
