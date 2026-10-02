import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

POLICIES = [
    {
        "id": "POLICY-001",
        "title": "RBI Vendor ESG Governance Guidelines 2024",
        "content": "Vendors with an ESG rating below 40 are strictly prohibited from auto-approval. High-risk ESG scores trigger mandatory human compliance review and manual sign-off."
    },
    {
        "id": "POLICY-002",
        "title": "GST Act Compliance & Tax Fraud Prevention",
        "content": "Any vendor flagged with a GST fraud indicator or active tax non-compliance must be immediately blocked (Risk Score = 0.95) and reported to financial risk controllers."
    },
    {
        "id": "POLICY-003",
        "title": "Enterprise Financial Stability Thresholds",
        "content": "Financial stability score below 0.3 indicates severe liquidity default risk. All contracts exceeding threshold limits require 2-factor CFO override."
    }
]

class VectorRAGRetriever:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.documents = POLICIES
        self._build_index()

    def _build_index(self):
        corpus = [doc["content"] for doc in self.documents]
        embeddings = self.model.encode(corpus, convert_to_numpy=True)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))

    def retrieve(self, query: str, top_k: int = 2):
        """Performs dense vector similarity search with scores"""
        query_vector = self.model.encode([query], convert_to_numpy=True).astype('float32')
        distances, indices = self.index.search(query_vector, top_k)
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.documents):
                doc = self.documents[idx].copy()
                doc["similarity_score"] = float(1 / (1+dist))
                doc["l2_distance"] = float(dist)
                results.append(doc)
        return results

rag_retriever = VectorRAGRetriever()

def get_relevant_policies(query: str):
    return rag_retriever.retrieve(query)
