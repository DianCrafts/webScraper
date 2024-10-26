# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import time

# # Function to get HTML from a dynamic page
# def get_dynamic_html(url):
#     # Set up the Selenium WebDriver (ensure the appropriate driver is installed)
#     driver = webdriver.Chrome()  # Change to webdriver.Firefox() for Firefox
#     driver.get(url)

#     # Example: Wait for a specific element to load (the first book's title)
#     try:
#         element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'h3 a'))
#         WebDriverWait(driver, 10).until(element_present)
#     except Exception as e:
#         print("Timed out waiting for page to load", e)

#     # Optionally wait for some time if content loads via JavaScript
#     time.sleep(5)  

#     # Get page source and parse with BeautifulSoup
#     html = driver.page_source
#     driver.quit()  # Close the browser
#     return html

# # Function to extract data from HTML
# def extract_data(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     books = []

#     # Find all book containers
#     for article in soup.find_all('article', class_='product_pod'):
#         title = article.h3.a['title']  # Get the title from the anchor tag
#         price = article.find('p', class_='price_color').text  # Get the price
#         books.append({'title': title, 'price': price})

#     return books

# # Main function to run the scraper
# def main():
#     url = "http://books.toscrape.com"
#     html = get_dynamic_html(url)
#     books = extract_data(html)

#     # Print extracted data
#     for book in books:
#         print(f"Title: {book['title']}, Price: {book['price']}")

# if __name__ == "__main__":
#     main()


import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def get_dynamic_html(url, wait_for_selector):
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()  # Use the appropriate driver for your browser
    driver.get(url)

    # Wait for a specific element to load
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_selector))
        WebDriverWait(driver, 10).until(element_present)
    except Exception as e:
        print("Timed out waiting for page to load", e)

    # Optionally wait for some time if content loads via JavaScript
    time.sleep(5)

    # Get page source and parse with BeautifulSoup
    html = driver.page_source
    driver.quit()  # Close the browser
    return html

# Function to extract data from HTML
def extract_data(html, title_selector, price_selector):
    soup = BeautifulSoup(html, 'html.parser')
    books = []

    # Find all book containers using dynamic selectors
    for article in soup.find_all('article', class_='product_pod'):
        title = article.select_one(title_selector)['title']  # Get the title
        price = article.select_one(price_selector).text  # Get the price
        books.append({'title': title, 'price': price})

    return books

def start_scraping():
    url = simpledialog.askstring("Input", "Enter the URL:")
    wait_for_selector = simpledialog.askstring("Input", "Enter the CSS selector to wait for:")
    title_selector = simpledialog.askstring("Input", "Enter the title CSS selector:")
    price_selector = simpledialog.askstring("Input", "Enter the price CSS selector:")

    # Get dynamic HTML
    html = get_dynamic_html(url, wait_for_selector)

    # Extract data using dynamic selectors
    books = extract_data(html, title_selector, price_selector)

    # Show results
    if books:
        messagebox.showinfo("Scraping Complete", f"Extracted {len(books)} items.")
        for book in books:
            print(book)  # Print the results to console
    else:
        messagebox.showinfo("Scraping Complete", "No items extracted.")

# Create the main window
root = tk.Tk()
root.title("Dynamic Web Scraper")

# Create a button to start scraping
start_button = tk.Button(root, text="Start Scraping", command=start_scraping)
start_button.pack(pady=20)

# Run the main loop
root.mainloop()
