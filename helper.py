# Helper file to grab data using the yfinance package. 
import pandas as pd 
import yfinance as yf 

def get_data(tickers: list, start: str = "2017-01-01", end: str = "2017-12-13", num_threads: int = 4) -> pd.DataFrame:
    data = yf.download(tickers, start, end, group_by='ticker', threads=num_threads)
    return data

def get_recent(tickers: list, period: str, num_threads: int = 4) -> pd.DataFrame:
    ''' 
    Returns data in format [('Ticker', 'Open')]
    '''
    # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    data = yf.download(tickers, group_by='ticker', period=period, threads=num_threads)
    threads = True 
    return data

def get_info(tickers: str) -> dict:
    info = yf.Ticker(tick).info 
    return info 