# libraries
from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

apt-get update 
apt install chromium-chromedriver

# NYT credentials
username = "heaven.31@live.cn"
password = "depintlaan11"

# initialize the Chrome driver
driver = webdriver.Chrome("chromedriver")

# head to github login page
#driver.get("https://myaccount.nydailynews.com/850/home")
# find username/email field and send the username itself to the input field
#driver.find_element("id", "login_field").send_keys(username)
# find password input field and insert password as well
#driver.find_element("id", "password").send_keys(password)
# click login button
#driver.find_element("name", "commit").click()

#Selenium supports 8 different types of locators namely id, name, className, tagName, linkText, partialLinkText, CSS selector and xpath. Using id is one of the most reliable and fast methods of element recognition. Usually, the id is always unique on a given web page.Nov 17, 2021

driver.get("https://www.nydailynews.com/news/politics/new-york-elections-government/ny-nyc-mayor-eric-adams-interfaith-breakfast-speech-2022-20220210-7yx7stpkdvg3lenkba3oepw4da-story.html")
driver.find_element(By.LINK_TEXT, '#').click()

WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)