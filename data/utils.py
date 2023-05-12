import csv
import json


def csv_json_converter(csv_file_path, json_file_path):
    csv_file = csv.DictReader(open(csv_file_path, 'r', encoding='utf-8'))
    json_list = [row for row in csv_file]

    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(json_list, file, ensure_ascii=False)

    return "File converted"


csv_json_converter('./datasets/ads.csv', './json/ads.json')
csv_json_converter('./datasets/categories.csv', './json/categories.json')
