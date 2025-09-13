import pandas as pd

def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Loads transaction data from a CSV file into a pandas DataFrame.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        pd.DataFrame: A DataFrame with transaction data.
    """
    try:
        df = pd.read_csv(file_path)
        # Ensure timestamp is in datetime format for calculations
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        print(f"✅ Data loaded successfully from {file_path}. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"❌ Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"❌ An error occurred while loading the data: {e}")
        return None