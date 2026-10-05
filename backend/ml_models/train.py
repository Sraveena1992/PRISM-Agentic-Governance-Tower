import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Ensure path is absolute
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, "random_forest_risk_model.joblib")

print(f"[TRAIN] Starting training, target: {MODEL_PATH}")

# 1500 synthetic samples - 5 features [esg, fin, gst, sanc, anomaly]
np.random.seed(42)
n_samples = 1500

esg = np.random.uniform(10, 95, n_samples)
fin = np.random.uniform(0.1, 1.0, n_samples)
gst = np.random.choice([0, 1], n_samples, p=[0.85, 0.15])
sanc = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
anom = np.random.uniform(0.0, 1.0, n_samples)

X = np.column_stack([esg, fin, gst, sanc, anom])

# Risk logic: fraud/sanctions = high risk, low esg/fin + high anomaly = high risk
y = ((gst == 1) | (sanc == 1) | (esg < 40) | (fin < 0.4) | (anom > 0.7)).astype(int)

# Add some noise
y = np.where(np.random.rand(n_samples) < 0.05, 1 - y, y)

clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(X, y)

os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(clf, MODEL_PATH)

print(f"✅ Model trained: {X.shape}, Risk samples: {np.sum(y)}")
print(f"✅ Model saved at {MODEL_PATH}")
print(f"✅ File exists: {os.path.exists(MODEL_PATH)}")
print(f"✅ File size: {os.path.getsize(MODEL_PATH)} bytes")

# Verify load
loaded = joblib.load(MODEL_PATH)
test = np.array([[85, 0.9, 0, 0, 0.1]])
print(f"✅ Verification pred: {loaded.predict_proba(test)[0]}")

if __name__ == "__main__":
    print("Training complete")
