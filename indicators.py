# Helper file for calculating technical indicators
import pandas as pd 
import numpy as np 

def SMA(df: pd.DataFrame, window: int = 15, num_decimals: int = 4) -> pd.DataFrame:
# Returns EMA for a given window, first [window] values are NaN
# Values are rounded to [num_decimals] places
    if 'Adj Close' in list(df):
        sma_values = df['Adj Close'].rolling(window).mean()
    else:
        sma_values = df.rolling(window).mean()
    return np.round(sma_values, decimals=num_decimals)


def EMA(df: pd.DataFrame, window: int = 15, num_decimals: int = 4) -> pd.DataFrame:
# Returns EMA for a given window, first [window] values are NaN
# Values are rounded to [num_decimals] places
    if 'Adj Close' in list(df):
        modPrice = df['Adj Close'].copy()
    else:
        modPrice = df.copy()
    modPrice.iloc[0:window] = modPrice.rolling(window).mean()
    ema_values = modPrice.ewm(span=window, adjust=False).mean()
    return np.round(ema_values, decimals=num_decimals)

def MACD(df: pd.DataFrame, ema_vals: list = [12, 26, 9], num_decimals: int = 4) -> pd.DataFrame:
# Returns MACD Line with standard settings of 9-Day EMA of (EMA12 - EMA26)
# Values are rounded to [num_decimals] places
    EMA_12 = EMA(df, window=ema_vals[0], num_decimals=num_decimals)
    EMA_26 = EMA(df, window=ema_vals[1], num_decimals=num_decimals)
    MACD_line = EMA_12 - EMA_26
    Signal_line = EMA(MACD_line, window=ema_vals[2], num_decimals=num_decimals)
    MACD_hist = MACD_line - Signal_line
    return MACD_line, Signal_line, MACD_hist
