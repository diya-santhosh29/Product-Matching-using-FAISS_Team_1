#Importing necessary libraries

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
import pandas as pd



# List of brand names
brands = ['Fire-Boltt','Noise','boAt','CrossBeats','Samsung','ZEBRONICS','Fastrack','TAGG','Apple','Fitbit','Titan']

#Creating an empty list "data" to store the scraped information
data=[]

#Setting up the Chrome web driver
driver = webdriver.Chrome("home/futures/Desktop/chromedriver")
wait = WebDriverWait(driver, 10)


#Creating a loop to iterate through a list of "brands"
#Within the loop for brands, there's another loop for "pages" (1 to 9) to scrape data from multiple pages of the website.
for brand in brands:
    for pages in range(1,10):
        driver.get("https://www.amazon.in/s?k=smart+watches&i=electronics&bbn=976419031&rh=n%3A976419031%2Cp_89%3A{brand}&dc&crid=17ZO8YTX0FCN4&qid=1675261614&rnid=3837712031&sprefix=%2Caps%2C200&ref=sr_pg_{pages}".format(brand=brand, pages=pages))
        urls = []
        links = driver.find_elements(By.TAG_NAME,"h2")

        #The script then extracts the product URLs from the page using the "find_elements" method and the "By.TAG_NAME" locator.
        for link in links:
            try:
                link2 = link.find_element(By.TAG_NAME,"a")
                urls.append(link2.get_attribute("href"))
            except Exception as e:
                print(f"Error accessing page: {e}")
            continue

        #In the next loop, the script navigates to each product URL and extracts the product name, price and specifications using the "find_element" method and the "By.XPATH" locator.
        #The extracted information is stored in dictionaries "dict_price", "dict_name", and "details_dict".
        for url in (urls):
            driver.get(url)
            Product_details_dictionary = {}
            Product_price_dictionary = {}
            Product_name_dictionary = {}
            try:
                product_price = driver.find_element(By.XPATH,"//span[@class='a-price-whole']").text
            except:
                product_price = "nan"
            Product_price_dictionary['price'] = product_price

            name = driver.find_element(By.XPATH,"//span[@class='a-size-large product-title-word-break']").text
            Product_nmae_dictionary['Name'] = name

            # try to find the attribute table
            try:
                try:
                    attribute_table = driver.find_element(By.XPATH, '//table[@class="a-normal a-spacing-micro"]')
                    rows = attribute_table.find_elements(By.XPATH, './/tr')
                except NoSuchElementException:
                    print("no specification")
                    break
                    # loop through each row in the table
                try:
                    for row in rows:
                        attribute_name = row.find_element(By.XPATH, './/td[1]/span[@class="a-size-base a-text-bold"]').text
                        attribute_value = row.find_element(By.XPATH, './/td[2]/span[@class="a-size-base po-break-word"]').text

                        # Add the specification name and value to the dictionary
                        Product_details_dictionary[attribute_name] = attribute_value
                except NoSuchElementException:
                    print("no specification")
                pass


            except NoSuchElementException:
                print("no specification")
            pass

            #The dictionaries are merged and added to the "data" list.
            Product_name_dictionary.update(Product_price_dictionary)
            Product_name_dictionary.update(Product_details_dictionary)
            data.append(Product_name_dictionary)

            #Finally, the script prints the "data" list to verify the extracted information.
            print(data)

#creating a Pandas DataFrame from the list data
Amazon_data_frame=pd.DataFrame(data)
Amazon_data_frame

#storing the dataframe into a CSV file named "smart_watches_amazon.csv".
Amazon_data_frame.to_csv("smart_watches_amazon.csv", index=False)
