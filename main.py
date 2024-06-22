from twilio.rest import Client
import datetime as dt
import requests
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

#twilio information
TWILIO_SID = 'AC1e4e3bc97c3521af65be03937877796b'
TWILIO_AUTH = '09fae01d2beaeb1d24e6dcd0f59f05dc'
FROM_NUMBER = 'whatsapp:+14155238886'
TO_NUMBER = 'whatsapp:+972544989488'

STOCK_API ='W5VCCLTQ35UQD31B'
DECREASE_OR_INCREASE = ""
#Function for sending the news of company of the stock by twilio
def send_sms(messages,decrease_increase,stock,precentage):
    client = Client(TWILIO_SID,TWILIO_AUTH)
    for message in messages:
        client.messages.create(from_=FROM_NUMBER, to=TO_NUMBER, body=f'the stock of {stock} is {decrease_increase}{abs(precentage)} \n{message}')

#get the stock prices
def get_stock_prices(stock):
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol':stock,
        'apikey':STOCK_API,
    }
    response = requests.get(url,params=params)
    response.raise_for_status()
    stock_prices = response.json()['Time Series (Daily)']
    return stock_prices

#get the stock news
def get_stock_news(company_name):
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'NEWS_SENTIMENT',
        'tickers': company_name,
        'limit':3,
        'apikey': STOCK_API
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    stock_news = response.json()["feed"]
    return stock_news


stock_prices = get_stock_prices(STOCK)

#getting the dates of today and yesterday and extracting the closing stock from today and yesterday
today = dt.datetime.now().date()
yesterday = str(dt.datetime(today.year,today.month,today.day -1).date())
today_closing_prices = float(stock_prices[str(today)]['4. close'])
yesterday_closing_prices = float(stock_prices[yesterday]['4. close'])

#get the precentage of increase or decrease
precentage = (today_closing_prices - yesterday_closing_prices) / yesterday_closing_prices * 100
if precentage < 0:
    DECREASE_OR_INCREASE = '🔻'
else:
    DECREASE_OR_INCREASE = '🔺'
#if precentage is greater then 5% get the news of stock and send in sms with twilio
if abs(precentage) > 5:
    stock_news = get_stock_news(COMPANY_NAME)
    news = [stock_news['title'] for news in stock_news[:3]]
    send_sms(news,DECREASE_OR_INCREASE, STOCK,precentage)
