import logging
from environs import Env

env = Env()
env.read_env()

AWS_TALK_BUCKET_KEY = env.str("AWS_TALK_BUCKET_KEY", "")
BUCKET = AWS_TALK_BUCKET_KEY  # Shortcut for the lazy
AWS_S3_ENABLED = len(AWS_TALK_BUCKET_KEY) > 0
REDDIT_CLIENT_ID = env.str("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = env.str("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = env.str("REDDIT_USER_AGENT", "")

logger = logging.getLogger("talkgenerator")


def reddit_auth():
    return {
        "client_id": REDDIT_CLIENT_ID,
        "client_secret": REDDIT_CLIENT_SECRET,
        "user_agent": REDDIT_USER_AGENT
    }


WIKIHOW_USERNAME = env.str("WIKIHOW_USERNAME", "")
WIKIHOW_PASSWORD = env.str("WIKIHOW_PASSWORD", "")


def wikihow_auth():
    return {
        "username": WIKIHOW_USERNAME,
        "password": WIKIHOW_PASSWORD,
    }


UNSPLASH_ACCESS_KEY = env.str("UNSPLASH_ACCESS_KEY", "")
UNSPLASH_SECRET_KEY = env.str("UNSPLASH_SECRET_KEY", "")
UNSPLASH_REDIRECT_URI = env.str("UNSPLASH_REDIRECT_URI", "")
UNSPLASH_CODE = env.str("UNSPLASH_CODE", "")


def unsplash_auth():
    return {
        "unsplash_access_key": UNSPLASH_ACCESS_KEY,
        "unsplash_secret_key": UNSPLASH_SECRET_KEY,
        "unsplash_redirect_uri": UNSPLASH_REDIRECT_URI,
        "unsplash_code": UNSPLASH_CODE,
    }


def check_environment_variables():
    valid_env_file = True
    if not WIKIHOW_PASSWORD:
        logger.error("Couldn't find a WIKIHOW_PASSWORD value in an .env file.")
        valid_env_file = False

    if not WIKIHOW_USERNAME:
        logger.error("Couldn't find a WIKIHOW_USERNAME value in an .env file.")
        valid_env_file = False

    if not REDDIT_CLIENT_ID:
        logger.error("Couldn't find a REDDIT_CLIENT_ID value in an .env file.")
        valid_env_file = False

    if not REDDIT_CLIENT_SECRET:
        logger.error("Couldn't find a REDDIT_CLIENT_SECRET value in an .env file.")
        valid_env_file = False

    if not REDDIT_USER_AGENT:
        logger.error("Couldn't find a REDDIT_USER_AGENT value in an .env file.")
        valid_env_file = False

    if not valid_env_file:
        print_env_file_warning()

    return valid_env_file


def print_env_file_warning():
    env_message = '''
    Hi! Before you can run talkgenerator you need to set some secret keys in an .env file.
    
    Which keys?
    -------------
    Take a look at https://github.com/korymath/talk-generator#setting-up-required-authentication

    Creating an .env file
    ------------- 
    $ touch .env
    $ echo VARIABLE_NEEDED=VALUE >> .env
    $ echo OTHER_VARIABLE_NEEDED=VALUE >> .env

    or you can use your favorite text editor (vi, nano, etc) to create it.
    '''

    logger.error(env_message)
