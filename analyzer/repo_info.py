from github import Github, GithubException


########################################
# for fetching meta information about repositories
########################################
class RepoInfoFetcher(object):
    def __init__(self):
        pass

    @staticmethod
    def get_repo_info(username):
        # dont change, login details
        g = Github('githubanalyzeruser', '!Analyzer80')
        repos = g.get_user(username).get_repos()
        repo_count = repos.totalCount
        total_commits = 0
        languages = {}
        for repo in repos:
            try:
                langs = repo.get_languages()
                for lang, chars in langs.items():
                    if lang in languages:
                        languages[lang] += chars
                    else:
                        languages[lang] = chars
                total_commits += repo.get_commits().totalCount
            except GithubException as exception:
                continue

        print(f'Username: {username}')
        print(f'Repositories: {repo_count}\nCommits: {total_commits}')
        print(languages)
        return {'username': username,
                'repo_count': repo_count,
                'total_commits': total_commits,
                'languages': languages
                }
