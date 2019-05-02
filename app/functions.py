#Functions for robo app
from dotenv import load_dotenv
import os

def to_USD(Number):
    Number = float(Number)
    Number = "${0:,.2f}".format(Number)
    return Number

def compile_URL(stockTicker):
    load_dotenv() #> loads contents of the .env file into the script's environment
    API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}".format(stockTicker, API_KEY)
    return request_url
