import requests
from bs4 import BeautifulSoup

url = 'https://www.nfl.com/players/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

player_tags = soup.find_all('a', class_='PlayerCard')
for player_tag in player_tags:
    name = player_tag.find('span', class_='PlayerCard-name').text
    team = player_tag.find('span', class_='PlayerCard-teamName').text
    img_url = player_tag.find('img')['src']
    print(f'Name: {name}, Team: {team}, Image URL: {img_url}')
