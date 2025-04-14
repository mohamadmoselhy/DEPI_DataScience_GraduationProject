from src.Data_Description import preprocess_and_generate_reports
from src.Data_Preprocessing import preprocess_data
import sys
from src.config import columns_to_remove , encoding_config, csv_path

def main(csv_path):
    # Run the preprocessing and generate reports for the given CSV file
    df = preprocess_and_generate_reports(csv_path, output_folder="1-preprocess_and_generate_reports_1")

    # Preprocess the data and save the processed dataframe
    processed_df,ProcessedCSV = preprocess_data(df, columns_to_remove, encoding_config, output_folder="2-Data_Preprocessing")
    
    # Run the preprocessing and generate reports for the given CSV file
    preprocess_and_generate_reports(ProcessedCSV, output_folder="1-preprocess_and_generate_reports_2")

    

main(csv_path)