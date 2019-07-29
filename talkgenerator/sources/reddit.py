from functools import lru_cache

from prawcore import ResponseException

from talkgenerator import settings
import praw

from talkgenerator.util import os_util

singleton_reddit = None


def get_reddit():
    reddit = singleton_reddit
    if not bool(reddit):
        try:
            reddit = praw.Reddit(**settings.reddit_auth())
        except FileNotFoundError:
            print(
                "No login file for Reddit exists. Please put a JSON containing 'client_id', 'client_secret' and "
                "'user_agent' attributes in data/auth/reddit.json."
                "Please contact the creators to get access to the file or create your own app to get access to the "
                "Reddit API, as this file is not uploaded to the git for security reasons.")
    return reddit


def has_reddit_access():
    return bool(get_reddit())


def get_subreddit(name):
    if has_reddit_access():
        return get_reddit().subreddit(name)


@lru_cache(maxsize=20)
def search_subreddit(name, query, sort="relevance", limit=500, filter_nsfw=True):
    if has_reddit_access():
        try:
            submissions = list(get_subreddit(name).search(query, sort=sort, limit=limit))

            if filter_nsfw:
                submissions = [submission for submission in submissions if not submission.over_18]
            return submissions

        except ResponseException as err:
            print("Exception with accessing Reddit: {}".format(err))
    else:
        print("WARNING: No reddit access!")
