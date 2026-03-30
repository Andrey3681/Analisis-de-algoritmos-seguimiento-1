import os

class DataLoader:
    """
    Saves the cleaned Pandas DataFrame into the system CSV format.
    """
    def __init__(self, data_dir):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
    def save_to_csv(self, df, filename):
        path = os.path.join(self.data_dir, filename)
        df.to_csv(path, index=False)
        print(f"Dataset successfully saved to {path} with {len(df)} records.")
