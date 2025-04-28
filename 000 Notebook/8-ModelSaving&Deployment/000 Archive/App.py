# 000 Notebook/8-ModelSaving&Deployment/App.py
import streamlit as st
import pandas as pd
import numpy as np
import time # For spinner
import traceback # For detailed error reporting

# Import from our streamlit_app package
# Ensure this runs correctly based on how streamlit executes the script
# If imports fail, Python path issues might need addressing (e.g., running from workspace root)
try:
    from streamlit_app.config import FEATURE_NAMES, MODEL_PATH
    from streamlit_app.labels import LABELS
    from streamlit_app.state import initialize_state
    from streamlit_app.models import load_model_and_explainer, preprocess_features
    from streamlit_app.ui import (
        select_language,
        display_main_title,
        build_sidebar,
        display_prediction_results,
        display_shap_plot,
    )
    from streamlit_app.styles import apply_custom_styles
except ImportError as e:
     st.error(f"Import Error: {e}. Please ensure the script is run from the workspace root directory ('GraduationProject/') and the 'streamlit_app' directory exists with an '__init__.py' file.")
     st.stop()


# --- Page Config (First Streamlit command) ---
st.set_page_config(
    page_title="Churn Prediction App", # Use a static title
    page_icon="🏦",
    layout="wide"
)

# Apply custom styles from styles.py
st.markdown(apply_custom_styles(), unsafe_allow_html=True)

def run_app():
    """Runs the main application flow."""

    initialize_state() # Initialize session state first

    lang_code = select_language() # Get language from sidebar

    # Load model and explainer (cached)
    components = load_model_and_explainer()
    if components.model is None:
        # Error message is handled within load_model_and_explainer
        st.stop() # Stop execution if model loading failed

    # Apply RTL class conditionally (must happen before content)
    # This adds a CSS class to a wrapper div for RTL styling
    rtl_div_open = '<div class="rtl">' if lang_code == 'ar' else ''
    rtl_div_close = '</div>' if lang_code == 'ar' else ''
    st.markdown(rtl_div_open, unsafe_allow_html=True)

    # --- Main Page Content ---
    display_main_title(lang_code)

    submit_button_pressed = build_sidebar(lang_code)

    # --- Prediction Logic ---
    if submit_button_pressed:
        # Get current values from session state
        try:
            current_age = st.session_state.age
            current_gender = st.session_state.gender
            current_geography = st.session_state.geography
            current_credit_score = st.session_state.credit_score
            current_balance = st.session_state.balance
            current_num_products = st.session_state.num_products
            current_is_active_member = st.session_state.is_active_member
        except KeyError as e:
             st.error(f"Session state error: Missing key {e}. Please refresh the page.")
             st.stop()

        with st.spinner(LABELS[lang_code]['Predicting']):
            time.sleep(0.2) # Keep short simulation

            st.divider()
            st.header(LABELS[lang_code]['Prediction'])

            # --- Feature Preparation ---
            try:
                # Prepare categorical features
                gender_label = 1 if current_gender == 'Male' else 0
                geo_fr = 1 if current_geography == 'France' else 0
                geo_de = 1 if current_geography == 'Germany' else 0
                geo_es = 1 if current_geography == 'Spain' else 0

                # Prepare numerical features
                age_num = pd.to_numeric(current_age, errors='coerce')
                if pd.isna(age_num):
                    st.error(f"Invalid Age input: '{current_age}'. Please enter a number.")
                    st.stop()

                # Create initial DataFrame with raw features
                features = {
                    'creditscore': float(current_credit_score),
                    'numofproducts': float(current_num_products),
                    'balance': float(current_balance),
                    'genderlabel': float(gender_label),
                    'age': float(age_num),  # Store raw age first
                    'isactivemember': float(current_is_active_member),
                    'geographyfrance': float(geo_fr),
                    'geographygermany': float(geo_de),
                    'geographyspain': float(geo_es)
                }
                
                # Create DataFrame
                input_df = pd.DataFrame([features])
                
                # Apply age transformation (sqrt) to create ageskewed
                input_df['ageskewed'] = np.sqrt(input_df['age'])
                # Drop the original age column as it's not used in prediction
                input_df = input_df.drop('age', axis=1)
                
                # Ensure column order matches FEATURE_NAMES
                input_df = input_df[FEATURE_NAMES]

                # Apply scaling to the features
                input_df = preprocess_features(input_df, components.scaler)

            except Exception as e:
                 st.error(f"Error preparing features: {e}")
                 st.error(traceback.format_exc())
                 st.stop()


            # --- Prediction and SHAP Calculation ---
            try:
                prediction = None
                probability = None
                shap_values_calculated = None

                # Predict probability if possible
                if hasattr(components.model, 'predict_proba'):
                    probs = components.model.predict_proba(input_df)[0]
                    if len(probs) > 1 : # Check if multi-class probabilities returned
                        prediction = np.argmax(probs) # Class with highest probability
                        probability = probs[1] # Probability of class 1 (assuming churn)
                    else: # Handle binary model returning only prob of class 1
                         probability = probs[0]
                         prediction = 1 if probability >= 0.5 else 0 # Thresholding
                         st.info("Model provided single probability; assuming binary classification.")

                else: # Fallback to predict
                    st.info(LABELS[lang_code]['Proba Error'])
                    prediction = components.model.predict(input_df)[0]
                    probability = None # Cannot determine probability

                # Calculate SHAP values if possible
                if components.explainer is not None:
                    try:
                        # SHAP calculation can fail if input data has unexpected format/values
                        shap_values_calculated = components.explainer(input_df)
                    except Exception as e:
                         st.warning(f"{LABELS[lang_code]['SHAP Error']} (Calculation): {e}")
                         # Optionally log traceback.format_exc() for debugging

                # --- Display Results ---
                if prediction is not None:
                    display_prediction_results(lang_code, prediction, probability)
                    st.divider()
                    # Display SHAP plot using the calculated values
                    display_shap_plot(lang_code, components.explainer, shap_values_calculated, input_df)
                else:
                     st.error("Prediction could not be made (Result was None).")


            except Exception as e:
                st.error(f"{LABELS[lang_code]['Prediction Error']}: {e}")
                st.error(traceback.format_exc()) # Show detailed traceback for debugging


    # Close the RTL div if it was opened
    st.markdown(rtl_div_close, unsafe_allow_html=True)


if __name__ == "__main__":
    run_app()