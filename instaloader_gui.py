"""
TODO: code only iterates through 50 followers, need to make it iterate through all
Instaloader app wrapped in a tkinter GUI
Usage: enter list of instagram usernames seperated by ','
"""

import tkinter as tk


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
        password = "hqMe5xCBQ8R8EYV"
        L.context.log("Logging in as %s..." % username)
        L.context.login(username, password)

        # list of usernames to scrape
        usernames = [x.strip() for x in self.input.get().split(',')]

        exceptions = 0
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
            try:
                profile_info = {
                    'username': profile.username,
                    'name': profile.full_name,
                    'bio': profile.biography
                }
            except Exception as e:
                exceptions += 1
                print("Caught exception while fetching profile info. Total so far: {}".format(exceptions))
                print(e)
                continue

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

                try:
                    # get follower info
                    follower_info = {
                        'username': follower.username,
                        'name': follower.full_name,
                        'bio': follower.biography
                    }
                except Exception as e:
                    exceptions += 1
                    print("Caught exception while fetching follower info. Total so far: {}".format(exceptions))
                    print(e)
                    continue

                # save follower info to file
                with open(os.path.join(username, follower.username, 'profile.json'), 'w', encoding='utf-8') as f:
                    json.dump(follower_info, f, ensure_ascii=False)

            print("Finished collection for {}.".format(username))
            print("===========================")


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
