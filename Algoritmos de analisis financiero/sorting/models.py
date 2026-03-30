class Record:
    """
    Represents a single row of our financial master dataset.
    Implements comparison dunder methods (__lt__, __le__, etc.) to allow
    standard comparative sorting algorithms to work natively with Record objects.
    
    Sorting criteria:
    1. Date (Ascending)
    2. Close Price (Ascending)
    """
    def __init__(self, symbol, date_str, open_p, high, low, close_p, volume):
        self.symbol = symbol
        self.date_str = date_str
        self.open_p = float(open_p)
        self.high = float(high)
        self.low = float(low)
        self.close_p = float(close_p)
        self.volume = int(volume)
        
        # Precomputed integer keys for non-comparative sorts (Radix, Bucket, Pigeonhole)
        # Convert YYYY-MM-DD to YYYYMMDD
        self.date_int = int(date_str.replace('-', ''))
        # Convert close price to an integer preserving 4 decimal places
        self.close_int = int(self.close_p * 10000)

    def __lt__(self, other):
        if self.date_str == other.date_str:
            return self.close_p < other.close_p
        return self.date_str < other.date_str

    def __le__(self, other):
        if self.date_str == other.date_str:
            return self.close_p <= other.close_p
        return self.date_str <= other.date_str
        
    def __gt__(self, other):
        return not self.__le__(other)
        
    def __ge__(self, other):
        return not self.__lt__(other)

    def __eq__(self, other):
        return self.date_str == other.date_str and self.close_p == other.close_p

    def __repr__(self):
        return f"Record({self.symbol}, {self.date_str}, {self.close_p})"
