# ML: Training on synthetic enterprise data - ET Hackathon requirement
import pandas as pd, pathlib, random, pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from faker import Faker

fake = Faker()
path = pathlib.Path(__file__).parent.parent / "data" / "synthetic_vendors" / "vendors.csv"
path.parent.mkdir(parents=True, exist_ok=True)

rows=[]
for i in range(2000):
    esg=random.randint(20,95); gst=random.choice([0,0,0,1]); sanc=random.choice([0,0,0,0,1]); inv=random.random()
    label=2 if sanc==1 or inv>0.8 else 1 if esg<45 or gst==1 else 0
    rows.append([f"VEND-{i}",esg,gst,sanc,inv,label])

df=pd.DataFrame(rows, columns=["vendor_id","esg_score","gst_fraud_flag","sanctions_match","invoice_anomaly","label"])
df.to_csv(path,index=False)

X=df[["esg_score","gst_fraud_flag","sanctions_match","invoice_anomaly"]]
y=df["label"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
model=RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train,y_train)
print(f"Accuracy: {model.score(X_test,y_test):.2f} | Data: {path}")
with open(pathlib.Path(__file__).parent / "risk_model.pkl","wb") as f:
    pickle.dump(model,f)
