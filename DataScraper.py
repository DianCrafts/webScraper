import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to retrieve data")
        return None
    

def extract_data(html, item_tag, item_class, selectors):
    """
    Extract data from the given HTML using dynamic selectors.

    :param html: The HTML content to scrape.
    :param item_tag: The tag used for item containers (e.g., 'div', 'article').
    :param item_class: The class used for item containers (e.g., 'quote', 'product_pod').
    :param selectors: A dictionary containing the selectors for different data fields.
    :return: A list of dictionaries containing extracted data.
    """
    soup = BeautifulSoup(html, 'html.parser')
    items = []
    
    for item in soup.find_all(item_tag, class_=item_class):
        item_data = {}
        for key, selector in selectors.items():
            try:
                # Extract the required data based on the key
                if isinstance(selector, str):  # Single selector for direct text
                    item_data[key] = item.select_one(selector).text.strip()
                elif isinstance(selector, list):  # Multiple selectors for lists
                    item_data[key] = [el.text.strip() for el in item.select(selector)]
            except (TypeError, AttributeError, IndexError):
                item_data[key] = "Not found"

        items.append(item_data)

    return items


def scrape_all_pages(base_url, item_tag, item_class, selectors):
    """Scrape all pages of products from the base URL."""
    page = 1
    all_products = []
    while True:
        url = f"{base_url}/catalogue/page-{page}.html"
        html = get_html(url)
        if not html:  # Stop if no more HTML is returned
            break
        products = extract_data(html, item_tag, item_class, selectors)
        if not products:  # Stop if no products found
            break
        all_products.extend(products)
        page += 1  # Go to the next page
    return all_products



def scrape_website(url, config):
    """
    Scrape the website based on the given configuration.

    :param url: The URL of the website to scrape.
    :param config: A dictionary containing the scraping configuration.
    :return: None
    """
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        data = extract_data(
            html,
            config['item_tag'],
            config['item_class'],
            config['selectors']
        )
    return data
    #     save_to_csv(data, config['output_filename'])
    #     print(f"Scraped {len(data)} items and saved to {config['output_filename']}.")
    # else:
    #     print(f"Failed to retrieve data from {url} with status code: {response.status_code}")

if __name__ == "__main__":
    # Dynamic configuration
    config = {
    "base_url": "http://books.toscrape.com",  # Base URL for the book categories
    "item_tag": "article",  # The tag that contains the book items
    "item_class": "product_pod",  # Class of the book item container
    "selectors": {  # Selectors for book data
        "title": "h3 a",  # CSS selector for book title
        "price": "p.price_color",  # CSS selector for book price
        "availability": "p.availability",  # CSS selector for availability
    },
    "output_filename": "books.csv"  # Output CSV file name
}
    all_books = scrape_all_pages(config["base_url"], config["item_tag"], config["item_class"], config["selectors"])


    print(all_books)