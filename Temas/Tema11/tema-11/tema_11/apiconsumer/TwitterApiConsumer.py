import tweepy as tw


class TwitterApiConsumer:
    def __init__(self, api_key, api_key_secret):
        self.api_key = api_key
        self.api_key_secret = api_key_secret

        self.auth = tw.OAuthHandler(self.api_key, self.api_key_secret)
        self.api = tw.API(self.auth)

    def get_tweets_with_search_query(self, search_query, num_tweets):
        tweets = tw.Cursor(self.api.search_tweets,
                           q=search_query).items(num_tweets)
        aux_tweets = []
        for tweet in tweets:
            aux_tweets.append(tweet.text)

        return aux_tweets