import os
import joblib
import numpy as np
from typing import Dict, Any

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "random_forest_risk_model.joblib"))

# 🔥 AUTO-HEAL: If model file missing on Render, create it instantly
if not os.path.exists(MODEL_PATH):
    try:
        from sklearn.ensemble import RandomForestClassifier
        print(f"⚠️ ML model missing at {MODEL_PATH}, training fallback...")
        # Training data matching your FEATURE_NAMES order: esg, fin, gst, sanc, anomaly
        X = np.array([
            [85, 0.9, 0, 0, 0.1],
            [20, 0.3, 1, 0, 0.8],
            [15, 0.2, 1, 1, 0.9],
            [90, 0.95, 0, 0, 0.05],
            [50, 0.4, 0, 1, 0.6],
            [30, 0.3, 1, 0, 0.7],
        ], dtype=np.float64)
        y = np.array([0, 1, 1, 0, 1, 1])
        clf = RandomForestClassifier(n_estimators=20, random_state=42)
        clf.fit(X, y)
        joblib.dump(clf, MODEL_PATH)
        print(f"✅ Fallback model created at {MODEL_PATH}")
    except Exception as e:
        print(f"❌ Auto-train failed (will use deterministic fallback): {e}")

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
    gst_flag = int(payload.get("gst_fraud_flag", 0))
    sanctions_flag = int(payload.get("sanctions_match", 0))
    if gst_flag == 1 or sanctions_flag == 1:
        return 0.99

    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            X = extract_features(payload)
            prob = model.predict_proba(X)[0][1]
            return float(round(prob, 4))
        except Exception as e:
            print(f"[ML Engine] Model inference fallback active: {e}")

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

class RiskScorer:
    def predict_risk(self, payload: Dict[str, Any]) -> float:
        return score_risk(payload)
    def score_risk(self, payload: Dict[str, Any]) -> float:
        return score_risk(payload)

risk_scorer = RiskScorer()

def predict_risk(payload: Dict[str, Any]) -> float:
    return score_risk(payload)
