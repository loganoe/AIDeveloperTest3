# Stock Market Simulator

This is a simple command-line stock market simulator written in Python.

## Features

- Buy and sell stocks
- Portfolio tracking (cash and holdings)
- Dynamically updating stock prices (based on volatility)
- Save and load game state (portfolio and stock data are saved to JSON files)
- Reset game option

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/loganoe/AIDeveloperTest3.git
   ```
2. Navigate into the directory:
   ```bash
   cd AIDeveloperTest3
   ```
3. Run the simulator:
   ```bash
   python stock_simulator.py
   ```

## Files

- `stock_simulator.py`: The main Python script for the simulator.
- `portfolio.json`: Stores the player's cash and stock holdings (created automatically).
- `stocks.json`: Stores the current stock prices and volatility (created automatically).
