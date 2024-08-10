import requests
import sys
import shutil
import os
from requests.auth import HTTPBasicAuth




def get_latest_version():
    url = 'https://api.github.com/repos/HyperHypno/PenUp/releases/latest'
    headers = {
        'Authorization': 'token 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'
    }
    response = requests.get(url, headers=headers)
    latest_release = response.json()
    return latest_release['tag_name'], latest_release['assets'][0]['browser_download_url']

def download_update(download_url, filename):
    headers = {
        'Authorization': 'token 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'
    }
    response = requests.get(download_url, headers=headers)
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename

def check_for_update(current_version):
    latest_version, _ = get_latest_version()
    if latest_version and latest_version != current_version:
        return latest_version
    return None

def replace_executable(new_exe_path):
    try:
        current_exe = sys.argv[0]
        temp_exe = 'new_version.exe'
        
        os.rename(current_exe, current_exe + '_old')
        shutil.move(new_exe_path, current_exe)
        os.remove(current_exe + '_old')
    except Exception as e:
        print(f"Error replacing executable: {e}")

def update_application():
    try:
        current_version = 'v1.0.0'  # Your current version
        latest_version = check_for_update(current_version)
        
        if latest_version:
            print(f"Update available: {latest_version}. Downloading...")
            
            download_url = get_latest_version()[1]
            new_exe = download_update(download_url, 'new_version.exe')
            
            if new_exe:
                replace_executable(new_exe)
                
                print("Updating and restarting the application...")
                os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        print(f"Error during application update: {e}")
print("Hello world")