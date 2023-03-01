"""
TODO: remove looping through posts and comments for each follower
Instaloader app wrapped in a tkinter GUI
Usage: enter list of instagram usernames seperated by ','
"""

import tkinter as tk
import random
from time import sleep


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.submit = tk.Button(self, text="Submit", command=self.run_instaloader)
        self.input = tk.Entry(self)
        self.label = tk.Label(self, text="Enter a list of Instagram accounts separated by commas:")
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label.pack(side="top")
        self.input.pack(side="top")
        self.submit.pack(side="bottom")

    def run_instaloader(self):
        import instaloader
        import json
        import os

        # initialize Instaloader
        L = instaloader.Instaloader()

        # Log in
        username = "throwawayaccountyahyeet"
        password = "CBUrQBbdVxJ6m53"
        L.context.log("Logging in as %s..." % username)
        L.context.login(username, password)

        # list of usernames to scrape
        usernames = [x.strip() for x in self.input.get().split(',')]

        artist_count = 0
        artist_total = len(usernames)
        # iterate through usernames
        for username in usernames:

            # Log run state
            print("{} - Number {} out of {}".format(username, artist_count, artist_total))
            print("Collecting account info of {}".format(username))

            # Increment for next iteration
            artist_count += 1

            # create directory to store data
            os.makedirs(username, exist_ok=True)

            # get profile
            profile = instaloader.Profile.from_username(L.context, username)

            # get profile info
            profile_info = {
                'username': profile.username,
                'name': profile.full_name,
                'bio': profile.biography
            }

            # save profile info to file
            with open(os.path.join(username, 'profile.json'), 'w', encoding='utf-8') as f:
                json.dump(profile_info, f, ensure_ascii=False)

            # get list of followers
            number_of_followers = profile.followers
            print("{} - Gathering data on followers. Total number of followers: {}".format(username,
                                                                                           number_of_followers))
            followers = []
            counter = 1
            for follower in profile.get_followers():

                if counter == 1 or counter % 1000 == 0:
                    print("Processed {} out of {}. {} accounts remaining".format(counter, number_of_followers,
                                                                                 number_of_followers-counter))
                counter += 1

                followers.append(follower.username)

                # create directory for follower
                os.makedirs(os.path.join(username, follower.username), exist_ok=True)

                # get follower info
                follower_info = {
                    'username': follower.username,
                    'name': follower.full_name,
                    'bio': follower.biography
                }

                # save follower info to file
                with open(os.path.join(username, follower.username, 'profile.json'), 'w', encoding='utf-8') as f:
                    json.dump(follower_info, f, ensure_ascii=False)

                # Sleep so we don't overwhelm the API, use a random value between 4-6 seconds each time
                wait_time = random.uniform(4, 6)
                sleep(wait_time)

            print("Finished collection for {}.".format(username))
            print("===========================")


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
