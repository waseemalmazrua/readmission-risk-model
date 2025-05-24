import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

def train_and_save_model(df, model_path="rf_model.pkl"):
    df = df.copy()

    # تأكد من وجود عمود Prediction
    if "Prediction" not in df.columns:
        raise ValueError("❌ Missing column 'Prediction' in training data.")

    features = ['ID','Age', 'LOS_days', 'Prev_Admissions', 'Comorbidity_Score']
    categorical = ['Discharge_Type', 'Follow_Up', 'Gender']

    X = pd.get_dummies(df[features + categorical], drop_first=False)
    y = df["Prediction"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump((model, X.columns.tolist()), model_path)

def load_model(model_path="rf_model.pkl"):
    return joblib.load(model_path)
