# create slack_client class first
#     have a SET 
#         "at Bob-Bot..."

#     create twitter client inside slack_client
#         CRUD

# pip install slackclient into virtual env
# $ pipenv install slackclient

# slackclient library
import slackclient
from twit import TwitterClient



class SlackBot:
    def __init__(self, bot_user_token, bot_token=None):
        self.sc = slackclient.SlackClient(token=bot_user_token)
        self.bot_id = bot_id
        if not self.bot_id and self.sc.rtm_connect(with_team_state=False):
            #get our bot's "BOT_ID" if it was not given to us
            response = self.sc.api_call('auth.test')
            self.bot_id = response.get('user_id')
        # this string allows me to filter away msgs not directed at me
        self.at_bot = '<@' + self.bot_id + '>'





def main():
        

if __name__=='__main__':
    main()

