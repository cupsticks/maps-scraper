print("SCRIPT STARTED")

import requests
import re
import json
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def search_maps(query, num_results=20):
    print(f"Searching Google Maps for: {query}")

    url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
    r = requests.get(url, headers=HEADERS)
    html = r.text

    # Extract the JSON blob inside "APP_INITIALIZATION_STATE"
    match = re.search(r"APP_INITIALIZATION_STATE=(.*?);window.APP", html)
    if not match:
        print("Could not find JSON in page")
        return []

    try:
        data = json.loads(match.group(1))
    except:
        print("Failed to parse JSON blob")
        return []

    # Navigate the structure
    try:
        items = data[3][6][0]
    except:
        print("Google changed structure again")
        return []

    results = []
    for item in items:
        try:
            name = item[14][11]
            address = item[14][2][0]
            website = item[14][7][0] if item[14][7] else None
            phone = item[14][3][0] if item[14][3] else None

            results.append({
                "name": name,
                "address": address,
                "website": website,
                "phone": phone
            })
        except:
            continue

        if len(results) >= num_results:
            break

    print(f"Found {len(results)} results")
    return results


def extract_emails_from_website(url):
    if not url:
        return None

    print(f"Extracting emails from: {url}")

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
    except:
        return None

    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", r.text)
    return list(set(emails)) if emails else None


def run_scraper():
    query = "coffee shops in tampa"

    results = search_maps(query)

    final_data = []
    for biz in results:
        emails = extract_emails_from_website(biz["website"])
        biz["emails"] = emails
        final_data.append(biz)
        time.sleep(1)

    print("\nFINAL RESULTS:")
    for biz in final_data:
        print(biz)


if __name__ == "__main__":
    run_scraper()
