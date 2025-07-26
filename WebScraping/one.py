import requests
import re
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/Mao_Zedong'

response = requests.get(url=url)
content = BeautifulSoup(response.text, 'html.parser')

print( content)

print( content.find('h2'))
print( content.find('h2').name)
print( content.find('h2').text)
print( content.find('h2').attrs)
print( content.find(attrs={"role": "button"}))
print( content.find(class_="vector-sticky-header-buttons"))
print(content.find('a', class_="cdx-button"))
print(content.find_all('a', class_="cdx-button"))
print(content.find_all('a', class_="cdx-button", limit=5))
print(content.find('li').get('id'))
print(content.find(re.compile('^d')))
print(content.select('li > a[title="Benjamin Tucker"]'))
print( content.find_all(['h1', 'h2']))