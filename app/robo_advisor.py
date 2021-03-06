#robo_advisor.py
import datetime
import statistics
from pandas import DataFrame
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from functions import to_USD, compile_URL, os, requests, get_response, transform_response

#Variable definitions
dashes = "---------------------------------------------"
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
    request_url = compile_URL(stockTicker)

    try: #Try block for invalid call
        ##requests and parses the info at the URL
        parsed_response = get_response(request_url)

        #The Time Series (Daily) dict of the larger dict
        tsd = parsed_response["Time Series (Daily)"] #> 'dict'

        #converts dict into a list of the days
        days = transform_response(tsd) #list(day_keys) #> 'list' of all the day values

        ###################################
        ##Starts the informational output##
        ###################################
        print(dashes)
        print("STOCK SYMBOL: " + stockTicker)

        print(dashes)
        print("CRUNCHING THE DATA...")
        print(dashes)

        #reassigns for each loop through if more than one
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
        csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "Prices_" + stockTicker + ".csv")
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
        print("The latest closing price is: ".ljust(35) + to_USD(closingStock).rjust(10))

        #recent average high
        recentHigh = max(highs)
        print("The recent high price is: ".ljust(35) + to_USD(recentHigh).rjust(10))

        #recent average low
        recentLow = min(lows)
        print("The recent low price is: ".ljust(35) + to_USD(recentLow).rjust(10))
        print(dashes)

        ###############################
        ##Calculate purchase decision## 
        ###############################
        difference = recentHigh - recentLow
        averageHigh = statistics.mean(highs)
        averageLow = statistics.mean(lows)
        averageStockPrice = (averageHigh + averageLow)/2
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
            print(" You should not buy " + stockTicker + " because it is not very volatile nor is it at a relative low. \n If you do purchase it is recomended that you wait until its price is at or below " + to_USD(averageLow) + ".")

        print(dashes)

        ###################################
        ##Implemennting Matplotlib Graphs##
        ###################################

        graphDecision = input("If you would like to see a graph of this stock value over time please enter \"YES\" otherwise, press enter: ")
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

