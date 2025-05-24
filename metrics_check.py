from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import joblib

# تحميل النموذج والبيانات
model, cols = joblib.load("rf_model.pkl")  # تأكد أن الملف موجود بنفس المجلد
df = pd.read_csv("readmission_training_data.csv")  # لازم يكون موجود بنفس المجلد

# تجهيز البيانات
features = ['ID''Age', 'LOS_days', 'Prev_Admissions', 'Comorbidity_Score']
categorical = ['Discharge_Type', 'Follow_Up', 'Gender']
X = pd.get_dummies(df[features + categorical], drop_first=False)
X = X.reindex(columns=cols, fill_value=0)
y_true = df["Prediction"]
y_pred = model.predict(X)

# طباعة المقاييس
print("✅ Model Performance Metrics:")
print("Accuracy:", accuracy_score(y_true, y_pred))
print("Precision:", precision_score(y_true, y_pred))
print("Recall:", recall_score(y_true, y_pred))
print("F1 Score:", f1_score(y_true, y_pred))
