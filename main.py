import time
import json

from binance import Client
from binance.exceptions import BinanceAPIException

# Load API key and secret from environment variables for better security
API_KEY = 'agLqIhhH5J2oHzi9ojavpIgpshnbCmndJywnCEZ4A5Kp70K4p2PxpqmPNbchP977'
API_SECRET = 'S6MSK7E9MVyXUWbOYW1DkruWNJG6sXcy3nTex8e78LAQtfzUneIfkL4xIrc7DjtG'

# Configuration
SYMBOL = "SHIBUSDT"
PROFIT_PERCENTAGE = 1.3  # Desired profit percentage (e.g., 1.3% profit)
RISK_PERCENTAGE = 1  # 1% of USDT balance
MIN_TRADE_AMOUNT = 5  # Minimum USDT amount for trade
INTERVAL = 3  # Time in seconds between each check


client = Client(API_KEY, API_SECRET, testnet=True)


def get_latest_price(symbol):
    ticker = client.get_all_tickers()
    for item in ticker:
        if item['symbol'] == symbol:
            return float(item['price'])
    return None


def get_usdt_balance():
    balance = client.get_asset_balance(asset='USDT')
    if balance:
        return float(balance['free'])
    return None


def calculate_trade_quantity(price, usdt_amount):
    # Calculate how much SHIB to buy with the available USDT amount
    return round(usdt_amount / price, 0)


def calculate_sell_price(buy_price, profit_percentage):
    # Calculate the price to sell to achieve the desired profit percentage
    sell_price = buy_price * (1 + profit_percentage / 100)
    # Format the sell price as a string with 8 decimal places
    return f"{sell_price:.8f}"


def buy_crypto(price):
    exchange_info = client.get_exchange_info()
    # Print the exchange information (this is just a sample)
    # print(exchange_info)

    # Get the list of symbols supported by the exchange
    symbols = exchange_info['symbols']

    # Print the first 5 symbols
    #print(symbols[:5])

    # Get information about a specific symbol (e.g., SHIBUSDT)
    symbol_info = next(s for s in exchange_info['symbols']
                       if s['symbol'] == SYMBOL)
    # Get available USDT balance
    usdt_balance = get_usdt_balance()
    if usdt_balance is not None:
        print(f"USDT Balance: {usdt_balance}")

        # Calculate USDT amount to trade (1% of balance or $5 minimum)
        usdt_amount = max(usdt_balance * RISK_PERCENTAGE / 100,
                          MIN_TRADE_AMOUNT)
        print(f"USDT Amount to trade: {usdt_amount}")

        # Calculate SHIB quantity to trade
        trade_quantity = calculate_trade_quantity(price, usdt_amount)
        print(f"Quantity of {SYMBOL} to trade: {trade_quantity}")

        # Place market buy order
        buy_order = client.order_market_buy(symbol=SYMBOL,
                                            quantity=trade_quantity)
        print(f"Placed buy order: {buy_order}")

        # Calculate the target sell price based on profit percentage
        buy_price = float(buy_order['fills'][0]
                          ['price'])  # Get the average price of the buy order
        
        buy_qty = buy_order['fills'][0]['qty']
        sell_price = calculate_sell_price(buy_price, PROFIT_PERCENTAGE)
        print(
            f"Target sell price for {SYMBOL} with {PROFIT_PERCENTAGE}% profit: {sell_price}"
        )
        

        # Place sell limit order to take profit at the calculated price
        sell_order = client.order_limit_sell(
            symbol=SYMBOL,
            quantity=buy_qty,
            price=sell_price  # Ensure the price has the correct precision
        )
        print(f"Placed sell limit order: {sell_order}")
    else:
        print("USDT balance not found. Skipping trade.")    
    return None


def main():

    #print(symbol_info)
    while True:
        try:
            price = get_latest_price(SYMBOL)
            if price:
                print(f"The price of {SYMBOL} is: {price:.8f}")
            # Check if there are any open orders for the symbol
            #buy_crypto(price)
            orders = client.get_open_orders(symbol=SYMBOL)
            #print(orders)
            
            if not orders:
                # Get the latest price of the trading pair
                buy_crypto(price)
            else:
                
                print(orders)
                Bprice=float(orders[-1]['price'])
                Bprice=Bprice * (1 - PROFIT_PERCENTAGE / 100)
                #print(Bprice)
                print(f"The position price of {SYMBOL} is: {Bprice:.8f}")
                percentage_change = ((price - Bprice) / Bprice) * 100
                print(
                    f"Percentage change from buy price: {percentage_change:.2f}%"
                )
                if abs(percentage_change) > PROFIT_PERCENTAGE:
                    buy_crypto(price)

        except BinanceAPIException as e:
            print(f"Binance API Exception: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Sleep for the specified interval before checking again
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
