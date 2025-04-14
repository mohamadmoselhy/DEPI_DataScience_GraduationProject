import numpy as np
import pandas as pd
import os

# Our own libraries
import MyDataUitlsLib as ul

def preprocess_data(df: pd.DataFrame, columns_to_remove: list, encoding_config: dict, output_folder: str = "2-Data_Preprocessing"):
    """
    Preprocess the input DataFrame by removing columns, handling missing values, encoding categorical columns,
    transforming numerical columns, and saving the processed data to a CSV file.

    Args:
        df (pd.DataFrame): The input DataFrame to be processed.
        columns_to_remove (list): List of columns to remove from the DataFrame.
        encoding_config (dict): Configuration dictionary for encoding and transforming columns.
        output_folder (str): Folder to save the output CSV file. Default is "2-Data_Preprocessing".
    
    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    try:
        # Remove specified columns
        df = ul.drop_columns(df, columns_to_remove)

        # Remove duplicate rows
        df = ul.drop_duplicates(df)

        # Handle missing values
        df = ul.handle_missing_values(df)

        # Encode 'gender' column using label encoding and 'geography' using one-hot encoding
        df = ul.encode_column(df, 'gender', encoding_type="label")
        df = ul.encode_column(df, 'geography', encoding_type="onehot")

        # Encode numerical columns by ranges (excluding 'age' as per your config)
        for column, config in encoding_config.items():
            df = ul.encode_by_ranges(df, column, config['new_column'], config['bins'], config['labels'])

        # Apply log transformation to 'age' column
        df['age'] = np.log1p(df['age'])

        # Generate the processed DataFrame's descriptive statistics
        print(df.describe())

        # Save the processed DataFrame to a CSV file
        output_file = f"{output_folder}/DataAfterDataPreProcessing.csv"
        ul.save_to_csv(df, output_file)

        print(f"Data saved to {output_file}")

        return df,output_file  # Return the processed DataFrame

    except Exception as e:
        print(f"An error occurred during preprocessing: {e}")
        return None

# Example usage:
df = pd.read_csv("D:/My drive/Course/Data Science/Projects/Graduation Projects/DataAnalysis_DEPI_GraduationProject/old_GraduationProject/Dataset and code/DataSet/InitailDataSet/DataSet Before Cleanig.csv")

columns_to_remove = ['rownumber', 'customerid', 'surname']
encoding_config = {
    "creditscore": {
        "new_column": "creditscorerange",
        "bins": [300, 580, 670, 740, 800, 851, float('inf')],
        "labels": [0, 1, 2, 3, 4]
    },
    "balance": {
        "new_column": "balancerange",
        "bins": [0, 40000, 120000, float('inf')],
        "labels": [0, 1, 2]
    },
    "estimatedsalary": {
        "new_column": "estimatedsalaryrange",
        "bins": [0, 40000, 70000, float('inf')],
        "labels": [0, 1, 2]
    },
    "tenure": {
        "new_column": "tenurerange",
        "bins": [0, 2, 4, 7, float('inf')],
        "labels": [0, 1, 2, 3]
    }
}

processed_df = preprocess_data(df, columns_to_remove, encoding_config)
