# In this project we have created a web crawler to crawl ecommerce webistes using their domain

Command to run the scraper


<!-- first activate venv -->
source bin/activate #linux/mac

<!-- change directory to ecommerce_crawler inside ecommerce_crawler  -->
<!-- then run below command -->
scrapy crawl product_spider -a domains="https://www.amazon.in/" -o output.json
!! domains can have comma separated domain urls

<!-- LOOM VIDEO for project reference -->
https://www.loom.com/share/ba680ae4eaf1463eb42bd9397b5931a4?sid=c90d6288-6e7e-46f1-87de-34eabdf29e10

