# config.py

#input file path without any handling
csv_path="D:\My drive\Course\Data Science\Projects\Graduation Projects\DataAnalysis_DEPI_GraduationProject\old_GraduationProject\Dataset and code\DataSet\InitailDataSet\DataSet Before Cleanig.csv"


# Columns to remove during preprocessing
columns_to_remove = ['rownumber', 'customerid', 'surname']

# Encoding configuration for various features
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
