import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import openpyxl

# Initiating empty list for product details
product_details = []

# Defining a function to fetch attributes
def get_attribute(element, xpath):
    try:
        attribute_elements = element.find_elements(By.XPATH, xpath)
        return [elem.text for elem in attribute_elements]
    except NoSuchElementException:
        return []

# Defining a function to scrape product details from a given link
def scrape_product_details(link, brand):
    driver.get(link)

    # Create a dictionary to store the product details
    details = {'Product_Link': link, 'Brand': brand}

    # Scraping the product name
    product_name = get_attribute(driver, "//span[@class='B_NuCI']")
    details['Product_Name'] = product_name

    # Scraping discounted price
    discounted_price = get_attribute(driver, "//div[@class='_30jeq3 _16Jk6d']")
    details['Discounted_Price'] = discounted_price

    # Scraping product rating
    rating = get_attribute(driver, "//div[@class='gUuXy- _16VRIQ']//child::div")
    details['Product_Rating'] = rating

    # Scraping original price
    original_price = get_attribute(driver, "//div[@class='_3I9_wc _2p6lqe']")
    details['Original_Price'] = original_price

    # To get attributes from the specifications table
    for specifications in range(1, 15):
        feature_element = driver.find_element(By.XPATH, f"(//td[@class='_1hKmbr col col-3-12'])[position()={specifications}]")
        feature_name = feature_element.text

        try:
            feature_value_element = driver.find_element(By.XPATH, f"(//td[@class='URwL2w col col-9-12'])[position()={specifications}]")
            feature_value = feature_value_element.text

            if feature_name == "Strap Color":
                details['Strap_Color'] = feature_value
            elif feature_name == "Model Number":
                details['Model'] = feature_value
            elif feature_name == "Size":
                details['Size'] = feature_value
        except NoSuchElementException:
            pass

    return details

# List of top 10 smartwatch brands
brand_names = ["Fire-Boltt", "boAt", "Noise", "CrossBeats", "Fastrack", "ZEBRONICS", "Samsung", "TAGG", "Titan", "FITBIT", "APPLE"]
# Opening the driver
driver = webdriver.Chrome('/home/diya/Downloads/chromedriver_linux64 (4)/chromedriver')
driver.maximize_window()

# Giving the brand name and page numbers in a loop
for brand in brand_names:
    for page in range(1, 10): # Scrape data of first 9 pages of each brand

        # Navigate to the given URL
        driver.get(f"https://www.flipkart.com/search?q=smartwatches&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.brand%255B%255D%3D{brand}&page={page}")
        driver.implicitly_wait(10)

        # Creating a list of product links
        elems = driver.find_elements(By.CLASS_NAME, 'IRpwTa')
        product_links = [elem.get_attribute('href') for elem in elems if elem.get_attribute('href') is not None]

        # Scraping the necessary attributes
        try:
            # Parsing through different links from the list
            for link in product_links:
                details = scrape_product_details(link, brand)
                product_details.append(details)

        except NoSuchElementException:
            pass

# Close the driver
driver.quit()

# Convert the list of product details to a DataFrame
df = pd.DataFrame(product_details)

# Save the DataFrame to an Excel file
with pd.ExcelWriter('SmartWatch_Flpikart.xlsx') as writer:
    df.to_excel(writer, index=False)




