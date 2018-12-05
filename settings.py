from environs import Env

env = Env()
env.read_env()

AWS_TALK_BUCKET_KEY = env.str("AWS_TALK_BUCKET_KEY", "")
BUCKET = AWS_TALK_BUCKET_KEY # Shortcut for the lazy
AWS_S3_ENABLED = len(AWS_TALK_BUCKET_KEY) > 0 

REDDIT_CLIENT_ID=env.str("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET=env.str("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT=env.str("REDDIT_USER_AGENT")

def reddit_auth():
    return {
  "client_id": REDDIT_CLIENT_ID,
  "client_secret": REDDIT_CLIENT_SECRET,
  "user_agent": REDDIT_USER_AGENT
    }

WIKIHOW_USERNAME=env.str("WIKIHOW_USERNAME")
WIKIHOW_PASSWORD=env.str("WIKIHOW_PASSWORD")

def wikihow_auth():
    return {
  "username": WIKIHOW_USERNAME,
  "password": WIKIHOW_PASSWORD,
    }