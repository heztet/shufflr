from config import *
import pytumblr
import random

##  Register an application on https://api.tumblr.com/console and uncomment the following variables:
# CONSUMER_KEY = 
# CONSUMER_SECRET = 
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
# Get all posts from GET_BLOG
blog_data = client.posts(GET_BLOG)

# Quit if blogs were not specified
if (GET_BLOG == '' and POST_BLOG == ''):
	print("You did not specify neither a source blog or destination blog.")
	raise SystemExit
elif GET_BLOG =='':
	print("You did not specify a source blog.")
	raise SystemExit
elif POST_BLOG == '':
	print("You did not specify a destination blog.")
	raise SystemExit

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

# Quit if GET_BLOG does not exist
if not ('blog' in blog_data):
	print("The blog you are attempting to get posts from does not exist.")
	raise SystemExit

posts = blog_data['posts']
random.shuffle(posts)

# Post blogs to POST_BLOG
for post in blog_data['posts']:
	client.reblog(POST_BLOG, id=post['id'], reblog_key=post['reblog_key'])


