import streamlit as st
import numpy as np
import pandas as pd
import joblib

@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

try:
    model = load_model()
except FileNotFoundError:
    st.error("Model file not found.")
    st.stop()

# This is the EXACT list you provided (minus 'y')
# The order must be exactly like this for the model to work
model_features = [
    'age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous',
    'job_blue-collar', 'job_entrepreneur', 'job_housemaid', 'job_management', 
    'job_retired', 'job_self-employed', 'job_services', 'job_student', 
    'job_technician', 'job_unemployed', 'marital_married', 'marital_single', 
    'education_secondary', 'education_tertiary', 'default_yes', 'housing_yes', 
    'loan_yes', 'contact_telephone', 'month_aug', 'month_dec', 'month_feb', 
    'month_jan', 'month_jul', 'month_jun', 'month_mar', 'month_may', 
    'month_nov', 'month_oct', 'month_sep'
]

st.title("Bank Marketing Prediction App")

# ... (keep your existing st.selectbox and st.number_input code here) ...

def preprocess_input():
    # Create a template of 36 zeros (37 features minus 'y')
    df_input = pd.DataFrame(0, index=[0], columns=model_features)

    # 1. Numerical values
    df_input['age'] = age
    df_input['balance'] = balance
    df_input['day'] = day
    df_input['duration'] = duration
    df_input['campaign'] = campaign
    df_input['pdays'] = pdays
    df_input['previous'] = previous

    # 2. Categorical values (Handling drop_first=True)
    # If the user selects the 'first' category (e.g., 'admin.' for job), 
    # all other job columns remain 0.
    
    if f'job_{job}' in model_features:
        df_input[f'job_{job}'] = 1
        
    if f'marital_{marital}' in model_features:
        df_input[f'marital_{marital}'] = 1
        
    if f'education_{education}' in model_features:
        df_input[f'education_{education}'] = 1
        
    if default == "yes":
        df_input['default_yes'] = 1
        
    if housing == "yes":
        df_input['housing_yes'] = 1
        
    if loan == "yes":
        df_input['loan_yes'] = 1
        
    if f'contact_{contact}' in model_features:
        df_input[f'contact_{contact}'] = 1
        
    if f'month_{month}' in model_features:
        df_input[f'month_{month}'] = 1

    return df_input



if st.button("🔮 Predict"):
    try:
        X_input = preprocess_input()
        
        # Ensure the column order is perfect
        X_input = X_input[model_features]
        
        prediction = model.predict(X_input)[0]

        if prediction == 1:
            st.success("The customer is likely to subscribe!")
        else:
            st.error("The customer is NOT likely to subscribe.")

    except Exception as e:
        st.error(f"Error: {e}")