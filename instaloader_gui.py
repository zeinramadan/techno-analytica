"""
TODO: add multithreading via 1 or more accounts
Instaloader app wrapped in a tkinter GUI
Usage: enter list of instagram usernames seperated by ','
"""
import threading
import tkinter as tk
import instaloader
import json
import os


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

    def scrape_user_data(self, L, username):

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
        followers = []
        for follower in profile.get_followers():

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

            # get follower posts if account is public
            if not follower.is_private:
                for post in follower.get_posts():

                    # create directory for post
                    post_dir = os.path.join(username, follower.username, post.shortcode)
                    os.makedirs(post_dir, exist_ok=True)

                    # get post info
                    post_info = {
                        'caption': post.caption,
                        'geotag': post.location.name if post.location else None
                    }

                    # save post info to file
                    with open(os.path.join(post_dir, 'post.json'), 'w', encoding='utf-8') as f:
                        json.dump(post_info, f, ensure_ascii=False)

                    # get comments
                    comments = []
                    for comment in post.get_comments():
                        comments.append({'text': comment.text, 'username': comment.owner.username})

                    # save comments to file
                    with open(os.path.join(post_dir, 'comments.json'), 'w', encoding='utf-8') as f:
                        json.dump(comments, f, ensure_ascii=False)

    def run_instaloader(self):

        # initialize Instaloader
        L = instaloader.Instaloader()

        # Log in
        username = "throwawayaccountyahyeet"
        password = "CBUrQBbdVxJ6m53"
        L.context.log("Logging in as %s..." % username)
        L.context.login(username, password)

        # list of usernames to scrape
        usernames = [x.strip() for x in self.input.get().split(',')]

        threads = []
        # iterate through usernames
        for username in usernames:
            t = threading.Thread(target=self.scrape_user_data, args=(L, username))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
