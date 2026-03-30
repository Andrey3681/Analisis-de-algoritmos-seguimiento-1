import pandas as pd
import numpy as np

class DataTransformer:
    """
    Transforms raw JSON data from Yahoo Finance into a clean, unified Pandas DataFrame.
    """
    def __init__(self, raw_data):
        self.raw_data = raw_data
        
    def parse_ticker_data(self, ticker, json_data):
        """Extracts timestamps and OHLCV from the Yahoo Finance JSON."""
        try:
            result = json_data['chart']['result'][0]
            timestamps = result.get('timestamp', [])
            
            if not timestamps:
                return pd.DataFrame()
                
            indicators = result['indicators']['quote'][0]
            
            open_p = indicators.get('open', [np.nan] * len(timestamps))
            high_p = indicators.get('high', [np.nan] * len(timestamps))
            low_p = indicators.get('low', [np.nan] * len(timestamps))
            close_p = indicators.get('close', [np.nan] * len(timestamps))
            vol = indicators.get('volume', [0] * len(timestamps))
            
            df = pd.DataFrame({
                'Date': pd.to_datetime(timestamps, unit='s').date,
                'Open': open_p,
                'High': high_p,
                'Low': low_p,
                'Close': close_p,
                'Volume': vol
            })
            df['Symbol'] = ticker
            return df
        except KeyError as e:
            print(f"Error parsing data for {ticker}: {e}")
            return pd.DataFrame()
            
    def transform(self):
        """
        Unifies and cleans the dataset:
        - Harmonizes dates for all assets (business day calendar)
        - Handles missing values via forward fill to maintain continuity over holidays.
        """
        dfs = []
        for ticker, data in self.raw_data.items():
            df = self.parse_ticker_data(ticker, data)
            if not df.empty:
                dfs.append(df)
                
        if not dfs:
            return pd.DataFrame()
            
        # Combine all data vertically
        master_df = pd.concat(dfs, ignore_index=True)
        
        # Data Cleaning
        master_df['Date'] = pd.to_datetime(master_df['Date'])
        
        # 1. Drop intra-day duplicates if any
        master_df = master_df.drop_duplicates(subset=['Symbol', 'Date'])
        
        # 2. Pivot to align all dates to a common business calendar
        min_date = master_df['Date'].min()
        max_date = master_df['Date'].max()
        all_business_days = pd.date_range(start=min_date, end=max_date, freq='B')
        
        clean_dfs = []
        for symbol, group in master_df.groupby('Symbol'):
            group = group.set_index('Date')
            
            # Remove any dates that fall on weekends (Yahoo sometimes returns anomalous weekend data)
            group = group[group.index.dayofweek < 5]
            
            # Reindex to the complete business day calendar
            group = group.reindex(all_business_days)
            group['Symbol'] = symbol
            
            # Missing prices handling:
            # We use forward fill assuming price remains the same if the market was closed (holiday).
            for col in ['Open', 'High', 'Low', 'Close']:
                group[col] = group[col].ffill() # Forward fill
                group[col] = group[col].bfill() # Backfill in case the start is NaN
                
            # Missing volume is assumed 0 (no trades)
            group['Volume'] = group['Volume'].fillna(0)
            
            group = group.reset_index().rename(columns={'index': 'Date'})
            clean_dfs.append(group)
            
        final_df = pd.concat(clean_dfs, ignore_index=True)
        
        # Rearrange and filter
        final_df = final_df[['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        
        # Final cleanup for types and rounding
        for col in ['Open', 'High', 'Low', 'Close']:
            final_df[col] = final_df[col].astype(float).round(4)
            
        final_df['Volume'] = final_df['Volume'].fillna(0).astype('int64')
        
        return final_df
