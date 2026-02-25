print("SCRIPT STARTED")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def create_driver():
    print("Setting Chrome options...")

    chrome_path = "/usr/bin/chromium-browser"
    driver_path = "/usr/local/bin/chromedriver"

    options = Options()
    options.binary_location = chrome_path

    # Required for Render
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")

    print("Launching Chrome...")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    print("Chrome launched successfully!")
    return driver


def run_scraper():
    try:
        driver = create_driver()

        print("Opening Google...")
        driver.get("https://www.google.com")
        time.sleep(3)

        print("Page title:", driver.title)
        print("Scraper finished successfully!")

    except Exception as e:
        print("ERROR:", e)

    finally:
        try:
            driver.quit()
            print("Chrome closed.")
        except:
            pass


if __name__ == "__main__":
    run_scraper()
