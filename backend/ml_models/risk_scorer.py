import os
import joblib
import numpy as np
from typing import Dict, Any

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "random_forest_risk_model.joblib"))

# Canonical Feature List (Must match training vector ordering exactly)
FEATURE_NAMES = [
    "esg_score",
    "financial_stability_score",
    "gst_fraud_flag",
    "sanctions_match",
    "invoice_anomaly"
]

def extract_features(payload: Dict[str, Any]) -> np.ndarray:
    """
    Extracts and normalizes features from input payload with safe type-casting and defaults.
    """
    # Key normalization alias support (e.g. esg_rating -> esg_score)
    esg = float(payload.get("esg_score", payload.get("esg_rating", 75.0)))
    fin = float(payload.get("financial_stability_score", 0.85))
    gst = int(payload.get("gst_fraud_flag", 0))
    sanc = int(payload.get("sanctions_match", 0))
    anom = float(payload.get("invoice_anomaly", payload.get("invoice_anomaly_score", 0.10)))

    # Feature Vector Construction
    features = np.array([[esg, fin, gst, sanc, anom]], dtype=np.float64)
    return features


def score_risk(payload: Dict[str, Any]) -> float:
    """
    Evaluates ML Risk Score.
    Uses trained Scikit-Learn RandomForest classifier if available, 
    otherwise falls back to deterministic fail-closed rule scoring.
    """
    # 1. Immediate Statutory Override (Fail-Closed Governance Rules)
    gst_flag = int(payload.get("gst_fraud_flag", 0))
    sanctions_flag = int(payload.get("sanctions_match", 0))
    if gst_flag == 1 or sanctions_flag == 1:
        return 0.99

    # 2. ML Model Inference
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            X = extract_features(payload)
            # Predict probability of High Risk class (Index 1)
            prob = model.predict_proba(X)[0][1]
            return float(round(prob, 4))
        except Exception as e:
            print(f"[ML Engine] Model inference fallback active: {e} | Using governance-approved deterministic scorer")

    # 3. Deterministic Scorer Fallback
    esg = float(payload.get("esg_score", payload.get("esg_rating", 75.0)))
    fin = float(payload.get("financial_stability_score", 0.85))
    anom = float(payload.get("invoice_anomaly", payload.get("invoice_anomaly_score", 0.10)))

    base_risk = 0.20
    if esg < 40.0:
        base_risk += 0.35
    if fin < 0.50:
        base_risk += 0.30
    if anom > 0.50:
        base_risk += 0.25

    return float(round(min(base_risk, 0.95), 4))
