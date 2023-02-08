import pandas as pd
from selenium import webdriver
import openpyxl
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import  NoSuchElementException



smartwatch_name=[]
smartwatch_discounted_price=[]
smartwatch_rating=[]
smartwatch_original_price=[]
smartwatch_color=[]
smartwatch_strap_color=[]
smartwatch_model=[]
smartwatch_size=[]





# List of top 10 smartwatch brands
brand_name =["Samsung","boAt" , "Noise", "CrossBeats", "Fastrack", "ZEBRONICS", "TAGG", "Titan","FITBIT","APPLE"]
driver = webdriver.Chrome('/home/diya/Downloads/chromedriver_linux64 (2)/chromedriver')

# Giving the brand name and page numbers in a loop
for brand in brand_name:
    for page in range(1,5): #Scrape data of first 2 pages of each brand


        driver.maximize_window()
        # Navigate to the given URL
        driver.get("https://www.flipkart.com/search?q=smartwatches&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.brand%255B%255D%3D{}&page={}".format(brand, page))
        #driver.implicitly_wait(20)


        elems = driver.find_elements_by_class_name('_1fQZEK')
        product_link = []
        for elem in elems:
            href = elem.get_attribute('href')
            product_link.append(href)
            if href is not None:
                print(href)

        try:
            for links in product_link:
                driver.get("{}".format(links))
                product_name=driver.find_elements_by_xpath("//span[@class='B_NuCI']")
                for name in product_name:
                    smartwatch_name.append(name.text)
                discounted_product_price = driver.find_elements_by_xpath("//div[@class='_30jeq3 _16Jk6d']")
                for dis_price in discounted_product_price:
                    smartwatch_discounted_price.append(dis_price.text)
                product_rating = driver.find_elements_by_xpath("//div[@class='gUuXy- _16VRIQ']//child::div")
                for rating in product_rating:
                    smartwatch_rating.append(rating.text)
                original_product_price = driver.find_elements_by_xpath("//div[@class='_3I9_wc _2p6lqe']")
                for ori_price in original_product_price:
                    smartwatch_original_price.append(ori_price.text)
                for specifications in range(1,15):
                    feature = driver.find_element(By.XPATH,("(//td[@class='_1hKmbr col col-3-12'])[position()={}]".format(specifications)))
                    try:
                        if (feature.text=="Strap Color"):
                            feature1= driver.find_element(By.XPATH,("(//td[@class='URwL2w col col-9-12'])[position()={}]".format(specifications)))
                            #print(feature1.text)
                            smartwatch_strap_color.append(feature1.text)
                        elif feature.text == "Model Number":
                            feature2 = driver.find_element(By.XPATH,("(//td[@class='URwL2w col col-9-12'])[position()={}]".format(specifications)))
                            smartwatch_model.append(feature2.text)
                        elif feature.text == "Size":
                            feature3= driver.find_element(By.XPATH,("(//td[@class='URwL2w col col-9-12'])[position()={}]".format(specifications)))
                            smartwatch_size.append(feature3.text)
                    except NoSuchElementException:
                        pass
        except NoSuchElementException:
            pass


final=zip(smartwatch_name,smartwatch_discounted_price,smartwatch_original_price,smartwatch_rating,smartwatch_strap_color,smartwatch_model,smartwatch_size)

# Initialize a new Excel workbook
wb=openpyxl.Workbook()
# Get the active worksheet
sheet1=wb.active

# Loop through the final list and add each row to the worksheet
#sheet1.append=(['Product Name','Product Price', 'Product Rating'])
for x in list(final):
    sheet1.append(x)

# Save the workbook to the specified file name
wb.save("SmartWatch_Flpikart_5.xlsx")





