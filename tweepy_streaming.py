from tweepy.streaming import streamListener
from tweepy import OAuthHandler
from tweepy import streamListener

import twitter_credentials

class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authentication and the connection to the Twitter Streaming API.
            listener = StdOutListener()
    auth = OAuthHandler(twitter credentials.CONSUMER KEY, twitter credentials.CONSUMER SECRET)
    auth.set access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener)

    stream.filter(track=hash_tag_list)


class StdOutListener(StreamListener):
    """
    This is a basic listener class that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            #following two lines will write the data to a file.
            # with open(self.fetched_tweets_filename, 'a') as tf:
            #     tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":

    hash_tag_list = ["tweet filter 1", "tweet filter 2", "tweet filter 3"]
    fetched_tweets_filename = "tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

