
import json
import random
import os

class StockSimulator:
    def __init__(self, portfolio_file="portfolio.json", stocks_file="stocks.json"):
        self.portfolio_file = portfolio_file
        self.stocks_file = stocks_file
        self.portfolio = self._load_portfolio()
        self.stocks = self._load_stocks()

    def _load_portfolio(self):
        if os.path.exists(self.portfolio_file):
            with open(self.portfolio_file, "r") as f:
                return json.load(f)
        return {"cash": 10000.0, "holdings": {}}

    def _save_portfolio(self):
        with open(self.portfolio_file, "w") as f:
            json.dump(self.portfolio, f, indent=4)

    def _load_stocks(self):
        if os.path.exists(self.stocks_file):
            with open(self.stocks_file, "r") as f:
                return json.load(f)
        # Initial dummy stocks
        return {
            "AAPL": {"price": 150.00, "volatility": 0.02},
            "GOOG": {"price": 2500.00, "volatility": 0.01},
            "MSFT": {"price": 300.00, "volatility": 0.015},
            "AMZN": {"price": 3000.00, "volatility": 0.025},
        }

    def _save_stocks(self):
        with open(self.stocks_file, "w") as f:
            json.dump(self.stocks, f, indent=4)

    def update_stock_prices(self):
        for symbol, data in self.stocks.items():
            current_price = data["price"]
            volatility = data["volatility"]
            change = random.uniform(-volatility, volatility)
            new_price = current_price * (1 + change)
            self.stocks[symbol]["price"] = round(max(0.01, new_price), 2) # Price cannot go below 0.01
        self._save_stocks()

    def display_portfolio(self):
        print("\n--- Your Portfolio ---")
        print(f"Cash: ${self.portfolio['cash']:.2f}")
        print("Holdings:")
        for symbol, quantity in self.portfolio["holdings"].items():
            if quantity > 0:
                current_price = self.stocks.get(symbol, {}).get("price", 0)
                value = current_price * quantity
                print(f"  {symbol}: {quantity} shares (Value: ${value:.2f})")
        print("----------------------")

    def display_stocks(self):
        print("\n--- Available Stocks ---")
        for symbol, data in self.stocks.items():
            print(f"  {symbol}: ${data['price']:.2f}")
        print("------------------------")

    def buy_stock(self, symbol, quantity):
        symbol = symbol.upper()
        if symbol not in self.stocks:
            print(f"Error: Stock {symbol} not found.")
            return

        stock_price = self.stocks[symbol]["price"]
        cost = stock_price * quantity

        if self.portfolio["cash"] >= cost:
            self.portfolio["cash"] -= cost
            self.portfolio["holdings"][symbol] = self.portfolio["holdings"].get(symbol, 0) + quantity
            self._save_portfolio()
            print(f"Successfully bought {quantity} shares of {symbol} for ${cost:.2f}.")
        else:
            print(f"Error: Not enough cash. You need ${cost:.2f} but only have ${self.portfolio['cash']:.2f}.")

    def sell_stock(self, symbol, quantity):
        symbol = symbol.upper()
        if symbol not in self.stocks:
            print(f"Error: Stock {symbol} not found.")
            return

        if symbol not in self.portfolio["holdings"] or self.portfolio["holdings"][symbol] < quantity:
            print(f"Error: You don't own {quantity} shares of {symbol}.")
            return

        stock_price = self.stocks[symbol]["price"]
        revenue = stock_price * quantity

        self.portfolio["cash"] += revenue
        self.portfolio["holdings"][symbol] -= quantity
        if self.portfolio["holdings"][symbol] == 0:
            del self.portfolio["holdings"][symbol]
        self._save_portfolio()
        print(f"Successfully sold {quantity} shares of {symbol} for ${revenue:.2f}.")

    def run(self):
        while True:
            self.update_stock_prices() # Update prices at the start of each "turn"
            self.display_portfolio()
            self.display_stocks()

            print("\n--- Stock Market Simulator ---")
            print("1. Buy Stock")
            print("2. Sell Stock")
            print("3. Next Turn (Update Prices)")
            print("4. Reset Game")
            print("5. Exit")
            
            choice = input("Enter your choice: ")

            if choice == "1":
                symbol = input("Enter stock symbol to buy: ").upper()
                try:
                    quantity = int(input(f"Enter quantity for {symbol}: "))
                    if quantity <= 0:
                        print("Quantity must be positive.")
                        continue
                    self.buy_stock(symbol, quantity)
                except ValueError:
                    print("Invalid quantity.")
            elif choice == "2":
                symbol = input("Enter stock symbol to sell: ").upper()
                try:
                    quantity = int(input(f"Enter quantity for {symbol}: "))
                    if quantity <= 0:
                        print("Quantity must be positive.")
                        continue
                    self.sell_stock(symbol, quantity)
                except ValueError:
                    print("Invalid quantity.")
            elif choice == "3":
                print("Moving to the next turn...")
            elif choice == "4":
                if os.path.exists(self.portfolio_file):
                    os.remove(self.portfolio_file)
                if os.path.exists(self.stocks_file):
                    os.remove(self.stocks_file)
                self.portfolio = self._load_portfolio()
                self.stocks = self._load_stocks()
                print("Game has been reset.")
            elif choice == "5":
                print("Exiting simulator. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    simulator = StockSimulator(portfolio_file="AIDeveloperTest3/portfolio.json", stocks_file="AIDeveloperTest3/stocks.json")
    simulator.run()
