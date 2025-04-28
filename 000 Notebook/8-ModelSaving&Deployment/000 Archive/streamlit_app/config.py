# streamlit_app/config.py
import streamlit as st
import os
from pathlib import Path

# --- Configuration ---
# Get the directory containing this file
CURRENT_DIR = Path(__file__).parent

# Model and scaler paths (relative to this file)
MODEL_PATH = CURRENT_DIR / "Model" / "model.joblib"
SCALER_PATH = CURRENT_DIR / "Model" / "scaler.joblib"

FEATURE_NAMES = [
    'creditscore',
    'numofproducts',
    'balance',
    'genderlabel',
    'ageskewed',  # Using transformed age
    'isactivemember',
    'geographyfrance',
    'geographygermany',
    'geographyspain'
]

# Features that need scaling
FEATURES_TO_SCALE = FEATURE_NAMES  # All features should be scaled

# Attempt to import SHAP and check availability
try:
    import shap
    import matplotlib.pyplot as plt
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    # You might want to display a warning in the UI instead of here
    # if SHAP is critical. Handled in ui.py for now.
