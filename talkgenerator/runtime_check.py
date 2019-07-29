import talkgenerator.util.language_util
import talkgenerator.settings 

def check_that_we_can_run():
    check_env = talkgenerator.settings.check_environment_variables()
    if check_env:
        print("Environment Variables passed")

    check_ntlk = talkgenerator.util.language_util.check_and_download()
    if check_ntlk:
        print ("NLTK Dictionaries available")
        
    return (check_ntlk and check_env)
