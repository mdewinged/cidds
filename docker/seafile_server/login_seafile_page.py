from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By

# Login informations
username = "alexandreamk1@gmail.com"
password = "Password123"

# Start Browser
opts = FirefoxOptions()
opts.add_argument("--headless")
print("Starting Firefox Browser on Headless mode")
browser = webdriver.Firefox(options=opts)

# Connect to the seafile login page
print("Connecting to the seafile login page")
browser.get('http://192.168.50.1:80')

# Fill Usersname field
print("Filling the username filde with " + username )
search = browser.find_element(By.NAME, "login")
search.send_keys(username)
search.send_keys(Keys.RETURN)

# Fill password field
search = browser.find_element(By.NAME, "password")
search.send_keys(password)
search.send_keys(Keys.RETURN)

# Submit
search = browser.find_element(By.CLASS_NAME, "submit.btn.btn-primary.btn-block").click()

# Close Browser
browser.quit()