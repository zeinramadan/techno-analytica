import json
import os
import random
from time import sleep, time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# TODO: improve logging


class AllProxiesExhaustedException(Exception):
    pass


def create_driver_with_proxy(proxy, chrm_options):
    """
    function to create a new driver using a given proxy
    :param proxy: a proxy from the proxy list
    :param chrm_options: chrome options
    :return: new driver using the proxy
    """

    chrm_options.add_argument(f"--proxy-server={proxy}")
    chrm_service = Service(executable_path="./chromedriver_mac_arm64/chromedriver")

    return webdriver.Chrome(service=chrm_service, options=chrm_options)


def get_profile_description(profile_url, chrome_driver, no_response_count, proxy_list, chrm_options):
    """
    function to get the bio of instagram profile using selenium. also contains logic to use proxies if rate limited
    :param profile_url: instagram url of a given profile
    :param chrome_driver: driver object
    :param no_response_count: dictionary to keep count of how many no responses we got
    :param proxy_list: list of proxies to use
    :param chrm_options: chrome options
    :return: bio of instagram account if available
    """

    # Make request and parse html
    chrome_driver.get(profile_url)
    html_content = chrome_driver.page_source

    # Extract element with the bio
    soup = BeautifulSoup(html_content, 'html.parser')
    script_element = soup.find('script', {'type': 'application/ld+json'})

    # clean the json and return the bio
    if script_element:
        json_data = json.loads(script_element.string.replace("\n", " "))

        if 'description' in json_data:
            return json_data['description']

    else:
        print("no response...")
        no_response_count["count"] += 1

        # Rate limit detected. Reset counter, try again using a proxy.
        if no_response_count["count"] == 2:

            # Reset no response count because we will be using a new proxy
            no_response_count["count"] = 0

            # If proxy list is not exhausted
            if proxy_list:

                print("Rate limited by IG. Trying new proxy")

                # Quit current driver, create new driver using one of the proxies from the list
                chrome_driver.quit()
                proxy = random.choice(proxy_list)
                print("Trying with proxy {}".format(proxy))
                chrome_driver = create_driver_with_proxy(proxy, chrm_options)

                # Remove the chosen proxy from the list of available proxies
                remaining_proxies = proxy_list.copy()
                remaining_proxies.remove(proxy)

                # Recursive call to try again with the new proxy
                return get_profile_description(profile_url, chrome_driver, remaining_proxies, chrm_options)

            else:
                print("All proxies exhausted. Writing to dataframe and exiting code. Please re-run later.")
                raise AllProxiesExhaustedException()

    return None


if __name__ == '__main__':

    # Set selenium params
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_service = Service(executable_path="./chromedriver_mac_arm64/chromedriver")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # Input and output directories
    input_folder_path = "phantom_files"
    output_folder_path = "augmented_phantom_files"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Iterate through all CSV files in the input_folder_path
    csv_files = [os.path.join(input_folder_path, f) for f in os.listdir(input_folder_path) if f.endswith('.csv')]

    # var to keep track of how many requests we have made in total. Sleeping based on this
    total_profile_count = 1

    # var to keep track of no responses
    no_response_counter = {"count": 0}

    # Proxies to use
    proxies = [
        "http://proxy1:port",
        "http://proxy2:port",
        "http://proxy3:port"
        # Add more proxies here
    ]

    # Log info
    print("Accounts (csv files) to iterate through: {}".format(len(csv_files)))

    # counter to keep count csv files we iterated through
    csv_counter = 1
    for csv_file in csv_files:

        # Log which account we are processing
        print("Starting collection for {}. Number {} out of {}".format(csv_file, csv_counter, len(csv_files)))
        csv_counter += 1

        # Read CSV, extract profileUrls
        df = pd.read_csv(csv_file)

        # Initialize variables, counter to track profile iterations, data structures, and timer
        bios_list = []
        profile_counter = 1
        total = len(df['profileUrl'].values.tolist())
        start_time = time()
        for profileUrl in df['profileUrl'].values.tolist():

            print("{}/{} - Processing {}".format(profile_counter, total, profileUrl))

            # Sleep 15mins every 6000 iterations or 30s every 200 iterations. 10 seconds otherwise between each call
            if total_profile_count % 6000 == 0:
                # Sleep for duration between 12-14 minutes
                delay = random.uniform(720, 840)
                sleep(delay)

            elif total_profile_count % 200 == 0:
                # Sleep for duration between 20-30 seconds
                delay = random.uniform(20, 30)
                sleep(delay)

            else:
                # Sleep for duration between 1-2 seconds between each call
                delay = random.uniform(1, 2)
                sleep(delay)

            # Get bio
            try:
                bio = get_profile_description(profileUrl, driver, no_response_counter, proxies, chrome_options)
            except AllProxiesExhaustedException:
                print("All proxies exhausted")
                pass

            bios_list.append(bio)
            profile_counter += 1
            total_profile_count += 1

        # Calculate time taken
        end_time = time()  # Record the end time
        duration_seconds = end_time - start_time
        duration_minutes, duration_seconds = divmod(duration_seconds, 60)
        duration_hours, duration_minutes = divmod(duration_minutes, 60)

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
        output_df.to_csv(f"{output_folder_path}/{os.path.basename(csv_file).rstrip('.csv')}_with_bios.csv", index=False)

        # Log completion
        print("Run complete for {}. Time taken: {} hours, {} minutes, and {} seconds"
              .format(csv_file, int(duration_hours), int(duration_minutes), int(duration_seconds)))
        print("===============================")

    # Close driver after completing
    driver.quit()
