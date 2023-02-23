import soundcloud

if __name__ == '__main__':

    # Create a SoundCloud client instance with your client ID
    client = soundcloud.Client(client_id='taLAWcuG1Ud1EWixcDx3IS0vnokXhd9J')

    # Get the user ID of the SoundCloud account
    user = client.get('/resolve', url='https://soundcloud.com/chlaer')
    user_id = user.id

    # Get the list of user IDs who follow the account
    followers = client.get('/users/{}/followers'.format(user_id))

    # Iterate over each follower and get their country and city information
    for follower in followers:
        # Get the user object of the follower
        follower_user = client.get('/users/{}'.format(follower.id))

        # Get the country and city information of the follower
        country = follower_user.country
        city = follower_user.city

        # Print the country and city information
        print('Follower: {}, Country: {}, City: {}'.format(follower_user.username, country, city))
