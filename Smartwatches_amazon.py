#Importing needed libraries
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
#Defining function for getting product links in a pages of different brands
def Product_links(product):
    #implementing our keyword search
    service = Service(executable_path=r"C:\Users\Arishma\.wdm\drivers\chromedriver\win32\109.0.5414\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)
    driver.get("https://amazon.in")
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
    search_box.send_keys(product)
    search_button = driver.find_element(By.ID, 'nav-search-submit-button')
    search_button.click()
    #listing our brands
    brands = ['Fire-Boltt','Noise','boAt','CrossBeats','Samsung','ZEBRONICS','Fastrack','TAGG','Apple','Fitbit','Wayon']
    #Collecting based on brands contains 3 pages

    for brand in brands:
        for pages in range(3):
                    driver.get("https://www.amazon.in/s?k=smart+watches&i=electronics&bbn=976419031&rh=n%3A976419031%2Cp_89%3A{brand}&dc&crid=17ZO8YTX0FCN4&qid"
                               "=1675261614&rnid=3837712031&sprefix=%2Caps%2C200&ref=sr_pg_{pages}".format(brand=brand, pages=pages))
                    #collecting products link
                    urls_collected = []
                    links = driver.find_elements(By.TAG_NAME, "h2")
                    for link in links:
                        try:
                            link2 = link.find_elements(By.XPATH,
                                                       "//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")
                            for link3 in link2:
                                urls_collected.append(link3.get_attribute("href"))
                        except Exception as e:
                            print(f"Error accessing page: {e}")
                        continue
    # Close the browser
    driver.close()
    # Return the list of product links
    return urls

#Defining function for getting product details in a pages of different brands

def details_of_product(link_of_the_Product):
    driver = webdriver.Chrome(r"C:\Users\Arishma\.wdm\drivers\chromedriver\win32\109.0.5414\chromedriver.exe")
    driver.get(link_of_the_Product)
    Product_details_dictionary = {}
    try:
        product_price = driver.find_element(By.XPATH, "//span[@class='a-price-whole']").text
    except:
        product_price = "nan"
    Product_details_dictionary['price'] = product_price
    Product_name = driver.find_element(By.XPATH, "//span[@class='a-size-large product-title-word-break']").text
    Product_details_dictionary['Name'] = Product_name

    try:
        attribute_table = driver.find_element(By.XPATH, "//table[@class='a-normal a-spacing-micro']")
        rows_in_attribute_table = attribute_table.find_elements(By.XPATH, './/tr')
    except NoSuchElementException:
        print("no specification")
        try:
            for row in rows_in_attribute_table:
                attribute_name = row.find_element(By.XPATH, "//td[1]/span[@class='a-size-base a-text-bold']").text
                attribute_value = row.find_element(By.XPATH, "//td[2]/span[@class='a-size-base po-break-word']").text
                Product_details_dictionary["attribute_name"] = attribute_value
        except NoSuchElementException:
            print("no specification")
            pass

    return Product_details_dictionary

#User approach
name_of_product = input('State the product:')
links_of_product = Product_links(name_of_product)
print(links_of_product)
list_of_details = []
for link in links_of_product:
    details = details_of_product(link)
    creating_DataFrame = pd.DataFrame(details, index=[0])
    list_of_details.append(creating_DataFrame)

Amazon_product_table = pd.concat(list_of_details, ignore_index=True)
Amazon_product_table = Amazon_product_table.reset_index(drop=True)