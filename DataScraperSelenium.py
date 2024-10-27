
import time
import csv
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By

url = "http://books.toscrape.com/catalogue/page-1.html"
driver = webdriver.Chrome()

# Open CSV file to save data
with open("books.csv", mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Rating"])  # Write headers
    
    # Iterate through all pages
    while True:
        driver.get(url)
        books = driver.find_elements(By.CLASS_NAME, "product_pod")
        
        for book in books:
            # Title
            title = book.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
            
            # Price
            price = book.find_element(By.CLASS_NAME, "price_color").text
            
            # Rating
            rating_element = book.find_element(By.CLASS_NAME, "star-rating")
            rating = rating_element.get_attribute("class").split()[-1]
            
            # Write data to CSV
            writer.writerow([title, price, rating])
            print(f"Title: {title}, Price: {price}, Rating: {rating}")

        # Look for the "next" button to navigate pages
        try:
            next_button = driver.find_element(By.CLASS_NAME, "next").find_element(By.TAG_NAME, "a")
            url = next_button.get_attribute("href")  # Update URL for the next page
        except:
            print("No more pages to scrape.")
            break  # Exit loop if no more pages

        # Random delay between pages
        time.sleep(randint(2, 5))

driver.quit()
