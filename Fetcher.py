import requests
from bs4 import BeautifulSoup
import re

def get_github_files_content(repo_url):
    # Fetch HTML content of the GitHub repository
    response = requests.get(repo_url)
    if response.status_code != 200:
        print("Failed to fetch repository:", response.status_code)
        return {}

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags with href containing "/blob/" (files in the repository)
    file_links = soup.find_all('a', href=re.compile(r'\/blob\/'))

    # Extract content of code files
    files_content = {}
    base_url = "https://github.com"
    for link in file_links:
        file_url = link['href']
        file_name = file_url.split("/")[-1]
        file_content_response = requests.get(base_url + file_url)
        if file_content_response.status_code == 200:
            files_content[file_name] = file_content_response.text

    return files_content

# Example usage:
github_repo_url = "https://github.com/user/repository"
files_content = get_github_files_content(github_repo_url)
for file_name, content in files_content.items():
    print(f"File: {file_name}\nContent:\n{content}\n")
