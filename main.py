import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
NEWS_API_KEY = "2af6e17cccb048eaae2a840966b3b5ce"
STOCK_API_KEY = "C8YDEP8S0PPZZBN9"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
TWILIO_SID = "AC38293d6c68ab8c8a57a14e2faf70cf49"
TWILIO_AUTH_TOKEN = "d556849cd6ba7412198b3cb8589892ee"
TWILIO_NUM = "+18442753605"
MY_CELL_NUM = "YOUR NUMBER HERE"
CONVERT_TO_PERCENT = 100
STOCK_FUNCTION_PARAMETER = "TIME_SERIES_DAILY_ADJUSTED"
STOCK_DATA_CLOSE_KEY = "4. close"
STOCK_RESPONSE_KEY = "Time Series (Daily)"
NEWS_ARTICLE_KEY = "articles"
NUM_OF_ARTICLES = 3
ARTICLE_TITLE_KEY = "title"
ARTICLE_DESCRIPTION_KEY = "description"
PERCENTAGE_DIFFERENCE = 5
YESTERDAY_INDEX = 0
DAY_BEFORE_INDEX = 1


# diff_percentage() takes closing stock price from 2 days and returns the percentage difference
def diff_percentage() -> float:

    stock_params = {
        "function": STOCK_FUNCTION_PARAMETER,
        "symbol": STOCK_NAME,
        "apikey": STOCK_API_KEY
    }
    response = requests.get(STOCK_ENDPOINT, params=stock_params)
    response.raise_for_status()

    data = response.json()[STOCK_RESPONSE_KEY]
    data_list = [value for (key, value) in data.items()]
    yesterday_data = data_list[YESTERDAY_INDEX]
    yesterday_close_price = yesterday_data[STOCK_DATA_CLOSE_KEY]

    # Get the day before yesterday's closing stock price
    day_before_yesterday_data = data_list[DAY_BEFORE_INDEX]
    day_yesterday_close_price = day_before_yesterday_data[STOCK_DATA_CLOSE_KEY]

    difference = abs(float(yesterday_close_price)) - abs(float(day_yesterday_close_price))
    return (difference / float(yesterday_close_price)) * CONVERT_TO_PERCENT


# send_sms() gets 3 news articles on about the company in the COMPANY_NAME variable and sends them through sms.
def send_sms():
    news_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()[NEWS_ARTICLE_KEY]
    three_articles = articles[:NUM_OF_ARTICLES]

    formatted_articles = [f"Headline: {article[ARTICLE_TITLE_KEY]}. "
                          f"\nBrief: {article[ARTICLE_DESCRIPTION_KEY]}" for article in three_articles]


# Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=TWILIO_NUM,
            to=MY_CELL_NUM,
            )


# stock_alert() calls send_sms() to send message to phone if percentage returned by diff_percentage() is greater than 5.
def stock_alert():

    diff_percent = diff_percentage()

    if diff_percent > PERCENTAGE_DIFFERENCE:
        send_sms()


if __name__ == "__main__":
    stock_alert()
