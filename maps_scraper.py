print("Scraper started on Render...")

import time
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

SEARCH_QUERY = "gift shops in Tampa, FL"
SCROLL_COUNT = 30  # how many scrolls to load more results


def extract_emails_from_website(url):
    if not url:
        return []

    try:
        html = requests.get(url, timeout=10).text
        emails = re.findall(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            html
        )
        return list(set(emails))
    except:
        return []


def run_scraper():
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    driver = uc.Chrome(options=options)

    print("Opening Google Maps...")
    driver.get("https://www.google.com/maps")
    time.sleep(3)

    print("Searching...")
    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.send_keys(SEARCH_QUERY)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

    # Scroll results
    results_panel = driver.find_element(By.XPATH, "//div[contains(@aria-label,'Results')]")

    for _ in range(SCROLL_COUNT):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_panel)
        time.sleep(1)

    print("Collecting business listings...")
    listings = driver.find_elements(By.XPATH, "//a[contains(@href,'/maps/place')]")

    data = []

    for listing in listings:
        try:
            listing.click()
            time.sleep(3)

            name = driver.find_element(By.XPATH, "//h1").text

            website = ""
            phone = ""
            address = ""

            info_elements = driver.find_elements(By.XPATH, "//button[contains(@aria-label,'Website') or contains(@aria-label,'Phone') or contains(@aria-label,'Address')]")

            for el in info_elements:
                label = el.get_attribute("aria-label")
                if "Website" in label:
                    website = label.replace("Website: ", "")
                elif "Phone" in label:
                    phone = label.replace("Phone: ", "")
                elif "Address" in label:
                    address = label.replace("Address: ", "")

            emails = extract_emails_from_website(website)

            data.append({
                "Name": name,
                "Website": website,
                "Phone": phone,
                "Address": address,
                "Emails": ", ".join(emails)
            })

            print(f"Scraped: {name}")

        except Exception as e:
            print("Error:", e)
            continue

    df = pd.DataFrame(data)
    df.to_csv("emails.csv", index=False)
    print("Saved emails.csv")

    driver.quit()


if __name__ == "__main__":
    run_scraper()