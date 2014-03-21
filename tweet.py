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
	latest_status = api.GetHomeTimeline(count=1)
	latest_status_text = latest_status[0].text.lower()
	latest_status_id = latest_status[0].id

	if "what" in latest_status_text and "temperature" in latest_status_text:
		api.DestroyStatus(latest_status_id)
		print "Getting and tweeting temp!"
		api.PostUpdate("The current temperature is %d deg. %s" % (current_temp, time.ctime()))

def tweet(tweet):
	try:
		api.PostUpdate("%s %s" % (tweet, time.ctime()))
	except:
		pass
