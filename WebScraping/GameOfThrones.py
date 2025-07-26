import requests
from bs4 import BeautifulSoup


url = "https://en.wikipedia.org/wiki/List_of_Game_of_Thrones_episodes"

response = requests.get(url)

content = BeautifulSoup(response.text, 'html.parser')

episodes = []

ep_tables = content.find_all('table', class_='wikiepisodetable')


for table in ep_tables:
    headers = []
    rows = table.find_all('tr')
    for header in table.find('tr').find_all('th'):
        headers.append(header.text)

    for row in rows[1:]:
        values = []
        for col in row.find_all(['td', 'td']):
            values.append(col.text)
        if values:
            episodes_dict = {headers[i]: values[i] for i in range(len(values))}
            episodes.append(episodes_dict)


print(episodes)