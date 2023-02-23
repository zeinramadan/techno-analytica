import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

if __name__ == '__main__':
    artist_username = "chlaer"
    driver = webdriver.Chrome()
    driver.get("https:////soundcloud.com/{}/followers".format(artist_username))

    # scroll down to get all followers
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3) #wait ajax request
        try:
            # loop until this loading element removed from the page
            driver.find_element_by_css_selector('div.loading.regular.m-padded')
        except:
            break

    # finally extract the followers, save to file
    followers = driver.find_elements_by_class_name('userBadgeListItem__heading')
    for f in followers:
        print('%s: %s' % (f.text, f.get_attribute('href')))


    # use soundcloud api wrapper, get country of every follower on list