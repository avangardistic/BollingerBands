import pandas as pd
import matplotlib.pyplot as plt


window = 20
no_of_std = 2


def get_stock_data():
    prices = pd.read_csv('./data.csv', index_col='Date',parse_dates=True,
                        usecols=['Date', 'Close'], na_values=['nan'])
    dates = pd.date_range('2019-02-13', '2020-07-28')
    df = pd.DataFrame(index=dates)
    df = df.join(prices)
    df = df.dropna()
    reversed_df = df.iloc[::-1]
    return reversed_df

def bollinger(df):
    #Calculate rolling mean and standard deviation using number of days set above
    rolling_mean = df['Close'].rolling(window).mean()
    rolling_std = df['Close'].rolling(window).std()

    #create two new DataFrame columns to hold values of upper and lower Bollinger bands
    df['Rolling Mean'] = rolling_mean
    df['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
    df['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)
    
    return df[['Rolling Mean', 'Bollinger High', 'Bollinger Low']].dropna()

print(bollinger(get_stock_data()))