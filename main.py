import instaloader

def main():
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")

    L = instaloader.Instaloader()

    # Login
    L.login(username, password)

    # Obtain profile metadata
    profile = instaloader.Profile.from_username(L.context, username)

    # Get your followers
    followers = set(profile.get_followers())

    # Get users you're following
    following = set(profile.get_followees())

    # Find users you follow but don't follow you back
    not_following_back = following - followers

    # Save usernames to a text file
    with open('not_following_back.txt', 'w') as file:
        for user in not_following_back:
            file.write(user.username + '\n')

    print("List of people you follow but don't follow you back has been saved to not_following_back.txt")

if __name__ == "__main__":
    main()
