
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import random
import os

app = Flask(__name__)

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
            self.stocks[symbol]["price"] = round(max(0.01, new_price), 2)
        self._save_stocks()

    def get_portfolio_data(self):
        holdings_data = []
        for symbol, quantity in self.portfolio["holdings"].items():
            if quantity > 0:
                current_price = self.stocks.get(symbol, {}).get("price", 0)
                value = current_price * quantity
                holdings_data.append({"symbol": symbol, "quantity": quantity, "value": value})
        return {"cash": self.portfolio["cash"], "holdings": holdings_data}

    def get_stocks_data(self):
        stocks_data = []
        for symbol, data in self.stocks.items():
            stocks_data.append({"symbol": symbol, "price": data["price"]})
        return stocks_data

    def buy_stock(self, symbol, quantity):
        symbol = symbol.upper()
        if symbol not in self.stocks:
            return False, f"Stock {symbol} not found."

        stock_price = self.stocks[symbol]["price"]
        cost = stock_price * quantity

        if self.portfolio["cash"] >= cost:
            self.portfolio["cash"] -= cost
            self.portfolio["holdings"][symbol] = self.portfolio["holdings"].get(symbol, 0) + quantity
            self._save_portfolio()
            return True, f"Successfully bought {quantity} shares of {symbol} for ${cost:.2f}."
        else:
            return False, f"Not enough cash. You need ${cost:.2f} but only have ${self.portfolio['cash']:.2f}."

    def sell_stock(self, symbol, quantity):
        symbol = symbol.upper()
        if symbol not in self.stocks:
            return False, f"Stock {symbol} not found."

        if symbol not in self.portfolio["holdings"] or self.portfolio["holdings"][symbol] < quantity:
            return False, f"You don't own {quantity} shares of {symbol}."

        stock_price = self.stocks[symbol]["price"]
        revenue = stock_price * quantity

        self.portfolio["cash"] += revenue
        self.portfolio["holdings"][symbol] -= quantity
        if self.portfolio["holdings"][symbol] == 0:
            del self.portfolio["holdings"][symbol]
        self._save_portfolio()
        return True, f"Successfully sold {quantity} shares of {symbol} for ${revenue:.2f}."

    def reset_game(self):
        if os.path.exists(self.portfolio_file):
            os.remove(self.portfolio_file)
        if os.path.exists(self.stocks_file):
            os.remove(self.stocks_file)
        self.portfolio = self._load_portfolio()
        self.stocks = self._load_stocks()
        return "Game has been reset."

simulator = StockSimulator(portfolio_file="AIDeveloperTest3/portfolio.json", stocks_file="AIDeveloperTest3/stocks.json")

@app.route('/')
def index():
    simulator.update_stock_prices()
    portfolio_data = simulator.get_portfolio_data()
    stocks_data = simulator.get_stocks_data()
    return render_template('index.html', portfolio=portfolio_data, stocks=stocks_data)

@app.route('/buy', methods=['POST'])
def buy():
    symbol = request.form['symbol'].upper()
    quantity = int(request.form['quantity'])
    success, message = simulator.buy_stock(symbol, quantity)
    return redirect(url_for('index'))

@app.route('/sell', methods=['POST'])
def sell():
    symbol = request.form['symbol'].upper()
    quantity = int(request.form['quantity'])
    success, message = simulator.sell_stock(symbol, quantity)
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    simulator.reset_game()
    return redirect(url_for('index'))

@app.route('/api/portfolio')
def api_portfolio():
    return jsonify(simulator.get_portfolio_data())

@app.route('/api/stocks')
def api_stocks():
    simulator.update_stock_prices()
    return jsonify(simulator.get_stocks_data())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

