from src.Data_Description import preprocess_and_generate_reports
from src.Data_Preprocessing import preprocess_data
import sys
from MyDataUitlsLib import save_to_csv

def main(csvpath):
    # Run the preprocessing and generate reports for the given CSV file
    df = preprocess_and_generate_reports(csvpath, output_folder="1-preprocess_and_generate_reports_1")

    # Columns to remove
    columns_to_remove = ['rownumber', 'customerid', 'surname']
    
    # Encoding configuration
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

    # Preprocess the data and save the processed dataframe
    processed_df,ProcessedCSV = preprocess_data(df, columns_to_remove, encoding_config, output_folder="2-Data_Preprocessing")
    
    # Run the preprocessing and generate reports for the given CSV file
    preprocess_and_generate_reports(ProcessedCSV, output_folder="1-preprocess_and_generate_reports_2")

    


if __name__ == "__main__":
    # Ensure the CSV path is passed as a command line argument
    if len(sys.argv) > 1:
        csvpath = sys.argv[1]  # Get the CSV path from the command line argument
        main(csvpath)
    else:
        print("Please provide the path to the CSV file.")
