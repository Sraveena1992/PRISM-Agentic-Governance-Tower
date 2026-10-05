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
    esg = float(payload.get("esg_score", payload.get("esg_rating", 75.0)))
    fin = float(payload.get("financial_stability_score", 0.85))
    gst = int(payload.get("gst_fraud_flag", 0))
    sanc = int(payload.get("sanctions_match", 0))
    anom = float(payload.get("invoice_anomaly", payload.get("invoice_anomaly_score", 0.10)))
    features = np.array([[esg, fin, gst, sanc, anom]], dtype=np.float64)
    return features

def score_risk(payload: Dict[str, Any]) -> float:
    """
    P1 FIXED: No silent fallback.
    MODEL AVAILABLE -> ML SCORE
    MODEL MISSING -> RAISE -> GOVERNANCE -> SAFE HOLD 0.99 REJECTED
    INFERENCE ERROR -> RAISE -> GOVERNANCE -> SAFE HOLD
    """
    # Statutory gate is deterministic - allowed before ML
    gst_flag = int(payload.get("gst_fraud_flag", 0))
    sanctions_flag = int(payload.get("sanctions_match", 0))
    if gst_flag == 1 or sanctions_flag == 1:
        return 0.99

    # P1 FIX: If model missing, RAISE - don't auto-heal
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"ML model missing at {MODEL_PATH} -> Triggering SAFE HOLD")

    # P1 FIX: If inference fails, RAISE - don't fallback to rules
    try:
        model = joblib.load(MODEL_PATH)
        X = extract_features(payload)
        prob = model.predict_proba(X)[0][1]
        return float(round(prob, 4))
    except FileNotFoundError:
        raise
    except Exception as e:
        print(f"[ML Engine] Inference FAILED - propagating to governance fail-closed: {e}")
        raise RuntimeError(f"ML inference failure: {e}")

class RiskScorer:
    def predict_risk(self, payload: Dict[str, Any]) -> float:
        return score_risk(payload)

    def score_risk(self, payload: Dict[str, Any]) -> float:
        return score_risk(payload)

risk_scorer = RiskScorer()

def predict_risk(payload: Dict[str, Any]) -> float:
    return score_risk(payload)
