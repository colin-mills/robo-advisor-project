# ROBO-Advisor-project
Third in class project dealing with API's

## Prerequisites

* Requires Python 3.7.
* pip

## Instalation 

1. Clone or download this repository to your computer

2. install needed packages from within an environment once you have navigated to it on your command line:

```
pip install -r requirements.txt
```

## Usage

1. Request an API key from https://www.alphavantage.co/

2. create a .env file in this project storing your API key as such
```
ALPHAVANTAGE_API_KEY= "Your Key"
```
3. Execute the "robo_advisor" program:
```
python app/robo_advisor.py
```
## Testing

run a test:

```sh
pytest
```
* For continous integration you need to go to the settings of your repository on Travis CI and input the API key 
