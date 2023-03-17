import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Replace with your Instagram credentials
username = 'your_username'
password = 'your_password'

# Set selenium params
chrome_options = Options()
chrome_service = Service(executable_path="./chromedriver_mac_arm64/chromedriver")
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Log in to Instagram
driver.get('https://www.instagram.com/accounts/login/')
time.sleep(2)
driver.find_element_by_name('username').send_keys(username)
driver.find_element_by_name('password').send_keys(password)
driver.find_element_by_name('password').send_keys(Keys.RETURN)
time.sleep(4)

# Navigate to the target profile
target_profile = 'target_username'
driver.get(f'https://www.instagram.com/{target_profile}/')
time.sleep(2)

# Click on the 'Followers' link
followers_link = driver.find_element_by_partial_link_text('followers')
followers_link.click()
time.sleep(2)

# Scroll through the followers list to load all the followers
followers_dialog = driver.find_element_by_css_selector('div[role="dialog"]')
scroll_pause_time = 1
last_height = 0
while True:
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_dialog)
    time.sleep(scroll_pause_time)
    new_height = driver.execute_script("return arguments[0].scrollHeight", followers_dialog)
    if new_height == last_height:
        break
    last_height = new_height

# Extract the usernames
usernames = [element.text for element in driver.find_elements_by_css_selector('a.FPmhX')]
print(f"Total followers: {len(usernames)}")
print("Usernames:", usernames)

# Close the driver
driver.quit()
