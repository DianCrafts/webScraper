# Overview
This project provides two tools for web scraping, each tailored for specific use cases.

- **Tool 1:** A versatile web scraper with a graphical user interface (GUI), built with `Tkinter`.
- **Tool 2:** A `Selenium`-based script for extracting book details from a website.

## Section 1: Web Scraper with GUI (`DataScraper.py`)
This script is a Python-based web scraper with a GUI created using Tkinter. It allows users to easily extract structured data from a website by specifying custom HTML elements and selectors. The scraped data can be exported as a CSV file for further analysis.

### Features
- Multi-Page Scraping: Automatically navigates through multiple pages, scraping specified data on each page.
- Customizable Selectors: Allows users to specify HTML tags, classes, and CSS selectors to precisely target content.
- CSV Export: Saves scraped data as a CSV file, making it easy to use in data analysis applications.
- User-Friendly Interface: A GUI for easy setup, input of parameters, and execution of the scraping task.
### Requirements
- Python 3.11.9
- Libraries:
- requests
- pandas
- beautifulsoup4
- tkinter (comes with Python)


run script: 
```bash
python DataScraper.py
```


### Enter Necessary Data:
- URL (required): The base URL of the target website 
- Item Tag: The HTML tag of the item to scrape
- Item Class: CSS class of the item to scrape
- Selectors (at least one): Enter CSS selectors to specify the data fields.
Example:
- Base URL: http://books.toscrape.com
- Item Tag: article
- Item Class: product_pod
Selectors:
 - Title: .product_pod h3 a
- Price: .price_color
- Rating: .star-rating
### Future Improvements
- Multi-Threading: Add multi-threading for faster data extraction.
- Enhanced Error Handling: Improve validation and error feedback in the GUI.



## Section 2: Selenium-Based Book Scraper (DataScraperSelenium.py)
This script uses Selenium to automate the extraction of book details, including title, price, and rating, from Books to Scrape and saves the results in a CSV file (books.csv).

### Key Features
- Automated Data Extraction: Uses Selenium to programmatically navigate the website and gather book details from each catalog page.
- CSV Export: Data is saved to books.csv, facilitating further analysis in applications like Excel.
- Pagination Handling: Automatically identifies and follows the “Next” button, ensuring all catalog pages are scraped without manual intervention.
- Randomized Delay: Introduces a 2-5 second delay between requests to mimic human browsing behavior and reduce the risk of IP blocking.
### Setup and Usage
- Install ChromeDriver:
Ensure ChromeDriver is installed and compatible with your Chrome version.

- Install Selenium:
Install the latest compatible version of Selenium. here version 4.25.0 is used. version 3 was not compatible.
python -c "import selenium; print(selenium.__version__)"
    
run the script:
```bash
    python DataScraperSelenium.py
