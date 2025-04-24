# streamlit_app/models.py
import streamlit as st
import joblib
from typing import Any, Optional, Tuple
import numpy as np # Needed here potentially for SHAP handling

# Import SHAP conditionally from config
from .config import SHAP_AVAILABLE, MODEL_PATH
if SHAP_AVAILABLE:
    import shap

# --- Model and SHAP Explainer Loading ---
@st.cache_resource
def load_model_and_explainer() -> Tuple[Optional[Any], Optional[Any]]:
    """
    Loads model from MODEL_PATH and creates SHAP explainer if available.

    Returns:
        Tuple[Optional[Any], Optional[Any]]: (model, explainer) or (None, None) on error.
    """
    try:
        model = joblib.load(MODEL_PATH)
        explainer = None
        if SHAP_AVAILABLE and model:
            try:
                # Use TreeExplainer for better compatibility with tree-based models
                explainer = shap.TreeExplainer(model)
            except Exception as shap_error:
                 # Use st.warning for non-critical errors during loading
                 st.warning(f"Could not create SHAP explainer (Model type might be unsupported): {shap_error}")
        return model, explainer
    except FileNotFoundError:
        # Use st.error for critical errors that prevent the app from running
        st.error(f"CRITICAL: Model file not found at {MODEL_PATH}")
        return None, None
    except Exception as e:
        st.error(f"CRITICAL: Error loading model from {MODEL_PATH}: {e}")
        return None, None