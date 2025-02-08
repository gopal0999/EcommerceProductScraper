import scrapy
from scrapy_selenium import SeleniumRequest
from selenium_driver import get_selenium_driver, save_cookies
from urllib.parse import urljoin
import tldextract
import re
from config_prod_category import config

class ProductSpider(scrapy.Spider):
    name = "product_spider"
    
    def __init__(self, domains=None, *args, **kwargs):
        super(ProductSpider, self).__init__(*args, **kwargs)

        # Load config from config_prod_category
        self.PRODUCT_PATTERNS = [re.compile(pattern) for pattern in config.get("product_patterns", [])]
        self.CATEGORY_PATTERNS = [re.compile(pattern) for pattern in config.get("category_patterns", [])]
        self.EXCLUDE_PATTERNS = [re.compile(pattern) for pattern in config.get("exclude_patterns", [])]

        # Selenium Driver with session management
        self.driver = get_selenium_driver()

        if domains:
            self.start_urls = domains.split(",")
        else:
            self.start_urls = ["https://www.amazon.in/"]

        self.visited_urls = set()

    def start_requests(self):
        """Use SeleniumRequest to fetch JavaScript-rendered pages with session persistence."""
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=5, screenshot=False)

    def parse(self, response):
        """Extract product and category URLs dynamically while maintaining session."""
        domain = tldextract.extract(response.url).registered_domain
        self.log(f"Crawling: {domain} - {response.url}")

        for link in response.css("a::attr(href)").getall():
            abs_url = urljoin(response.url, link)

            if domain not in abs_url or abs_url in self.visited_urls:
                continue  

            self.visited_urls.add(abs_url)

            if any(pattern.search(abs_url) for pattern in self.EXCLUDE_PATTERNS):
                continue

            if any(pattern.search(abs_url) for pattern in self.PRODUCT_PATTERNS):
                yield {"product_url": abs_url}

            elif any(pattern.search(abs_url) for pattern in self.CATEGORY_PATTERNS):
                yield SeleniumRequest(url=abs_url, callback=self.parse, wait_time=5)

    def closed(self, reason):
        """Save session cookies when spider is closed."""
        save_cookies(self.driver)
