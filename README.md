Personal Stock-Screener
A simple Python application that allows users to retrieve real-time stock information using the Alpha Vantage API.

Features
Search for a specific stock by symbol
Display basic stock information, including symbol, name, and region
Retrieve real-time price data, including open, high, low, and close prices
Requirements
Python 3.x
Alpha Vantage API key (free)
Installation
Install Python 3.x from the official website: https://www.python.org/downloads/
Sign up for a free Alpha Vantage API key: https://www.alphavantage.co/support/#api-key
Replace the placeholder in the geturl function with your API key
Usage
Run the stock_screener.py script
Enter '1' to search for a stock
Input the stock symbol when prompted
View the stock information displayed in the console
Code Structure
geturl(unique): Generates the URL for a specific stock symbol search
getdata(url): Fetches data from a given URL
main(): Handles user input and displays stock information
Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss the changes.

License
MIT
