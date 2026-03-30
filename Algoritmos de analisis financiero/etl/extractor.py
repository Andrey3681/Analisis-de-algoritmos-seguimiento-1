import time
import requests
import logging

class YahooFinanceExtractor:
    """
    Extracts historical financial data directly from Yahoo Finance query API.
    Does not rely on high-level standard libraries like yfinance.
    """
    BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    
    def __init__(self, tickers, start_timestamp, end_timestamp):
        self.tickers = tickers
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        # Standard header to mimic a browser and avoid 403 Forbidden errors
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
    def fetch_data(self, ticker, retries=3):
        url = self.BASE_URL.format(ticker=ticker)
        params = {
            "period1": self.start_timestamp,
            "period2": self.end_timestamp,
            "interval": "1d",
            "events": "history"
        }
        
        for attempt in range(retries):
            try:
                response = requests.get(url, params=params, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429: # Rate limit hit
                    logging.warning(f"Rate limit hit for {ticker}. Waiting {2 ** attempt}s...")
                    time.sleep(2 ** attempt)
                else:
                    logging.error(f"Failed to fetch {ticker}: HTTP {response.status_code}")
                    time.sleep(2)
            except requests.exceptions.RequestException as e:
                logging.error(f"Network error for {ticker} on attempt {attempt+1}: {e}")
                time.sleep(2)
                
        return None
        
    def extract_all(self):
        """
        Iterates over all tickers and returns a dictionary of JSON responses.
        Handles API politeness by sleeping between requests.
        """
        raw_data = {}
        for ticker in self.tickers:
            logging.info(f"Fetching data for {ticker}...")
            data = self.fetch_data(ticker)
            if data:
                raw_data[ticker] = data
            # Polite delay to avoid hammering the Yahoo API
            time.sleep(1)
        return raw_data
