import csv
import json
import os


def get_file_path(file_name):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file_path = os.path.join(project_root, 'data', file_name)
    return data_file_path


def read_from_csv(file_path) -> list[dict]:
    with open(file_path, 'r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        return list(csv_reader)


def read_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_to_json(file_path, data):
    json_object = json.dumps(data, indent=4)
    with open(file_path, 'w', encoding='utf-8') as out_file:
        out_file.write(json_object)



