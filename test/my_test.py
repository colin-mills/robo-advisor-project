from app.functions import to_USD, compile_URL, os, get_response, transform_response
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")

def test_to_USD():
    assert to_USD(4) == "$4.00" #should have two decimal points
    assert to_USD(57.9999) == "$58.00" #test rounding 
    assert to_USD(99999.99) == "$99,999.99" #test commas 
    assert to_USD(100000) == "$100,000.00" #test commas and decimals 
    assert to_USD(8.00000000001) == "$8.00" #Should round down

def test_compile_URL():
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMZN&apikey={}".format(API_KEY)
    assert compile_URL("AMZN") == request_url

def test_get_response():
     request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMZN&apikey={}".format(API_KEY)
     response = get_response(request_url)
     response = list(response)
     assert response[0] == "Meta Data"
     assert response[1] == "Time Series (Daily)"

def test_transform_response():
    testDict = {"first": 1, "second" : 2}
    newList = transform_response(testDict)

    assert type(newList) == list
    assert newList[0] == "first"
    assert newList[1] == "second"
