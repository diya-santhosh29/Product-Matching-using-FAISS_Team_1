from selenium import webdriver
import openpyxl
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager

## Initialize the ChromeDriver
driver = webdriver.Chrome('/home/diya/Downloads/chromedriver_linux64 (2)/chromedriver')
driver.maximize_window()
# Navigate to the given URL
driver.get("https://www.flipkart.com/search?q=smartwatches&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.brand%255B%255D%3DboAt")
driver.implicitly_wait(10)


# Initialize empty lists for the smartwatch names, prices, and ratings
smartwatch_name=[]
smartwatch_price=[]
smartwatch_rating=[]
for next_button in range(3):
    # Find all elements with the product names
    product_names=driver.find_elements_by_xpath("//div[contains(@class,'_4rR01T')]")
    # Find all elements with the product price
    product_price=driver.find_elements_by_xpath("//div[contains(@class,'_30jeq3 _1_WHN1')]")
    # Find  the product rating
    product_rating=driver.find_elements_by_xpath("//span[contains(@class,'_1lRcqv')]//child::div")


    #Store the respective value into the lists
    for name in product_names:
        print(name.text)
        smartwatch_name.append(name.text)

    for price in product_price:
        print(price.text)
        smartwatch_price.append(price.text)

    for rating in product_rating:
        print(rating.text)
        smartwatch_rating.append(rating.text)

    # Find the next button and click on it
next_button=driver.find_element_by_xpath("//a[contains(@class,'_1LKTO3')]")
next_button.click()
sleep(5000)


final=zip(smartwatch_name,smartwatch_price,smartwatch_rating)

# Initialize a new Excel workbook
wb=openpyxl.Workbook()
# Get the active worksheet
sh1=wb.active

# Loop through the final list and add each row to the worksheet
for x in list(final):
    sh1.append(x)

# Save the workbook to the specified file name
wb.save("SmartWatch_Flpikart_2.xlsx")