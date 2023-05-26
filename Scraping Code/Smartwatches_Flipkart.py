import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


# Initiating empty list for product details
product_details = []

# List of top 10 smartwatch brands
brand_names = ["Fire-Boltt","boAt", "Noise", "CrossBeats", "Fastrack", "ZEBRONICS", "Samsung", "TAGG", "Titan", "FITBIT", "APPLE"]

# Opening the driver
driver = webdriver.Chrome()
driver.maximize_window()

# Function to fetch attributes from a list of elements
def get_attribute(attribute_elements):
    return [elem.text for elem in attribute_elements]

# Function to scrape product details from a given brand and page number
def scrape_product_details(brand, page):
    # Navigate to the given URL
    driver.get("https://www.flipkart.com/search?q=smartwatches&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.brand%255B%255D%3D{}&page={}".format(brand, page))
    driver.implicitly_wait(10)

    # Creating a list of product links
    elems = driver.find_elements(By.CLASS_NAME, 'IRpwTa')
    product_links = [elem.get_attribute('href') for elem in elems if elem.get_attribute('href') is not None]

    # Scraping the necessary attributes
    try:
        # Parsing through different links from the list
        for link in product_links:
            driver.get(link)

            # Create a dictionary to store the product details
            details = {'Product_Link': link, 'Brand': brand}

            # Scraping the product name
            product_name_elements = driver.find_elements(By.XPATH, "//span[@class='B_NuCI']")
            details['Product_Name'] = get_attribute(product_name_elements)[0]

            # Scraping discounted price
            discounted_price_elements = driver.find_elements(By.XPATH, "//div[@class='_30jeq3 _16Jk6d']")
            details['Discounted_Price'] = get_attribute(discounted_price_elements)[0]

            # Scraping product rating
            rating_elements = driver.find_elements(By.XPATH, "//div[@class='gUuXy- _16VRIQ']//child::div")
            details['Product_Rating'] = get_attribute(rating_elements)[0]

            # Scraping original price
            original_price_elements = driver.find_elements(By.XPATH, "//div[@class='_3I9_wc _2p6lqe']")
            details['Original_Price'] = get_attribute(original_price_elements)[0]

            read_more = driver.find_element_by_xpath("//button[@class='_2KpZ6l _1FH0tX']").click()
            # Find the specifications table element
            specifications_table = driver.find_elements_by_xpath("//table[@class='_14cfVK']")

            # Extract data from the table
            for i in specifications_table:
                rows = i.find_elements_by_xpath(".//tr")

                for row in rows:
                    cells = row.find_elements_by_xpath(".//td")
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    details[key] = value

            product_details.append(details)

    except :
        continue

# Scrape data for each brand and page number
for brand in brand_names:
    for page in range(1, 10): # Scrape data of first 9 pages of each brand
        scrape_product_details(brand, page)

# Close the driver
driver.quit()

# Convert the list of product details to a DataFrame
dataframe = pd.DataFrame(product_details)

# Save the DataFrame to a CSV file
dataframe.to_csv('flipkart_product_details.csv', index=False)





