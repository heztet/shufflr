from config import *
import pytumblr
import random
import math
import sys

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
	offset_int = 0
	posts = []
	data = {'posts': ['not_empty']}

	# Get total number of posts
	total_posts = get_post_total(client, GET_BLOG)

	if notes:
		while len(data['posts']) > 0:
			data = client.posts(GET_BLOG, notes_info=True, offset=offset_int)
			for post in data['posts']:
				posts.append(post)
			offset_int += 20
			#print('Stepping... (on post %d)' % offset_int)
			progress_bar(offset_int, total_posts)
	else:
		while len(data['posts']) > 0:
			data = client.posts(GET_BLOG, notes_info=False, offset=offset_int)
			for post in data['posts']:
				posts.append(post)
			offset_int += 20
			#print('Stepping... (on post %d)' % offset_int)
			progress_bar(offset_int, total_posts)
	end_progress_bar()
	return posts

def get_post_total(client, GET_BLOG):
	request = client.posts(GET_BLOG)
	return request['total_posts']

# Sorts an array of posts by number of notes (descending)
def sort_likes(arr):
	return sorted(arr, key = lambda post: post['note_count'], reverse=True)

def sort_tiered(arr, total):
	# Get number of posts per tier
	top_end = int(math.floor(0.2 * len(arr)))
	middle_end = int(math.floor(0.3 * len(arr)))

	# Sort by likes descending first
	arr = sort_likes(arr)

	# Split into tiers
	top = arr[0:top_end]
	middle = arr[(top_end+1):middle_end]
	bottom = arr[(middle_end+1)::]

	tiers = [top, middle, bottom]

	# Shuffle tiers and recombine
	posts = []
	for tier in tiers:
		random.shuffle(tier)
		for post in tier:
			posts.append(post)

	return posts

def progress_bar(current, end, length=20):
	# Ensure that progress bar isn't maxed out
	if current > end:
		current = end

	# Create pieces of progress bar
	percent = float(current) / end
	bar = '#' * int(round(percent * length))
	spaces = ' ' * (length - len(bar))

	# Write to console
	sys.stdout.write("\rPercent: [{0}] {1}% ({2}/{3}) ".format(bar + spaces, int(round(percent * 100)), current, end))
	sys.stdout.flush()

def end_progress_bar():
	print('')

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
print('(3) By Tiers')

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
print('')

# Get all posts from GET_BLOG
print('Fetching posts...')
if user_input == 1: # Does not need notes
	posts = retrieve_posts(client, GET_BLOG, notes=False)
else:
	posts = retrieve_posts(client, GET_BLOG, notes=False)


# Sort posts
if user_input == 1:
	random.shuffle(posts)
elif user_input == 2:
	posts = sort_likes(posts)
elif user_input == 3:
	total_posts = get_post_total(client, GET_BLOG)
	posts = sort_tiered(posts, total_posts)

# Post blogs to POST_BLOG
print('Posting to blog...')
if posts == [] or posts is None:
	print('There was nothing to post!')
else:
	total = len(posts)
	count = 0
	for post in posts[::-1]: # Reverses post order so that most desired posts are at the top
		client.reblog(POST_BLOG, id=post['id'], reblog_key=post['reblog_key'])
		count += 1
		progress_bar(count, total)
	end_progress_bar
print('Done!')