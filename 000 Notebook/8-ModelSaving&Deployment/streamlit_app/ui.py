# streamlit_app/ui.py
import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

# Import constants and utils from other modules within the package
from .labels import LABELS
from .config import FEATURE_NAMES, SHAP_AVAILABLE
from .styles import apply_custom_styles

# Conditionally import SHAP for plotting types
if SHAP_AVAILABLE:
    import shap
    import matplotlib.pyplot as plt

def setup_page():
    """Apply custom styles to the page."""
    st.markdown(apply_custom_styles(), unsafe_allow_html=True)
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        section[data-testid="stSidebar"] {display: none;}
        div[data-testid="stToolbar"] {display: none;}
        div[data-testid="stDecoration"] {display: none;}
        div[data-testid="stStatusWidget"] {display: none;}
        div.block-container {padding: 0 !important;}
        div[data-testid="stVerticalBlock"] > div {padding-top: 0 !important;}
        </style>
    """, unsafe_allow_html=True)
    

def select_language() -> str:
    """Creates language selector and returns the selected language code ('en' or 'ar')."""
    lang_options = {'English': 'en', 'Arabic': 'ar'}
    # Use English key for the label itself for consistency before selection
    selected_lang_display = st.sidebar.selectbox(
        LABELS['en']['Select Language'], # Use English key for the label
        options=list(lang_options.keys()),
        index=0 # Default to English
    )
    return lang_options[selected_lang_display]

# apply_rtl_styling function removed - CSS handled globally in App.py

def display_main_title(lang_code: str):
    """Displays the main application title."""
    st.markdown(f'<div class="title-box">{LABELS[lang_code]["Churn Prediction"]}</div>', unsafe_allow_html=True)

def build_sidebar(lang_code: str) -> bool:
    """Builds the sidebar with the input form.

    Args:
        lang_code: The selected language code.

    Returns:
        bool: True if the submit button was pressed, False otherwise.
    """
    st.sidebar.header(LABELS[lang_code]['Input Features'])
    st.sidebar.divider()

    # --- Input Form ---
    with st.sidebar.form(key='input_form'):
        st.subheader(LABELS[lang_code]['title']) # Customer Data subheader
        # Use st.session_state keys directly here
        st.number_input(
            LABELS[lang_code]['Age'], min_value=18, max_value=100, step=1,
            key='age', help=LABELS[lang_code]['Age Help']
        )
        st.selectbox(
            LABELS[lang_code]['Gender'], ['Male', 'Female'],
            key='gender', help=LABELS[lang_code]['Gender Help']
        )
        st.selectbox(
            LABELS[lang_code]['Geography'], ['France', 'Germany', 'Spain'],
            key='geography', help=LABELS[lang_code]['Geography Help']
        )

        st.sidebar.divider()
        st.subheader(LABELS[lang_code]['Account Details']) # Account Details subheader
        st.number_input(
            LABELS[lang_code]['Credit Score'], min_value=300, max_value=850, step=10,
            key='credit_score', help=LABELS[lang_code]['Credit Score Help']
        )
        st.number_input(
            LABELS[lang_code]['Balance'], min_value=0.0, step=1000.0, format="%.2f",
            key='balance', help=LABELS[lang_code]['Balance Help']
        )
        st.number_input(
            LABELS[lang_code]['Number of Products'], min_value=1, max_value=4, step=1,
            key='num_products', help=LABELS[lang_code]['Num Products Help']
        )
        st.selectbox(
            LABELS[lang_code]['Active Member'], options=[1, 0],
            format_func=lambda x: ('Yes' if x == 1 else 'No') if lang_code=='en' else ('نعم' if x == 1 else 'لا'),
            key='is_active_member', help=LABELS[lang_code]['Active Member Help']
        )

        st.sidebar.divider()
        # The submit button for the form
        submit_button_pressed = st.form_submit_button(label=LABELS[lang_code]['Submit'])

    return submit_button_pressed

def display_prediction_results(lang_code: str, prediction: int, probability: Optional[float]):
    """Displays the prediction outcome (churn/stay) and recommendation."""
    st.subheader(LABELS[lang_code]['Result'])
    prob_display = ""
    if probability is not None:
        # Format probability safely
        try:
            prob_display = f"({LABELS[lang_code]['Probability']}: {float(probability):.1%})"
        except (ValueError, TypeError):
             prob_display = "(Probability: N/A)" # Handle cases where prob might not be a number


    if prediction == 1: # Assuming 1 is churn
        st.warning(f"🚨 {LABELS[lang_code]['Churn Message']} {prob_display}")
        st.info(f"💡 {LABELS[lang_code]['Churn Recommendation']}")
    else:
        st.success(f"✅ {LABELS[lang_code]['Stay Message']} {prob_display}")
        st.info(f"💡 {LABELS[lang_code]['Stay Recommendation']}")

def display_shap_plot(lang_code: str, explainer: Any, shap_values: Any, input_df: pd.DataFrame):
    """Displays the SHAP explanation plot if possible.
    
    This function provides a clear visualization of how the model makes its prediction
    using SHAP (SHapley Additive exPlanations) values. The visualization shows:
    
    1. A waterfall plot that displays:
       - The starting point (average prediction across all customers)
       - How each feature contributes to the final prediction
       - The final prediction value
    
    2. Features are color-coded:
       - Red bars: Features that increase the chance of churn
       - Blue bars: Features that decrease the chance of churn
    
    3. The length of each bar represents the magnitude of the feature's impact
    
    This visualization helps users understand:
    - Which features are most important for this prediction
    - How each feature affects the prediction (positively or negatively)
    - The exact contribution of each feature to the final prediction
    
    The plot is designed to be intuitive and easy to interpret, with clear labels
    and a detailed explanation below the visualization.
    """
    if not SHAP_AVAILABLE:
        st.info(LABELS[lang_code]['Feature Importance Info'])
        return
    if explainer is None or shap_values is None:
        return

    st.subheader("How the Model Made This Prediction")
    try:
        import matplotlib.pyplot as plt
        
        # Calculate SHAP values for the current input
        shap_values = explainer.shap_values(input_df)
        
        # Create a single figure for the waterfall plot
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # For binary classification, shap_values is a list with two elements
        if isinstance(shap_values, list) and len(shap_values) == 2:
            # Get SHAP values for class 1 (churn)
            values = shap_values[1][0]  # First instance, class 1
            base_value = explainer.expected_value[1]
        else:
            values = shap_values[0]  # First instance
            base_value = explainer.expected_value
            
        # Create waterfall plot
        shap.waterfall_plot(
            shap.Explanation(
                values=values,
                base_values=base_value,
                data=input_df.iloc[0],
                feature_names=FEATURE_NAMES
            ),
            max_display=10,
            show=False
        )
        
        # Customize the plot
        plt.title("Feature Contributions to Prediction", fontsize=14, pad=20)
        plt.xlabel("SHAP Value (Impact on Prediction)", fontsize=12)
        plt.ylabel("Features", fontsize=12)
        plt.tight_layout()
        
        st.pyplot(fig)
        plt.close(fig)
        
        # Add clear explanation text
        st.markdown("""
        ### Understanding the Plot:
        
        - The plot shows how each feature contributes to the final prediction
        - **Starting Point (E[f(X)])**: The average prediction across all customers
        - **Red Bars**: Features that increase the chance of churn
        - **Blue Bars**: Features that decrease the chance of churn
        - **Bar Length**: Shows how much each feature affects the prediction
        - **Final Value (f(X))**: The model's prediction for this customer
        
        The most important features are shown at the top, with their exact contribution to the prediction.
        """)

    except Exception as e:
        st.error(f"{LABELS[lang_code]['SHAP Error']}: {e}")
        if 'fig' in locals() and plt.fignum_exists(fig.number):
            plt.close(fig)
