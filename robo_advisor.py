#robo_advisor.py
import json
import os
import requests
import datetime
import statistics
from dotenv import load_dotenv
from pandas import DataFrame

#################################
##Get secret API code from .env##
#################################

load_dotenv() #> loads contents of the .env file into the script's environment
API_KEY = os.environ.get("MY_API_KEY")
#print(API_KEY)

#Get stock Ticker from user
stockTicker = input("Which stock would you like to get information on? ")

#validates for irregular inputs of stock tickers
if stockTicker.isalpha() and len(stockTicker) <= 4:
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}".format(stockTicker, API_KEY)
    print(request_url)

    #Try block for invalid call
    try:
        #requests the info at the URL
        response = requests.get(request_url)
        print("RESPONSE STATUS: " + str(response.status_code))

        #parses this data from json to dict
        parsed_response = json.loads(response.text)
        
        #The Time Series (Daily) dict of the larger dict
        tsd = parsed_response["Time Series (Daily)"] #> 'dict'

        #Gets list of all keys in tsd (days) and converts to list
        day_keys = tsd.keys() #> 'dict_keys' of all the day values
        days = list(day_keys) #> 'list' of all the day values

        ###################################
        ##Starts the informational output##
        ###################################
        dashes = "-----------------------"
        print(dashes)
        print("STOCK SYMBOL: " + stockTicker)

        print(dashes)
        print("CRUNCHING THE DATA...")
        print(dashes)

        timeStamps = []
        opens = []
        highs = []
        lows = []
        closes = []
        volumes = []

        #Loops through all stocks to append to previous lists 
        for date in days:
            timeStamps.append(date)
            opens.append(tsd[date]["1. open"])
            highs.append(float(tsd[date]["2. high"]))
            lows.append(float(tsd[date]["3. low"]))
            closes.append(tsd[date]["4. close"])
            volumes.append(tsd[date]["5. volume"])

        #creates dictionnary of lists for data frame
        Stocks = {
                'timestamp': timeStamps,
                'open': opens,
                'high': highs,
                'low': lows, 
                'close': closes,
                'volume': volumes
                }


        #Help with dataframes: https://datatofish.com/export-dataframe-to-csv/
        #Also help from: https://github.com/hiepnguyen034/robo-stock/blob/master/robo_advisor.py#L29-L44
        df = DataFrame(Stocks)
        #exports to CSV file in data
        csv_file_path = os.path.join(os.path.dirname(__file__), "data", "Prices_" + stockTicker)
        export_csv = df.to_csv(csv_file_path, header=True)
        
        print("Data stored succesfully!")
        print(dashes)
        print("\nProccesing Data...\n")
        
        #####################
        ##Stock information##
        #####################

        print("Stock Selected: ".ljust(20) + stockTicker)

        #DateTime help from: https://docs.python.org/3/library/datetime.html
        timeRun = datetime.datetime.now()
        print("Run at: ".ljust(20) + str(timeRun.hour) + ":" + str(timeRun.minute) + " on " + str(timeRun.strftime("%B")) + " " + str(timeRun.day) + ", " + str(timeRun.year))


        #Gets date into readable datetime format
        newestDate = datetime.datetime.fromisoformat(days[0])
        print("Latest data from: ".ljust(20) + str(newestDate.strftime("%B")) + " " + str(newestDate.day) + ", " + str(newestDate.year))

        #Statistics help from: https://docs.python.org/3/library/statistics.html 

        #Closing stock price
        closingStock = tsd[days[0]]["4. close"]
        closingStock_USD = "${0:,.2f}".format(float(closingStock))
        print("The latest closing price is: ".ljust(30) + closingStock_USD)

        #recent average high
        recentHigh = statistics.mean(highs)
        recentHigh_USD = "${0:,.2f}".format(recentHigh)
        print("The recent average high price is: ".ljust(30) + recentHigh_USD)

        #recent avaerage low
        recentLow = statistics.mean(lows)
        recentLow_USD = "${0:,.2f}".format(recentLow)
        print("The recent average high price is: ".ljust(30) + recentLow_USD)

        difference = recentHigh - recentLow
        averageStockPrice = (recentHigh + recentLow)/2
        percentDifference = difference / averageStockPrice

        if percentDifference > .10 and float(closingStock) < recentLow:
            print("You should buy this stock because it has an above average volatility, with a below average closing price,\n Therefore, this stock could have a big jump up.")
        elif float(closingStock) < recentLow:
            print("Although this stock is at a relative low, you should not buy it as it is not very volatile and, \ntherefore, will not earn much money")
        else:
            print("You should not buy this stock because it is not very volatile nor is it at a relative low.")



        
    except requests.exceptions.ConnectionError:
        print("Sorry we can't find any trading data for that stock symbol.")
else:
    print("Sorry this doesn't seem like an existing stock ticker. \nPlease ensure that your choice only contains letters and is less than four characters.")
