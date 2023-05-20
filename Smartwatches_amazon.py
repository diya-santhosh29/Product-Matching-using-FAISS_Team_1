import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

# Setting up the Chrome web driver
driver = webdriver.Chrome("path/to/chromedriver")

# Function to extract product URLs from the page
def get_product_urls(brand, num_pages):
    urls = []
    for page in range(1, num_pages + 1):
        url = "https://www.amazon.in/s?k=smart+watches&i=electronics&bbn=976419031&rh=n%3A976419031%2Cp_89%3A{brand}&dc&crid=17ZO8YTX0FCN4&qid=1675261614&rnid=3837712031&sprefix=%2Caps%2C200&ref=sr_pg_{page}".format(brand=brand, page=page)
        driver.get(url)
        links = driver.find_elements(By.TAG_NAME, "h2")
        for link in links:
            try:
                product_link = link.find_element(By.TAG_NAME, "a").get_attribute("href")
                urls.append(product_link)
            except Exception as e:
                print(f"Error accessing page: {e}")
    return urls

# Function to extract product details from a URL
def get_product_details(url):
    driver.get(url)
    details_dict = {}
    dict_price = {}
    dict_name = {}
    dict_links = {}

    dict_links['link'] = url

    try:
        product_price = driver.find_element(By.XPATH, "//span[@class='a-price-whole']").text
    except:
        product_price = "NaN"
    dict_price['price'] = product_price

    try:
        name = driver.find_element(By.XPATH, "//span[@class='a-size-large product-title-word-break']").text
    except:
        name = "NaN"
    dict_name['Name'] = name

    try:
        attribute_table = driver.find_element(By.XPATH, '//table[@class="a-normal a-spacing-micro"]')
        rows = attribute_table.find_elements(By.XPATH, './/tr')
        for row in rows:
            attribute_name = row.find_element(By.XPATH, './/td[1]/span[@class="a-size-base a-text-bold"]').text
            attribute_value = row.find_element(By.XPATH, './/td[2]/span[@class="a-size-base po-break-word"]').text
            details_dict[attribute_name] = attribute_value
    except NoSuchElementException:
        print("No specifications")

    dict_name.update(dict_price)
    dict_name.update(details_dict)
    dict_name.update(dict_links)
    return dict_name

# Main function to scrape data for multiple brands and pages
def scrape_data(brands, num_pages):
    data = []
    for brand in brands:
        urls = get_product_urls(brand, num_pages)
        for url in urls:
            product_details = get_product_details(url)
            data.append(product_details)
            print(data)
    return data

# List of brands and number of pages to scrape
brands = ['Fire-Boltt', 'Noise', 'boAt', 'CrossBeats', 'ZEBRONICS', 'Fastrack', 'TAGG', 'Apple', 'Fitbit', 'Titan']
num_pages = 5

# Scrape data
data = scrape_data(brands, num_pages)

#creating a Pandas DataFrame from the list data
data=pd.DataFrame(data)
data

#storing the dataframe into a CSV file named "smart_watches_amazon.csv".
data.to_csv("smart_watches_amazon.csv",na_rep='NaN',index=False)
