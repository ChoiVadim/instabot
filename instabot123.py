import os
import time
import random

from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from dotenv import load_dotenv


load_dotenv()
username = os.getenv('LOGIN')
password = os.getenv('PASSWORD')

hashtags = ['arlettemagazine', 'arcanamagazine', 'heavyrainmag', 'insomniamag', 'portraitphotography',
            '야외스냅', '인물촬영', '스냅사진촬영', '개인스냅', 'good_portraits_world', 'as_archive',
            'globe_portraits', 'portrait_shot', 'girlsonfilm', 'girlportrait', 'ourmag', 'portraitmood',
            '777luckyfish', 'portraituring', 'portraitgreatness', 'portraitvision_', 'theportraitbazaar',
            'фотограф', 'фотография', 'фотосессия', 'фото']

def main():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    cl = Client()
    session = cl.load_settings("session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(username, password)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                print("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(username, password)
            login_via_session = True
        except Exception as e:
            print("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            print("Attempting to login via username and password. username: %s" % username)
            if cl.login(username, password):
                login_via_pw = True
        except Exception as e:
            print("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")


    for hashtag in hashtags:
        medias = cl.hashtag_medias_recent(hashtag, 30)

        for i, media in enumerate(medias, 1):
            
            cl.media_like(media.id)
            print(f'Liked post number {i} of hashtag {hashtag}')
            time.sleep(random.randint(0, 4))

            if i % 4 == 0:
                cl.user_follow(media.user.pk)
                print(f'Followed user: {media.user.username}')
                cl.delay_range = [1, 3]       

            # except Exception as e:
            #     print("Error: %s" % e)
        

    count = 0
    followers = cl.user_following(cl.user_id)
    for user_id in followers.keys():
        try:
            if count < 50:
                cl.user_unfollow(user_id)
                count += 1
                print(f'Unfollowed users: {count}')
                cl.delay_range = [1, 3]
                
        except Exception as e:
            print("Error: %s" % e)


if __name__ == "__main__":
    main()
        

