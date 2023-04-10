from dataauxscripts import DownloadIMDBData, IMDBDataExtractor, JSONManipulator
from apiconsumer.TwitterApiConsumer import TwitterApiConsumer
import logging
from datetime import datetime
import boto3
import csv

LOGGER_NAME_MAIN = 'main'

logger_main = logging.getLogger(LOGGER_NAME_MAIN)
logger_main.setLevel(logging.INFO)

logging.basicConfig(format='\n%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

PROPERTIES_PATH = 'access.properties'
LAST_UPDATE_PATH = 'last_update.json'
TWEETS_FOLDER_PATH = 'data/twitterdata/'
S3_BUCKET_NAME = 'jt-dataeng-felipenogueira'
S3_FOLDER_PATH = 'Tema08/actors_tweets/'

TWEETS_CSV_FOLDER_PATH = 'logs/twitterdata/tweets.csv'
TWEETS_CSV_NAME_LOG = 'tweets_log.csv'
TWEETS_CSV_NAME = 'tweets.csv'

NUM_TWEETS = 10


def data_daily_update():
    today_date = datetime.today().strftime('%Y-%m-%d')
    last_date = JSONManipulator.get_obj_from_json(LAST_UPDATE_PATH)
    if last_date != today_date:
        DownloadIMDBData.download_data()
        logger_main.info('Data Processing...')

        logger_main.info('running title_basic_gz_to_json()...')
        IMDBDataExtractor.title_basic_gz_to_json()
        logger_main.info('title_basic_gz_to_json() finished!')

        logger_main.info('running top_ten_acts_to_json()...')
        IMDBDataExtractor.top_ten_acts_to_json()
        logger_main.info('top_ten_acts_to_json() finished!')

        logger_main.info('caching top ten actors list...')
        JSONManipulator.write_list_in_jason_file(LAST_UPDATE_PATH, today_date)
        logger_main.info('Done!')


def save_tweet_list_in_csv(csv_path, tweets_list=[], fields=[]):
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        write = csv.writer(file)
        write.writerow(fields)
        write.writerows(tweets_list)


if __name__ == '__main__':
    s3 = boto3.resource('s3')
    data_daily_update()

    properties = JSONManipulator.get_obj_from_json(PROPERTIES_PATH)
    api_key = properties.get('api_key')
    api_key_secret = properties.get('api_key_secret')
    api_user = TwitterApiConsumer(api_key, api_key_secret)

    top_actors_list = IMDBDataExtractor.get_top_ten_acts_list()

    bucket = s3.Bucket(S3_BUCKET_NAME)

    actor_tweets_list_log = []
    fields_csv_log = ['name', 'tweet_length', 'date']

    actor_tweets_list = []
    fields_csv = ['name', 'tweet']

    for lin in top_actors_list:
        search_query = lin[1] + " -filter:retweets"
        cache_list = api_user.get_tweets_with_search_query(search_query, NUM_TWEETS)

        for tweet in cache_list:
            full_today_time = datetime.today()
            processed_tweet = tweet.replace(',','')
            processed_tweet = processed_tweet.replace('\n',' ')
            actor_tweets_list_log.append([lin[1], processed_tweet, full_today_time])
            actor_tweets_list.append([lin[1], tweet])
            
    tweets_csv_path = TWEETS_FOLDER_PATH + TWEETS_CSV_NAME_LOG  # to save logs
    save_tweet_list_in_csv(tweets_csv_path, actor_tweets_list_log, fields_csv_log)

    tweets_csv_path = TWEETS_FOLDER_PATH + TWEETS_CSV_NAME  # to save tweets for S3
    save_tweet_list_in_csv(tweets_csv_path, actor_tweets_list, fields_csv)

    full_today_time = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    s3.meta.client.upload_file(tweets_csv_path, S3_BUCKET_NAME, S3_FOLDER_PATH +
                               full_today_time + TWEETS_CSV_NAME)
