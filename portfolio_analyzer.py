from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

# Step 1: Load fixed stock purchase data
df = pd.read_csv("portfolio.csv")
df["LTP"] = np.nan
df["Total Value"] = np.nan
df["Profit/Loss"] = np.nan
df["Profit/Loss (%)"] = np.nan
df["Suggestion"] = ""

# Step 2: Set up headless Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

# Step 3: Fetch LTP for each eligible stock (only Secondary Market)
for index, row in df.iterrows():
    stock_name = row["Stock"].lower()
    url = f'https://www.sharesansar.com/company/{stock_name}'
    driver.get(url)

    # Wait until the "Volume:" label is present
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Volume:')]"))
        )
    except:
        print(f"[{row['Stock']}] Volume label not found or timeout.")
        continue

    # Parse page content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    ltp_label = soup.find(string="Volume:")
    ltp_value = ltp_label.find_next().text.strip() if ltp_label else "Not found"

    # Extract number after Ltp:
    if ltp_value != "Not found":
        match = re.search(r'Ltp:\s*([\d,]+\.?\d*)', ltp_value)
        if match:
            ltp_number = float(match.group(1).replace(',', ''))
            df.at[index, "LTP"] = ltp_number
        else:
            print(f"[{row['Stock']}] LTP not found.")
    else:
        print(f"[{row['Stock']}] Volume label not found.")

driver.quit()

# Step 4: Calculate total value, profit/loss, and profit/loss percentage
df["Total Value"] = df["LTP"] * df["Total Shares"]
df["Profit/Loss"] = df["Total Value"] - df["Total Purchase Value"]
df["Profit/Loss (%)"] = (df["Profit/Loss"] / df["Total Purchase Value"]) * 100

# Step 5: Suggest selling if profitable (and equity stock)
df["Suggestion"] = np.where(
    (df["LTP"] > df["Purchase Rate"]) & (df["Source"] != "IPO"),
    "Sell the stock now",
    ""
)

# Final Output
print(df[["Stock", "Purchase Rate", "LTP", "Total Value", "Profit/Loss", "Profit/Loss (%)", "Suggestion"]])
