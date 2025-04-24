# streamlit_app/state.py
import streamlit as st

def initialize_state():
    """Initializes session state for input fields if they don't exist."""
    # Define default values for the input fields
    default_values = {
        'age': 35,
        'gender': 'Male',
        'geography': 'France',
        'credit_score': 650,
        'balance': 50000.0,
        'num_products': 1,
        'is_active_member': 1,
        'selected_preset': 'Preset Custom' # Default to no preset selected
    }
    # Check if 'init' flag exists, if not, initialize state
    if 'init' not in st.session_state:
        for key, value in default_values.items():
            if key not in st.session_state:
                st.session_state[key] = value
        # Also initialize the preset selector state if it's missing
        if 'preset_selector' not in st.session_state:
             st.session_state['preset_selector'] = default_values['selected_preset']
        st.session_state['init'] = True # Mark state as initialized
