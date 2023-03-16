import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_profile_description(profile_url):

    # Set selenium params
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_service = Service(executable_path="./chromedriver_mac_arm64/chromedriver")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # Make request and parse html - Need to add some randomness in here so we don't get our IP address blocked by IG
    driver.get(profile_url)
    html_content = driver.page_source
    driver.quit()

    # Extract element with the bio
    soup = BeautifulSoup(html_content, 'html.parser')
    script_element = soup.find('script', {'type': 'application/ld+json'})

    # clean the json and return the bio
    if script_element:
        json_data = json.loads(script_element.string)

        if 'description' in json_data:
            return json_data['description']

    return None


if __name__ == '__main__':

    # Read the CSV file
    file_path = "result_short.csv"
    df = pd.read_csv(file_path)

    # Apply the get_profile_description() function to each row in the DataFrame
    # This will loop through all profile URLs and fetch the bio for each URL
    df['Bio'] = df['profileUrl'].apply(get_profile_description)

    # Save the modified DataFrame to a new CSV file
    df.to_csv("output_with_bio.csv", index=False)
