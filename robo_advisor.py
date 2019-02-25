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

dashes = "--------------------------------------------"
stars =  "************************************************************************************************"
stockList = []
Continue = ""
Ticker = ""
nextStock = 0
firstMessage = False
riskLevelMessage = False

#Get stock Ticker from user
while Ticker != 'DONE': 
    Ticker = input("Please enter the stock sticker you would you like to get information on. (Eg. \"AMZN\" \"AAPL\" \"GOOG\"): ")
    Ticker = Ticker.upper()
    #validates for irregular inputs of stock tickers
    if Ticker == "DONE":
        ##Do nothing
        print("Fetching data from the internet...")
    elif Ticker.isalpha() and len(Ticker) <= 5:
        stockList.append(Ticker)
    else:
        print("Sorry " +  Ticker + " doesn't seem like an existing stock ticker. \nPlease ensure that your choice only contains letters and is five or less characters.")
    
    if not firstMessage:
        print("If you have more stocks to input please continue to enter them one at a time, otherwise input \"DONE\" ")
        firstMessage = True

for stockTicker in stockList:
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}".format(stockTicker, API_KEY)
    print(request_url)

    #Try block for invalid call
    try:
        #requests the info at the URL
        print(dashes)
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

        #recent average low
        recentLow = statistics.mean(lows)
        recentLow_USD = "${0:,.2f}".format(recentLow)
        print("The recent average low price is: ".ljust(35) + recentLow_USD)
        print(dashes)

        ###############################
        ##Calculate purchase decision## 
        ###############################

        maxValue = max(highs)
        minValue = min(lows)
        difference = maxValue - minValue
        averageStockPrice = (recentHigh + recentLow)/2
        percentDifference = difference / averageStockPrice

        if riskLevelMessage == False:
            risk = .2

            riskLevel = input("How much risk are you willing to take on in an investment?\n enter \"HIGH\", \"MED\", or \"LOW\": ")
            riskLevel = riskLevel.upper()
            
            if riskLevel == "HIGH":
                risk = .3
            elif riskLevel == "MED":
                risk = .2
            elif riskLevel == "LOW":
                risk = .1
            else:
                print("Invalid input, reverting to default risk value of 20% volatility.") 
            
            print(dashes)
            riskLevelMessage = True


        print("Evaluating stock purchase decision...")
        print("Recomendation: ")
        if percentDifference > risk and float(closingStock) < recentLow:
            print(" You should buy " + stockTicker + " because it has an above average volatility for you, with a below average closing price,\n Therefore this stock could have a big jump up.")
        elif float(closingStock) < recentLow:
            print(" Although " + stockTicker + " is at a relative low, you should not buy it as it is not as volatile as you indicated you were willing to risk and, \n Therefore you will not earn as much money.")
        else:
            print(" You should not buy " + stockTicker + " because it is not very volatile nor is it at a relative low. \n If you do purchase it is recomended that you wait until its price is at or below " + recentLow_USD + ".")

        print(dashes)

        ###################################
        ##Implemennting Matplotlib Graphs##
        ###################################

        graphDecision = input("If you would like to see a graph of this stock value over time please enter \"YES\" Otherwise, press enter: ")
        graphDecision = graphDecision.upper()

        if graphDecision == "YES":
            dayPlot = []
            x = len(highs)

            for number in highs:
                dayPlot.append(x)
                x = x-1

            plt.plot(dayPlot, highs)
            plt.plot(dayPlot, lows)
            plt.title("Graph of " + stockTicker + " High and Low values over the past 100 days")
            plt.ylabel("Stock Values in USD ($)")
            plt.xlabel("Days")
            plt.show()

        nextStock = nextStock + 1

        if nextStock < len(stockList) and graphDecision == "YES":
            Continue = input("Please close out of graph and press enter to view stock information on " + stockList[nextStock] + ": ")
            print(stars)
            print(stars)
        elif nextStock < len(stockList):
            Continue = input("Press enter to view stock information on " + stockList[nextStock] + ": ")
            print(stars)
            print(stars)
        else:
            print("\nAll stocks have been viewed.")

    except requests.exceptions.ConnectionError:
        print("Sorry we can't find any trading data for " + stockTicker + ".")
    except KeyError:
        print("Sorry we can't find any trading data for " + stockTicker + ".")

