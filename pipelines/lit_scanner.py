
import os
import json
from datetime import datetime
from scrapers.contemporary_islam import scrape_contemporary_islam
from scrapers.arab_studies_journal import scrape_arab_studies_journal
from scrapers.ajiss import scrape_ajiss
from scrapers.arab_law_quarterly import scrape_arab_law_quarterly
from scrapers.der_islam import scrape_der_islam
from scrapers.journal_islamic_ethics import scrape_journal_islamic_ethics
from scrapers.quranic_studies import scrape_quranic_studies
from scrapers.sociology_of_islam import scrape_sociology_of_islam
import requests
from bs4 import BeautifulSoup

def log(msg):
    print(f"[lit_scanner] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")

def save_results(results):
    os.makedirs("data", exist_ok=True)
    filename = f"data/journal_results_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    log(f"Saved {len(results)} results to {filename}")

def scrape_arxiv():
    try:
        log("Scraping arXiv...")
        base_url = "https://export.arxiv.org/rss/cs.AI"
        r = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(r.content, "xml")
        items = soup.find_all("item")
        results = []
        for item in items:
            title = item.title.text
            authors = ["arXiv"]
            date = datetime.now().strftime("%Y-%m-%d")
            abstract = item.description.text
            full_text = item.link.text
            summary = abstract[:300]
            results.append({
                "journal": "arXiv",
                "title": title,
                "authors": authors,
                "date": date,
                "abstract": abstract,
                "summary": summary,
                "full_text": full_text
            })
        return results
    except Exception as e:
        log(f"⚠️ Skipping arXiv due to error: {e}")
        return []

if __name__ == "__main__":
    log("Starting journal scraping pipeline...")
    results = []
    results += scrape_arxiv()
    results += scrape_contemporary_islam()
    results += scrape_arab_studies_journal()
    results += scrape_ajiss()
    results += scrape_arab_law_quarterly()
    results += scrape_der_islam()
    results += scrape_journal_islamic_ethics()
    results += scrape_quranic_studies()
    results += scrape_sociology_of_islam()
    save_results(results)
    log("Finished journal scraping pipeline.")
