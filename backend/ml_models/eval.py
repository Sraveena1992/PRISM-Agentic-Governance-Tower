import os
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

def evaluate_model():
    model_path = os.path.join(os.path.dirname(__file__), "risk_scorer.joblib")
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}. Run train.py first.")
        return

    model = joblib.load(model_path)
    
    # Generate holdout evaluation set (500 synthetic enterprise vendor profiles)
    np.random.seed(42)
    eval_data = {
        'financial_stability_score': np.random.uniform(0.1, 1.0, 500),
        'compliance_history_score': np.random.uniform(0.1, 1.0, 500),
        'esg_rating': np.random.uniform(20, 100, 500),
        'gst_fraud_flag': np.random.choice([0, 1], size=500, p=[0.85, 0.15])
    }
    df = pd.DataFrame(eval_data)
    
    # Synthetic ground truth risk condition
    y_true = ((df['gst_fraud_flag'] == 1) | 
              (df['esg_rating'] < 40) | 
              (df['financial_stability_score'] < 0.3)).astype(int)
    
    X = df[['financial_stability_score', 'compliance_history_score', 'esg_rating', 'gst_fraud_flag']]
    
    # Predict probabilities & labels
    y_pred_probs = model.predict_proba(X)[:, 1]
    y_pred = (y_pred_probs >= 0.60).astype(int)
    
    print("=== PRISM ML RISK ENGINE BENCHMARK REPORT ===")
    print("\nClassification Report (High-Risk Threshold = 0.60):")
    print(classification_report(y_true, y_pred, target_names=['Low/Medium Risk', 'High Risk']))
    
    cm = confusion_matrix(y_true, y_pred)
    print("Confusion Matrix:")
    print(f"True Negatives: {cm[0][0]} | False Positives: {cm[0][1]}")
    print(f"False Negatives: {cm[1][0]} | True Positives: {cm[1][1]}")
    
    auc = roc_auc_score(y_true, y_pred_probs)
    print(f"\nROC-AUC Score: {auc:.4f}")
    
if __name__ == "__main__":
    evaluate_model()
