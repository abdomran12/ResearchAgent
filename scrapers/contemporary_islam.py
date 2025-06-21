
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_contemporary_islam():
    url = "https://link.springer.com/journal/11562/volumes-and-issues"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for article in soup.select("a[href*='/article/']")[:5]:
        title = article.get_text(strip=True)
        link = "https://link.springer.com" + article.get("href")
        articles.append({
            "journal": "Contemporary Islam",
            "title": title,
            "authors": ["Unknown"],
            "date": datetime.now().strftime("%Y-%m-%d"),
            "abstract": "Abstract not parsed yet.",
            "summary": title[:300],
            "full_text": link
        })

    return articles
