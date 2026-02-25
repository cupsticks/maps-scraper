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

    url = (
        "https://www.google.com/maps/preview/search?"
        f"q={query.replace(' ', '+')}"
    )

    r = requests.get(url, headers=HEADERS)
    raw = r.text

    # Extract JSON from the response
    try:
        data = json.loads(raw[raw.find("/*") + 2 : raw.rfind("*/")])
    except:
        print("Failed to parse Google Maps response")
        return []

    results = []
    for item in data[0][1][0][14][0]:
        try:
            name = item[5][0][1]
            address = item[5][0][2]
            website = item[5][0][3][0] if item[5][0][3] else None
            phone = item[5][0][4][0] if item[5][0][4] else None

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
