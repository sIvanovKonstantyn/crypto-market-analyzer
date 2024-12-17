import requests

from rsi_calculator import recalculate_latest_rsi


def get_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price'
    params = {
        'symbol': symbol
    }
    response = requests.get(url, params=params)
    data = response.json()

    return float(data['price'])


def main():
    res = get_current_prices()
    print(res)


def get_current_prices():
    crypto_pairs = ['BTCUSDT', 'ETHUSDT', 'TWTUSDT', 'SOLUSDT', 'BNBUSDT', 'XRPUSDT']

    res = ""
    for symbol in crypto_pairs:
        price = get_price(symbol)
        recalculate_latest_rsi(symbol, price)
        res += f'\nThe current price for {symbol} is: {price}'

    return res


if __name__ == '__main__':
    main()
