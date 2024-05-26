import requests

from api import api_key()

def geturl(unique):
    return f'https://www.alphavantage.co/query?function={unique}&apikey={api_key()}'



def getdata(url):
    return requests.get(url).json()
    
topics = ["blockchain", "earnings", "ipo", "mergers_and_acquisitions", "financial_markets", "economy_fiscal", "economy_monetary", "economy_macro", "energy_transportation", "finance", "life_sciences", "manufacturing", "real_estate", "retail_wholesale", "technology"]


def main():
    global stock
    global apikey
    #apikey = open("api_key.txt")

    while True:
        try:
            if action =="1":
                stock = input("What Stock do you want to know about?")
                data = getdata(geturl(f"SYMBOL_SEARCH&keywords={stock}"))
                if len(data) <2:
                    raise BadRequest
                basicdata = {
                    "symbol" : data["bestMatches"][0]["1. symbol"],
                    "name"   : data["bestMatches"][0]["2. name"],
                    "region" : data["bestMatches"][0]["4. region"] }
                price_data = getdata(geturl(f'TIME_SERIES_INTRADAY&{basicdata["symbol"]}=IBM&interval=5min'))
                if len(price_data) <2:
                    raise BadRequest
                price = {
                    "open"   : price_data["Time Series (5min)"][0]["1. open"],
                    "high"   : price_data["Time Series (5min)"][0]["2. high"],
                    "low"    : price_data["Time Series (5min)"][0]["3. low"],
                    "close"  : price_data["Time Series (5min)"][0]["4. close"] }
                basicdata["price"] = price
                print(basicdata)

            if action =="2":
                i = 0
                search = input("Search by Topic or by Stock?\n\'1\' for Topic\n\'2\' for Stock\n\'.\' for all News")
                if search == ".":
                    news = getdata(geturl("NEWS_SENTIMENT"))
                elif search == "2":
                    ticker = input("Enter Ticker Symbol")
                    news = getdata(geturl(f"NEWS_SENTIMENT&tickers={ticker}"))
                elif search == "1":
                    while True:
                        topic = input("Enter Topic")
                        if topic in topics:
                            news = getdata(geturl(f"NEWS_SENTIMENT&topics={topic}"))
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
                    i+=1
        except BadRequest:
            print("Got no API answer")
        except:
            pass



action = input("Hello, this is your Personal Stock-Screener.\nFor Information about a Certain Stock Press \'1\'")
main()


