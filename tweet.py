import time

import twitter

import twitter_tokens

api = twitter.Api(
        consumer_key=twitter_tokens.api_key,
        consumer_secret=twitter_tokens.api_secret,
        access_token_key=twitter_tokens.access_token,
        access_token_secret=twitter_tokens.access_token_secret
    )

# api.PostUpdate("This is the first tweet")
def temp_request(current_temp):
    print "Working temp request"
    try:
        latest_status = api.GetHomeTimeline(count=1)
        latest_status_text = latest_status[0].text.lower()
        latest_status_id = latest_status[0].id

        if "what" in latest_status_text and "temperature" in latest_status_text:
            api.DestroyStatus(latest_status_id)
            print "Getting and tweeting temp!"
            api.PostUpdate("The current temperature is %d deg. (%s)" % (current_temp, time.ctime()))
    except Exception as e:
        print "There is a problem with connecting to twitter at %s, please check your internet connection. The exception is %s" % (time.ctime(), e)
        pass

def tweet(tweet):
    try:
        api.PostUpdate("%s (%s)" % (tweet, time.ctime()))
    except Exception as e:
        print "There is a problem connecting to twitter, could not tweet '%s' at %s due to exception %s" % (tweet, time.ctime(), e)
        pass

# from twython import Twython

# twy = Twython(
#         twitter_tokens.api_key,
#         twitter_tokens.api_secret,
#         twitter_tokens.access_token,
#         twitter_tokens.access_token_secret
#     )

# photo = open("/Users/macuser/Desktop/Programming/python/data_analysis/temp.png", 'rb')

# twy.update_status_with_media(media=photo, status="Testing temp graphs.")
