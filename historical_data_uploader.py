import pandas as pd
import psycopg2
from psycopg2 import sql
import os.path


def upload(symbol):
    # Read the CSV file into a DataFrame
    csv_file_path = f'data/{symbol}_RSI.csv'

    if not os.path.isfile(csv_file_path):
        return

    df = pd.read_csv(csv_file_path)

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

    # Define the table name
    table_name = 'crypto_data'

    # Create the table if it doesn't exist
    create_table_query = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {table_name} (
        date DATE,
        symbol VARCHAR,
        close_price FLOAT,
        rsi FLOAT
    )
    """).format(table_name=sql.Identifier(table_name))
    cur.execute(create_table_query)
    conn.commit()

    df['Symbol'] = symbol

    # Insert DataFrame into the PostgreSQL table
    for index, row in df[['Date', 'Symbol', 'Close', 'RSI']].iterrows():
        insert_query = sql.SQL("""
        INSERT INTO {table_name} (date, symbol, close_price, rsi)
        VALUES (%s, %s, %s, %s)
        """).format(table_name=sql.Identifier(table_name))

        cur.execute(insert_query, tuple(row))

    conn.commit()

    # Close the database connection
    cur.close()
    conn.close()

    print("Data has been successfully inserted into the database!")


def main():
    crypto_pairs = ['BTCUSDT', 'ETHUSDT', 'TWTUSDT', 'SOLUSDT', 'BNBUSDT', 'XRPUSDT']

    for symbol in crypto_pairs:
        upload(symbol)


if __name__ == "__main__":
    main()
