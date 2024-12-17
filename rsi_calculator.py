import pandas as pd
import os.path
import psycopg2
from psycopg2 import sql
from datetime import datetime


def calculate_rsi(data, window=14):
    """
    Calculate the Relative Strength Index (RSI) for the provided data.

    Parameters:
    data (pd.Series): A pandas Series containing the price data (e.g., 'Close' prices).
    window (int): The window size for calculating RSI (default is 14).

    Returns:
    pd.Series: A pandas Series containing the RSI values.
    """
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def recalculate_latest_rsi(symbol, price):
    # Define the connection parameters
    conn_params = {
        'host': 'localhost',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'port': 5432
    }

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()

    # Get the latest 14 rows for the given symbol
    table_name = 'crypto_data'

    query = sql.SQL("""
        SELECT date, close_price FROM {table_name}
        WHERE symbol = %s
        ORDER BY date DESC
        LIMIT 14
        """).format(table_name=sql.Identifier(table_name))

    cur.execute(query, (symbol,))
    rows = cur.fetchall()

    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=['date', 'close_price'])
    df = df.sort_values(by='date')  # Ensure it's sorted by date ascending

    if df.empty:
        return

    # Check if there's already data for today's date
    today = datetime.now().date()
    if today in df['date'].values:
        df.loc[df['date'] == today, 'close_price'] = price
        new_item = False
    else:
        # Drop the oldest row and append the new data
        df = df.drop(df.index[0])
        new_row = {'date': today, 'close_price': price}
        df = df._append(new_row, ignore_index=True)
        new_item = True

    # Calculate the RSI for the updated DataFrame
    df['rsi'] = calculate_rsi(df['close_price'])

    # Update or Insert the price for the current date in the database
    if not new_item:
        # Update the existing record with the current date
        update_query = sql.SQL("""
            UPDATE crypto_data
            SET close_price = %s, rsi = %s
            WHERE date = %s AND symbol = %s
        """).format(table_name=sql.Identifier(table_name))
        rsi_value = float(df.loc[df['date'] == today, 'rsi'].values[0])
        cur.execute(update_query, (price, rsi_value, today, symbol))
    else:
        # Insert a new row if there isn't already a record for today
        insert_query = sql.SQL("""
            INSERT INTO crypto_data (date, close_price, rsi, symbol)
            VALUES (%s, %s, %s, %s)
        """).format(table_name=sql.Identifier(table_name))
        rsi_value = float(df['rsi'].iloc[-1])
        cur.execute(insert_query, (today, price, rsi_value, symbol))

    conn.commit()
    cur.close()
    conn.close()


def main():
    crypto_pairs = ['BTCUSDT', 'ETHUSDT', 'TWTUSDT', 'SOLUSDT', 'BNBUSDT', 'XRPUSDT']

    for symbol in crypto_pairs:
        # Load the CSV file
        file_path = f'data/{symbol}.csv'
        if not os.path.isfile(file_path):
            continue

        data = pd.read_csv(file_path)

        # Check if 'Close' column exists
        if 'Close' not in data.columns:
            print("Error: 'Close' column not found in the data.")
            return

        # Calculate RSI
        data['RSI'] = calculate_rsi(data['Close'])

        # Save the result to a new CSV file
        output_file_path = f'data/{symbol}_RSI.csv'
        data.to_csv(output_file_path, index=False)

        print(f"RSI calculation completed. Results saved to {output_file_path}")


if __name__ == "__main__":
    main()
