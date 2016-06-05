from config import *
import pytumblr
import random

def validate_client(client):
	request = client.info()
	# Quit if client credentials are invalid
	if not ('user' in request):
		print("Client credentials were invalid. Please fix your keys/secrets and try again.")
		raise SystemExit

def validate_blogs(client, GET_BLOG, POST_BLOG):
	request = client.info()

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

	# Get the client's user blogs and return an error if the POST_BlOG isn't in that list
	valid_post_blogs = []
	for blog in request['user']['blogs']:
		valid_post_blogs.append(blog['name'])
	if not (POST_BLOG in valid_post_blogs):
		print("You do not own the blog you would like to post to.")
		raise SystemExit

	# Quit if GET_BLOG does not exist
	blog_data = client.posts(GET_BLOG)
	if not ('blog' in blog_data):
		print("The blog you are attempting to get posts from does not exist.")
		raise SystemExit

def retrieve_posts(client, GET_BLOG):
	data = client.posts(GET_BLOG)
	return data['posts']

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
	CONSUMER_KEY,
	CONSUMER_SECRET,
	OAUTH_KEY,
	OAUTH_SECRET
	)

# Check that client and blog inputs are valid
validate_client(client)
validate_blogs(client, GET_BLOG, POST_BLOG)

# Get all posts from GET_BLOG
posts = retrieve_posts(client, GET_BLOG)
random.shuffle(posts)

# Post blogs to POST_BLOG
for post in posts:
	client.reblog(POST_BLOG, id=post['id'], reblog_key=post['reblog_key'])
	print('Posted (id: %s)' % post['id'])