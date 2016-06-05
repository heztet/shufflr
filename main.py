from config import *
import pytumblr

##  Register an application on https://api.tumblr.com/console and uncomment the following variables:
# CONSUMER_KEY = 
# OAUTH_KEY = 
# OAUTH_SECRET = 

GET_BLOG = ''
POST_BLOG = ''

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
	CONSUMER_KEY,
	CONSUMER_SECRET,
	OAUTH_KEY,
	OAUTH_SECRET
	)

# Make a basic request
request = client.info()

# Quit if client credentials are invalid
if not ('user' in request):
	print("Client credentials were invalid. Please fix your keys/secrets and try again.")
	raise SystemExit

# Get the client's user blogs and return an error if the POST_BlOG isn't in that list
valid_post_blogs = []
for blog in request['user']['blogs']:
	valid_post_blogs.append(blog['name'])
if not (POST_BLOG in valid_post_blogs):
	print("You do not own the blog you would like to post to.")
	raise SystemExit

# Get all posts from GET_BLOG
blog_data = client.posts(GET_BLOG)

# Post blogs to POST_BLOG
for post in blog_data['posts']:
	client.reblog(POST_BLOG, id=post['id'], reblog_key=post['reblog_key'])



