# Helper file for calculating technical indicators
import pandas as pd 
import numpy as np 

def SMA(df: pd.DataFrame, window: int = 15, num_decimals: int = 4) -> pd.DataFrame:
# Returns EMA for a given window, first [window] values are NaN
# Values are rounded to [num_decimals] places
# Data must be a dataframe, with the value 'Adj Close' as one of its columns
    if 'Adj Close' in list(df):
        sma_values = df['Adj Close'].rolling(window).mean()
    else:
        sma_values = df.rolling(window).mean()
    return np.round(sma_values, decimals=num_decimals)


def EMA(df: pd.DataFrame, window: int = 15, num_decimals: int = 4) -> pd.DataFrame:
# Returns EMA for a given window, first [window] values are NaN
# Values are rounded to [num_decimals] places
# Data must be a dataframe, with the value 'Adj Close' as one of its columns
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

def RSI(df: pd.DataFrame, lookback: int = 14, num_decimals: int = 4) -> pd.DataFrame:
    change = df['Adj Close'].diff()
    gain, loss = change.copy(), change.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    loss = np.absolute(loss)
    # First compute the first avg gain or loss, which can be represented as the average of previous [lookback] days
    avg_gain = gain.rolling(lookback).mean()
    avg_loss = loss.rolling(lookback).mean()
    # Assign the current gain / loss for each following period past the first average gain
    avg_gain[lookback+1:] = gain[lookback+1:]
    avg_loss[lookback+1:] = loss[lookback+1:]
    # Helper function to compute the recursiveness of the average gain and loss
    def weighted_rolling(x):
        for i in range(1, len(x)):
            x[i] += (lookback-1) * x[i-1]
            x[i] /= lookback 
        return x
    # Calculate remaining average gain and loss and assign it to the remaining portion of the series
    tmp_gain = weighted_rolling(list(avg_gain[lookback:].copy()))
    avg_gain[lookback:] = tmp_gain

    tmp_loss = weighted_rolling(list(avg_loss[lookback:].copy()))
    avg_loss[lookback:] = tmp_loss
    # RS and RSI Calculation
    rs = avg_gain / avg_loss
    rsi = (100 - (100 / (1 + rs)))
    return np.round(rsi, num_decimals)

def OBV(df: pd.DataFrame, num_decimals: int=4) -> pd.DataFrame:
    out = df[['Close', 'Volume']].copy()
    out['Up-Down'] = np.sign(np.diff(out['Close'], prepend=np.nan))
    out['Pos / Neg'] = out['Volume'] * out['Up-Down']
    out['OBV'] = np.cumsum(out['Pos / Neg'])
    return np.round(out['OBV'], num_decimals)

def ATR(df: pd.DataFrame, period:int = 14, num_decimals: int=4) -> pd.DataFrame:
    # Outputs df[ATR]
    
    out = df[['High', 'Low', 'Close']].copy()
    out['H-L'] = out['High'] - out['Low']
    out['|H-Cp|'] = np.nan
    out['|H-Cp|'][1:] = np.absolute(out['High'][1:].values - out['Close'][:-1].values)
    out['|L-Cp|'] = np.nan
    out['|L-Cp|'][1:] = np.absolute(out['Low'][1:].values - out['Close'][:-1].values)
    out['TR'] = np.nanmax([out['H-L'], out['|H-Cp|'], out['|L-Cp|']], axis=0)
    out['ATR'] = np.nan
    out['ATR'][period] = np.mean(out['TR'][:period], axis=0)
    out['ATR'][period+1:] = ((period - 1) * out['ATR'][period+1:])

    # Seems this part of the calculation can't be done using vectorization since it's based on the previous ATR value and thus requires recursion / iteration.
    for i in range(out.shape[0] - period - 1):
        out['ATR'][period + 1 + i] = (out['TR'][period + 1 + i] + (period - 1) * out['ATR'][period+i]) / period

    return np.round(out['ATR'], num_decimals)

def ACTION(df: pd.DataFrame, pct_change: float = 0.01) -> pd.DataFrame:
    out = df[['Adj Close']].copy()
    # print(out)
    out['Diff'] = out['Adj Close'].diff(periods = -1) * -1
    out['Pct Diff'] = out['Diff'] / out['Adj Close']
    out['BUY'] = out['Pct Diff'] >= pct_change 
    out['SELL'] = out['Pct Diff'] < -pct_change 
    # print(out)
    return out['BUY'], out['SELL']