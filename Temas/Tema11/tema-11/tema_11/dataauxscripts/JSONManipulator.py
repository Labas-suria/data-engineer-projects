import json


def write_list_in_jason_file(path, list_to_write):
    with open(path, 'w') as outfile:
        json.dump(list_to_write, outfile)

    outfile.close()


def get_list_from_json(path):
    cache_list = []
    data = json.load(open(path, 'r'))

    for i in data:
        aux = i
        cache_list.append(aux)

    return cache_list


def get_obj_from_json(path):
    cache_dic = json.load(open(path, 'r'))
    return cache_dic
