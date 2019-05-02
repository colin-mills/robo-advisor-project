#Functions for robo app
from dotenv import load_dotenv
import os
import json
import requests

def to_USD(Number):
    Number = float(Number)
    Number = "${0:,.2f}".format(Number)
    return Number

def compile_URL(stockTicker):
    load_dotenv() #> loads contents of the .env file into the script's environment
    API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}".format(stockTicker, API_KEY)
    return request_url

def get_response(request_url):
    #issues request
    response = requests.get(request_url)
    #parses this data from json to dict

    parsed_response = json.loads(response.text)
    return parsed_response

def transform_response(tsd):
    #Gets list of all keys in tsd (days) and converts to list
    day_keys = tsd.keys() #> 'dict_keys' of all the day values
    days = list(day_keys) #> 'list' of all the day values
    return days