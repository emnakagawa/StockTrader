# Module for predicting the value of a given stock
from helper import get_data, get_recent, get_info 
from indicators import EMA, SMA, MACD, RSI, OBV, ATR, ACTION
import argparse 
import pandas as pd 



def main():

    # Parse input for a single argument 
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=False)
    args = parser.parse_args() 
    
    # TODO: Figure out method to download available stocks so crashing doesn't happen
    TICKER = 'AAPL'
    if args.name != None:
        TICKER = args.name 
    
    period = '10y'
    data = get_recent(TICKER, period)

    # Calculate indicators for TICKER
    # Can tweak individual settings here: num_decimals, pct_change 
    data['MACD(line)'], data['MACD(signal)'], data['MACD(hist)'] = MACD(data)
    data['RSI'] = RSI(data)
    data['OBV'] = OBV(data)
    data['ATR'] = ATR(data)
    data['BUY'], data['SELL'] = ACTION(data, pct_change = 0.01)
    
    print(data)
    
    
    return 

if __name__ == '__main__':
    main()