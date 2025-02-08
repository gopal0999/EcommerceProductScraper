import os
import time
import shutil
import pickle
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

COOKIE_FILE = "cookies.pkl"  # Store session cookies

def get_selenium_driver():
    """Setup Selenium WebDriver with headless Chrome and session persistence."""
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-blink-features=AutomationControlled")  
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-gpu")  
    options.add_argument("--window-size=1920,1080")  
    options.add_argument("--user-data-dir=./selenium_profile")  # Store session data

    # Download ChromeDriver if not available
    chromedriver_path = shutil.which("chromedriver") or ChromeDriverManager().install()
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Load session cookies if available
    if os.path.exists(COOKIE_FILE):
        driver.get("https://www.amazon.in/")  # Open a page to set cookies
        time.sleep(3)  # Allow the page to load
        with open(COOKIE_FILE, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()  # Apply cookies

    return driver

def save_cookies(driver):
    """Save cookies after login to maintain session persistence."""
    cookies = driver.get_cookies()
    with open(COOKIE_FILE, "wb") as f:
        pickle.dump(cookies, f)
