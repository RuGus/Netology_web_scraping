import requests
from bs4 import BeautifulSoup
from requests.api import get
import datetime

url = "https://habr.com/ru/all/"
KEYWORDS = ["дизайн", "фото", "web", "python"]


def habr_check_keyword_in_article(url: str, keywords: list or tuple) -> bool:
    with requests.get(url) as article_full:
        article_full.raise_for_status()
    soup_article_content = BeautifulSoup(article_full.text, features="html5lib")
    content = soup_article_content.find(id="post-content-body").text
    result = False
    for word in keywords:
        if content.find(word) != -1:
            result = True
            break
    return result


def habr_articles_by_keywors(url: str, keywords: list or tuple) -> None:
    with requests.get(url) as responce:
        responce.raise_for_status()
    soup_page = BeautifulSoup(responce.text, features="html5lib")
    articles = soup_page.find_all("article")
    for article in articles:
        create_datetime = datetime.datetime.strptime(
            article.find("time")["datetime"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        header = article.find("h2")
        title = header.text
        link = None
        if header.find("a"):
            link = "https://habr.com" + header.find("a")["href"]
        if habr_check_keyword_in_article(link, keywords):
            print(create_datetime.date(), title, link)


if __name__ == "__main__":
    habr_articles_by_keywors(url, KEYWORDS)
