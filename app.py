import pandas as pd

def preprocess_input():
    # 1. Initialize a dictionary with all required features set to 0
    feature_dict = {
        'age': age, 'balance': balance, 'day': day, 'duration': duration,
        'campaign': campaign, 'pdays': pdays, 'previous': previous,
        'job_blue-collar': 0, 'job_entrepreneur': 0, 'job_housemaid': 0,
        'job_management': 0, 'job_retired': 0, 'job_self-employed': 0,
        'job_services': 0, 'job_student': 0, 'job_technician': 0,
        'job_unemployed': 0, 'marital_married': 0, 'marital_single': 0,
        'education_secondary': 0, 'education_tertiary': 0, 'default_yes': 0,
        'housing_yes': 0, 'loan_yes': 0, 'contact_telephone': 0,
        'month_aug': 0, 'month_dec': 0, 'month_feb': 0, 'month_jan': 0,
        'month_jul': 0, 'month_jun': 0, 'month_mar': 0, 'month_may': 0,
        'month_nov': 0, 'month_oct': 0, 'month_sep': 0
    }

    # 2. Update categorical features based on user input
    if f"job_{job}" in feature_dict:
        feature_dict[f"job_{job}"] = 1
    
    if f"marital_{marital}" in feature_dict:
        feature_dict[f"marital_{marital}"] = 1
        
    if f"education_{education}" in feature_dict:
        feature_dict[f"education_{education}"] = 1

    if month != "apr": # Assuming 'apr' was the dropped baseline during encoding
        if f"month_{month}" in feature_dict:
            feature_dict[f"month_{month}"] = 1

    # 3. Handle Binary/Boolean inputs
    if default == "yes": feature_dict['default_yes'] = 1
    if housing == "yes": feature_dict['housing_yes'] = 1
    if loan == "yes": feature_dict['loan_yes'] = 1
    if contact == "telephone": feature_dict['contact_telephone'] = 1

    # 4. Convert to DataFrame to ensure correct column order
    # Note: 'y' is excluded as it is the target variable
    feature_order = [
        'age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous',
        'job_blue-collar', 'job_entrepreneur', 'job_housemaid', 'job_management',
        'job_retired', 'job_self-employed', 'job_services', 'job_student',
        'job_technician', 'job_unemployed', 'marital_married', 'marital_single',
        'education_secondary', 'education_tertiary', 'default_yes', 'housing_yes',
        'loan_yes', 'contact_telephone', 'month_aug', 'month_dec', 'month_feb',
        'month_jan', 'month_jul', 'month_jun', 'month_mar', 'month_may',
        'month_nov', 'month_oct', 'month_sep'
    ]
    
    df_input = pd.DataFrame([feature_dict])[feature_order]
    return df_input