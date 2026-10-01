import pandas as pd, random
vendors=[]
for i in range(2000):
    esg = random.randint(15,95)
    gst_fraud = 1 if esg<30 and random.random()>0.7 else 0
    sanction = 1 if random.random()<0.02 else 0
    spend = random.choice([50000, 250000, 1200000])
    if sanction==1: risk=0.99
    elif gst_fraud==1 or esg<40: risk=0.65
    else: risk=0.05
    vendors.append([f"VEND-{1000+i}", esg, gst_fraud, sanction, spend, risk])
df=pd.DataFrame(vendors, columns=["vendor_id","esg_score","gst_fraud_flag","sanction_flag","spend_value","risk_score"])
df.to_csv("backend/data/synthetic_vendors.csv", index=False)
print("2000 vendors generated - ML Ready")
