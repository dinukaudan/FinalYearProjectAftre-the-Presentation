from analyzer.analyzer_utils import generate_analysis_csv, generate_report, generate_meta_json, save_current_user, \
    get_current_user
from deep_learning.core import get_prediction_for_user_id
from deep_learning.extract_features import extract_features
from deep_learning.preprocess import preprocess_user_data
from utils import get_repo_list, empty_dir, clone_by_url


########################################
# for analyzing code & generating reports
########################################
class Analyzer(object):

    def clone(self, printer, indicator, prompter, username):
        if username.strip() is '':
            printer('Invalid username! Please try again.')
            indicator(f'Cloning failed.', False)
            return 1
        else:
            save_current_user(username)
            printer(f'Scanning user GitHub account \'{username}\'...')
            indicator(f'Scanning GitHub account...', True)
            generate_meta_json(username)
            printer(f'Fetching repositories of user \'{username}\'...')
            indicator(f'Cloning from {username}...', True)
            repo_list = get_repo_list(username)
            repo_count = len(repo_list)
            if repo_count == 0:
                printer(f'No repositories found for user \'{username}\'! Please try again.')
                indicator(f'Cloning failed.', False)
                return 2
            printer(f'Found {repo_count} repositories.')
            proceed = prompter(
                f'Do you want to clone all {repo_count} repositories found for the user \'{username}\'?')
            if proceed:
                empty_dir('./repos')
                for url in repo_list:
                    printer(f'Cloning repository \'{url}\'')
                    clone_by_url(url)
                printer(f'Cloned {repo_count} repositories successfully!')
                indicator(f'Cloning successful!', False)
                return 0
            else:
                printer('Cloning aborted by user. Previously cloned repositories might be removed!')
                indicator(f'Cloning aborted.', False)
                return -1

    def analyze(self, printer, indicator):
        printer('Performing static source code analysis...')
        indicator(f'Analyzing repositories...', True)
        try:
            generate_analysis_csv(self.get_inspection_csv_path())
        except Exception as e:
            printer(f'Analysis failed!\n\nError Occured: {e}')
            indicator(f'Analysis failed.', False)
            return 1

        printer('Analysis completed. Click \'Report\' for a report.')
        indicator(f'Analysis successful!', False)
        return 0

    def report(self, printer, indicator, user_expertise_getter):
        indicator('Generating analysis report...', True)
        printer('Generating analysis report...')
        printer('============ REPORT START ============')
        printer(generate_report(self.get_inspection_csv_path()))
        printer('------------------------------------')
        printer(f'PREDICTED USER EXPERTISE: {user_expertise_getter(get_current_user())}')
        printer('------------------------------------')
        printer('============= REPORT END =============')
        indicator('Report generated!', False)

    def get_inspection_csv_path(self):
        return f'./outputs/{get_current_user()}/inspection_output.csv'

    def get_user_expertise(self, user_id):
        preprocess_user_data()
        extract_features()
        return get_prediction_for_user_id(user_id).upper()
