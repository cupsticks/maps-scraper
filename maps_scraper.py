print("SCRIPT STARTED")

import requests
import re
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def google_search(query):
    print(f"Searching Google for: {query}")

    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    for g in soup.select("div.g"):
        name = g.select_one("h3")
        link = g.select_one("a")
        snippet = g.select_one(".VwiC3b")

        if not name or not link:
            continue

        website = link["href"]

        results.append({
            "name": name.text,
            "website": website,
            "snippet": snippet.text if snippet else None
        })

    print(f"Found {len(results)} results")
    return results


def extract_emails(url):
    print(f"Extracting emails from: {url}")

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
    except:
        return None

    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", r.text)
    return list(set(emails)) if emails else None


def run_scraper():
    query = "coffee shops in tampa"

    results = google_search(query)

    final_data = []
    for biz in results:
        emails = extract_emails(biz["website"])
        biz["emails"] = emails
        final_data.append(biz)
        time.sleep(1)

    print("\nFINAL RESULTS:")
    for biz in final_data:
        print(biz)


if __name__ == "__main__":
    run_scraper()
