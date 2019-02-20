#robo_advisor.py
import json
import os
import requests
from dotenv import load_dotenv
from pandas import DataFrame

#load_dotenv() #> loads contents of the .env file into the script's environment
#
#API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
##print(API_KEY)

# goal: print the latest closing price

load_dotenv() #> loads contents of the .env file into the script's environment

API_KEY = os.environ.get("MY_API_KEY")
#print(API_KEY)

stockTicker = input("Which stock would you like to get information on? ")

stockTicker = "AMZN"

if stockTicker.isalpha() and len(stockTicker) <= 4:
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}".format(stockTicker, API_KEY)
    print(request_url)

    try:
        response = requests.get(request_url)

        print("RESPONSE STATUS: " + str(response.status_code))
        parsed_response = json.loads(response.text)


        #print(parsed_response["Time Series (Daily)"]["2019-02-19"]["4. close"])
        # > '1627.5800'

        tsd = parsed_response["Time Series (Daily)"] #> 'dict'
        #
        # What keys or attributes does this dictionary have?
        # ... see: https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/notes/python/datatypes/dictionaries.md
        day_keys = tsd.keys() #> 'dict_keys' of all the day values

        #
        # convert weird dict_keys datatype to a list so we can work with it!
        days = list(day_keys) #> 'list' of all the day values
        #print(days)
        #print(days[0]) # 'str' of the latest day!
        #latest_day = days[0] #> '2019-02-19'
        #
        #print(parsed_response["Time Series (Daily)"][latest_day]["4. close"])
        # > '1627.5800'
        #
        #print(tsd[latest_day]["4. close"])
        # > '1627.5800'

        print("-----------------------")
        print("STOCK SYMBOL: " + stockTicker)

        print("-----------------------")
        print("CRUNCHING THE DATA...")

        timeStamps = []

        opens = []
        highs = []
        lows = []
        closes = []
        volumes = []

        for date in days:
            timeStamps.append(str(date))
            opens.append(tsd[date]["1. open"])
            highs.append(tsd[date]["2. high"])
            lows.append(tsd[date]["3. low"])
            closes.append(tsd[date]["4. close"])
            volumes.append(tsd[date]["5. volume"])
           

        Stocks = {
                'timestamp': timeStamps,
                'open': opens,
                'high': highs,
                'low': lows, 
                'close': closes,
                'volume': volumes
                }

        df = DataFrame(Stocks, columns= ['timestamps', 'open','high','low','close','volume'])

        #export_csv = df.to_csv (r"robo_advisor\data\prices_{}.csv".format(stockTicker), index = None, header=True) #Don't forget to add '.csv' at the end of the path

        print (df)

        print("-----------------------")
        print("LATEST CLOSING PRICE: $1,259.19")
    except requests.exceptions.ConnectionError:
        print("Sorry we can't find any trading data for that stock symbol.")
else:
    print("Sorry this doesn't seem like an existing stock ticker. \nPlease ensure that your choice only contains letters and is less than four characters.")
