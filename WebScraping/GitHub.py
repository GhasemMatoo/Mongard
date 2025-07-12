import requests
import re
from bs4 import BeautifulSoup


url = 'https://github.com/{}'
Username = input('Enter User name: ')


response = requests.get(url.format(Username), params={'tab': 'repositories'})

content = BeautifulSoup(response.text, 'html.parser')

repos_elements = content.find(attrs={'id': 'user-repositories-list'})
repos = repos_elements.find_all('li')

for repo in repos:
    name = repo.find('h3').find('a').get_text(strip=True)
    language = repo.find(attrs={"itemprop": "programmingLanguage"})
    language = language.get_text(strip=True) if language else "unknown"
    stars = repo.find('a', attrs={"class":"Link--muted mr-3"})
    stars = int(stars.get_text(strip=True)) if stars else 0
    print(name, language,  stars)