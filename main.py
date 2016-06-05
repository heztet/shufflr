from config import *
import pytumblr
import random

# Checks that the client is valid
# Exits if validation fails
def validate_client(client):
	request = client.info()
	# Quit if client credentials are invalid
	if not ('user' in request):
		print("Client credentials were invalid. Please fix your keys/secrets and try again.")
		raise SystemExit
	else:
		print("Client validated!")

# Checks that both input blogs are valid
# Exits otherwise
def validate_blogs(client, GET_BLOG, POST_BLOG):
	has_error = False
	errors = []

	request = client.info()

	# Blogs were not specified
	if (GET_BLOG == '' and POST_BLOG == ''):
		errors.append("You did not specify neither a source blog or destination blog.")
		has_error = True
	elif GET_BLOG =='':
		errors.append("You did not specify a source blog.")
		has_error = True
	elif POST_BLOG == '':
		errors.append("You did not specify a destination blog.")
		has_error = True

	# Get the client's user blogs and return an error if the POST_BlOG isn't in that list
	valid_post_blogs = []
	for blog in request['user']['blogs']:
		valid_post_blogs.append(blog['name'])
	if not (POST_BLOG in valid_post_blogs):
		errors.append("You do not own the blog you would like to post to.")
		has_error = True

	# GET_BLOG does not exist
	blog_data = client.posts(GET_BLOG)
	if not ('blog' in blog_data):
		errors.append("The blog you are attempting to get posts from does not exist.")
		has_error = True

	# Print errors and quit if they exist
	if has_error:
		print("The following problems were encountered:")
		print()

		for error in errors:
			print("* %s" % error)

		raise SystemExit
	else:
		print("Source and destination blogs found!")

# Returns posts from GET_BLOG
def retrieve_posts(client, GET_BLOG, notes=False):
	if notes:
		data = client.posts(GET_BLOG, notes_info=True)
	else:
		data = client.posts(GET_BLOG)
	return data['posts']

# Randomly shuffles an array of posts
def sort_random(arr):
	return random.shuffle(arr)

# Sorts an array of posts by number of notes (descending)
def sort_likes(arr):
	return sorted(arr, key = lambda post: len(post['notes']), reverse=True)

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


# Get sort method from user
print('')
print('Choose a sorting method:')
print('(1) Random')
print('(2) By Notes (descending)')
print('')

user_input = ''
while user_input == '':
	user_input = input('> ')

	# Convert to integer
	try:
		user_input = int(user_input)
	except:
		print("Input was not an integer.")
		user_input = ''

	# Check that input is in range
	if (user_input < 1) or (user_input > 3):
		print('Please select a given option')
		user_input = ''

# Get all posts from GET_BLOG
if user_input == 1: # Does not need notes
	posts = retrieve_posts(client, GET_BLOG)
else:
	posts = retrieve_posts(client, GET_BLOG, notes=True)

# Sort posts
if user_input == 1:
	posts = sort_random(posts)
elif user_input == 2:
	posts = sort_likes(posts)

for post in posts:
	print(len(post['notes']))

# Post blogs to POST_BLOG
# Reverses post order so that most desired posts are at the top
for post in posts.reverse():
	client.reblog(POST_BLOG, id=post['id'], reblog_key=post['reblog_key'])
	print('Posted (id: %s)' % post['id'])
