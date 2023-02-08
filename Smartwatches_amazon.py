import selenium
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# List of brands to scrape data for

brands = ['Fire-Boltt', 'Noise', 'boAt', 'CrossBeats', 'Samsung', 'ZEBRONICS', 'PTorn', 'Garmin', 'Fastrack', 'Honor',
          'TAGG', 'Apple', 'Fitbit', 'Google', 'Generic', 'OLICOM', 'Huawei', 'Titan', 'MI', 'GOQii', 'Sounce',
          'Maxima', 'Fosiil', 'GIONEE', 'Suunto', 'AYL', 'WOW IMAGINE', 'sekyo', 'helix', 'Priefy', 'SKY BUYER',
          'MATTSPY'          'Prolet', 'B M C', 'Brain Freezer', 'HOBBACHI', 'OBOE', 'EXZZER', 'VTech']
# Initialize the Chrome driver
# Loop through each brand
# Loop through each page (1-3) for each brand


driver = webdriver.Chrome("home/futures/Desktop/chromedriver")

for brand in brands:
    for pages in range(1, 4):
        driver.get(
            "https://www.amazon.in/s?k=smart+watches&i=electronics&bbn=976419031&rh=n%3A976419031%2Cp_89%3A{brand}&dc&crid=17ZO8YTX0FCN4&qid=1675261614&rnid=3837712031&sprefix=%2Caps%2C200&ref=sr_pg_{pages}".format(
                brand=brand, pages=pages))
        # Navigate to the page on Amazon
        urls = []
        name = []
        links = driver.find_elements(By.TAG_NAME, "h2")
        for i in links:
            link2 = i.find_element(By.TAG_NAME, "a")
            urls.append(link2.get_attribute("href"))


        # Get all product links on the page
        for l in (urls):
            driver.get(l)
            price = driver.find_element(By.XPATH, "//span[@class='a-price-whole']").text
            name = driver.find_element(By.XPATH, "//span[@class='a-size-large product-title-word-break']").text
            attributes = driver.find_elements(By.XPATH, "//span[@class='a-size-base po-break-word']")
            # Get product name, price, and attributes
            for attribute in range(len(attributes)):
                print(attributes[attribute].text)
            print(name)
            print(price)
