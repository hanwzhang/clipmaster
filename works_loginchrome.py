from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('user-data-dir=C:/Users/HaZhang/Desktop/clipmaster-main/Clipperprofile') 
driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
driver.get('https://nytimes.com')

# basically we need to set up a user profile for this app, and copy the whole file into here
# get it from C:/Users/HaZhang/AppData/Local/Google/Chrome/User Data