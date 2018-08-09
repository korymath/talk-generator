import json
from functools import lru_cache

import praw

singleton_reddit = None


def get_reddit():
    reddit = singleton_reddit
    if not bool(reddit):
        try:
            reddit_login = json.load(open("./data/auth/reddit.json"))
            reddit = praw.Reddit(**reddit_login)
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
def search_subreddit(name, query, sort="relevance", limit=200):
    if has_reddit_access():
        return list(get_subreddit(name).search(query, sort=sort, limit=limit))
    else:
        print("WARNING: No reddit access!")
