import streamlit as st
import pandas as pd
import pickle

# Load your trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

obesity_mapping = {
    0: 'Insufficient_Weight',
    1: 'Normal_Weight',
    2: 'Overweight_Level_I',
    3: 'Overweight_Level_II',
    4: 'Obesity_Type_I',
    5: 'Obesity_Type_II',
    6: 'Obesity_Type_III'
}

# Define the input features for the user to input
def user_input_features():
    age = st.number_input('Age:',min_value=14, max_value=100, value=24, step=1, format="%d")
    height = st.number_input('Height' ,min_value=1.0, max_value=2.8, value=1.7, format='%.2f')
    weight = st.number_input('Weight',min_value=10.0, max_value=200.0, value=67.0, format='%.1f')
    family_history_with_overweight = st.radio('Family history with overweight', ('Yes', 'No'))
    favc = st.radio('Frequent consumption of high caloric food (FAVC)', ('Yes', 'No'))
    fcvc = st.number_input('Frequency of consumption of vegetables (FCVC)', min_value=14.0, max_value=100.0, value=24.0, format='%.2f')
    ncp = st.number_input('Number of main meals (NCP)', min_value=0.0, max_value=10.0, value=3.0, step=0.5, format='%.1f')
    caec = st.radio('Consumption of food between meals (CAEC)', ('Never', 'Sometimes', 'Frequently', 'Always'))
    smoke = st.radio('Smoke', ('Yes', 'No'))
    ch2o = st.number_input('Consumption of water daily (CH2O)', min_value=0.0, max_value=20.0, value=1.5, step=0.1, format='%.2f')
    scc = st.radio('Calories consumption monitoring (SCC)', ('Yes', 'No'))
    faf = st.number_input('Physical activity frequency (FAF)',min_value=0.0, max_value=3.0, value=1.0, format='%.2f')
    tue = st.number_input('Time using technology devices (TUE)', min_value=0.0, max_value=24.0, value=1.0, step=0.1, format='%.2f')
    calc = st.radio('Alcohol consumption (CALC)', ('Never', 'Sometimes', 'Frequently', 'Always'))
    mtrans = st.selectbox(
        'Transportation used (MTRANS)', 
        ('Public_Transportation', 'Automobile', 'Walking', 'Bike', 'Motorbike')
    )
    gender = st.radio('Gender', ('Female', 'Male'))

    # Convert Yes/No to 1/0
    family_history_with_overweight = 1 if family_history_with_overweight == 'Yes' else 0
    favc = 1 if favc == 'Yes' else 0
    smoke = 1 if smoke == 'Yes' else 0
    scc = 1 if scc == 'Yes' else 0

    # Convert other categorical features to numbers if necessary
    caec = ['Never', 'Sometimes', 'Frequently', 'Always'].index(caec)
    calc = ['Never', 'Sometimes', 'Frequently', 'Always'].index(calc)
    mtrans = ['Public_Transportation', 'Automobile', 'Walking', 'Bike', 'Motorbike'].index(mtrans)
    gender_female = 1 if gender == 'Female' else 0
    gender_male = 1 if gender == 'Male' else 0

    # Organize data in the same structure as the training data
    data = {
        'id' : 0,
        'Age': age,
        'Height': height,
        'Weight': weight,
        'family_history_with_overweight': family_history_with_overweight,
        'FAVC': favc,
        'FCVC': fcvc,
        'NCP': ncp,
        'CAEC': caec,
        'SMOKE': smoke,
        'CH2O': ch2o,
        'SCC': scc,
        'FAF': faf,
        'TUE': tue,
        'CALC': calc,
        'MTRANS': mtrans,
        'Gender_Female': gender_female,
        'Gender_Male': gender_male
    }
    features = pd.DataFrame(data, index=[0])
    return features

st.title('Obesity Prediction App')

# Display the input fields
input_df = user_input_features()

# Predict button
if st.button('Predict'):
    # Make a prediction
    prediction = model.predict(input_df)
    prediction_proba = model.predict_proba(input_df)[0]

    data = {
        'Obesity Type': [obesity_mapping[i] for i in range(len(prediction_proba))],
        'Probability': prediction_proba
    }

    # Create a dataframe to display the results
    result_df = pd.DataFrame(data)

    # Transpose the dataframe to have obesity types as columns and add a row header
    result_df = result_df.T
    result_df.columns = result_df.iloc[0]
    result_df = result_df.drop(result_df.index[0])
    result_df.index = ['Probability']

    # Display the results in a table with proper formatting
    st.table(result_df.style.format("{:.4f}"))
