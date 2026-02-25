print("SCRIPT STARTED — DEBUG MODE")

import requests
from bs4 import BeautifulSoup
import re
import time

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


def scrape_yelp_debug(query, location):
    print(f"Scraping Yelp DEBUG for: {query} in {location}")

    url = (
        "https://www.yelp.com/search?"
        f"find_desc={query.replace(' ', '+')}"
        f"&find_loc={location.replace(' ', '+')}"
        f"&start=0"
    )

    print("Fetching:", url)
    r = proxy_get(url)
    html = r.text
    print(f"HTML length: {len(html)}")

    soup = BeautifulSoup(html, "html.parser")

    # Print page title to see what we actually got
    title = soup.title.text.strip() if soup.title else "NO TITLE"
    print(f"Page title: {title}")

    # If we get 0 matches, we’ll dump a snippet of HTML to logs
    results = []

    # Try multiple patterns for businesses
    selectors = [
        "div.container__09f24__21w3G",          # previous guess
        "li[class*='business']",                # generic business li
        "div[class*='businessName']",           # name container
    ]

    businesses = []
    for sel in selectors:
        found = soup.select(sel)
        print(f"Selector '{sel}' matched {len(found)} elements")
        if len(found) > 0 and not businesses:
            businesses = found

    if not businesses:
        print("No business containers found. Dumping HTML snippet:")
        print(html[:1500])
        return []

    for biz in businesses[:10]:
        # Try multiple ways to get name
        name_tag = (
            biz.select_one("a.css-1m051bw") or
            biz.select_one("a[class*='businessName']") or
            biz.select_one("a[href*='/biz/']")
        )
        phone_tag = biz.find("p", string=re.compile(r"\(\d{3}\)")) if biz else None
        website_tag = biz.select_one("a[href^='http']") if biz else None
        address_tag = biz.find("address") if biz else None

        if not name_tag:
            continue

        results.append({
            "name": name_tag.text.strip(),
            "phone": phone_tag.text.strip() if phone_tag else None,
            "website": website_tag["href"] if website_tag else None,
            "address": address_tag.text.strip() if address_tag else None
        })

    print(f"Collected {len(results)} businesses (DEBUG MODE)")
    return results


def extract_emails_debug(url):
    if not url or "yelp.com" in url:
        return None

    print(f"Extracting emails from: {url}")

    try:
        r = proxy_get(url)
    except Exception as e:
        print(f"Error fetching website: {e}")
        return None

    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", r.text)
    return list(set(emails)) if emails else None


def run_scraper():
    query = "coffee shops"
    location = "Tampa, FL"

    yelp_results = scrape_yelp_debug(query, location)

    final_data = []
    for biz in yelp_results:
        emails = extract_emails_debug(biz["website"])
        biz["emails"] = emails
        final_data.append(biz)
        time.sleep(1)

    print("\nFINAL RESULTS (DEBUG MODE):")
    for biz in final_data:
        print(biz)


if __name__ == "__main__":
    run_scraper()
