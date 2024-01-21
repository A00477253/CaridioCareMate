import streamlit as st
import json
import openai

openai.api_key = st.secrets["openai_api_key"]


def generate_advice(result):
    # Construct a prompt based on the user's input data
    prompt = f"Provide health benefits and preventive measures based on the following health data: {json.dumps(result)}"

    # Make an API call to OpenAI's completion endpoint using the new interface
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or another model name if you prefer
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content']

def show_prediction_page():
    st.title('Prediction Form')
    with st.form("prediction_form"):
        # Creating two columns for inputs
        col1, col2 = st.columns(2)

        # Column 1
        with col1:
            age = st.number_input('Age', min_value=0, max_value=120, value=30)
            height = st.number_input('Height (in cm)', min_value=0, value=170)
            weight = st.number_input('Weight (in kg)', min_value=0, value=70)
            systolic_pressure = st.number_input('Systolic Pressure (mmHg)', min_value=80, value=120)
            diastolic_pressure = st.number_input('Diastolic Pressure (mmHg)', min_value=60, value=80)

        # Column 2
        with col2:
            gender = st.radio("Gender", ('Male', 'Female'))
            gender_value = 1 if gender == 'Male' else 0

            cholesterol_options = {
                "Less than 200 mg/dL (Normal)": 0,
                "200 to 239 mg/dL (Borderline high)": 1,
                "240 mg/dL or greater (High)": 2,
            }
            cholesterol = st.selectbox(
                'Cholesterol Level',
                list(cholesterol_options.keys())
            )
            cholesterol_value = cholesterol_options[cholesterol]

            glucose_options = {
                "Below 5.7% (Normal)": 0,
                "5.7 – 6.4% (Prediabetes)": 1,
                "6.5% or above (Diabetes)": 2,
            }
            glucose = st.selectbox(
                'Blood Glucose Level (A1C Test)',
                list(glucose_options.keys())
            )
            glucose_value = glucose_options[glucose]

        smoke = st.radio("Do you smoke?", ('No', 'Yes'))
        smoke_value = 1 if smoke == 'Yes' else 0

        alcohol = st.radio("Do you consume alcohol?", ('No', 'Yes'))
        alcohol_value = 1 if alcohol == 'Yes' else 0

        active = st.radio("Are you physically active?", ('No', 'Yes'))
        active_value = 1 if active == 'Yes' else 0

        # Submit button in the main column
        submit_button = st.form_submit_button('Show')

        if submit_button:
            # Construct the result JSON
            result = {
                "age": age,
                "gender": gender_value,
                "height": height,
                "weight": weight,
                "ap_hi": systolic_pressure,
                "ap_lo": diastolic_pressure,
                "cholesterol": cholesterol_value,
                "gluc": glucose_value,
                "smoke": smoke_value,
                "alco": alcohol_value,
                "active": active_value,
                "cardiac_risk":"87%"
            }

            # Convert the dictionary to a JSON string for display
            result_json = json.dumps(result)
            st.json(result_json)  # Display the JSON in the Streamlit app
            advice = generate_advice(result)
            st.write("Health Benefits and Preventive Measures:")
            st.write(advice)

# Only run the app if this file is executed as a script (not imported)
if __name__ == '__main__':
    show_prediction_page()
