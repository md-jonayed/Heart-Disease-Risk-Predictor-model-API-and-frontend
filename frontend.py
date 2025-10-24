import streamlit as st
import requests
import json
import numpy as np

# --- Configuration ---
# NOTE: Ensure your FastAPI/Backend server is running on this address
API_URL = "http://fastapi-service:8000/predict"

# Set Streamlit page configuration
st.set_page_config(
    page_title="Heart Disease Predictor (Streamlit)",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Helper function to get the display string (the second element of the tuple)


def get_display_string(option):
    """Returns the display string (second element) from an option tuple (key, display_string)."""
    # Ensure it handles the case where the input might not be a tuple (though rare in selectbox)
    if isinstance(option, tuple) and len(option) > 1:
        return option[1]
    return str(option)


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

    # Display probability for class 1 (Heart Disease)
    st.markdown(f"**Probability of Heart Disease (Class=1):** <span style='color:{color}; font-weight: bold;'>{(probability * 100):.2f}%</span>",
                unsafe_allow_html=True)

    # Calculate and display probability for class 0
    prob0 = 1.0 - probability
    prob0_color = "green" if prediction == 0 else "red"
    st.markdown(f"**Probability of No Disease (Class=0):** <span style='color:{prob0_color}; font-weight: bold;'>{(prob0 * 100):.2f}%</span>",
                unsafe_allow_html=True)

    # Add a confidence display based on the maximum probability
    confidence = max(probability, prob0)
    st.markdown(f"**Model Confidence:** {(confidence * 100):.2f}%")

    st.markdown("---")
    st.info("Disclaimer: This tool provides a risk assessment and is not a substitute for professional medical advice.")


def main():
    """Main Streamlit application function."""

    st.title("Heart Disease Risk Predictor")
    st.markdown(
        "Input patient clinical parameters below to predict the probability of heart disease.")

    # Define all options upfront for clarity and consistency
    CP_OPTIONS = {
        0: "0 - Typical Angina", 1: "1 - Atypical Angina",
        2: "2 - Non-Anginal Pain", 3: "3 - Asymptomatic"
    }
    RESTECG_OPTIONS = {
        0: "0 - Normal", 1: "1 - ST-T Wave Abnormality", 2: "2 - Left Ventricular Hypertrophy"
    }
    SLOPE_OPTIONS = {
        0: "0 - Upsloping", 1: "1 - Flat", 2: "2 - Downsloping"
    }
    CA_OPTIONS = {
        0: "0 Vessels", 1: "1 Vessel", 2: "2 Vessels", 3: "3 Vessels"
    }
    THAL_OPTIONS = {
        1: "1 - Normal", 2: "2 - Fixed Defect", 3: "3 - Reversible Defect"
    }

    # Convert dictionary options to a list of (key, value) tuples for Streamlit selectbox
    cp_options_list = list(CP_OPTIONS.items())
    restecg_options_list = list(RESTECG_OPTIONS.items())
    slope_options_list = list(SLOPE_OPTIONS.items())
    ca_options_list = list(CA_OPTIONS.items())
    thal_options_list = list(THAL_OPTIONS.items())

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
            sex_selection = st.selectbox(
                "Sex",
                options=[(1, "1 - Male"), (0, "0 - Female")],
                format_func=get_display_string,
                help="1 = Male, 0 = Female."
            )
            sex = sex_selection[0]  # Extract the key (0 or 1)

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
            cp_selection_tuple = st.selectbox(
                "Chest Pain Type (cp)",
                options=cp_options_list,
                format_func=get_display_string
            )
            # Extract the key (0, 1, 2, or 3)
            cp_selection = cp_selection_tuple[0]

        with col2:
            fbs_selection = st.selectbox(
                "Fasting Blood Sugar > 120 mg/dL? (fbs)",
                options=[(1, "1 - True"), (0, "0 - False")],
                format_func=get_display_string,
                help="1 = True, 0 = False."
            )
            fbs = fbs_selection[0]  # Extract the key (0 or 1)

        # Row 4: Restecg and Thalach
        with col1:
            restecg_selection_tuple = st.selectbox(
                "Resting ECG Results (restecg)",
                options=restecg_options_list,
                format_func=get_display_string
            )
            # Extract the key (0, 1, or 2)
            restecg_selection = restecg_selection_tuple[0]

        with col2:
            thalach = st.number_input(
                "Maximum Heart Rate Achieved (thalach)",
                min_value=40, max_value=250, value=168, step=1,
                help="Range: 40 to 250 bpm."
            )

        # Row 5: Exang and Oldpeak
        with col1:
            exang_selection = st.selectbox(
                "Exercise Induced Angina? (exang)",
                options=[(1, "1 - Yes"), (0, "0 - No")],
                format_func=get_display_string,
                help="1 = Yes, 0 = No."
            )
            exang = exang_selection[0]  # Extract the key (0 or 1)
        with col2:
            oldpeak = st.number_input(
                "ST Depression (oldpeak)",
                min_value=0.0, max_value=10.0, value=1.0, step=0.1,
                format="%.1f",
                help="ST depression induced by exercise relative to rest. Range: 0.0 to 10.0."
            )

        # Row 6: Slope and Ca
        with col1:
            slope_selection_tuple = st.selectbox(
                "Peak Exercise ST Segment Slope (slope)",
                options=slope_options_list,
                format_func=get_display_string
            )
            # Extract the key (0, 1, or 2)
            slope_selection = slope_selection_tuple[0]

        with col2:
            ca_selection_tuple = st.selectbox(
                "Number of Major Vessels (ca)",
                options=ca_options_list,
                format_func=get_display_string,
                help="Number of major vessels (0–3) colored by fluoroscopy."
            )
            # Extract the key (0, 1, 2, or 3)
            ca_selection = ca_selection_tuple[0]

        # Row 7: Thal
        thal_selection_tuple = st.selectbox(
            "Thalassemia Type (thal)",
            options=thal_options_list,
            format_func=get_display_string,
            help="A blood disorder."
        )
        # Extract the key (1, 2, or 3)
        thal_selection = thal_selection_tuple[0]

        # Submit button (REQUIRED)
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

                    # --- FIX: Robust extraction of prediction and probability ---
                    prediction = None
                    probability = None

                    # 1. Try to extract prediction (integer 0 or 1)
                    if isinstance(data.get("prediction"), (int, float)):
                        prediction = int(round(data["prediction"]))
                    elif isinstance(data.get("predicted_category"), str):
                        # Handle string categories like "Positive" or "Negative"
                        category = data["predicted_category"].lower()
                        if category.startswith("pos"):
                            prediction = 1
                        elif category.startswith("neg"):
                            prediction = 0

                    # 2. Try to extract probability (for class 1)
                    if isinstance(data.get("probability_of_heart_disease"), (int, float)):
                        probability = float(
                            data["probability_of_heart_disease"])
                    elif isinstance(data.get("probability"), (int, float)):
                        # Common fallback key
                        probability = float(data["probability"])
                    elif isinstance(data.get("class_probabilities"), dict):
                        # Check for dictionary of probabilities {'0': 0.X, '1': 0.Y}
                        prob_dict = data["class_probabilities"]
                        if '1' in prob_dict:
                            probability = float(prob_dict['1'])
                        elif 1 in prob_dict:
                            probability = float(prob_dict[1])

                    # 3. Final check and display
                    if prediction is not None and probability is not None:
                        # Ensure probability is a float between 0 and 1
                        probability = np.clip(probability, 0.0, 1.0)
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
