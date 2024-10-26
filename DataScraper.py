# import requests
# from bs4 import BeautifulSoup


# def get_html(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.text
#     else:
#         print("Failed to retrieve data")
#         return None
    

# def extract_data(html, item_tag, item_class, selectors):
#     """
#     Extract data from the given HTML using dynamic selectors.

#     :param html: The HTML content to scrape.
#     :param item_tag: The tag used for item containers (e.g., 'div', 'article').
#     :param item_class: The class used for item containers (e.g., 'quote', 'product_pod').
#     :param selectors: A dictionary containing the selectors for different data fields.
#     :return: A list of dictionaries containing extracted data.
#     """
#     soup = BeautifulSoup(html, 'html.parser')
#     items = []
    
#     for item in soup.find_all(item_tag, class_=item_class):
#         item_data = {}
#         for key, selector in selectors.items():
#             try:
#                 # Extract the required data based on the key
#                 if isinstance(selector, str):  # Single selector for direct text
#                     item_data[key] = item.select_one(selector).text.strip()
#                 elif isinstance(selector, list):  # Multiple selectors for lists
#                     item_data[key] = [el.text.strip() for el in item.select(selector)]
#             except (TypeError, AttributeError, IndexError):
#                 item_data[key] = "Not found"

#         items.append(item_data)

#     return items


# def scrape_all_pages(base_url, item_tag, item_class, selectors):
#     """Scrape all pages of products from the base URL."""
#     page = 1
#     all_products = []
#     while True:
#         url = f"{base_url}/catalogue/page-{page}.html"
#         html = get_html(url)
#         if not html:  # Stop if no more HTML is returned
#             break
#         products = extract_data(html, item_tag, item_class, selectors)
#         if not products:  # Stop if no products found
#             break
#         all_products.extend(products)
#         page += 1  # Go to the next page
#     return all_products



# def scrape_website(url, config):
#     """
#     Scrape the website based on the given configuration.

#     :param url: The URL of the website to scrape.
#     :param config: A dictionary containing the scraping configuration.
#     :return: None
#     """
#     response = requests.get(url)
#     if response.status_code == 200:
#         html = response.text
#         data = extract_data(
#             html,
#             config['item_tag'],
#             config['item_class'],
#             config['selectors']
#         )
#     return data
#     #     save_to_csv(data, config['output_filename'])
#     #     print(f"Scraped {len(data)} items and saved to {config['output_filename']}.")
#     # else:
#     #     print(f"Failed to retrieve data from {url} with status code: {response.status_code}")

# if __name__ == "__main__":
#     # Dynamic configuration
#     config = {
#     "base_url": "http://books.toscrape.com",  # Base URL for the book categories
#     "item_tag": "article",  # The tag that contains the book items
#     "item_class": "product_pod",  # Class of the book item container
#     "selectors": {  # Selectors for book data
#         "title": "h3 a",  # CSS selector for book title
#         "price": "p.price_color",  # CSS selector for book price
#         "availability": "p.availability",  # CSS selector for availability
#     },
#     "output_filename": "books.csv"  # Output CSV file name
# }
#     all_books = scrape_all_pages(config["base_url"], config["item_tag"], config["item_class"], config["selectors"])
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd  # Import pandas for data handling
from bs4 import BeautifulSoup
import requests

def get_html(url):
    response = requests.get(url)
    return response.text if response.status_code == 200 else None

def extract_data(html, item_tag, item_class, selectors):
    soup = BeautifulSoup(html, 'html.parser')
    items = []
    
    # Find all elements based on item_tag and optional item_class
    if item_class:
        for item in soup.find_all(item_tag, class_=item_class):
            items.append(extract_item_data(item, selectors))
    else:
        for item in soup.find_all(item_tag):
            items.append(extract_item_data(item, selectors))

    return items

def extract_item_data(item, selectors):
    item_data = {}
    for key, selector in selectors.items():
        try:
            if isinstance(selector, str):
                item_data[key] = item.select_one(selector).text.strip()
            elif isinstance(selector, list):
                item_data[key] = [el.text.strip() for el in item.select(selector)]
        except (TypeError, AttributeError, IndexError):
            item_data[key] = "Not found"
    return item_data

def scrape_all_pages(base_url, item_tag, item_class, selectors):
    page = 1
    all_products = []
    while True:
        url = f"{base_url}/catalogue/page-{page}.html"
        html = get_html(url)
        if not html:
            break
        products = extract_data(html, item_tag, item_class, selectors)
        if not products:
            break
        all_products.extend(products)
        page += 1
    return all_products

def start_scraping():
    global scraped_data  # Store scraped data globally
    base_url = url_entry.get()
    item_tag = item_tag_entry.get()
    item_class = item_class_entry.get() or None
    
    selectors = {}
    for key, entry in selector_entries.items():
        selector = entry.get()
        if selector:  # Only add non-empty selectors
            selectors[key] = selector
    
    # Only base URL is mandatory; at least one additional field is needed
    if not base_url:
        messagebox.showerror("Input Error", "Please fill in the Base URL.")
        return

    if not item_tag and not selectors:
        messagebox.showerror("Input Error", "Please provide at least an Item Tag or one Selector.")
        return

    scraped_data = scrape_all_pages(base_url, item_tag, item_class, selectors)
    
    if scraped_data:
        messagebox.showinfo("Scraping Complete", f"Extracted {len(scraped_data)} items.")
        download_button = tk.Button(root, text="Download Results", command=download_results)
        download_button.grid(row=8 + len(selector_entries), columnspan=2)
    else:
        messagebox.showinfo("Scraping Complete", "No items extracted.")

def download_results():
    if not scraped_data:
        messagebox.showwarning("Download Error", "No data to download.")
        return

    # Ask the user for the file path to save the results
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        # Convert the scraped data to a DataFrame and save as CSV
        df = pd.DataFrame(scraped_data)
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Download Complete", "Data downloaded successfully.")

def add_selector_field():
    global selector_entries
    global scrape_button
    count = len(selector_entries) + 1
    key = f"selector_{count}"
    tk.Label(root, text=f"Selector {count}:").grid(row=6 + count, column=0)
    entry = tk.Entry(root, width=50)
    entry.grid(row=6 + count, column=1)
    selector_entries[key] = entry

    scrape_button.grid(row=7 + count, columnspan=2)  # Position it based on number of selectors

# Create the main window
root = tk.Tk()
root.title("Web Scraper")

# Create input fields
tk.Label(root, text="Base URL:").grid(row=0, column=0)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1)

tk.Label(root, text="Item Tag (Optional):").grid(row=1, column=0)
item_tag_entry = tk.Entry(root, width=50)
item_tag_entry.grid(row=1, column=1)

tk.Label(root, text="Item Class (Optional):").grid(row=2, column=0)
item_class_entry = tk.Entry(root, width=50)
item_class_entry.grid(row=2, column=1)

# Dictionary to hold selector entry fields
selector_entries = {}

# Initial selector field


# Button to add more selector fields
add_selector_button = tk.Button(root, text="Add Selector Field", command=add_selector_field)
add_selector_button.grid(row=6, columnspan=2)

# Create a button to start scraping (positioned below selector section)
scrape_button = tk.Button(root, text="Start Scraping", command=start_scraping)
scrape_button.grid(row= 7, columnspan=2)  # Position it based on number of selectors

# # Create a button for downloading results (initially hidden)
  # Position it below the scrape button
add_selector_field()
# Run the main loop
root.mainloop()
