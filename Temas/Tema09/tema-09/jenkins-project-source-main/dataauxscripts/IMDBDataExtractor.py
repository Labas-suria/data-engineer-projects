from pandas import read_csv
import json
import os
from dataauxscripts import JSONManipulator

MIN_YEAR = 2012

TITLE_BASIC_PATH = 'data/imdbdata/original/title.basics.tsv.gz'
NAME_BASIC_PATH = 'data/imdbdata/original/name.basics.tsv.gz'
TITLE_PRINCIPALS_PATH = 'data/imdbdata/original/title.principals.tsv.gz'

PATH_FILM_INFO_JSON = 'data/imdbdata/transformed/film_info.json'
PATH_TOP_TEN = 'data/imdbdata/transformed/top_ten_actors.json'

CHUNK_SIZE = 1000000


def title_basic_gz_to_json():
    d_type = {'startYear': 'string'}
    title_basic_data = read_csv(TITLE_BASIC_PATH, compression='gzip', sep='\t', chunksize=CHUNK_SIZE,
                                on_bad_lines='skip', usecols=['tconst', 'titleType', 'originalTitle', 'startYear'],
                                dtype=d_type)

    film_info_list = []
    for data in title_basic_data:

        df_mask = data.titleType == 'movie'
        filtered_data = data[df_mask]

        for lin in filtered_data.values:
            if lin[3] != '\\N':  # lin[3] == startYear.
                if int(lin[3]) >= MIN_YEAR:
                    film_info_list.append([lin[0], lin[2]])  # lin[0] == tconst, lin[2] == originalTitle

    with open(PATH_FILM_INFO_JSON, 'w') as outfile:
        json.dump(film_info_list, outfile)


def get_title_basic_dic():
    data = json.load(open(PATH_FILM_INFO_JSON, 'r'))

    dic_titles = {}
    for lin in data:
        dic_titles[lin[0]] = lin[1]  # lin[0] == tconst, lin[1] == originalTitle

    return dic_titles


def search_name_basic_data(nconst):
    name_basic_data = read_csv(NAME_BASIC_PATH, compression='gzip', sep='\t', chunksize=CHUNK_SIZE, on_bad_lines='skip',
                               usecols=['nconst', 'primaryName', 'primaryProfession'])
    for data in name_basic_data:
        df_mask = data['nconst'] == nconst
        filtered_df = data[df_mask]
        if len(filtered_df.values) > 0:
            return filtered_df.values[0]  # ['nconst', 'primaryName', 'primaryProfession']


def top_ten_acts_to_json():
    title_princ_data = read_csv(TITLE_PRINCIPALS_PATH, compression='gzip', sep='\t', chunksize=CHUNK_SIZE,
                                on_bad_lines='skip',
                                usecols=['tconst', 'nconst'])

    dic_title = get_title_basic_dic()
    actor_num_films_dic = {}
    
    for data in title_princ_data:
        for lin in data.values:
            if dic_title.get(lin[0]) is not None:  # tconst in filtered databases

                if actor_num_films_dic.get(lin[1]) is not None:  # lin[1] == nconst
                    actor_num_films_dic[lin[1]] = actor_num_films_dic.get(lin[1]) + 1
                else:
                    actor_num_films_dic[lin[1]] = 1

    actors_list = []
    aux_actor_num_films_dic = sorted(actor_num_films_dic,
                                     key=actor_num_films_dic.get, reverse=True)
    
    while len(actors_list) < 10:

        tmp_to_actor_list = aux_actor_num_films_dic.pop(0)
        tmp_name_pkg = search_name_basic_data(tmp_to_actor_list)

        if 'actor' in str(tmp_name_pkg[2]) or \
                'actress' in str(tmp_name_pkg[2]):  # tmp_name_pkg[2] == primaryProfession
            actors_list.append([actor_num_films_dic.get(tmp_to_actor_list),
                                tmp_name_pkg[1]])  # tmp_name_pkg[1] == primaryName

    JSONManipulator.write_list_in_jason_file(PATH_TOP_TEN, actors_list)

    if os.path.exists(TITLE_BASIC_PATH) and \
            os.path.exists(NAME_BASIC_PATH) \
            and os.path.exists(TITLE_PRINCIPALS_PATH):
        os.remove(TITLE_BASIC_PATH)
        os.remove(NAME_BASIC_PATH)
        os.remove(TITLE_PRINCIPALS_PATH)


def get_top_ten_acts_list():
    cache_list = []
    data = json.load(open(PATH_TOP_TEN, 'r'))

    for lin in data:
        cache_list.append(lin)

    return cache_list
