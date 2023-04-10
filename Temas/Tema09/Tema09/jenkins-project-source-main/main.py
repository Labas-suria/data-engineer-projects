from dataauxscripts import DownloadIMDBData, IMDBDataExtractor, JSONManipulator
from apiconsumer.TwitterApiConsumer import TwitterApiConsumer
import logging
from datetime import datetime
import boto3

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

PROPERTIES_PATH = 'access.properties'
LAST_UPDATE_PATH = 'last_update.json'
TWEETS_FOLDER_PATH = 'data/twitterdata/'
S3_BUCKET_NAME = 'jt-dataeng-felipenogueira'
S3_FOLDER_PATH = 'Tema08/actors_tweets/'
NUM_TWEETS = 10


def data_daily_update():
    today_date = datetime.today().strftime('%Y-%m-%d')
    last_date = JSONManipulator.get_obj_from_json(LAST_UPDATE_PATH)
    if last_date != today_date:
        DownloadIMDBData.download_data()
        logging.info('Data Processing...')
        IMDBDataExtractor.title_basic_gz_to_json()
        IMDBDataExtractor.top_ten_acts_to_json()
        JSONManipulator.write_list_in_jason_file(LAST_UPDATE_PATH, today_date)
        logging.info('Done!')


if __name__ == '__main__':
    s3 = boto3.resource('s3')
    data_daily_update()

    properties = JSONManipulator.get_obj_from_json(PROPERTIES_PATH)
    api_key = properties.get('api_key')
    api_key_secret = properties.get('api_key_secret')
    api_user = TwitterApiConsumer(api_key, api_key_secret)

    top_actors_list = IMDBDataExtractor.get_top_ten_acts_list()

    bucket = s3.Bucket(S3_BUCKET_NAME)
    bucket.objects.filter(Prefix=S3_FOLDER_PATH).delete()

    for lin in top_actors_list:
        search_query = lin[1] + " -filter:retweets"
        cache_list = api_user.get_tweets_with_search_query(search_query, NUM_TWEETS)
        file_name = lin[1] + '.json'
        path = TWEETS_FOLDER_PATH + file_name
        JSONManipulator.write_list_in_jason_file(path, cache_list)
        s3.meta.client.upload_file(path, S3_BUCKET_NAME, S3_FOLDER_PATH + file_name)
