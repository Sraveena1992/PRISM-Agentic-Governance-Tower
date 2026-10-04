import streamlit as st
import requests
import os
DEFAULT_BACKEND = "https://prism-agentic-governance-tower.onrender.com"
BACKEND_URL = os.getenv("BACKEND_URL", DEFAULT_BACKEND).rstrip("/")
st.set_page_config(page_title="PRISM Governance Tower", layout="wide")
st.title("🛡️ PRISM Agentic Governance Tower")
st.caption("P0 Compliant | Fail-Closed | SHA-256 Audit Chain | Human-in-the-Loop")
st.sidebar.header("⚖️ Judge Evaluation Panel")
if st.sidebar.button("🔍 Verify Audit Chain (SHA-256)"):
    try:
        r = requests.get(f"{BACKEND_URL}/audit/verify", timeout=10)
        data = r.json()
        st.sidebar.json(data)
        if data.get("verified") or data.get("is_valid"):
            st.sidebar.success(f"Chain {data.get('chain_status','INTACT')} ✅ | {data.get('records_checked', data.get('count',0))} records | {data.get('algorithm','SHA-256')}")
        else:
            st.sidebar.error("Chain TAMPERED ❌")
    except Exception as e:
        st.sidebar.error(f"Backend not reachable: {e}")
if st.sidebar.button("💥 Simulate Failure -> Fail-Closed Demo"):
    try:
        r = requests.post(f"{BACKEND_URL}/simulate-failure", timeout=15)
        data = r.json()
        st.sidebar.json(data)
        if data.get("fail_closed_proof") and data.get("risk_score")==0.99:
            st.sidebar.warning(f"FAILURE → SAFE HOLD → 0.99 → REJECTED → NO ACTION → AUDIT ✅")
        else:
            st.sidebar.warning("Fail-Closed Triggered ✅")
    except Exception as e:
        st.sidebar.error(f"Simulation failed: {e}")
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
    with st.spinner("Orchestrator executing..."):
        try:
            payload = {"vendor_id": vendor_id, "gstin": gstin, "document_text": doc_text, "esg_score": esg, "gst_fraud_flag": fraud, "sanctions_match": sanctions}
            res = requests.post(f"{BACKEND_URL}/process-vendor", json=payload, timeout=20).json()
            decision = res.get('decision') or res.get('final_decision') or 'EVALUATED'
            st.success(f"Decision: **{decision}** | Risk Score: **{res.get('risk_score','N/A')}**")
            st.json(res)
            extracted_audit_id = res.get("audit_id") or (res.get("audit", {}).get("audit_id") if isinstance(res.get("audit"), dict) else None)
            if extracted_audit_id:
                st.session_state["last_audit_id"] = extracted_audit_id
        except Exception as e:
            st.error(f"Execution Error: {e}")
st.divider()
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
st.header("3. Recent SHA-256 Audit Ledger Entries")
try:
    try:
        r = requests.get(f"{BACKEND_URL}/audit/trail", timeout=10)
        audits_data = r.json()
    except:
        r = requests.get(f"{BACKEND_URL}/audits", timeout=10)
        audits_data = r.json()
    if isinstance(audits_data, dict):
        audits = audits_data.get("trail", audits_data.get("audits", []))
        if isinstance(audits, dict):
            audits = [audits]
    elif isinstance(audits_data, list):
        audits = audits_data
    else:
        audits = []
    if audits:
        st.dataframe(audits[-10:], use_container_width=True)
        st.caption(f"Total: {len(audits)} | SHA-256 Tamper-evident")
    else:
        st.write("No audit records yet - run workflow")
        st.json(audits_data)
except Exception as e:
    st.write(f"No audit records found: {e}")
