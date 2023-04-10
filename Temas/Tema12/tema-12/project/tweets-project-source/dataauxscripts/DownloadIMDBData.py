import logging
import sys
from urllib import request
import os

logging.basicConfig(format='\n%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

LOGGER_NAME = 'downloader'

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)

URL_NAME_BASICS = 'https://datasets.imdbws.com/name.basics.tsv.gz'
FILE_NM_NAME_BASICS = 'name.basics.tsv.gz'

URL_TITLE_BASICS = 'https://datasets.imdbws.com/title.basics.tsv.gz'
FILE_NM_TITLE_BASICS = 'title.basics.tsv.gz'

URL_TITLE_PRINCIPALS = 'https://datasets.imdbws.com/title.principals.tsv.gz'
FILE_NM_TITLE_PRINCIPALS = 'title.principals.tsv.gz'


def report(count, blockSize, totalSize):
    percent = int(count * blockSize * 100 / totalSize)
    sys.stdout.write("\r%d%%" % percent + ' complete')
    sys.stdout.flush()


def download_data():
    path_to_root = os.getcwd()

    name_basics_file = os.path.join(path_to_root, 'data', 'imdbdata', 'original', FILE_NM_NAME_BASICS)
    logger.info('Starting download: ' + FILE_NM_NAME_BASICS)
    request.urlretrieve(URL_NAME_BASICS, name_basics_file, reporthook=report)

    title_basics_file = os.path.join(path_to_root, 'data', 'imdbdata', 'original', FILE_NM_TITLE_BASICS)
    logger.info('Starting download: ' + FILE_NM_TITLE_BASICS)
    request.urlretrieve(URL_TITLE_BASICS, title_basics_file, reporthook=report)

    title_principals_file = os.path.join(path_to_root, 'data', 'imdbdata', 'original', FILE_NM_TITLE_PRINCIPALS)
    logger.info('Starting download: ' + FILE_NM_TITLE_PRINCIPALS)
    request.urlretrieve(URL_TITLE_PRINCIPALS, title_principals_file, reporthook=report)