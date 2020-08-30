# Helper file for calculating technical indicators
import pandas as pd 
import numpy as np 

def SMA(df: pd.DataFrame, window: int = 15, num_decimals: int = 3) -> pd.DataFrame:
    sma_values = df['Adj Close'].rolling(window).mean()
    return np.round(sma_values, decimals=num_decimals)

def EMA(df: pd.DataFrame, window: int = 15, num_decimals: int = 3) -> pd.DataFrame:
    modPrice = df['Adj Close'].copy()
    modPrice.iloc[0:window] = modPrice.rolling(window).mean()
    ema_values = modPrice.ewm(span=window, adjust=False).mean()
    return np.round(ema_values, decimals=num_decimals)
