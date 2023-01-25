import openpyxl
from selenium import webdriver
import openpyxl
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome('/home/diya/Downloads/chromedriver_linux64 (2)/chromedriver')
driver.maximize_window()
driver.get("https://www.flipkart.com/search?q=smartwatch&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
driver.implicitly_wait(10)


names=driver.find_elements_by_xpath("//div[contains(@class,'_4rR01T')]")
price=driver.find_elements_by_xpath("//div[contains(@class,'_30jeq3 _1_WHN1')]")
rating=driver.find_elements_by_xpath("//span[contains(@class,'_1lRcqv')]//child::div")

sw_name=[]
sw_price=[]
sw_rating=[]

for i in names:
    print(i.text)
    sw_name.append(i.text)

for j in price:
    print(j.text)
    sw_price.append(j.text)

for k in rating:
    print(k.text)
    sw_rating.append(k.text)

final=zip(sw_name,sw_price,sw_rating)


wb=openpyxl.Workbook()
sh1=wb.active

for x in list(final):
    sh1.append(x)

wb.save("SmartWatch_Flpikart_1.xlsx")
