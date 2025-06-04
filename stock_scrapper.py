from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Volume:')]"))
    )
except:
    raise Exception(f"Stock data not found or timeout occured: {stock_name}")

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
