from optparse import OptionParser

import matplotlib.pyplot as plt
import pandas as pd
import math


window = 20
no_of_std = 2
low = 5000
high = 5000


def get_stock_data(path):
    """Turn stock data into pandas dataframe to calculate the bollinger bands"""
    prices = pd.read_csv(path, index_col='Date', parse_dates=True,
                         usecols=['Date', 'Close'], na_values=['nan'])
    dates = pd.date_range('2019-02-13', '2020-07-28')
    df = pd.DataFrame(index=dates)
    df = df.join(prices)
    df = df.dropna()
    reversed_df = df.iloc[::-1]
    return reversed_df


def bollinger(df):
    """Calculate bollinger bands and return the mean, bb high, bb low"""
    # Calculate rolling mean and standard deviation using number of days set above
    rolling_mean = df['Close'].rolling(window).mean()
    rolling_std = df['Close'].rolling(window).std()

    # Create two new DataFrame columns to hold values of upper and lower Bollinger bands
    df['Rolling Mean'] = rolling_mean
    df['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
    df['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)

    print(df.head(50))
    return df[['Rolling Mean', 'Bollinger High', 'Bollinger Low']]


def distance(a, b):
    if (a == b):
        return 0
    elif (a < 0) and (b < 0) or (a > 0) and (b > 0):
        if (a < b):
            return (abs(abs(a) - abs(b)))
        else:
            return -(abs(abs(a) - abs(b)))
    else:
        return math.copysign((abs(a) + abs(b)), b)


def is_near_to_bb(ud: bool, price: int, bb):
    """Retrun true if the price is near to the bb up or down! for bollinger high make `ud` true & for bollinger low make `ud` false"""
    if ud == False:
        if distance(df['Bollinger Low'].iloc[window], price) <= low:
            # print(distance(int(df['Bollinger Low'].iloc[window]), price))
            return True
        else:
            return False
    elif ud == True:
        if distance(df['Bollinger High'].iloc[window], price) <= high:
            # print(distance(int(df['Bollinger Low'].iloc[window]), price))
            return True
        else:
            return False
    else:
        print("ud argument is required...")
        exit()


if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = "**\tSome options are required\t**\nusage: python main.py --file=/home/user/data.csv"
    parser.add_option("-f", "--file", type="string",
                      help="price '.csv' path for dataframe['date', 'close']",
                      dest="filename", )
    options, arguments = parser.parse_args()

    if options.filename:
        df = get_stock_data(options.filename)
        print("processing data...")
    else:
        print(parser.usage)
        exit()

    print(is_near_to_bb(ud=False, price=41470, bb=bollinger(df=df)))
