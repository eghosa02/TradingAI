import subprocess
import git
import os
import shutil
import requests

def onerror(func, path, exc_info):
    import stat
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def download_changes(repo_url, local_path):
    try:
        repo = git.Repo.clone_from(repo_url, local_path)
        origin = repo.remotes.origin
        origin.fetch()
    except git.exc.GitCommandError as e:
        print("Error:", e)
    
def move_files(source_dir, destination_dir):

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for filename in os.listdir(source_dir):
        if filename != '.git' and filename != 'README.md':
            source_file_path = os.path.join(source_dir, filename)
            destination_file_path = os.path.join(destination_dir, filename)

            if os.path.exists(destination_file_path):
                os.remove(destination_file_path)

            shutil.move(source_file_path, destination_dir)
    shutil.rmtree(source_dir, onerror=onerror)

def readFromGitHub(owner, repo, percorso_file, branch="master"):
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{percorso_file}"
    risposta = requests.get(url)
    if risposta.status_code == 200:
        return risposta.text
    else:
        print(f"Error: Immpossible read the file ({risposta.status_code})")
        return None

if __name__ == '__main__':

    with open('version.txt', 'r') as file:
        version = int(file.read().strip())

    owner = "eghosa02"
    repo = "TradingBot"
    percorso_file = "version.txt"
    contenuto_file = readFromGitHub(owner, repo, percorso_file)
    github_version = ""

    if contenuto_file is not None:
        github_version = contenuto_file
    else:
        github_version = "0"

    if int(github_version) > version:
        repo_url = "https://github.com/eghosa02/TradingAI.git"
        local_path = "./update"
        dest_path = "./"
        download_changes(repo_url, local_path)
        move_files(local_path, dest_path)
        print("update done")

    subprocess.run(["python", "./trading_bot.py"])
