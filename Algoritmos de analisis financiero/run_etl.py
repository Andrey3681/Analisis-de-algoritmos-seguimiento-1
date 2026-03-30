import os
import time
from datetime import datetime, timedelta
import logging

from etl.extractor import YahooFinanceExtractor
from etl.transformer import DataTransformer
from etl.loader import DataLoader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_etl():
    logging.info("Initiating ETL Process...")
    
    # Define Tickers (20 assets mixed of ADRs of Colombian companies and global ETFs)
    tickers = [
        "EC", "CIB", "AVAL", "TGLS",  # Colombian linked / ADRs
        "VOO", "CSPX.L", "QQQ", "DIA", "IWM",  # Global ETFs
        "EFA", "EEM", "VTI", "VEA", "VWO", 
        "ARKK", "XLF", "XLK", "XLV", "XLE", "VT"
    ]
    
    # Define time range: 5 years from today
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5*365)
    
    start_timestamp = int(time.mktime(start_date.timetuple()))
    end_timestamp = int(time.mktime(end_date.timetuple()))
    
    # 1. Extract
    extractor = YahooFinanceExtractor(tickers, start_timestamp, end_timestamp)
    raw_data = extractor.extract_all()
    
    if not raw_data:
        logging.error("No data extracted. Aborting ETL.")
        return
        
    logging.info("Extraction complete. Beginning transformation...")
    
    # 2. Transform
    transformer = DataTransformer(raw_data)
    clean_df = transformer.transform()
    
    if clean_df.empty:
        logging.error("Transformed data is empty. Aborting ETL.")
        return
        
    logging.info(f"Transformation complete. Cleaned data size: {clean_df.shape}")
        
    # 3. Load
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    
    loader = DataLoader(data_dir)
    loader.save_to_csv(clean_df, 'dataset_maestro.csv')
    
    logging.info("ETL Process Completed Successfully.")

if __name__ == "__main__":
    run_etl()
