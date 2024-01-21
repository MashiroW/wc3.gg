import os
import pandas as pd

def check_duplicate_rows(data):
    if isinstance(data, str):  # If a file path is provided, read the CSV file
        df = pd.read_csv(data)
    elif isinstance(data, pd.DataFrame):  # If a DataFrame is provided, use it directly
        df = data
    else:
        raise ValueError("Input must be either a file path or a DataFrame.")

    duplicate_rows = df[df.duplicated(df.columns.difference(['rank']), keep=False)]
    
    if duplicate_rows.empty:
        print("No duplicate rows found.")
    else:
        print("Duplicate rows found in the following rows:")
        print(duplicate_rows.to_string(index=False))
        return True
    
    return False

def check_discontinuous_ranks(data):
    if isinstance(data, str):  # If a file path is provided, read the CSV file
        df = pd.read_csv(data)
    elif isinstance(data, pd.DataFrame):  # If a DataFrame is provided, use it directly
        df = data
    else:
        raise ValueError("Input must be either a file path or a DataFrame.")

    ranks = df['rank'].tolist()
    min_rank, max_rank = min(ranks), max(ranks)
    all_ranks = set(range(min_rank, max_rank + 1))
    missing_ranks = list(all_ranks - set(ranks))
    
    if not missing_ranks:
        print("No discontinuous ranks found.")
    else:
        print("Discontinuous ranks found. Missing ranks:")
        print(missing_ranks)
        return True
    
    return False

folder_path = "./databases"

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    if os.path.isfile(file_path):
        # Your code to process each file goes here
        print(f"Processing file: {file_path}")
        check_duplicate_rows(data=file_path)
        check_discontinuous_ranks(data=file_path)
        input("Press a key for the next file...")
        print("--------------------------------")

exit()

check_duplicate_rows(data="./databases/wc3_S3_1v1_all.csv")
check_discontinuous_ranks(data="./databases/wc3_S3_1v1_all.csv")