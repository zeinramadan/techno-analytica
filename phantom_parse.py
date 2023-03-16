import json

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# Function to make an HTTP request and parse the contents of a URL
def parse_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    else:
        print(f"Failed to fetch {url}, status code: {response.status_code}")
        return None


# Function to load a URL with Selenium and parse the contents
def selenium_parse(url):
    chrome_service = Service(executable_path="./chromedriver_mac_arm64/chromedriver")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get(url)
    html_content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html_content, "html.parser")
    return soup


if __name__ == '__main__':

    # Read the CSV file
    file_path = "result_short.csv"
    df = pd.read_csv(file_path)

    # Set up Selenium WebDriver options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (without opening a browser window)

    # Loop through each URL in the 'ProfileURL' column
    for index, row in df.iterrows():
        profile_url = row['profileUrl']
        parsed_content = selenium_parse(profile_url)

        if parsed_content:

            # Extract the bio from the json response
            script_element = parsed_content.find('script', {'type': 'application/ld+json'})
            json_data = json.loads(script_element.string)

            # Add the bio to the pandas dataframe
            json_data['description']

            # Write parsed HTML to file
            output_file_name = f"output_{index}.html"
            with open(output_file_name, "w", encoding="utf-8") as output_file:
                output_file.write(str(parsed_content))

            # Write JSON to file
            json_file_name = f"json_output_{index}.json"
            with open(json_file_name, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False)
