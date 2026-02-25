print("SCRIPT STARTED — TEST MODE (10 requests max)")

import requests
from bs4 import BeautifulSoup
import re
import time

# 👉 Insert your ScraperAPI key here
SCRAPER_API_KEY = "0ebb6acaf4d5e302329a5521e36dbbfc"

def proxy_get(url):
    proxy_url = (
        f"https://api.scraperapi.com?"
        f"api_key={SCRAPER_API_KEY}"
        f"&premium=true"
        f"&country_code=us"
        f"&render=true"
        f"&browser=true"
        f"&url={url}"
    )
    return requests.get(proxy_url, timeout=60)


def scrape_yelp_test(query, location):
    print(f"Scraping Yelp TEST for: {query} in {location}")

    url = (
        "https://www.yelp.com/search?"
        f"find_desc={query.replace(' ', '+')}"
        f"&find_loc={location.replace(' ', '+')}"
        f"&start=0"
    )

    print("Fetching:", url)
    r = proxy_get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    businesses = soup.select("div.container__09f24__21w3G")

    results = []
    for biz in businesses[:10]:  # LIMIT TO FIRST 10
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

    print(f"Collected {len(results)} businesses (TEST MODE)")
    return results


def extract_emails_test(url):
    if not url or "yelp.com" in url:
        return None

    print(f"Extracting emails from: {url}")

    try:
        r = proxy_get(url)
    except:
        return None

    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", r.text)
    return list(set(emails)) if emails else None


def run_scraper():
    query = "coffee shops"
    location = "Tampa, FL"

    yelp_results = scrape_yelp_test(query, location)

    final_data = []
    for biz in yelp_results:
        emails = extract_emails_test(biz["website"])
        biz["emails"] = emails
        final_data.append(biz)
        time.sleep(1)

    print("\nFINAL RESULTS (TEST MODE):")
    for biz in final_data:
        print(biz)


if __name__ == "__main__":
    run_scraper()

def proxy_get(url):
    proxy_url = (
        f"https://api.scraperapi.com?"
        f"api_key={SCRAPER_API_KEY}"
        f"&premium=true"
        f"&country_code=us"
        f"&render=true"
        f"&browser=true"
        f"&url={url}"
    )
    return requests.get(proxy_url, timeout=60)


def scrape_yelp_test(query, location):
    print(f"Scraping Yelp TEST for: {query} in {location}")

    url = (
        "https://www.yelp.com/search?"
        f"find_desc={query.replace(' ', '+')}"
        f"&find_loc={location.replace(' ', '+')}"
        f"&start=0"
    )

    print("Fetching:", url)
    r = proxy_get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    businesses = soup.select("div.container__09f24__21w3G")

    results = []
    for biz in businesses[:10]:  # LIMIT TO FIRST 10
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

    print(f"Collected {len(results)} businesses (TEST MODE)")
    return results


def extract_emails_test(url):
    if not url or "yelp.com" in url:
        return None

    print(f"Extracting emails from: {url}")

    try:
        r = proxy_get(url)
    except:
        return None

    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", r.text)
    return list(set(emails)) if emails else None


def run_scraper():
    query = "coffee shops"
    location = "Tampa, FL"

    yelp_results = scrape_yelp_test(query, location)

    final_data = []
    for biz in yelp_results:
        emails = extract_emails_test(biz["website"])
        biz["emails"] = emails
        final_data.append(biz)
        time.sleep(1)

    print("\nFINAL RESULTS (TEST MODE):")
    for biz in final_data:
        print(biz)


if __name__ == "__main__":
    run_scraper()

def proxy_get(url):
    proxy_url = f"https://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={url}"
    return requests.get(proxy_url, timeout=60)

def scrape_yelp(query, location, pages=10):
    print(f"Scraping Yelp for: {query} in {location}")

    results = []

    for page in range(pages):
        url = (
            "https://www.yelp.com/search?"
            f"find_desc={query.replace(' ', '+')}"
            f"&find_loc={location.replace(' ', '+')}"
            f"&start={page*10}"
        )

        print("Fetching:", url)
        r = proxy_get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        # Container selector may need adjustment over time
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
    if not url or "yelp.com" in url:
        return None

    print(f"Extracting emails from: {url}")

    try:
        r = proxy_get(url)
    except:
        return None

    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", r.text)
    return list(set(emails)) if emails else None


def run_scraper():
    # 👉 You can change these to any category/city
    query = "coffee shops"
    location = "Tampa, FL"

    yelp_results = scrape_yelp(query, location, pages=10)

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


