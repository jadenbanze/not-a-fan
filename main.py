import instaloader
from tqdm import tqdm
from getpass import getpass
import time

def main():
    username = input("Enter your Instagram username: ")
    password = getpass("Enter your Instagram password: ")

    print(f"Fetching followers and followees of", username, "... This could take a few minutes!")

    L = instaloader.Instaloader()

    try:
        # Login with more robust error handling
        print("Attempting to log in...")
        L.login(username, password)
        
        # Add a longer delay after login
        print("Login successful! Waiting 10 seconds before proceeding...")
        time.sleep(10)
        
        # Verify login was successful
        test_profile = instaloader.Profile.from_username(L.context, username)
        if not L.context.is_logged_in:
            raise Exception("Login failed - please check your credentials")
            
        print("Login verified!")
        
        #obtain profile metadata
        profile = test_profile

        # Add delay before fetching followers
        time.sleep(5)
        
        #prepare to fetch followers
        followers = set()
        followers_gen = profile.get_followers()
        #estimate the total number of followers for the progress bar
        for follower in tqdm(followers_gen, desc="Fetching followers", total=profile.followers):
            followers.add(follower)
            time.sleep(2)  # Add delay between each follower fetch

        # Add delay before fetching following
        time.sleep(5)

        #prepare to fetch followees
        following = set()
        followees_gen = profile.get_followees()
        #estimate the total number of followees for the progress bar
        for followee in tqdm(followees_gen, desc="Fetching following", total=profile.followees):
            following.add(followee)
            time.sleep(2)  # Add delay between each following fetch

    except Exception as e:
        print(f"Login failed: {e}")
        return

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
