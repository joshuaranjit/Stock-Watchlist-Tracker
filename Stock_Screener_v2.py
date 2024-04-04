from selenium import webdriver
import os
import time
import base64
import fitz  # PyMuPDF
from datetime import datetime

print("Initializing WebDriver...")
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
print("WebDriver initialized successfully.")

pdf_folder = 'PDFs'
os.makedirs(pdf_folder, exist_ok=True)
print(f"PDFs will be saved in the directory: {pdf_folder}")

stock_urls = {
    "TMB": "https://www.tickertape.in/stocks/tamilnad-mercantile-bank-TMB",
    "JYOTHYLAB": "https://www.tickertape.in/stocks/jyothy-labs-JYOI",
    "INDHOTEL": "https://www.tickertape.in/stocks/indian-hotels-company-IHTL"
}

errors = []  # To store error messages
start_time = time.time()

for ticker, url in stock_urls.items():
    print(f"Processing {ticker}...")
    try:
        driver.get(url)
        time.sleep(3)
    except Exception as e:
        errors.append(f"Error accessing {url} for {ticker}: {e}")
        print(f"Error accessing {url}. Please update the correct URL for {ticker}. Skipping to the next stock.")
        continue

    print(f"Saving {ticker} webpage as PDF...")
    try:
        result = driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})
        if not result or 'data' not in result:
            raise ValueError("Failed to generate PDF")
        pdf_content = base64.b64decode(result['data'])
    except Exception as e:
        errors.append(f"Failed to save {ticker} as PDF: {e}")
        print(f"Failed to save {ticker} as PDF. Skipping to the next stock.")
        continue

    pdf_path = os.path.join(pdf_folder, f"{ticker}.pdf")
    with open(pdf_path, "wb") as f:
        f.write(pdf_content)
    print(f"{ticker} webpage has been saved as PDF.")

driver.quit()
print("Finished saving webpages as PDFs. Now classifying stocks based on keyword presence...")

good_entry_points, average_entry_points = [], []

for pdf_file in os.listdir(pdf_folder):
    if not pdf_file.endswith(".pdf"):
        continue
    try:
        with fitz.open(os.path.join(pdf_folder, pdf_file)) as doc:
            text = "".join(page.get_text() for page in doc).lower()
    except Exception as e:
        errors.append(f"Failed to read {pdf_file}: {e}")
        print(f"Failed to read {pdf_file}. It might be empty or corrupted.")
        continue

    if "the stock is underpriced and is not in the overbought zone" in text:
        good_entry_points.append(pdf_file[:-4])
    else:
        average_entry_points.append(pdf_file[:-4])
    print(f"{pdf_file} analyzed.")

end_time = time.time()
duration = end_time - start_time

print("\n--- Classification Results ---")
print(f"Time Taken: {duration:.2f} seconds")
print(f"Executed Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Stocks with Good Entry Point:", ", ".join(good_entry_points) or "None")
print("Stocks with Average Entry Point:", ", ".join(average_entry_points) or "None")

# Error Report
print("\n--- Error Report ---")
if errors:
    for error in errors:
        print(error)
else:
    print("No errors found.")

# Optional: Clean up by deleting the PDFs and the folder
print("\nCleaning up PDF files...")
for pdf_file in os.listdir(pdf_folder):
    os.remove(os.path.join(pdf_folder, pdf_file))
os.rmdir(pdf_folder)
print("Cleanup completed.")
