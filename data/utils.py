import csv
import json


def csv_json_converter(csv_file_path, json_file_path, model_path):
    """
    Function for converting csv to json (as django required) steps depends on differences in initial data
    In this case differences are: format no for Django, line breakers in text, wrong register
    :param csv_file_path: path to file with initial data
    :param json_file_path: path to json file
    :param model_path:name that model should have
    :return: -
    """
    csv_file = csv.DictReader(open(csv_file_path, 'r', encoding='utf-8'))

    json_list = [row for row in csv_file]
    upd_data = []
    for item in json_list:
        new_item = {k.lower(): v.replace("\n", " ") for k, v in item.items()}
        upd_data.append(new_item)

    bool_upd_data = []
    for item in upd_data:
        if "is_published" in item.keys():
            if item["is_published"] == "TRUE":
                item["is_published"] = True
            else:
                item["is_published"] = False
            bool_upd_data.append(item)
        else:
            bool_upd_data = upd_data

    django_format_data = []
    for item in bool_upd_data:
        new_item = {"pk": item["id"], "model": model_path, "fields": {k: v for k, v in item.items() if k != "id"}}
        django_format_data.append(new_item)
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(django_format_data, file, ensure_ascii=False)


csv_json_converter('./datasets/ads.csv', '../fixtures/ads.json', 'ads.ads')
csv_json_converter('./datasets/categories.csv', '../fixtures/categories.json', 'ads.categories')
