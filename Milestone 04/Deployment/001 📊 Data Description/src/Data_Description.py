import pandas as pd
import warnings
import os
warnings.filterwarnings("ignore")

# Our own libraries
import MyMachineLearningLib as ml
import MyDataUitlsLib as ul
import MyVisualizationLib as vl

def preprocess_and_generate_reports(csvpath, columns_to_drop: list = None, output_folder: str = "Data_Description-AfterDataPreprocessing"):
    """
    Perform data preprocessing, generate statistical reports, and save the results in text files and images.

    Args:
        df (pd.DataFrame): The input DataFrame to be processed.
        columns_to_drop (list, optional): List of columns to drop from the DataFrame. Default is None (no columns dropped).
        output_folder (str): The folder where the output files will be saved. Default is "1-Data_Description".
    
    Returns:
        None: Saves reports and images in the specified output folder.
    """
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")

    df = ul.load_data(csvpath)

    # If columns_to_drop is provided, drop the specified columns
    if columns_to_drop:
        df = ul.drop_columns(df, columns_to_drop)

    # Generate basic statistics report
    BasicStatistics = ul.DataFrameStatistics(df).generate_report_lines()
    ul.write_to_text_file(BasicStatistics, filename=f"{output_folder}/BasicStatistics.txt")
    
    # Generate summary check report
    SummaryCheck = ul.check_data_for_preprocessing(df, return_text_report=True)
    ul.write_to_text_file(SummaryCheck, filename=f"{output_folder}/SummaryCheck1.txt")

    # Identify outliers and save the report
    outlier = ul.identify_outliers(df)
    ul.write_to_text_file(outlier, filename=f"{output_folder}/outlier.txt")
    
    # Plot boxplots and histograms and save them
    vl.plot_boxplots(df, df.columns, figsize=(8, 10), save_folder=f"{output_folder}/boxplot_images")
    vl.plot_histograms(df, df.columns, save_folder=f"{output_folder}/histogram_images")

    print("Reports and images have been saved successfully.")

    return df

# Example usage:
"""
df = pd.read_csv("D:/My drive/Course/Data Science/Projects/Graduation Projects/DataAnalysis_DEPI_GraduationProject/old_GraduationProject/Dataset and code/DataSet/InitailDataSet/DataSet Before Cleanig.csv")
preprocess_and_generate_reports(df, columns_to_drop=['RowNumber','CustomerId','Surname'])  # No columns dropped
"""

"""
csvpath=(r"D:\My drive\Course\Data Science\Projects\Graduation Projects\DataAnalysis_DEPI_GraduationProject\old_GraduationProject\Milestone 04\Deployment\001 📊 Data Description\Data_Preprocessing\DataAfterDataPreProcessing.csv")
preprocess_and_generate_reports(csvpath)  # No columns dropped
"""
