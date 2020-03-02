import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd

base_url = "https://montreal.craigslist.org/search/sss?query=car&sort=rel&lang=en&cc=us"

page = requests.get(base_url)
if page.status_code == requests.codes.ok:
  soup = BeautifulSoup(page.text, 'lxml')

data = {
  'Title':[],
  'Price':[],
  'Date':[]
}

all_items = soup.find('div', class_='content').findAll('ul')[-1].findAll('li')

for item in all_items:
  # Getting date of the item
  date = item.find('p').find('time').text
  if date:
    data['Date'].append(date)
  else:
    date['Date'].append('None')

  # Getting price of the item
  price = item.find('span').text.strip
  if price:
    data['Price'].append(price)
  else:
    date['Price'].append('None')

  # Getting title of the item
  title = item.find('p').find('a').text
  if title:
    data['Title'].append(title)
  else:
    date['Title'].append('None')

