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


def analyze_market_pattern(df):
    """
    Analyze market pattern based on candlestick data.

    :param df: DataFrame with candlestick data
    :return: 'Bull' if the market is bullish, 'Bear' if the market is bearish
    """
    # Calculate percentage change in closing prices
    df['pct_change'] = df['close'].pct_change()

    # Drop NA values created by pct_change
    df = df.dropna()

    # Calculate the average percentage change
    avg_pct_change = round(df['pct_change'].mean(), 2)

    if avg_pct_change > 0:
        return f'Bull: {avg_pct_change}'
    elif avg_pct_change < 0:
        return f'Bear: {avg_pct_change}'
    else:
        return 'Neutral'


def main():
    res = get_analyze_results()
    print(res)

def get_analyze_results():
    interval = '1w'  # Example interval (1 day)
    limit = 1500  # Number of candles to retrieve

    cryptoPairs = ['BTCUSDT', 'ETHUSDT', 'TWTUSDT']

    res = ""
    for symbol in cryptoPairs:
        df = get_candles(symbol, interval, limit)
        pattern = analyze_market_pattern(df)
        res += f'\nThe market pattern for {symbol} is: {pattern}'

    return res


if __name__ == '__main__':
    main()