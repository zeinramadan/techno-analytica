'''
# #LOGIC IN PSEUDOCODE
# #final structure should look like:
# #data = [(artist, followers, follower_posts), (artist, followers, follower_posts), ...]
#
# data = []
# artists = ["alarico", "chlaer"]
# for artist in artists:
#
#     #get data about artist and save it in the following datastructure
#     artist_data = {
#         name = artist,
#         bio = bio,
#         number_of_followers = n_followers,
#         list_of_followers = followers
#     }
#
#     #Get each follower's data save it in the following datastructure
#     followers = []
#     for follower in followers:
#         follower_data = {
#             username = follower,
#             name = full_name,
#             bio = bio,
#             list_of_posts = posts
#         }
#         followers.append(follower_data)
#
#         #Get post data for each follower if account is public
#         if (account is public):
#             posts = []
#             for post in posts:
#                 post_data = {
#                     caption = caption,
#                     geotag = geotag,
#                     comments = START--comment1--SEP--comment2--SEP--comment3--SEP----END
#                 }
#                 posts.append(post_data)
#
#     if account is public:
#         entry = (artist_data, followers, posts)
#     else:
#         entry = (artist_data, followers, None)
#
#     data = append(entry)
'''

import instaloader
import json
import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # initialize Instaloader
    L = instaloader.Instaloader()

    # Log in
    username = "throwawayaccountyahyeet"
    password = "CBUrQBbdVxJ6m53"
    L.context.log("Logging in as %s..." % username)
    L.context.login(username, password)

    # list of usernames to scrape
    usernames = ['alarico___']

    # iterate through usernames
    for username in usernames:
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
