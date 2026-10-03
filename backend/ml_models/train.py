import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "random_forest_risk_model.joblib"))

def generate_synthetic_training_data(n_samples: int = 1000):
    np.random.seed(42)
    
    esg_score = np.random.uniform(10.0, 100.0, n_samples)
    financial_stability = np.random.uniform(0.1, 1.0, n_samples)
    gst_fraud_flag = np.random.choice([0, 1], size=n_samples, p=[0.92, 0.08])
    sanctions_match = np.random.choice([0, 1], size=n_samples, p=[0.95, 0.05])
    invoice_anomaly = np.random.uniform(0.0, 1.0, n_samples)

    # Risk Labeling Logic
    high_risk_condition = (
        (gst_fraud_flag == 1) | 
        (sanctions_match == 1) | 
        (esg_score < 40.0) | 
        (financial_stability < 0.5) | 
        (invoice_anomaly > 0.6)
    )
    labels = np.where(high_risk_condition, 1, 0)

    df = pd.DataFrame({
        "esg_score": esg_score,
        "financial_stability_score": financial_stability,
        "gst_fraud_flag": gst_fraud_flag,
        "sanctions_match": sanctions_match,
        "invoice_anomaly": invoice_anomaly,
        "high_risk_label": labels
    })
    return df


def train_and_save_model():
    print("[ML Train] Generating synthetic procurement dataset...")
    df = generate_synthetic_training_data(n_samples=1500)
    
    X = df[["esg_score", "financial_stability_score", "gst_fraud_flag", "sanctions_match", "invoice_anomaly"]]
    y = df["high_risk_label"]

    clf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    clf.fit(X, y)

    joblib.dump(clf, MODEL_PATH)
    print(f"[ML Train] Trained RandomForest model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save_model()
