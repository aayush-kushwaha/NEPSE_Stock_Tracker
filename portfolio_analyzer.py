from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
import re

# Step 1: Load fixed stock purchase data
data = [
    ["CHDC", "Investment", "IPO", None, 100, 10, 2, 12, 9500],
    ["UAIL", "Merged", "IPO + Secondary Market", None, 950, 9, 0, 9, 9500],
    ["GBIME", "CommercialBank", "Secondary Market", "27-07-2021", 489, 10, 2, 12, 4890],
    ["NIFRA", "Investment", "Secondary Market", "27-07-2021", 483, 10, 0, 10, 4830],
    ["EBL", "CommercialBank", "Secondary Market", "05-08-2021", 766.2, 10, 4, 14, 7662],
    ["RADHI", "Hydropower", "Secondary Market", "05-08-2021", 956.2, 10, 0, 10, 9562],
    ["CHCL", "Hydropower", "Secondary Market", "05-08-2021", 720, 10, 3, 13, 7200],
    ["JBBL", "Development Bank", "Secondary Market", "05-08-2021", 499, 10, 1, 11, 4990],
    ["JBBL", "Development Bank", "Secondary Market", "06-04-2025", 327, 10, 0, 10, 3270],
    ["PMLI", "Life Insurance", "Secondary Market", "08-08-2021", 775.5, 20, 4, 24, 15510],
    ["NABIL", "CommercialBank", "Secondary Market", "09-08-2021", 1414, 20, 11, 31, 28280],
    ["PCBL", "CommercialBank", "Secondary Market", "09-08-2021", 488.7, 10, 1, 11, 4887],
]

columns = ["Stock", "Sector", "Source", "Date", "Purchase Rate", "Purchased Shares", "Bonus Shares",
           "Total Shares", "Total Purchase Value"]

df = pd.DataFrame(data, columns=columns)
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
    # if row["Source"] == "IPO":
    #     continue  # Skip IPO

    stock_name = row["Stock"].lower()
    url = f'https://www.sharesansar.com/company/{stock_name}'
    driver.get(url)
    time.sleep(5)  # wait for JS to render

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
