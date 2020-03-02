import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd

base_url = "https://montreal.craigslist.org/search/sss?query=cars&sort=rel&lang=en&cc=us"

page = requests.get(base_url)
if page.status_code == requests.codes.ok:
  soup = BeautifulSoup(page.text, 'lxml')

data = {
  'Title':[],
  'Price':[],
  'Date':[]
}

all_items = soup.find('div', class_='content').find('ul', class_='rows').findAll('li')

for item in all_items:
  # Getting date of the item
  date = item.find('p').find('time', class_='result-date').text.strip()
  if date:
    data['Date'].append(date)
  else:
    date['Date'].append('none')

  # Getting price of the item
  price = item.find('span').text.strip()
  if price:
    data['Price'].append(price)
  else:
    date['Price'].append('none')

  # Getting title of the item
  title = item.find('p').find('a', class_='result-title hdrlnk').text.strip()
  if title:
    data['Title'].append(title)
  else:
    date['Title'].append('none')

table = pd.DataFrame(data, columns=['Title', 'Price', 'Date'])
table.index = table.index + 1

table.to_csv('craigslist-products.csv', sep=',', index=False, encoding='utf-8')