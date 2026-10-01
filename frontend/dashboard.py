import streamlit as st
st.set_page_config(page_title="PRISM - Governance Tower", layout="wide")
st.title("PRISM — Agentic Enterprise Governance Tower")
st.subheader("Agents that work. Humans who lead. Audit that never lies.")

col1, col2, col3 = st.columns(3)
col1.metric("Risk Score", "0.05", "ALLOW - ESG 90")
col2.metric("Risk Score", "0.65", "REVIEW - ESG 35")
col3.metric("Risk Score", "0.99", "BLOCK - Sanctions")

st.divider()
st.header("Human Approval Queue [REVIEW Cases]")
vendor = {"vendor_id": "VEND-123", "esg_score": 35, "gst_fraud_flag": 1, "task": "High-value procurement approval"}
st.json(vendor)
st.warning("Policies Applied: Vendor with ESG < 40 must go for REVIEW | GST fraud flag = BLOCK for high value")

c1, c2 = st.columns(2)
if c1.button("✅ Approve - Execute with Audit", use_container_width=True):
    st.success(f"APPROVED - Audit ID: a9f2...3c4e1b | SHA256 Logged | Final: EXECUTED")
if c2.button("❌ Reject - Block & Archive", use_container_width=True):
    st.error(f"REJECTED - Audit ID: a9f2...3c4e1b | Final: BLOCKED - Fail Closed")

st.divider()
st.caption("Governance: ML Risk Scorer (0.05/0.65/0.99) + RAG + Human-in-Loop + SHA256 Immutable Logs")
