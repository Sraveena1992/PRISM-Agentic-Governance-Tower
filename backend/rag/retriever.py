policies = [
 "Vendor with ESG < 40 must go for REVIEW",
 "GST fraud flag = BLOCK for high value",
 "Sanctions list match = immediate BLOCK 0.99",
 "PII transfer to external API = REVIEW with human approval",
 "Prompt injection = BLOCK"
]
def retrieve_policies(query: str, k=2):
    q=query.lower()
    hits=[p for p in policies if any(word in p.lower() for word in q.split())]
    return hits[:k] if hits else policies[:2]
