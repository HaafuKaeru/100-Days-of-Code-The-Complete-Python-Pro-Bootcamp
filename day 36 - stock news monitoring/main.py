import requests
import requests_cache
import os


# create requests caches
requests_cache.install_cache('stocks_cache')
requests_cache.install_cache('news_cache')


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHAVANTAGE_API_URL = "https://www.alphavantage.co/query"
NEWSAPI_API_URL = "https://newsapi.org"
# to add env variables in windows ps, run this in pycharm terminal or elevated ps and restart pycharm
# [System.Environment]::SetEnvironmentVariable("VARIABLE", "VALUE", "User")


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": os.getenv("ALPHAVANTAGE_API_KEY"),
    "datatype": "json"
}
stock_response = requests.get(ALPHAVANTAGE_API_URL, params=stock_params)
stock_response.raise_for_status()
print(f"Source: {'CACHE' if getattr(stock_response, 'from_cache', False) else 'API'}")
daily_results = dict(stock_response.json()["Time Series (Daily)"])
# print(daily_results)
gestern = sorted(daily_results.keys())[-2]
gestern_closing = float(daily_results[gestern]["4. close"])
vorgestern = sorted(daily_results.keys())[-34]
vorgestern_closing = float(daily_results[vorgestern]["4. close"])
print(vorgestern_closing, gestern_closing)
diff_percentage = (gestern_closing - vorgestern_closing) / gestern_closing * 100
print(diff_percentage)
if abs(diff_percentage) > 5:
    print("Get News")


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file 
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.
"""

