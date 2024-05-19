import instaloader
from tqdm import tqdm
from getpass import getpass

def main():
    username = input("Enter your Instagram username: ")
    password = getpass("Enter your Instagram password: ")

    print(f"Fetching followers and followees of", username, "... This could take a few minutes!")

    L = instaloader.Instaloader()

    #login
    L.login(username, password)

    #obtain profile metadata
    profile = instaloader.Profile.from_username(L.context, username)

    #prepare to fetch followers
    followers = set()
    followers_gen = profile.get_followers()
    #estimate the total number of followers for the progress bar
    for follower in tqdm(followers_gen, desc="Fetching followers", total=profile.followers):
        followers.add(follower)

    #prepare to fetch followees
    following = set()
    followees_gen = profile.get_followees()
    #estimate the total number of followees for the progress bar
    for followee in tqdm(followees_gen, desc="Fetching following", total=profile.followees):
        following.add(followee)

    #find users you follow but don't follow you back
    not_following_back = following - followers

    #prepare verified/unverified containers
    not_following_back_verified = set()
    not_following_back_unverified = set()

    #sort verified/unverified users from the not_following_back set
    for user in tqdm(not_following_back, desc="Checking if users are verified", total=len(not_following_back)):
        if user.is_verified:
            not_following_back_verified.add(user)
        else:
            not_following_back_unverified.add(user)

    #save usernames to a text file
    with open('not_following_back_verified.txt', 'w') as file:
        for user in not_following_back_verified:
            file.write(user.username + '\n')
    
    with open('not_following_back_unverified.txt', 'w') as file:
        for user in not_following_back_unverified:
            file.write(user.username + '\n')

    print("List of verified people you follow but don't follow you back has been saved to not_following_back_verified.txt")
    print("List of unverified people you follow but don't follow you back has been saved to not_following_back_verified.txt")

if __name__ == "__main__":
    main()
