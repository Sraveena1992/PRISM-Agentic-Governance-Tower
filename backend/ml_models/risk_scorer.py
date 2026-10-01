import pathlib
try:
    import pickle
    model_path = pathlib.Path(__file__).parent / "risk_model.pkl"
    model = pickle.load(open(model_path,"rb")) if model_path.exists() else None
except:
    model = None

def score_risk(esg_score,gst_fraud_flag,sanctions_match,invoice_anomaly):
    if sanctions_match==1: return 0.99
    if model is None: return 0.65
    try:
        pred = model.predict_proba([[esg_score,gst_fraud_flag,sanctions_match,invoice_anomaly]])[0]
        if pred[2]>0.5: return 0.99
        if pred[1]>0.5: return 0.65
        return 0.05
    except:
        return 0.65
