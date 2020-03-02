import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd

data = {
    'Title': [],
    'Price': [],
    'Date': [],
    'URL': []
}

base_url = "https://montreal.craigslist.org/search/sss?query=cars&sort=rel&lang=en&cc=us"
# grabbing the page
page = requests.get(base_url)
# Checking if we got the good response from the server-side
if page.status_code == requests.codes.ok:
  soup = BeautifulSoup(page.text, 'lxml')

# This function parse the page
def parse_page(URL):

    # Getting list of items available in the page
    all_items = soup.find('div', class_='content').find('ul', class_='rows').findAll('li')

    # Iterating through the items in page
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


# This function saves data into a csv file
def to_csv():
    table = pd.DataFrame(data, columns=['Title', 'Price', 'Date', "URL"])
    table.index = table.index + 1
    table.to_csv('craigslist-products.csv', sep=',', index=False, encoding='utf-8')

def next_page():
    next_page_text = soup.find('a', class_='button next').text

    if next_page_text == 'next > ':
        next_page_url = soup.find('a', class_='button next')['href']
        new_url = base_url + next_page_url
        print(new_url)
    else:
        print('It was last page')

parse_page(base_url)
to_csv()
