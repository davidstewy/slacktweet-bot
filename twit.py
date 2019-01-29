import sys
import os
import logging
from datetime import datetime as dt
import time
import tweepy

from threading import thread

logger = logging.getLogger(os.path.basename(__file__))
exit_flag = False

# Monkey patch for the tweepy.Stream class!
def _start(self, is_async):
    self.running = True
    if is_async:
        print("starting ASYNC stream as DAEMON thread")
        self._thread= thread(name='tweepy.thread', target=self._run, daemon=True)
        self._thread.start()
    else:
        self._run()

print('**** Applying Monkey Patch to tweepy.Stream ****')
tweepy.stream_start = _start


class TwitterClient(tweepy.StreamListener):
    """ My own Twitterclient class. Inherits from tweepy """
    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret):

        auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
        auth.set_access_token(acess_token, access_token_secret)
        
        self.api = tweepy.API(auth)
        self.stream_handler = None
        assert self.api is not None
        logger.debug('Twitter client is setup')

    def __enter__(self):
        """ Implement twitterClient as a context manager """
        logger.warn('Enter TwitterClient')
        return self

    def __exit__(self ,type, value, traceback):

        logger.warn('Exit TwitterClient')
        """ Implement twitterClient as a context manager """
        # If we were streaming, then shut down the stream
        if self.stream is not None:
            self.stream.disconnect()
        

    def on_status(self, status):
        """ Callback for receiving tweets """
        if self.stream_handler is not None:
            return self.stream_handler(status)
        # return False to disconnect from tweepy, True to stay connected.
        return (not exit_flag)
        

    def register_stream_handler(self, func):
        """ Allows an external thing to hook into our tweet stream """
        self.stream_handler = func


    def on_error(self, status_code):
        """ Called when a non-200 status code is returned """
        # Return False to disconnect stream, True to reconnect with backoff.
        logger.warn('Tweepy error:{}'.format(error_code))
        if error_code == 420:
            return False
        logger.warn('Attempting to reconnect to twitter...')
        return True


    def create_stream(self, track_list):
        # We create our own instatnce of a tweepy stream
        if self.stream is not None:
            self.stream.disconnect()
        self.stream = tweepy.Stream(auth=self.api.auth, listener=self)
        #We call the filter method on our own stream object
        self.stream.filter(track=track_list, is_async=True)
        logger.info('Subscribed to keyword{}'.format(track_list))


def main(loglevel):
    # # """ copy from dirwatcher """
    # logging.basicConfig(
    #     stream=sys.stout,
    #     level='DEBUG'
    #     format=
    #     datefmt=
    #     )

    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(name)-12s '
                            '%(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
    logger.setLevel(logging.DEBUG)
    app_start_time = dt.datetime.now()
    logger.info(
        '\n'
        '--------------------------------------------------\n'
        '       Running {0}\n'
        '       Started on {1}\n'
        '       loglevel is [2]\n'
        '--------------------------------------------------\n'
        .format(__file__, app_start_time.isoformat(), loglevel)
    )
    parser = create_parser()
    args = parser.parse_args()
    watch_directory(args)
    uptime = dt.datetime.now()-app_start_time
    logger.info(
        '\n'
        '--------------------------------------------------\n'
        '       Stopped {0}\n'
        '       Uptime was {1}\n'
        '--------------------------------------------------\n'
        .format(__file__, str(uptime))
    )


    #create an instance of TwitterClient (context manager)
    with TwitterClient(
        access_token=os.environ.get('ACCESS_TOKEN'),
        access_secret=os.environ.get('ACCESS_SECRET'),
        consumer_key=os.environ.get('CONSUMER_KEY'),
        consumer_secret=os.environ.get('CONSUMER_SECRET')
    ) as twc:
    # This is an async method, so it will NOT BLOCK us.
        twc.create_stream(['python'])

        try:
            while not exit_flag:
                time.sleep(2.0)
                logger.debug('zzzz....')
        except KeyboardInterrupt:
            pass
            logger.warn('Done with main loop')
            
    logger.warn('Done with main loop')

if __name__ == "__main__":
    loglevel = sys.argv[1]
    main(loglevel)