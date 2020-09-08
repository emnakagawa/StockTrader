# Module for predicting the value of a given stock
from helper import get_data, get_recent, get_info 
from indicators import EMA, SMA, MACD, RSI, OBV, ATR, ACTION
import argparse 
import pandas as pd 
import numpy as np
# from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


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
    data['ACTION'] = ACTION(data, upper = 0.005, lower = 0)
    data.dropna(inplace=True) # Remove np.nan values
    print(np.unique(data.iloc[:, -1].values, return_counts=True))
    # Print out data using slicing (PRACTICE)
    # print(data.iloc[0:-100, :])
    # print(data.dropna().shape[0])

    # Separate data and create an X and y variable
    # Remove First 6 columns: Open, High, Low, Close, Adj Close, Volume
    data = data.iloc[:, 6:]
    # print(list(data)
    # print(data.iloc[:, -1])
    # print(data.iloc[:, [0, 1, 3]])
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values
    # print(np.unique(y))
    # print(y)
    print(X)
    # TODO: Train data  
    test_split = 0.1
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_split, random_state=1)
    
    print(X_test.shape)
    # # KNN Classification
    # from sklearn.neighbors import KNeighborsClassifier
    # knn_clf = KNeighborsClassifier()
    # knn_clf.fit(X_train, y_train)
    # knn_predictions = knn_clf.predict(X_test)
    # score = accuracy_score(y_test, knn_predictions)
    # print(score)

    # # RANDOM FORESTS --> 0.2 train/test --> 0.38 accuracy :(
    # rf_classifier = RandomForestClassifier()
    # rf_classifier.fit(X_train, y_train)
    
    # rf_predictions = rf_classifier.predict(X_test)
    # score = accuracy_score(y_test, rf_predictions)
    # print(score)

    # DNN classifier
    from sklearn.neural_network import MLPClassifier 
    dnn_clf = MLPClassifier(hidden_layer_sizes = [10] * 2,  max_iter=10000, random_state=1)
    dnn_clf.fit(X_train, y_train)
    dnn_predictions = dnn_clf.predict(X_test)
    score = accuracy_score(y_test, dnn_predictions)
    print(score)
    print(dnn_predictions)
    print(np.unique(dnn_predictions, return_counts=True))

    # # One-vs-all (One-vs-rest)
    # from sklearn.multiclass import OneVsRestClassifier 
    # dnns_clf = OneVsRestClassifier(MLPClassifier(hidden_layer_sizes = [100] * 5))
    # dnns_clf.fit(X_train, y_train)
    # dnns_predictions = dnns_clf.predict(X_test)
    # score = accuracy_score(y_test, dnns_predictions)
    # print(score)

    # TODO: Test data

    # TODO: Evaluate performance
    
    return 

if __name__ == '__main__':
    main()