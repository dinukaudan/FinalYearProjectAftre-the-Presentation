## Requirements:

1. Windows 10
2. Python 3.6
3. Git for Windows (https://git-scm.com/download/win)

## Environment Setup

1. Open 'Windows PowerShell' in Administrator mode
2. Run the following command as a single line. This will install `chocolaty` on your computer.

    `Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))`

3. When `chocolaty` is installed, run the following command to install **PMD** (static analyzer tool).

    `choco install -y pmd`

## Running Program

1. Clone & open the project in Pycharm
2. Create a Python 3.6 virtual environment for the project (tutorial: https://www.youtube.com/watch?v=ZvQY-FdsYGE).
3. Run `pip install -r requirements.txt` in the root directory to install requirements.
4. Run `python main.py` to run the program

## References

1. `PMD` cross-language static code analyzer (https://pmd.github.io)
    - for static code analysis
2. `gitpython` python package (https://gitpython.readthedocs.io/en/stable/)
    - for counting & cloning user repositories
3. `PyGithub` python package (https://pygithub.readthedocs.io/en/stable/)
    - for getting meta information about user & repositories