import streamlit as st
import numpy as np
import pandas as pd # Needed for handling column names
import joblib

@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

try:
    model = load_model()
except FileNotFoundError:
    st.error("Model file not found. Please ensure 'model.pkl' is in the same directory.")
    st.stop()

# --- DEFINING THE 37 COLUMNS ---
# This list MUST match the exact order of X_train.columns from your notebook
model_features = [
    'age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous',
    'job_admin.', 'job_blue-collar', 'job_entrepreneur', 'job_housemaid', 
    'job_management', 'job_retired', 'job_self-employed', 'job_services', 
    'job_student', 'job_technician', 'job_unemployed', 'job_unknown',
    'marital_divorced', 'marital_married', 'marital_single',
    'education_primary', 'education_secondary', 'education_tertiary', 'education_unknown',
    'default_no', 'default_yes', 'housing_no', 'housing_yes',
    'loan_no', 'loan_yes', 'contact_cellular', 'contact_telephone', 'contact_unknown',
    'month_apr', 'month_aug', 'month_dec', 'month_feb', 'month_jan', 'month_jul', 
    'month_jun', 'month_mar', 'month_may', 'month_nov', 'month_oct', 'month_sep'
]
# Note: I've included the standard 37 columns from the bank dataset. 
# Check your notebook with `print(X_train.columns.tolist())` to verify the order.

st.title("Bank Marketing Prediction App")
st.write("Predict if a customer will subscribe to a term deposit.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    balance = st.number_input("Average Yearly Balance", value=1000)
    day = st.slider("Last Contact Day of Month", 1, 31, 15)
    duration = st.number_input("Last Call Duration (seconds)", min_value=0, value=200)
    campaign = st.number_input("Contacts during this Campaign", min_value=1, value=1)

with col2:
    pdays = st.number_input("Days since last contact (-1 if never)", value=-1)
    previous = st.number_input("Previous contacts before this campaign", min_value=0, value=0)
    job = st.selectbox("Job", ["admin.", "blue-collar", "entrepreneur", "housemaid", "management", "retired", "self-employed", "services", "student", "technician", "unemployed", "unknown"])
    marital = st.selectbox("Marital Status", ["married", "single", "divorced"])
    education = st.selectbox("Education", ["primary", "secondary", "tertiary", "unknown"])

col3, col4, col5 = st.columns(3)
with col3:
    housing = st.selectbox("Housing Loan?", ["no", "yes"])
with col4:
    loan = st.selectbox("Personal Loan?", ["no", "yes"])
with col5:
    default = st.selectbox("Credit Default?", ["no", "yes"])

contact = st.selectbox("Contact Communication", ["cellular", "telephone", "unknown"])
month = st.selectbox("Last Contact Month", ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])

def preprocess_input():
    # 1. Create a DataFrame with all zeros matching the 37 model features
    df_input = pd.DataFrame(0, index=[0], columns=model_features)

    # 2. Fill Numerical Columns
    df_input['age'] = age
    df_input['balance'] = balance
    df_input['day'] = day
    df_input['duration'] = duration
    df_input['campaign'] = campaign
    df_input['pdays'] = pdays
    df_input['previous'] = previous

    # 3. Fill Categorical Columns (One-Hot Encoding logic)
    # This sets the specific column (e.g., 'job_management') to 1
    cat_inputs = {
        'job': job, 'marital': marital, 'education': education,
        'default': default, 'housing': housing, 'loan': loan,
        'contact': contact, 'month': month
    }

    for key, value in cat_inputs.items():
        col_name = f"{key}_{value}"
        if col_name in model_features:
            df_input[col_name] = 1

    return df_input

st.markdown("---")

if st.button("🔮 Predict"):
    try:
        X_input = preprocess_input()
        
        # Ensure the columns are in the EXACT order the model expects
        X_input = X_input[model_features]
        
        prediction = model.predict(X_input)[0]

        st.subheader("Prediction Result")
        if prediction == 1 or str(prediction).lower() == "yes":
            st.success("✅ The customer is likely to subscribe to a term deposit.")
        else:
            st.error("❌ The customer is NOT likely to subscribe.")

        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(X_input)[0]
            st.write(f"Confidence: **{np.max(prob) * 100:.2f}%**")

    except Exception as e:
        st.error("Prediction failed due to feature mismatch.")
        st.write(f"Error details: {e}")
        st.info(f"Model expects {len(model_features)} features, App generated {X_input.shape[1]} features.")

st.markdown("---")
st.caption("Bank Marketing ML App | One-Hot Encoding Enabled")