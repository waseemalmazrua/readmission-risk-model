import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# تحميل البيانات
df = pd.read_csv("realistic_readmission_data.csv")

# تحديد المتغيرات
features = ['Age', 'LOS_days', 'Prev_Admissions', 'Comorbidity_Score']
categorical = ['Discharge_Type', 'Follow_Up', 'Gender']
X = pd.get_dummies(df[features + categorical], drop_first=False)
y = df["Prediction"]
print(df["Prediction"].value_counts(normalize=True))


# تقسيم البيانات إلى تدريب واختبار
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# تدريب النموذج
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# تقييم الأداء على بيانات الاختبار
y_pred = model.predict(X_test)
print("✅ Realistic Model Performance (on unseen data):")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))

# حفظ النموذج والمتغيرات
joblib.dump((model, X.columns.tolist()), "rf_model.pkl")
