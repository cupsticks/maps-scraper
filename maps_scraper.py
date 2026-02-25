print("SCRIPT STARTED")

import shutil
import undetected_chromedriver as uc
import time

def create_driver():
    print("Setting up Chrome options...")

    # Try all common Chromium paths
    possible_paths = [
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
        shutil.which("google-chrome"),
        shutil.which("google-chrome-stable"),
    ]

    possible_paths = [p for p in possible_paths if p]

    print("Checking for Chromium binary...")
    chromium_path = None
    for path in possible_paths:
        print("Testing:", path)
        if path:
            chromium_path = path
            break

    if not chromium_path:
        raise Exception("Chromium binary not found on system.")

    print("Chromium found at:", chromium_path)

    options = uc.ChromeOptions()
    options.binary_location = chromium_path

    # REQUIRED flags for Render
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--remote-debugging-port=9222")

    print("Launching Chrome...")
    driver = uc.Chrome(options=options)
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
