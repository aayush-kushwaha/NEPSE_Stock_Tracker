from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def get_ltp(stock_name: str) -> float | None:
    """
    Fetch the latest traded price (LTP) of a stock from sharesansar.com

    Args:
        stock_name (str): The name of the stock (in lowercase or uppercase)

    Returns:
        float | None: The LTP as a float if found, else None
    """
    # Set up headless Chrome
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        stock_name = stock_name.lower()
        url = f'https://www.sharesansar.com/company/{stock_name}'
        driver.get(url)

        # Wait until 'Volume:' appears on page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Volume:')]"))
        )

        # Parse page content
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ltp_label = soup.find(string="Volume:")
        ltp_value = ltp_label.find_next().text.strip() if ltp_label else None

        if ltp_value:
            match = re.search(r'Ltp:\s*([\d,]+\.?\d*)', ltp_value)
            if match:
                return float(match.group(1).replace(',', ''))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

    return None

if __name__ == "__main__":
    stock_name = input("Enter stock name: ")
    ltp = get_ltp(stock_name)
    if ltp:
        print(f"LTP is: {ltp}")
    else:
        print("LTP not found.")
