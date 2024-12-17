# crypto-market-analyzer>

import requests
import pandas as pd


def get_candles(symbol, interval='1d', limit=100):
    """
    Retrieve candlestick data from Binance API.

    :param symbol: Cryptocurrency pair, e.g., 'BTCUSDT'
    :param interval: Time interval for candlesticks, e.g., '1d' (1 day), '1h' (1 hour)
    :param limit: Number of candlesticks to retrieve
    :return: DataFrame with candlestick data
    https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/Kline-Candlestick-Data
    """
    url = f'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        "interval": interval,
        'limit': limit
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                     'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                     'taker_buy_quote_asset_volume', 'ignore'])

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Convert numerical columns to float
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

    return df


def analyze_avg_price(df):
    # Calculate median in closing prices
    return df['close'].mean()



def main():
    res = get_analyze_results('1M')
    print(res)

def get_analyze_results(interval):
    limit = 1500  # Number of candles to retrieve

    cryptoPairs = ['BTCUSDT', 'ETHUSDT', 'TWTUSDT', 'SOLUSDT', 'BNBUSDT', 'XRPUSDT']

    res = ""
    for symbol in cryptoPairs:
        df = get_candles(symbol, interval, limit)
        price = analyze_avg_price(df)
        res += f'\nThe avg price for {symbol} is: {price}'

    return res


if __name__ == '__main__':
    main()
