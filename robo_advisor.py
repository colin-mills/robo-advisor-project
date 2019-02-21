#robo_advisor.py
import json
import os
import requests
import datetime
import statistics
from dotenv import load_dotenv
from pandas import DataFrame
import matplotlib.pyplot as plt

#################################
##Get secret API code from .env##
#################################

load_dotenv() #> loads contents of the .env file into the script's environment
API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
#print(API_KEY)

stockList = []
Continue = ""

#Get stock Ticker from user
while Continue != 'n' and Continue != 'N':
    Ticker = input("Which stock would you like to get information on? ")
    stockList.append(Ticker)
    Continue = input("More stocks to input? (y/n): ")

for stockTicker in stockList:
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
            dashes = "--------------------------------------------"
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

            print(dashes)
            print("Stock Selected: " + stockTicker)

            #DateTime help from: https://docs.python.org/3/library/datetime.html
            timeRun = datetime.datetime.now()
            print("Run at: " + str(timeRun.hour) + ":" + str(timeRun.minute) + " on " + str(timeRun.strftime("%B")) + " " + str(timeRun.day) + ", " + str(timeRun.year))


            #Gets date into readable datetime format
            newestDate = datetime.datetime.fromisoformat(days[0])
            print("Latest data from: " + str(newestDate.strftime("%B")) + " " + str(newestDate.day) + ", " + str(newestDate.year))
            print(dashes)
            #Statistics help from: https://docs.python.org/3/library/statistics.html 

            #Closing stock price
            closingStock = tsd[days[0]]["4. close"]
            closingStock_USD = "${0:,.2f}".format(float(closingStock))
            print("The latest closing price is: ".ljust(35) + closingStock_USD)

            #recent average high
            recentHigh = statistics.mean(highs)
            recentHigh_USD = "${0:,.2f}".format(recentHigh)
            print("The recent average high price is: ".ljust(35) + recentHigh_USD)

            #recent avaerage low
            recentLow = statistics.mean(lows)
            recentLow_USD = "${0:,.2f}".format(recentLow)
            print("The recent average low price is: ".ljust(35) + recentLow_USD)
            print(dashes)
            difference = recentHigh - recentLow
            averageStockPrice = (recentHigh + recentLow)/2
            percentDifference = difference / averageStockPrice

            if percentDifference > .10 and float(closingStock) < recentLow:
                print("You should buy this stock because it has an above average volatility, with a below average closing price,\n Therefore this stock could have a big jump up.\n\n")
            elif float(closingStock) < recentLow:
                print("Although this stock is at a relative low, you should not buy it as it is not very volatile and, \n Therefore you will not earn much money.\n\n")
            else:
                print("You should not buy this stock because it is not very volatile nor is it at a relative low.\n\n")

            char = input("Press enter when you are ready to view a graph of the stock value over time.")

            dayPlot = []
            x = 0

            for number in highs:
                x = x+1
                dayPlot.append(x)

            plt.plot(dayPlot, highs)
            plt.plot(dayPlot, lows)
            plt.title("Graph of " + stockTicker + " High and Low Values over the past 100 days")
            plt.ylabel("Sales in USD ($)")
            plt.xlabel("Days")
            plt.show()

        except requests.exceptions.ConnectionError:
            print("Sorry we can't find any trading data for that stock symbol.")
        except KeyError:
            print("Sorry we can't find any trading data for that stock symbol.")
    else:
        print("Sorry this doesn't seem like an existing stock ticker. \nPlease ensure that your choice only contains letters and is less than four characters.")
