import streamlit as st
import requests
import json

# --- Configuration ---
# NOTE: Ensure your FastAPI/Backend server is running on this address
API_URL = "http://fastapi-service:8000/predict"

# Set Streamlit page configuration
st.set_page_config(
    page_title="Heart Disease Predictor (Streamlit)",
    layout="centered",
    initial_sidebar_state="expanded",
)


def display_result(prediction, probability):
    """Displays the prediction result in a formatted box."""
    st.subheader("Prediction Result")

    # Define colors and icons based on prediction
    if prediction == 1:
        color = "red"
        icon = "💔"
        result_text = "POSITIVE for Heart Disease"
        st.error(f"## {icon} {result_text}")
    else:
        color = "green"
        icon = "❤️"
        result_text = "NEGATIVE for Heart Disease"
        st.success(f"## {icon} {result_text}")

    # FIX: Removed the backticks (`) around the <span> tag to allow HTML rendering.
    st.markdown(f"**Probability:** <span style='color:{color}; font-weight: bold;'>{(probability * 100):.2f}%</span>",
                unsafe_allow_html=True)
    st.markdown("---")
    st.info("Disclaimer: This tool provides a risk assessment and is not a substitute for professional medical advice.")


def main():
    """Main Streamlit application function."""

    st.title("Heart Disease Risk Predictor")
    st.markdown(
        "Input patient clinical parameters below to predict the probability of heart disease.")

    # --- Input Form ---
    with st.form("prediction_form"):
        st.markdown("### Patient Clinical Data")

        # Create two columns for a clean layout
        col1, col2 = st.columns(2)

        # Row 1: Age and Sex
        with col1:
            age = st.number_input(
                "Age (Years)",
                min_value=1, max_value=119, value=52, step=1,
                help="Range: 1 to 119 years."
            )
        with col2:
            sex = st.selectbox(
                "Sex",
                options=[(1, "1 - Male"), (0, "0 - Female")],
                format_func=lambda x: x[1],
                help="1 = Male, 0 = Female."
            )[0]

        # Row 2: Trestbps and Chol
        with col1:
            trestbps = st.number_input(
                "Resting Blood Pressure (trestbps)",
                min_value=50, max_value=250, value=125, step=1,
                help="Range: 50 to 250 mm Hg."
            )
        with col2:
            chol = st.number_input(
                "Serum Cholesterol (chol)",
                min_value=100, max_value=700, value=212, step=1,
                help="Range: 100 to 700 mg/dl."
            )

        # Row 3: Cp and Fbs
        with col1:
            cp_options = {
                0: "0 - Typical Angina", 1: "1 - Atypical Angina",
                2: "2 - Non-Anginal Pain", 3: "3 - Asymptomatic"
            }
            cp_selection = st.selectbox(
                "Chest Pain Type (cp)",
                options=list(cp_options.keys()),
                format_func=lambda x: cp_options[x]
            )
        with col2:
            fbs = st.selectbox(
                "Fasting Blood Sugar > 120 mg/dL? (fbs)",
                options=[(1, "1 - True"), (0, "0 - False")],
                format_func=lambda x: x[1],
                help="1 = True, 0 = False."
            )[0]

        # Row 4: Restecg and Thalach
        with col1:
            restecg_options = {
                0: "0 - Normal", 1: "1 - ST-T Wave Abnormality", 2: "2 - Left Ventricular Hypertrophy"
            }
            restecg_selection = st.selectbox(
                "Resting ECG Results (restecg)",
                options=list(restecg_options.keys()),
                format_func=lambda x: restecg_options[x]
            )
        with col2:
            thalach = st.number_input(
                "Maximum Heart Rate Achieved (thalach)",
                min_value=40, max_value=250, value=168, step=1,
                help="Range: 40 to 250 bpm."
            )

        # Row 5: Exang and Oldpeak
        with col1:
            exang = st.selectbox(
                "Exercise Induced Angina? (exang)",
                options=[(1, "1 - Yes"), (0, "0 - No")],
                format_func=lambda x: x[1],
                help="1 = Yes, 0 = No."
            )[0]
        with col2:
            oldpeak = st.number_input(
                "ST Depression (oldpeak)",
                min_value=0.0, max_value=10.0, value=1.0, step=0.1,
                format="%.1f",
                help="ST depression induced by exercise relative to rest. Range: 0.0 to 10.0."
            )

        # Row 6: Slope and Ca
        with col1:
            slope_options = {
                0: "0 - Upsloping", 1: "1 - Flat", 2: "2 - Downsloping"
            }
            slope_selection = st.selectbox(
                "Peak Exercise ST Segment Slope (slope)",
                options=list(slope_options.keys()),
                format_func=lambda x: slope_options[x]
            )
        with col2:
            ca_options = {
                0: "0 Vessels", 1: "1 Vessel", 2: "2 Vessels", 3: "3 Vessels"
            }
            ca_selection = st.selectbox(
                "Number of Major Vessels (ca)",
                options=list(ca_options.keys()),
                format_func=lambda x: ca_options[x],
                help="Number of major vessels (0–3) colored by fluoroscopy."
            )

        # Row 7: Thal
        thal_options = {
            1: "1 - Normal", 2: "2 - Fixed Defect", 3: "3 - Reversible Defect"
        }
        thal_selection = st.selectbox(
            "Thalassemia Type (thal)",
            options=list(thal_options.keys()),
            format_func=lambda x: thal_options[x]
        )

        # Submit button
        submitted = st.form_submit_button(
            "Predict Heart Disease Risk", type="primary")

    if submitted:
        # Construct the payload dictionary
        payload = {
            "age": age,
            "sex": sex,
            "cp": cp_selection,
            "trestbps": trestbps,
            "chol": chol,
            "fbs": fbs,
            "restecg": restecg_selection,
            "thalach": thalach,
            "exang": exang,
            "oldpeak": oldpeak,
            "slope": slope_selection,
            "ca": ca_selection,
            "thal": thal_selection
        }

        with st.spinner('Sending request to model and predicting...'):
            try:
                # Send POST request to the FastAPI endpoint
                response = requests.post(API_URL, json=payload, timeout=10)

                # Check for successful response status
                if response.status_code == 200:
                    data = response.json()

                    prediction = data.get("prediction")
                    probability = data.get("probability_of_heart_disease")

                    if prediction is not None and probability is not None:
                        display_result(prediction, probability)
                    else:
                        st.error(
                            "Prediction result format is incorrect. Check backend response structure.")
                        st.json(data)  # Show raw response for debugging

                elif response.status_code == 422:
                    # Handle validation errors from Pydantic in FastAPI
                    error_data = response.json()
                    detail = error_data.get(
                        "detail", "Unknown validation error")
                    st.error(
                        f"Input Validation Error (Status 422): Please check your inputs against the constraints.")
                    st.json(detail)
                else:
                    st.error(
                        f"Prediction failed with HTTP status code: {response.status_code}")
                    st.text(response.text)

            except requests.exceptions.Timeout:
                st.error(
                    "The request timed out. The backend server might be too slow or not responding.")
            except requests.exceptions.ConnectionError:
                st.error(
                    f"Could not connect to the API at {API_URL}. Please ensure your FastAPI backend is running.")
            except json.JSONDecodeError:
                st.error(
                    "Received a non-JSON response from the server. Check backend logs.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
