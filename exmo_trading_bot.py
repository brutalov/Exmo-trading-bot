import ccxt


class ExmoTradingBot:
    def __init__(self, api_key, api_secret, symbol="ETH/USDT",
                 quantity=0.01, buy_price=3000, sell_price=3500):
        self.api_key = api_key
        self.api_secret = api_secret
        self.symbol = symbol  # Trading pair (e.g., ETH/USDT)
        self.quantity = quantity  # Amount to trade
        self.buy_price = buy_price  # Price to buy
        self.sell_price = sell_price  # Price to sell

        # Initialize the ccxt Exmo client
        self.exchange = ccxt.exmo({
            "apiKey": self.api_key,
            "secret": self.api_secret,
        })

        # Initialize bot state
        self.current_price = 0.0
        self.last_buy_price = 0.0
        self.last_sell_price = 0.0
        self.status = "Idle"

    def get_market_price(self):
        """Fetch the current market price of the symbol."""
        try:
            ticker = self.exchange.fetch_ticker(self.symbol)
            self.current_price = ticker['last']
            return self.current_price
        except Exception as e:
            print(f"Error fetching market price: {e}")
            return None

    def place_order(self, side, price):
        """Place an order (buy or sell) on the exchange."""
        try:
            order = self.exchange.create_limit_order(
                symbol=self.symbol,
                side=side,
                amount=self.quantity,
                price=price,
            )
            return order
        except Exception as e:
            print(f"Error placing {side} order: {e}")
            return None

    def place_buy_order(self):
        """Place a buy order."""
        print(f"Placing buy order at {self.buy_price}...")
        order = self.place_order("buy", self.buy_price)
        if order:
            self.last_buy_price = self.buy_price
            self.status = "Buy order placed"
            print(f"Buy order placed: {order}")
        else:
            self.status = "Error placing buy order"

    def place_sell_order(self):
        """Place a sell order."""
        print(f"Placing sell order at {self.sell_price}...")
        order = self.place_order("sell", self.sell_price)
        if order:
            self.last_sell_price = self.sell_price
            self.status = "Sell order placed"
            print(f"Sell order placed: {order}")
        else:
            self.status = "Error placing sell order"

    def trade_once(self):
        """Perform one iteration of the trading logic."""
        print("Starting trade cycle...")
        market_price = self.get_market_price()
        if market_price is None:
            print("Failed to fetch market price.")
            return

        print(f"Current market price: {market_price}")
        if market_price < self.buy_price:
            self.place_buy_order()
        elif market_price > self.sell_price:
            self.place_sell_order()
        else:
            self.status = "No action needed"
            print("No action taken this cycle.")
