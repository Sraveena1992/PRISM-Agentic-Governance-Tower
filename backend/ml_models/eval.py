import os
import joblib
from sklearn.metrics import classification_report, roc_auc_score
from backend.ml_models.train import generate_synthetic_training_data, MODEL_PATH

def evaluate_model():
    if not os.path.exists(MODEL_PATH):
        print(f"[ML Eval] Model not found at {MODEL_PATH}. Running train.py first...")
        from backend.ml_models.train import train_and_save_model
        train_and_save_model()

    clf = joblib.load(MODEL_PATH)
    test_df = generate_synthetic_training_data(n_samples=300)
    
    X_test = test_df[["esg_score", "financial_stability_score", "gst_fraud_flag", "sanctions_match", "invoice_anomaly"]]
    y_test = test_df["high_risk_label"]

    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]

    auc = roc_auc_score(y_test, y_prob)

    print("\n================ ML RISK ENGINE BENCHMARK METRICS ================")
    print(classification_report(y_test, y_pred, target_names=["Low Risk (0)", "High Risk (1)"]))
    print(f"ROC-AUC Score: {auc:.4f}")
    print("==================================================================\n")

if __name__ == "__main__":
    evaluate_model()
