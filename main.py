from config import *
import pytumblr

##  Register an application on https://api.tumblr.com/console and uncomment the following variables:
# CONSUMER_KEY = 
# OAUTH_KEY = 
# OAUTH_SECRET = 

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
	CONSUMER_KEY,
	CONSUMER_SECRET,
	OAUTH_KEY,
	OAUTH_SECRET
	)

# Make a basic request
request = client.info()
print(request)
