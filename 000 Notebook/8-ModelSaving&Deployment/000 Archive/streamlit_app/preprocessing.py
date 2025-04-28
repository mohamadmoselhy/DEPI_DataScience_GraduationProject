import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
from .config import SCALER_PATH, FEATURE_NAMES

def load_scaler():
    """Load the pre-trained scaler."""
    try:
        return joblib.load(SCALER_PATH)
    except Exception as e:
        print(f"Error loading scaler: {e}")
        return StandardScaler()

def preprocess_features(features_df: pd.DataFrame) -> np.ndarray:
    """
    Preprocess the features using the pre-trained scaler.
    
    Args:
        features_df (pd.DataFrame): DataFrame containing the features
        
    Returns:
        np.ndarray: Scaled features
    """
    # Ensure features are in the correct order
    features_df = features_df[FEATURE_NAMES]
    
    # Load the scaler
    scaler = load_scaler()
    
    # Scale the features
    scaled_features = scaler.transform(features_df)
    
    return scaled_features

def prepare_features(
    credit_score: float,
    num_products: int,
    balance: float,
    gender: str,
    age: float,
    is_active: bool,
    geography: str
) -> pd.DataFrame:
    """
    Prepare features for prediction.
    
    Args:
        credit_score (float): Customer's credit score
        num_products (int): Number of products
        balance (float): Account balance
        gender (str): Customer's gender
        age (float): Customer's age
        is_active (bool): Whether customer is active
        geography (str): Customer's geography
        
    Returns:
        pd.DataFrame: Prepared features ready for scaling
    """
    # Create gender label (1 for Male, 0 for Female)
    gender_label = 1 if gender.lower() == 'male' else 0
    
    # Create geography one-hot encoding
    geography_france = 1 if geography.lower() == 'france' else 0
    geography_germany = 1 if geography.lower() == 'germany' else 0
    geography_spain = 1 if geography.lower() == 'spain' else 0
    
    # Transform age (square root transformation)
    age_skewed = np.sqrt(age)
    
    # Create features dictionary
    features = {
        'creditscore': credit_score,
        'numofproducts': num_products,
        'balance': balance,
        'genderlabel': gender_label,
        'ageskewed': age_skewed,
        'isactivemember': int(is_active),
        'geographyfrance': geography_france,
        'geographygermany': geography_germany,
        'geographyspain': geography_spain
    }
    
    # Convert to DataFrame
    features_df = pd.DataFrame([features])
    
    return features_df 