from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score
import joblib
import numpy as np
from datetime import datetime
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier

def calculate_regression_metrics(y_test, y_predict):
    """
    Calculates regression metrics for model evaluation: Mean Squared Error (MSE), 
    Mean Absolute Error (MAE), and R² Score.

    This function computes three common metrics to evaluate the performance of a regression model:
    1. Mean Squared Error (MSE)
    2. Mean Absolute Error (MAE)
    3. R² Score (Coefficient of Determination)
    
    Parameters:
    - y_test (array-like): The true values (ground truth) of the target variable.
    - y_predict (array-like): The predicted values generated by the regression model.

    Returns:
    - mse (float): The Mean Squared Error between the true and predicted values.
    - mae (float): The Mean Absolute Error between the true and predicted values.
    - r2 (float): The R² Score, representing the goodness of fit of the model.

    """
    mse = mean_squared_error(y_test, y_predict)
    mae = mean_absolute_error(y_test, y_predict)
    r2 = r2_score(y_test, y_predict)
    
    return mse, mae, r2

def prepare_and_train_linear_regression_model(x, y, test_size=0.3, shuffle=True, random_state=0):
    """
    Splits the dataset into training and testing sets, scales the features using 
    StandardScaler, and trains a Linear Regression model on the scaled training data.

    This function:
    1. Splits the dataset (features and target) into training and testing sets.
    2. Scales the feature data using StandardScaler to normalize the input.
    3. Trains a Linear Regression model on the scaled training data.

    Parameters:
    - x (array-like): The feature data (independent variables).
    - y (array-like): The target data (dependent variable).
    - test_size (float, optional): Proportion of the dataset to include in the test split (default is 0.3).
    - shuffle (bool, optional): Whether to shuffle the data before splitting (default is True).
    - random_state (int, optional): The seed used by the random number generator for reproducibility (default is 0).

    Returns:
    - MyScaler (StandardScaler): The scaler used to normalize the features.
    - LinearRegMod (LinearRegression): The trained Linear Regression model.
    - x_train (array-like): The feature data for the training set.
    - x_test (array-like): The feature data for the test set.
    - y_train (array-like): The target data for the training set.
    - y_test (array-like): The target data for the test set.
    """
    # Split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, shuffle=shuffle, random_state=random_state)
    
    # Initialize the StandardScaler
    MyScaler = StandardScaler()
    
    # Fit and transform the training data, then transform the test data
    x_Scaled_train = MyScaler.fit_transform(x_train)
    x_Scaled_test = MyScaler.transform(x_test)
    
    # Initialize and fit the Linear Regression model
    LinearRegMod = LinearRegression()
    LinearRegMod.fit(x_Scaled_train, y_train)
    
    # Return scaler, model, and data splits
    return MyScaler, LinearRegMod, x_train, x_test, y_train, y_test

def prepare_and_train_svc_model(X, y, test_size=0.3, shuffle=True, random_state=42, kernel='rbf', C=1.0, gamma='scale'):
    """
    Splits the dataset, scales features, and trains an SVM classifier using the SVC model.

    Parameters:
    - X (array-like): Feature data (independent variables).
    - y (array-like): Target data (dependent variable).
    - test_size (float): Proportion of the dataset to include in the test split.
    - shuffle (bool): Whether to shuffle the data before splitting.
    - random_state (int): Random seed for reproducibility.
    - kernel (str): Specifies the kernel type to be used in the algorithm ('linear', 'rbf', 'poly', etc.).
    - C (float): Regularization parameter.
    - gamma (str or float): Kernel coefficient for 'rbf', 'poly', and 'sigmoid'.

    Returns:
    - scaler (StandardScaler): The fitted scaler used for feature normalization.
    - model (SVC): The trained SVM classifier.
    - X_train, X_test, y_train, y_test: The respective training and test sets.
    - accuracy (float): Accuracy score of the model on the test set.
    """
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, shuffle=shuffle, random_state=random_state
    )

    # Normalize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Initialize and train the SVC model
    model = SVC(kernel=kernel, C=C, gamma=gamma, random_state=random_state)
    model.fit(X_train_scaled, y_train)

    # Calculate accuracy
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    return scaler, model, X_train, X_test, y_train, y_test, accuracy

def prepare_and_train_rf_model(X, y, test_size=0.3, shuffle=True, random_state=42, n_estimators=100, class_weight='balanced'):
    """
    Splits the dataset, scales features, and trains a Random Forest classifier.

    Parameters:
    - X (array-like): Feature data (independent variables).
    - y (array-like): Target data (dependent variable).
    - test_size (float): Proportion of the dataset to include in the test split.
    - shuffle (bool): Whether to shuffle the data before splitting.
    - random_state (int): Random seed for reproducibility.
    - n_estimators (int): The number of trees in the forest.
    - class_weight (str or dict): The class weights to handle imbalanced data.

    Returns:
    - MyScaler (StandardScaler): The fitted scaler used for feature normalization.
    - model (RandomForestClassifier): The trained Random Forest classifier.
    - X_train, X_test, y_train, y_test: The respective training and test sets.
    - accuracy (float): Accuracy score of the model on the test set.
    """
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, shuffle=shuffle, random_state=random_state
    )

    # Normalize the features
    MyScaler = StandardScaler()
    X_train_scaled = MyScaler.fit_transform(X_train)
    X_test_scaled = MyScaler.transform(X_test)

    # Initialize and train the Random Forest model
    model = RandomForestClassifier(n_estimators=n_estimators, class_weight=class_weight, random_state=random_state)
    model.fit(X_train_scaled, y_train)

    # Calculate accuracy
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    return MyScaler, model, X_train, X_test, y_train, y_test, accuracy

