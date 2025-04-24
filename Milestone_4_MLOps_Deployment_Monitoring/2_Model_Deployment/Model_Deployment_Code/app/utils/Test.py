import pandas as pd
from utils import load_data
import numpy as np
from sklearn.preprocessing import LabelEncoder


def encode_column(df: pd.DataFrame, column: str, method: str = 'label') -> pd.DataFrame:
    """
    Encodes a categorical column using either label encoding or one-hot encoding.

    Args:
        df (pd.DataFrame): The input DataFrame.
        column (str): The name of the column to encode.
        method (str): The encoding method - 'label' or 'onehot'. Default is 'label'.

    Returns:
        pd.DataFrame: The DataFrame with the encoded column.
    """
    column = column.strip()
    
    if column not in df.columns:
        print(f"Column '{column}' not found in the DataFrame.")
        return df

    if method == 'label':
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column].astype(str))
        print(f"Column '{column}' encoded using Label Encoding.")
    elif method == 'onehot':
        df = pd.get_dummies(df, columns=[column], prefix=column)
        print(f"Column '{column}' encoded using One-Hot Encoding.")
    else:
        print("Invalid method. Choose either 'label' or 'onehot'.")
    
    return df

    
df = load_data("D:\My drive\Course\Data Science\Projects\Graduation Projects\DataAnalysis_DEPI_GraduationProject\old_GraduationProject\Dataset and code\DataSet\CleanedDataSet\cleaned_dataset.csv")


print(encode_column(df, 'gender', method='label'))
print(encode_column(df, 'geography', method='onehot'))