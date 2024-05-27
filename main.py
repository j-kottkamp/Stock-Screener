import requests
import api
from api import log

    
topics = ["blockchain", "earnings", "ipo", "mergers_and_acquisitions", "financial_markets", "economy_fiscal", "economy_monetary", "economy_macro", "energy_transportation", "finance", "life_sciences", "manufacturing", "real_estate", "retail_wholesale", "technology"]


def main():
    while True:
        try:
            if action =="1":
                stock = input("What Stock do you want to know about?")
                data = api.get(f"SYMBOL_SEARCH&keywords={stock}")
                log(f"Gotten Matches best on follwing input: {stock} <> Data: {data}")
                best_matches = data["bestMatches"]  
                basicdata = {
                    "symbol" : best_matches[0]["1. symbol"],
                    "name"   : best_matches[0]["2. name"],
                    "region" : best_matches[0]["4. region"] }
                
                log(f"Convertet data to Basicdata and sending request... <> Basicdata: {basicdata}")

                price_data = api.get(f'TIME_SERIES_INTRADAY&symbol={basicdata["symbol"]}&interval=5min')
                log(f"Gotten following price data: {price_data}")
                newest_date = list(price_data["Time Series (5min)"].keys())[0]
                log(f"Gotten newest Date: {newest_date}")
                five_min = price_data["Time Series (5min)"][newest_date]
                price = {
                    "open"   : five_min["1. open"],
                    "high"   : five_min["2. high"],
                    "low"    : five_min["3. low"],
                    "close"  : five_min["4. close"] }
                basicdata["price"] = price
                log(f"Basicdata is now: {basicdata}")
                print(basicdata)

            if action =="2":
                i = 0
                search = input("Search by Topic or by Stock?\n\'1\' for Topic\n\'2\' for Stock\n\'.\' for all News")
                if search == ".":
                    news = api.get("NEWS_SENTIMENT")
                elif search == "2":
                    ticker = input("Enter Ticker Symbol")
                    news = api.get(f"NEWS_SENTIMENT&tickers={ticker}")
                elif search == "1":
                    while True:
                        topic = input("Enter Topic")
                        if topic in topics:
                            news = api.get(f"NEWS_SENTIMENT&topics={topic}")
                            break
                        else:
                            print("Cant find Topic. Please choose one of the provided topics", topics)
                newsfeed = {
                    "title"  : news["feed"][i]["title"],
                    "summary": news["feed"][i]["summary"],
                    "newsurl": news["feed"][i]["url"],
                    "flow"   : news["feed"][i]["overall_sentiment_label"]
                }
                for i in newsfeed:
                    print(f"News!\n>>>{newsfeed['title']}<<<\n{newsfeed['summary']}\nSource:{newsfeed['newsurl']}\nExperts say, the Market is {newsfeed['flow']}.")
        except Exception as e:
            print(f"Error: {e}")



action = input("Hello, this is your Personal Stock-Screener.\nFor Information about a Certain Stock Press \'1\'")
main()


