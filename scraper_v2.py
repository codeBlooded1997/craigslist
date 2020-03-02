import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd

base_url = "https://montreal.craigslist.org"
search_url = "https://montreal.craigslist.org/search/sss?s=360&query=cars&sort=rel"

page = requests.get(search_url)
if page.status_code == requests.codes.ok:
    soup = BeautifulSoup(page.text, 'lxml')

data = {
    'Title': [],
    'Price': [],
    'Date': [],
    'URL': []
}

all_items = soup.find('div', class_='content').find('ul', class_='rows').findAll('li')

for item in all_items:
    # Getting url for the item
    url = item.find('p').find('a')['href']
    if url:
        data['URL'].append(url)
    else:
        data['URL'].append('none')

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
next_page_text = soup.find('a', class_='button next')['href']

#if next_page_text == 'next > ':
#    next_page_url = soup.find('a', class_='button next')['href']
#    new_url = base_url + next_page_url
#    print(new_url)
#else:
#    print('It was last page')
print(len(next_page_text))

table = pd.DataFrame(data, columns=['Title', 'Price', 'Date', 'URL'])
table.index = table.index + 1

#table.to_csv('craigslist-products.csv', sep=',', index=False, encoding='utf-8')
