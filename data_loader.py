import pandas as pd

def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
        raise
