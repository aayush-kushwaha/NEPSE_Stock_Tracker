from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Set up headless Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

# Load the target page
stock_name = input("Enter stock name: ")
stock_name = stock_name.lower()
url = f'https://www.sharesansar.com/company/{stock_name}'
driver.get(url)
time.sleep(5)  # wait for JavaScript to render the page

# Parse page content
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find the LTP section
ltp_label = soup.find(string="Volume:")
ltp_value = ltp_label.find_next().text.strip() if ltp_label else "Not found"

# Extract only the number after "Ltp:"
import re
if ltp_value != "Not found":
    match = re.search(r'Ltp:\s*([\d,]+\.?\d*)', ltp_value)
    if match:
        ltp_number = match.group(1).replace(',', '')
        print(ltp_number)
    else:
        print("Not found")
else:
    print("Not found")

driver.quit()
