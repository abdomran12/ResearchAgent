
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_sociology_of_islam():
    # Replace this URL with the journal's page
    url = "https://example.com"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for article in soup.select("a[href*='/article']")[:5]:
        title = article.get_text(strip=True)
        link = "https://example.com" + article.get("href")
        articles.append({
            "journal": "Sociology of Islam",
            "title": title,
            "authors": ["Unknown"],
            "date": datetime.now().strftime("%Y-%m-%d"),
            "abstract": "Abstract not parsed yet.",
            "summary": title[:300],
            "full_text": link
        })

    return articles
