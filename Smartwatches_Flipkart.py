#Importing the necessary libraries
import pandas as pd
from selenium import webdriver
import openpyxl
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import  NoSuchElementException


#Initiating empty lists
smartwatch_name=[]
smartwatch_brand=[]
smartwatch_discounted_price=[]
smartwatch_rating=[]
smartwatch_original_price=[]
smartwatch_color=[]
smartwatch_strap_color=[]
smartwatch_model=[]
smartwatch_size=[]



# List of top 10 smartwatch brands
brand_name =["Fire-Boltt","boAt","Noise", "CrossBeats", "Fastrack", "ZEBRONICS",'Samsung' "TAGG", "Titan","FITBIT","APPLE"]
#Opening the driver
driver = webdriver.Chrome('/home/diya/Downloads/chromedriver_linux64 (2)/chromedriver')
driver.maximize_window()

#Defining a function for appending fetched elements into a list
def attribute_function(list_name,final_list_name):
    for numbers in list_name:
    final_list_name.append(numbers.text)


# Giving the brand name and page numbers in a loop
for brand in brand_name:
    for page in range(1,10): #Scrape data of first 9 pages of each brand

        # Navigate to the given URL
        driver.get("https://www.flipkart.com/search?q=smartwatches&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.brand%255B%255D%3D{}&page={}".format(brand, page))
        driver.implicitly_wait(10)

        #Creating a list of product links
        elems = driver.find_elements(By.CLASS_NAME,'_1fQZEK')
        product_link = []
        for elem in elems:
            href = elem.get_attribute('href')
            product_link.append(href)
            if href is not None:
                print(href)


        #Scraping the necessary attributes
        try:
            #Parsing through different links from the list
            for links in product_link:
                driver.get("{}".format(links))
                #Appending brand name to the list
                smartwatch_brand.append(brand)

                #Scraping the product name
                product_name=driver.find_elements(By.XPATH,"//span[@class='B_NuCI']")
                attribute_function(product_name,smartwatch_name)

                #Scraping discounted price
                discounted_product_price = driver.find_elements(By.XPATH,"//div[@class='_30jeq3 _16Jk6d']")
                attribute_function(discounted_product_price,smartwatch_discounted_price)

                #Scraping product rating
                product_rating = driver.find_elements(By.XPATH,"//div[@class='gUuXy- _16VRIQ']//child::div")
                attribute_function(product_rating,smartwatch_rating)

                #Scraping original price
                original_product_price = driver.find_elements(By.XPATH,"//div[@class='_3I9_wc _2p6lqe']")
                attribute_function(original_product_price,smartwatch_original_price)


                #To get attributes from the specifications table
                for specifications in range(1,15):
                    feature = driver.find_element(By.XPATH,("(//td[@class='_1hKmbr col col-3-12'])[position()={}]".format(specifications)))
                    try:
                        #To get Strap Color
                        if (feature.text=="Strap Color"):
                            feature1= driver.find_element(By.XPATH,("(//td[@class='URwL2w col col-9-12'])[position()={}]".format(specifications)))
                            #print(feature1.text)
                            smartwatch_strap_color.append(feature1.text)
                        #To get Model Number
                        elif feature.text == "Model Number":
                            feature2 = driver.find_element(By.XPATH,("(//td[@class='URwL2w col col-9-12'])[position()={}]".format(specifications)))
                            smartwatch_model.append(feature2.text)
                        #To get Size
                        elif feature.text == "Size":
                            feature3= driver.find_element(By.XPATH,("(//td[@class='URwL2w col col-9-12'])[position()={}]".format(specifications)))
                            smartwatch_size.append(feature3.text)
                    except NoSuchElementException:
                        pass
        except NoSuchElementException:
            pass

#Merging the attributes
final=zip(product_link,smartwatch_brand,smartwatch_name,smartwatch_discounted_price,smartwatch_original_price,smartwatch_rating,smartwatch_strap_color,smartwatch_model,smartwatch_size)

# Initialize a new Excel workbook
wb=openpyxl.Workbook()
# Get the active worksheet
sheet1=wb.active

# Loop through the final list and add each row to the worksheet
#sheet1.append=(['Product Link','Brand','Product Name','Discounted Price', 'Original Price', 'Product Rating','Strap Color','Model','Size'])
for x in list(final):
    sheet1.append(x)

# Save the workbook to the specified file name
wb.save("SmartWatch_Flpikart_5.xlsx")





