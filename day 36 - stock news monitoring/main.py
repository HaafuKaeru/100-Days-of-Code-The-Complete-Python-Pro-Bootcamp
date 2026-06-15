import requests
import requests_cache
import os


# create requests caches for testing
# requests_cache.install_cache('stocks_cache')
# requests_cache.install_cache('news_cache')


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHAVANTAGE_API_URL = "https://www.alphavantage.co/query"
NEWSAPI_API_URL = "https://newsapi.org/v2/everything"
TEXTBEE_API_URL = "https://api.textbee.dev/api/v1"
# to add env variables in windows ps, run this in pycharm terminal or elevated ps and restart pycharm
# [System.Environment]::SetEnvironmentVariable("VARIABLE", "VALUE", "User")


def api_get(api_url: str, parameters: dict) -> str:
    rsp = requests.get(api_url, params=parameters)
    rsp.raise_for_status()
    print(f"Source: {'CACHE' if getattr(rsp, 'from_cache', False) else 'API'}")
    return rsp.json()

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": os.getenv("ALPHAVANTAGE_API_KEY"),
    "datatype": "json"
}
daily_results_json = api_get(ALPHAVANTAGE_API_URL, stock_params)
daily_results = dict(daily_results_json["Time Series (Daily)"])
gestern = sorted(daily_results.keys())[-2]
gestern_closing = float(daily_results[gestern]["4. close"])
vorgestern = sorted(daily_results.keys())[-3]
vorgestern_closing = float(daily_results[vorgestern]["4. close"])
diff_percentage = (gestern_closing - vorgestern_closing) / gestern_closing * 100

# debug
print(vorgestern, gestern)
print(vorgestern_closing, gestern_closing)
print(diff_percentage)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
if abs(diff_percentage) > 1:
    news_params = {
        "apiKey": os.getenv("NEWSAPI_API_KEY"),
        "q": COMPANY_NAME,
        "sortBy": "publishedAt",
        "to": gestern,
        "language": "en",
    }
    news_results_json = api_get(NEWSAPI_API_URL, news_params)
    news_results = news_results_json["articles"]
    top3_articles = news_results[:15]

    ## STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.
    msg = "[STOCK ALERT]\n\n"
    msg += (f"{STOCK}: {'🔺' if diff_percentage > 0 else '🔻'}{int(diff_percentage)}%\n\n"
            f"Latest news regarding {COMPANY_NAME}\n\n")
    for article in top3_articles:
        date = article["publishedAt"].split("T")[0]
        title = article["title"]
        brief = article["description"]
        url = article["url"]
        msg += (f"Dated: {date}\n"
                f"📢 {title}\n"
                f"📰 {brief}\n"
                f"Read more: {url}\n\n")

    text_rsp = requests.post(
        url=f'{TEXTBEE_API_URL}/gateway/devices/{os.getenv("TEXTBEE_PHONE_ID")}/send-sms',
        json={'recipients': [os.getenv("PHONE_NUMBER")], 'message': msg},
        headers={'x-api-key': os.getenv("TEXTBEE_API_KEY")}
    )
    text_rsp.raise_for_status()