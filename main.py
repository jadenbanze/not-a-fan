import instaloader
from tqdm import tqdm

def main():
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")

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

    #save usernames to a text file
    with open('not_following_back.txt', 'w') as file:
        for user in not_following_back:
            file.write(user.username + '\n')

    print("List of people you follow but don't follow you back has been saved to not_following_back.txt")

if __name__ == "__main__":
    main()
