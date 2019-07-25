from environs import Env

env = Env()
env.read_env()

AWS_TALK_BUCKET_KEY = env.str("AWS_TALK_BUCKET_KEY", "")
BUCKET = AWS_TALK_BUCKET_KEY  # Shortcut for the lazy
AWS_S3_ENABLED = len(AWS_TALK_BUCKET_KEY) > 0
REDDIT_CLIENT_ID = env.str("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = env.str("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = env.str("REDDIT_USER_AGENT")
WIKIHOW_USERNAME = env.str("WIKIHOW_USERNAME")
WIKIHOW_PASSWORD = env.str("WIKIHOW_PASSWORD")
UNSPLASH_ACCESS_KEY = env.str("UNSPLASH_ACCESS_KEY")
UNSPLASH_SECRET_KEY = env.str("UNSPLASH_SECRET_KEY")
UNSPLASH_REDIRECT_URI = env.str("UNSPLASH_REDIRECT_URI")
UNSPLASH_CODE = env.str("UNSPLASH_CODE")


def reddit_auth():
    return {
        "client_id": REDDIT_CLIENT_ID,
        "client_secret": REDDIT_CLIENT_SECRET,
        "user_agent": REDDIT_USER_AGENT
    }


def wikihow_auth():
    return {
        "username": WIKIHOW_USERNAME,
        "password": WIKIHOW_PASSWORD,
    }


def unsplash_auth():
    return {
        "unsplash_access_key": UNSPLASH_ACCESS_KEY,
        "unsplash_secret_key": UNSPLASH_SECRET_KEY,
        "unsplash_redirect_uri": UNSPLASH_REDIRECT_URI,
        "unsplash_code": UNSPLASH_CODE,
    }
