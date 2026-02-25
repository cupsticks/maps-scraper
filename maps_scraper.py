print("SCRIPT STARTED")

import requests
from bs4 import BeautifulSoup
import re
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def scrape_yelp(query, location, pages=5):
    print(f"Scraping Yelp for: {query} in {location}")

    results = []

    for page in range(pages):
        url = f"https://www.yelp.com/search?find_desc={query.replace(' ', '+')}&find_loc={location.replace(' ', '+')}&start={page*10}"
        print("Fetching:", url)

        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")

        businesses = soup.select("div.container__09f24__21w3G")

        for biz in businesses:
            name_tag = biz.select_one("a.css-1m051bw")
            phone_tag = biz.select_one("p.css-1p9ibgf")
            website_tag = biz.select_one("a.css-1idmmu3")
            address_tag = biz.select_one("address")

            if not name_tag:
                continue

            results.append({
                "name": name_tag.text.strip(),
                "phone": phone_tag.text.strip() if phone_tag else None,
                "website": website_tag["href"] if website_tag else None,
                "address": address_tag.text.strip() if address_tag else None
            })

        time.sleep(1)

    print(f"Collected {len(results)} businesses from Yelp")
    return results


def extract_emails(url):
    if not url or "yelp" in url:
        return None

    print(f"Extracting emails from: {url}")

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
    except:
        return None

    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", r.text)
    return list(set(emails)) if emails else None


def run_scraper():
    query = "coffee shops"
    location = "Tampa, FL"

    yelp_results = scrape_yelp(query, location, pages=10)  # 10 pages = ~100 results

    final_data = []
    for biz in yelp_results:
        emails = extract_emails(biz["website"])
        biz["emails"] = emails
        final_data.append(biz)
        time.sleep(1)

    print("\nFINAL RESULTS:")
    for biz in final_data:
        print(biz)


if __name__ == "__main__":
    run_scraper()
