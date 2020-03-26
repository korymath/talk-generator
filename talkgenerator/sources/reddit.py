import datetime
import logging
from functools import lru_cache
from pathlib import Path

import praw
from cachier import cachier
from prawcore import ResponseException
from prawcore import RequestException

from talkgenerator import settings

singleton_reddit = None

logger = logging.getLogger("talkgenerator")


def get_reddit():
    reddit = singleton_reddit
    if not bool(reddit):
        reddit = praw.Reddit(**settings.reddit_auth())
    return reddit


def has_reddit_access():
    return bool(get_reddit())


def get_subreddit(name):
    if has_reddit_access():
        subreddit = get_reddit().subreddit(name)
        if subreddit:
            return subreddit


@lru_cache(maxsize=20)
@cachier(
    cache_dir=Path("..", "tmp").absolute(), stale_after=datetime.timedelta(weeks=2)
)
def search_subreddit(name, query, sort="relevance", limit=500, filter_nsfw=True):
    if has_reddit_access():
        try:
            submissions = list(
                get_subreddit(name).search(query, sort=sort, limit=limit)
            )

            if filter_nsfw:
                submissions = [
                    submission for submission in submissions if not submission.over_18
                ]
            return submissions

        except ResponseException as err:
            logger.error("Exception with accessing Reddit: {}".format(err))
        except RequestException as err:
            logger.error("Exception with accessing Reddit: {}".format(err))
    else:
        logger.warning("WARNING: No reddit access!")
