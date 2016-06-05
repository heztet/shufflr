# shufflr
Posts a shuffled instance of a Tumblr blog to a specified Tumblr blog. Uses Python 2.7.

# How to start
Register an application on https://api.tumblr.com/console and place the following variables in a file called `config.py`:
* `CONSUMER_KEY` --> Provided by Tumblr
* `CONSUMER_SECRET` --> Provided by Tumblr
* `OAUTH_KEY` --> Provided by Tumblr
* `OAUTH_SECRET` --> Provided by Tumblr
* 'GET_BLOG' --> The blog you're getting posts from
* 'POST_BLOG' --> The blog you're posting to