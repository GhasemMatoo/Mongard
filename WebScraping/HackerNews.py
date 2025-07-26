import requests
import re
from bs4 import BeautifulSoup

url = 'https://news.ycombinator.com/news'

articles = []
response = requests.get(url=url)
content = BeautifulSoup(response.text, 'html.parser')

for item in content.find_all('tr', class_='athing'):
    item_a = item.find('a', class_='titelink')
    item_link = item_a.get('href') if item_a else None
    item_text = item_a.get_text(strip=True) if item_a else None
    next_row = item.find_next_sibling('tr')
    item_score = next_row.find('span', class_='score')
    item_score = item_score.get_text(strip=True) if item_score else '0 points'
    item_comments = next_row.find('a', text=re.compile('\d+(&nbsp;|\s)comment(s?)'))
    item_comments = item_comments.get_text(strip=True).replace('\xa0', ' ') if item_comments else '0 comments'


    articles.append(
        {
            'link': item_link,
            'titel': item_text,
            'score':item_score,
            'comment': item_comments
        }
    )

print(articles)