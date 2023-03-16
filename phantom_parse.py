import json
import random
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_profile_description(profile_url, driver):

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

    # Set selenium params
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_service = Service(executable_path="./chromedriver_mac_arm64/chromedriver")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # Given a collection of CSV files containing the profileUrls of each follower for 1 instagram account, loop through
    # and add the bio to each CSV file
    input_folder_path = "phantom_files"
    output_folder_path = "augmented_phantom_files"
    csv_files = [f"{input_folder_path}/result.csv"]

    print("Accounts to iterate through: {}".format(len(csv_files)))

    counter = 1
    for csv_file in csv_files:

        # Log which account we are processing
        print("Starting collection for {}. Number {} out of {}".format(csv_file, counter, len(csv_files)))
        counter += 1

        # Read CSV, extract profileUrls
        df = pd.read_csv(csv_file)
        bios_list = []
        profile_count = 1
        for profileUrl in df['profileUrl'].values.tolist():

            # Sleep 15mins every 6000 iterations or 30s every 200 iterations. 10 seconds otherwise between each call
            if profile_count % 6000 == 0:
                # Sleep for duration between 12-14 minutes
                delay = random.uniform(720, 840)
                sleep(delay)

            elif profile_count % 200 == 0:
                # Sleep for duration between 20-30 seconds
                delay = random.uniform(20, 30)
                sleep(delay)

            else:
                # Sleep for duration between 1-2 seconds between each call
                delay = random.uniform(1, 2)
                sleep(delay)

            bio = get_profile_description(profileUrl, driver)
            bios_list.append(bio)
            profile_count += 1

        # create the dataframe
        data = {
            "id": df["id"].values.tolist(),
            "username": df["username"].values.tolist(),
            "fullName": df["fullName"].values.tolist(),
            "bio": bios_list,
            "profileUrl": df['profileUrl'].values.tolist(),
            "isPrivate": df["isPrivate"].values.tolist(),
            "isVerified": df["isVerified"].values.tolist()
        }

        # Create dataframe
        output_df = pd.DataFrame(data)

        # Save the modified DataFrame to a new CSV file
        output_df.to_csv(f"{output_folder_path}/{csv_file}_with_bios.csv", index=False)

        # Log completion
        print("Run complete for {}".format(csv_file))
        print("===============================")
