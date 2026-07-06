import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇
response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")

# css_selectors = [
#     "div.gallery",
#     "section.gallery__content-item.gallery__content-item--gallery",
#     "div.article-title-description",
#     "div.article-title-description__text",
#     "h3",
# ]
# movies = [header.text for header in soup.select(" ".join(css_selectors))]
movies = soup.find_all(name="h3", class_="title")
movie_titles = [movie.text for movie in movies]
movie_titles = movie_titles[::-1]

movies_string = "\n".join(movie_titles)
with open("movies.txt", "w", encoding='utf-8') as f:
    f.writelines(movies_string)



