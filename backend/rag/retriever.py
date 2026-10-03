# Lightweight Vector RAG - Render 512MB friendly
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

POLICIES = [
    {"id": "POLICY-001", "text": "ESG Compliance requires rating above 60 and no environmental violations"},
    {"id": "POLICY-002", "text": "GST fraud flag leads to high risk and human approval required"},
    {"id": "POLICY-003", "text": "Data privacy violation needs immediate review"},
    {"id": "POLICY-004", "text": "Financial fraud history blocks vendor"},
    {"id": "POLICY-005", "text": "Low ESG rating 35 triggers fail-closed gate"},
]

_vectorizer = TfidfVectorizer()
_corpus = [p["text"] for p in POLICIES]
_tfidf_matrix = _vectorizer.fit_transform(_corpus)

def get_relevant_policies(query: str, top_k=2):
    """Real Vector Search using TF-IDF + Cosine Similarity - FAISS-style execution"""
    if not query:
        query = "ESG GST Compliance"
    q_vec = _vectorizer.transform([query])
    scores = cosine_similarity(q_vec, _tfidf_matrix)[0]
    top_idx = np.argsort(scores)[::-1][:top_k]
    results = []
    for i in top_idx:
        results.append({
            "id": POLICIES[i]["id"],
            "text": POLICIES[i]["text"],
            "similarity_score": round(float(scores[i]), 4),
            "retriever": "TF-IDF Vector + Cosine Matrix"
        })
    return results
