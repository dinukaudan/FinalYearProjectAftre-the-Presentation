import json
import os

from analyzer.counter import count_lines
from analyzer.repo_info import RepoInfoFetcher
from deep_learning.core import get_prediction_for_user_id
from deep_learning.preprocess import preprocess_user_data
from utils import utils, generate_dictionary


########################################
# all utilities required by the analyzer
########################################
def generate_analysis_csv(csv_path):
    os.system(f'pmd -d ./repos/ -R rulesets/java/quickstart.xml,ruleset.xml -f csv > {csv_path}')


def generate_meta_json(username):
    repo_meta = RepoInfoFetcher.get_repo_info(username)
    with open(f'./outputs/{username}/meta.json', 'w') as outfile:
        json.dump(repo_meta, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)


def save_current_user(username):
    utils.create_folder_if_not_exist(f'./outputs/{username}')
    data = {'username': username}
    with open(f'./settings/current_username.json', 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)


def get_current_user():
    raw = open(f'./settings/current_username.json').read()
    username = json.loads(raw)['username']
    return username


def categorize_inspections(unsorted_inspections):
    inspections = {}
    for item in unsorted_inspections:
        ruleset = item['Rule set']
        rule = item['Rule']
        if ruleset not in inspections:
            inspections[ruleset] = {}
        if rule not in inspections[ruleset]:
            inspections[ruleset][rule] = []
        inspections[ruleset][rule].append(item)
    return inspections


def get_performance(line_count):
    return 1 - (line_count['errorLines'] / line_count['codeLines'])


def get_formatted_meta():
    import json
    meta_raw = open(f'./outputs/{get_current_user()}/meta.json').read()
    meta = json.loads(meta_raw)
    meta_str = ''
    meta_str += f'Total repositories: {meta["repo_count"]}\n'
    meta_str += f'Total commits: {meta["total_commits"]}\n'
    languages = meta["languages"]
    meta_str += f'{len(languages)} Languages\n'
    for lang, chars in languages.items():
        meta_str += f'({lang}: {chars} bytes )'
    return meta_str + '\n'


def generate_report(csv_path):
    report = ''
    inspections = generate_dictionary(csv_path)
    line_count = count_lines('./repos', ['.java', '.js'])
    line_count['errorLines'] = len(inspections)
    performance_score = get_performance(line_count)
    user_id = get_current_user()
    with open(f'./outputs/{user_id}/data.json', 'w') as outfile:
        json.dump(inspections, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)
    ruleset_count = 0
    categorized = categorize_inspections(inspections)
    for rulesetKey, rulesetVal in categorized.items():
        rule_count = 0
        ruleset_count += 1
        report += f'{ruleset_count}: {rulesetKey}\n'
        for ruleKey, ruleVal in rulesetVal.items():
            rule_count += 1
            report += f' > {rule_count}: {ruleKey} ({len(ruleVal)} issues)\n'
    report += '=' * 20 + '\n'
    report += get_formatted_meta()
    report += f'Total code lines: {line_count["codeLines"]}\n'
    report += f'Total lines with violations: {line_count["errorLines"]}\n'
    report += f'Performance Score: {"{0:.2%}".format(performance_score)}\n'
    return report