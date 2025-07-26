import requests
import re
from bs4 import BeautifulSoup


url = 'https://github.com/{}'
username = input('Enter User name : ')
password = input('Enter User password : ')

session = requests.Session()

response = session.get(url.format('login'))
content = BeautifulSoup(response.text, 'html.parser')


data = {}
for form in content.find_all('form'):
    for inp in form.select('input[type=hidden]'):
        data[inp.get('name')] = inp.get('value')

data.update({'login': username, 'password': password})

response = session.post(url=url.format("session"), data=data)
response = session.get(url=url.format(username))
content = BeautifulSoup(response.text, "html.parser")
user_info = content.find(class_= 'vcard-details')
print(user_info.text)