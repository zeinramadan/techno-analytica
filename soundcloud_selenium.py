import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# TODO: improve file writing
# TODO: handle edge cases (Name provided instead of location, nothing provided at all, ...)

def write_followers_to_file(followers_list, file_name):
    """
    Function to write follower list to file
    :param followers_list:
    :param file_name:
    :return: None
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        for follower in followers_list:
            file.write(f'{follower[0]}: {follower[1]}\n')


def write_locations_to_file(followers_list, file_name):
    """
    Function to write locations to file
    :param followers_list:
    :param file_name:
    :return: None
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        for follower in followers_list:
            file.write(f'{follower[0]}, {follower[1]}, {follower[2]}\n')


def get_soundcloud_followers(driver, user_url):
    """
    Function to retrieve a the profile URLs of all soundcloud followers of a specific user.
    :param user_url: soundcloud username to parse
    :return: followers_list - a tuple of (follower username, follower soundcloud profile url)
    """

    base_url = "https://soundcloud.com/"
    url = f"{base_url}{user_url}/followers"
    driver.get(url)

    # Wait for the accept button and click on it
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    accept_button.click()

    print("Button clicked")

    # scroll down to get all followers
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1.5)  # wait ajax request
        try:
            # loop until this loading element removed from the page
            driver.find_element(By.CSS_SELECTOR, "div.loading.regular.m-padded")
        except:
            break

    # finally extract the followers
    raw_followers = driver.find_elements(By.CLASS_NAME, "userBadgeListItem__heading")

    followers_list = []
    for f in raw_followers:
        print('%s: %s' % (f.text, f.get_attribute('href')))
        followers_list.append((f.text, f.get_attribute('href')))

    return followers_list


def get_follower_locations(driver, followers_list):
    """
    function to extract the city from the soundcloud profile
    :param driver: WebDriver object
    :param followers_list: output file from get_soundcloud_followers
    :return: List of cities for each follower
    """

    locations = []

    with open(followers_list, "r") as f:
        lines = f.readlines()

        for line in lines:
            profile_name = line.strip().split(": ")[0]
            profile_url = line.strip().split(": ")[1]

            driver.get(profile_url)
            time.sleep(1)  # wait for the page to load

            try:
                location_element = driver.find_element(By.CLASS_NAME, "profileHeaderInfo__additional")
                location = location_element.text

            except:
                location = "Location not provided"

            print(f"{profile_name}: {location}")
            locations.append((profile_name, profile_url, location))

    return locations


if __name__ == '__main__':

    # Create driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_service = Service(executable_path="./chromedriver_mac_arm64/chromedriver")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # Replace 'user_url' with the desired SoundCloud account's username
    followers = get_soundcloud_followers(driver, "zeinramadan")
    print(followers)

    # Write followers to a file
    write_followers_to_file(followers, 'followers.txt')

    # Extract city from follower profile
    cities = get_follower_locations(driver, 'followers.txt')
    print(cities)
    write_locations_to_file(cities, 'follower_cities.txt')
    driver.quit()
