from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Reverb.com product search for Neumann U87 microphone sale listings
url = "https://reverb.com/marketplace?query=Neumann%20U%2087&make=neumann&product_type=pro-audio"

# Configure Selenium to use a specific browser driver (e.g., Chrome)
driver = webdriver.Chrome()  # Make sure ChromeDriver is in your PATH
driver.get(url)

time.sleep(6) # pause so Selenium Browser fully loads before processing

items_list = []
item_listings = driver.find_elements(By.CLASS_NAME, "rc-listing-grid__item")

# Scrape item info from page listings
for listing in item_listings:
    title = listing.find_element(By.CLASS_NAME, "rc-listing-card__titleblock" ).text.strip()
    title_trunc = (title[:40] + "...") if len(title) > 43 else title # truncates the title to 40 char
    price = listing.find_element(By.CLASS_NAME, "rc-price-block__price").text.strip()
    condition = listing.find_element(By.CLASS_NAME, "rc-listing-card__condition").text.strip()
    item_link = listing.find_element(By.TAG_NAME, "a").get_attribute("href")

    if listing.find_elements(By.CLASS_NAME, "rc-price-block__nudge"):
        shipping = "Free Shipping"
    else:
        shipping = "Shipping Fees Apply"

    # Print to test data elements were scraped
    ##print(f"Title: {title} \nPrice: {price} \nCondition: {condition} \nLink: {item_link}\n"
          ##f"Shipping: {shipping}\n")

    # put listing data/elements into a dictionary, then append to item_list
    item = {
       'Title' : title_trunc,
       'Price' : price,
       'Condition' : condition,
       'Shipping' : shipping,
       'Item URL' : item_link
    }
    # Add listing to items_list
    items_list.append(item)


# Create Pandas DataFrame and CSV file for items_list
df = pd.DataFrame(items_list)
print(df.head())
df.to_csv('item_results.csv')

input()
driver.quit()
