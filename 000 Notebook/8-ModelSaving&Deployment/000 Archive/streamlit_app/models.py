# streamlit_app/models.py
import streamlit as st
import joblib
from typing import Any, Optional, Tuple, NamedTuple
import numpy as np # Needed here potentially for SHAP handling
import pandas as pd

# Import SHAP conditionally from config
from .config import SHAP_AVAILABLE, MODEL_PATH, SCALER_PATH, FEATURES_TO_SCALE
if SHAP_AVAILABLE:
    import shap

class ModelComponents(NamedTuple):
    model: Optional[Any]
    explainer: Optional[Any]
    scaler: Optional[Any]

# --- Model and SHAP Explainer Loading ---
@st.cache_resource
def load_model_and_explainer() -> ModelComponents:
    """
    Loads model, scaler from respective paths and creates SHAP explainer if available.

    Returns:
        ModelComponents: Named tuple containing (model, explainer, scaler) or (None, None, None) on error.
    """
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        
        explainer = None
        if SHAP_AVAILABLE and model:
            try:
                # Use TreeExplainer for better compatibility with tree-based models
                explainer = shap.TreeExplainer(model)
            except Exception as shap_error:
                 # Use st.warning for non-critical errors during loading
                 st.warning(f"Could not create SHAP explainer (Model type might be unsupported): {shap_error}")
        
        return ModelComponents(model, explainer, scaler)
    
    except FileNotFoundError as e:
        # Use st.error for critical errors that prevent the app from running
        if "model.joblib" in str(e):
            st.error(f"CRITICAL: Model file not found at {MODEL_PATH}")
        elif "scaler.joblib" in str(e):
            st.error(f"CRITICAL: Scaler file not found at {SCALER_PATH}")
        return ModelComponents(None, None, None)
    except Exception as e:
        st.error(f"CRITICAL: Error loading model components: {e}")
        return ModelComponents(None, None, None)

def preprocess_features(df: pd.DataFrame, scaler: Any) -> pd.DataFrame:
    """
    Preprocesses the input features using the provided scaler.
    
    Args:
        df: Input DataFrame with features
        scaler: The fitted scaler object
    
    Returns:
        pd.DataFrame: Preprocessed features
    """
    if scaler is None:
        return df
        
    # Create a copy to avoid modifying the original
    df_processed = df.copy()
    
    try:
        # Apply scaling to all features since the scaler was trained on all of them
        scaled_features = scaler.transform(df_processed)
        # Convert back to DataFrame with original column names
        df_processed = pd.DataFrame(scaled_features, columns=df_processed.columns)
        return df_processed
    except Exception as e:
        st.error(f"Error during feature scaling: {e}")
        return df  # Return original data if scaling fails