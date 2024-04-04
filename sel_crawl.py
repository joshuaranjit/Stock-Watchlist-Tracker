from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time

print("Initializing WebDriver...")
driver = webdriver.Chrome()
print("WebDriver initialized successfully.")

# Dictionary of stock tickers and their corresponding URLs
stock_urls = {
    "TMB": "https://www.tickertape.in/stocks/tamilnad-mercantile-bank-TMB",
    "JYOTHYLAB": "https://www.tickertape.in/stocks/jyothy-labs-JYOI",
    "INDHOTEL": "https://www.tickertape.in/stocks/indian-hotels-company-IHTL"
}

def check_entry_point(url):
    print(f"\nNavigating to {url}")
    driver.get(url)
    print("Page loaded. Waiting for content to fully render...")
    time.sleep(5)  # Adjust based on observation
    
    page_source = driver.page_source.lower()  # Convert page source to lowercase for case-insensitive search
    good_keyword = "the stock is underpriced and is not in the overbought zone"
    average_keywords = [
        "the stock is overpriced but is not in the overbought zone",
        "the stock is not in the overbought zone"
    ]

    if good_keyword in page_source:
        return "Good Entry Point"
    elif any(average_keyword in page_source for average_keyword in average_keywords):
        return "Average Entry Point"
    else:
        return "No Keywords Found"

# Results dictionary
results = {}

# Iterate over the URLs and classify the entry point quality
for ticker, url in stock_urls.items():
    classification = check_entry_point(url)
    results[ticker] = classification
    print(f"Result for {ticker}: {classification}")

print("\nClosing WebDriver...")
driver.quit()  # Important to close the browser after the script is done
print("WebDriver closed.")

# Optionally, include the script run time
script_run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"\nScript run completed at {script_run_time}")
