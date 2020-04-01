import csv
import json
import os
from os import path


def get_all_output_dirs(dir_path):
    dirs = [os.path.join(dir_path, o) for o in os.listdir(dir_path)
            if os.path.isdir(os.path.join(dir_path, o))]
    print(dirs)
    return dirs


def preprocess_user_data():
    dir_list = get_all_output_dirs('./outputs/')
    aggregated_list = []
    for dirpath in dir_list:
        aggregated = {
            'inspections': {
                'Best Practices': 0, 'Code Style': 0, 'Design': 0, 'Documentation': 0, 'Error Prone': 0,
                'Multithreading': 0, 'Performance': 0, 'Security': 0,
            },
        }
        # DATA PROCESSING
        categorized = load_data(dirpath)
        if categorized is None:
            continue
        for ruleset in categorized:
            ruleset_key = ruleset['Rule set']
            if ruleset_key not in aggregated['inspections']:
                continue
            for ruleKey, ruleVal in ruleset.items():
                aggregated['inspections'][ruleset_key] += 1

        # META PROCESSING
        meta = load_meta(dirpath)
        meta["languages"] = len(meta["languages"])
        aggregated['meta'] = meta
        print(aggregated)
        aggregated_list.append(aggregated)
    generate_dataset(aggregated_list)


def load_data(dirpath):
    try:
        data_raw = open(path.join(dirpath, 'data.json')).read()
        categorized = json.loads(data_raw)
        return categorized
    except:
        return None


def load_meta(dirpath):
    meta_raw = open(path.join(dirpath, 'meta.json')).read()
    meta = json.loads(meta_raw)
    return meta


def generate_dataset(aggregated_list):
    # flattening
    flattened = []
    for deep_data in aggregated_list:
        flat_data = {
            **deep_data.get('meta'),
        }
        key: str
        for key, val in deep_data.get('inspections').items():
            new_key = key.lower().replace(' ', '_')
            flat_data[f'ins_{new_key}'] = val
        flattened.append(flat_data)

    # writing to file
    keys = flattened[0].keys()
    with open('./outputs/dataset.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(flattened)
