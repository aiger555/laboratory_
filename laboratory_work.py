import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


class Kivano:
    def __init__(self, data):
        self.depDF = pd.DataFrame({
            'category_name': data.category_names,
            'title': data.titles,
            'link': data.links
        })

    def write_to_csv(self):
        csvfile = self.depDF.to_csv(index=False)
        with open('kivano.csv', 'a', encoding='utf-8') as file:
            file.write(csvfile)

class End_res:
    def __init__(self, ads):
        self.ads = ads
        self.category_names = []
        self.titles = []
        self.links = []
        for i in ads:
            self.category_names.append(i.category_name)
            self.titles.append(i.title)
            self.links.append(i.link)


class Kivano_ad:
    def __init__(self, category_name, title, link):
        self.category_name = category_name
        self.title = title
        self.link = link

url = 'https://www.kivano.kg/'

def get_html(url):
    response = requests.get(url)
    return response.text

def parser(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.find('div', class_='list-view').find_all('div', class_='item')
    lst = []
    for ad in ads:
        try:
            category_name = soup.find('div', class_='product-index').find_next('div', class_='portlet-title').find_next('ul', class_='breadcrumb2').find_all_next('li', itemprop='itemListElement')[-1].text
        except:
            category_name = 'No category'
        try:
            title = ad.find('div', class_='listbox_title').text.replace('\n', ' ')
        except:
            title = 'No title'
        try:
            link = ad.find('div', class_='listbox_title').find_next('a').get('href')
        except:
            link = 'No link'
        lst.append(Kivano_ad(category_name, title, link))
    return lst

urls = [
        'https://www.kivano.kg/feny', 
        'https://www.kivano.kg/shiny-vsesezonnye',
        'https://www.kivano.kg/kofevarki',
        'https://www.kivano.kg/gladilnye-doski'
        ]

def change(url):
    page_part = '?page='
    for u in url:
        for i in range(1, 4):
            url_gen = u + page_part + str(i)
            res = End_res(parser(get_html(url_gen), url))
            write_ = Kivano(res)
            write_.write_to_csv()

urls = [
        'https://www.kivano.kg/feny', 
        'https://www.kivano.kg/shiny-vsesezonnye',
        'https://www.kivano.kg/kofevarki',
        'https://www.kivano.kg/gladilnye-doski'
        ]
    
 
change(urls)




        
 