def prepare_and_train_log_reg_model(X, y, test_size=0.3, shuffle=True, random_state=42, C=0.1, max_iter=10000):
    """
    Splits the dataset into training and testing sets, scales the features using 
    StandardScaler, and trains a Logistic Regression model on the scaled training data.

    This function:
    1. Splits the dataset (features and target) into training and testing sets.
    2. Scales the feature data using StandardScaler to normalize the input.
    3. Trains a Logistic Regression model on the scaled training data.

    Parameters:
    - X (array-like): Feature data (independent variables).
    - y (array-like): Target data (dependent variable).
    - test_size (float, optional): Proportion of the dataset to include in the test split (default is 0.3).
    - shuffle (bool, optional): Whether to shuffle the data before splitting (default is True).
    - random_state (int, optional): The seed used by the random number generator for reproducibility (default is 42).
    - C (float, optional): Regularization strength. Smaller values specify stronger regularization (default is 0.1).
    - max_iter (int, optional): Maximum number of iterations taken for the solvers to converge (default is 10000).

    Returns:
    - scaler (StandardScaler): The fitted scaler used for feature normalization.
    - model (LogisticRegression): The trained Logistic Regression model.
    - X_train, X_test, y_train, y_test: The respective training and test sets.
    - accuracy (float): Accuracy score of the model on the test set.
    """
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, shuffle=shuffle, random_state=random_state
    )
    
    # Initialize and apply the StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Initialize and train the Logistic Regression model
    model = LogisticRegression(C=C, max_iter=max_iter, random_state=random_state)
    model.fit(X_train_scaled, y_train)
    
    # Predict on the test set
    y_pred = model.predict(X_test_scaled)
    
    # Calculate the accuracy score
    accuracy = accuracy_score(y_test, y_pred)
    
    # Return the scaler, trained model, data splits, and accuracy score
    return scaler, model, X_train, X_test, y_train, y_test, accuracy

def prepare_and_train_xgb_model(X, y, test_size=0.3, shuffle=True, random_state=42, n_estimators=100, max_depth=3, learning_rate=0.1):
    """
    Splits the dataset, scales features, and trains an XGBoost classifier.

    Parameters:
    - X (array-like): Feature data (independent variables).
    - y (array-like): Target data (dependent variable).
    - test_size (float): Proportion of the dataset to include in the test split.
    - shuffle (bool): Whether to shuffle the data before splitting.
    - random_state (int): Random seed for reproducibility.
    - n_estimators (int): The number of boosting rounds (trees) to fit.
    - max_depth (int): The maximum depth of each tree.
    - learning_rate (float): The learning rate (shrinkage).

    Returns:
    - scaler (StandardScaler): The fitted scaler used for feature normalization.
    - model (XGBClassifier): The trained XGBoost classifier.
    - X_train, X_test, y_train, y_test: The respective training and test sets.
    - accuracy (float): Accuracy score of the model on the test set.
    """
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, shuffle=shuffle, random_state=random_state
    )

    # Normalize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Initialize and train the XGBoost model
    model = XGBClassifier(n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate, random_state=random_state)
    model.fit(X_train_scaled, y_train)

    # Calculate accuracy
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    return scaler, model, X_train, X_test, y_train, y_test, accuracy

def save_model_and_scaler(model, scaler, model_filename='model', scaler_filename='scaler', save_dir='Model'):
    """
    Saves the model and scaler to disk with a timestamped filename to ensure unique storage.

    This function:
    1. Generates a timestamp in the format "YYYY-MM-DD_HH-MM-SS".
    2. Saves the model and scaler to disk in the specified directory with the timestamped filenames.
    3. Prints the file paths where the model and scaler have been saved.

    Parameters:
    - model (sklearn model or similar): The trained machine learning model to be saved.
    - scaler (scikit-learn Scaler or similar): The scaler used to scale the features.
    - model_filename (str, optional): The base filename for the model (default is 'model').
    - scaler_filename (str, optional): The base filename for the scaler (default is 'scaler').
    - save_dir (str, optional): The directory where the model and scaler will be saved (default is 'Model').

    Returns:
    - None: This function saves the model and scaler to disk and prints the file paths.
    """
    # Generate timestamp with the format "YYYY-MM-DD_HH-MM-SS"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create the full paths with timestamp
    model_path = f'{save_dir}/{model_filename}_{timestamp}.pkl'
    scaler_path = f'{save_dir}/{scaler_filename}_{timestamp}.pkl'
    
    # Save the model and scaler with timestamped filenames
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    print(f"Model saved as {model_path}")
    print(f"Scaler saved as {scaler_path}")

def predict(user_input,ModelPath,ScalerPath):
    """
    Makes a prediction using a pre-trained model and a saved scaler.

    This function:
    1. Loads the pre-trained model and scaler from the specified file paths.
    2. Converts the user input (in dictionary format) to a 2D array.
    3. Scales the input data using the loaded scaler.
    4. Returns the prediction result from the model based on the scaled input.

    Parameters:
    - user_input (dict): A dictionary containing feature names as keys and feature values as inputs for prediction.
    - ModelPath (str): The file path to the saved pre-trained model (in .pkl format).
    - ScalerPath (str): The file path to the saved scaler (in .pkl format) used to scale the input data.

    Returns:
    - result: The prediction made by the model based on the processed and scaled input data.

    Exceptions:
    - FileNotFoundError: If the model or scaler file is not found at the specified paths.
    - Any other errors during input processing, scaling, or prediction will be logged and raised.
    """
    Model = joblib.load(ModelPath)  # Load the trained model
    MyScaler = joblib.load(ScalerPath)  # Load the saved scaler
    # Convert dict to 2D array if needed
    input_array = np.array([list(user_input.values())])
    input_array=MyScaler.transform(input_array)
    result = Model.predict(input_array)
    return result    

