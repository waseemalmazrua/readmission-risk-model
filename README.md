# 🏥 30-Day Readmission Risk Prediction Model

This repository contains a machine learning model to predict the risk of hospital readmission within 30 days using clinical and demographic patient data.

The project was built using a Random Forest classifier and trained on a structured dataset representing key patient risk factors.

---

## 📁 Project Structure

| File                          | Description                                         |
|------------------------------|-----------------------------------------------------|
| `train_model.py`             | Trains the Random Forest model and saves it        |
| `rf_model.pkl`               | Saved model file using `joblib`                    |
| `realistic_readmission_data.csv` | Clean, synthetic dataset used for training     |
| `patient_data_for_clients.csv` | Template input format for user predictions     |
| `app.py`                     | Dash web app to allow user CSV upload and prediction |

---

## ⚙️ Features Used

The model uses the following patient features:
- Age
- Length of Stay (LOS_days)
- Number of Previous Admissions
- Comorbidity Score (Charlson Index)
- Discharge Type (Categorical)
- Follow-Up Type (Categorical)
- Gender (Categorical)

---

## 📈 Model Evaluation (on test split)

> ⚠️ **Note:** This model achieved perfect scores due to the synthetic and clean structure of the dataset used for prototyping.  
> In real-world scenarios, such performance may not be achievable and proper cross-validation with real data is recommended.

- ✅ Accuracy: 100%
- ✅ Precision: 100%
- ✅ Recall: 100%
- ✅ F1 Score: 100%

---

## 📥 Usage Instructions

1. Download `patient_data_for_clients.csv`
2. Open the Dash app (`app.py`) locally or deploy online
3. Upload a CSV file following the required structure
4. View predictions for each patient

---

## 👨‍⚕️ Author

**Waseem Almazrua**  
Registered Nurse | Data Analyst | CPHQ  

---

## ⭐️ Star this repo if you find it useful or want to support healthcare analytics!
