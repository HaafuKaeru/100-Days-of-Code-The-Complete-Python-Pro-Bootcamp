from bs4 import BeautifulSoup
import requests


YC_HACKERNEWS_URL = "https://news.ycombinator.com/news"

response = requests.get(YC_HACKERNEWS_URL)
yc_webpage = response.text

soup = BeautifulSoup(yc_webpage, "html.parser")

titles = soup.select("td.title span.titleline")
article_texts = []
article_links = []
for title in titles:
    article = title.select_one("a")
    text = article.getText()
    article_texts.append(text)
    link = article.get("href")
    article_links.append(link)

article_upvotes = [int(score.text.split(' ')[0]) for score in soup.find_all(name="span", class_="score")]

# print(article_texts)
# print(article_links)
# print(article_upvotes)

highest_upvote = max(article_upvotes)
index = article_upvotes.index(highest_upvote)
print(article_texts[index])
print(article_links[index])