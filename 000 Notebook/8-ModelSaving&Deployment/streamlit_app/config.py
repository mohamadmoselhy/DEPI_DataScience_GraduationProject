# streamlit_app/config.py
import streamlit as st
import os

# --- Configuration ---
MODEL_PATH = os.path.join('streamlit_app', 'Model', 'model.joblib')  # Path relative to workspace root

FEATURE_NAMES: list[str] = [
    'creditscore', 'numofproducts', 'balance', 'genderlabel', 'ageskewed',
    'isactivemember', 'geographyfrance', 'geographygermany', 'geographyspain'
]

# Attempt to import SHAP and check availability
try:
    import shap
    import matplotlib.pyplot as plt
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    # You might want to display a warning in the UI instead of here
    # if SHAP is critical. Handled in ui.py for now.
