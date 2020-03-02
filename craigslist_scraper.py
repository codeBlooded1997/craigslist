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

base_url = "https://montreal.craigslist.org"
search_url = "https://montreal.craigslist.org/search/sss?query=cars&sort=rel&lang=en&cc=us"
page_counter = 1


def soup_maker(URL):
    global page_counter
    # grabbing the page
    print('Grabbing page {} ...'.format(page_counter))
    page = requests.get(URL)
    # Checking if we got the good response from the server-side
    if page.status_code == requests.codes.ok:
        soup = BeautifulSoup(page.text, 'lxml')
        return soup


# This function parse the page
def parse_page(soup_obj):
    global page_counter
    # Getting list of items available in the page
    all_items = soup_obj.find('div', class_='content').find('ul', class_='rows').findAll('li')

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

    # Findig url to next page
    next_page_text = soup_obj.find('a', class_='button next')['href']
    if len(next_page_text) != 0:
        page_counter = page_counter + 1
        next_page_url = soup_obj.find('a', class_='button next')['href']
        print("Page {} found".format(page_counter))
        new_url = base_url + next_page_url
        new_bsObj = soup_maker(new_url)
        parse_page(new_bsObj)
    else:
        print('It was last page')



# This function saves data into a data frame and creates a csv file
def to_csv():
    print('panda created!')
    table = pd.DataFrame(data, columns=['Title', 'Price', 'Date', "URL"])
    table.index = table.index + 1
    print("csv created")
    table.to_csv('craigslist-products.csv', sep=',', index=False, encoding='utf-8')


bsObj = soup_maker(search_url)
parse_page(bsObj)
print('{} items scraped.'.format(len(data['Title'])))
to_csv()
