# libraries
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=C:\\Users\\HaZhang\\AppData\\Local\\Google\\Chrome\\User Data") #Path to your chrome profile
#options.add_argument('--profile-directory=Person 1')
driver = webdriver.Chrome(executable_path="C:\\Users\\chromedriver.exe", chrome_options=options)

# head to github login page
#driver.get("https://www.bloomberg.com/news/articles/2023-01-20/google-slashes-most-jobs-at-incubator-area-120-as-part-of-cuts?srnd=premium")

# https://stackoverflow.com/questions/31062789/how-to-load-default-profile-in-chrome-using-python-selenium-webdriver
