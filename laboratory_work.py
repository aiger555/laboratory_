import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


class Kivano:
    def __init__(self, data):
        self.depDF = pd.DataFrame({
            'category_name': data.category_name,
            'title': data.title,
            'link': data.link
        })

    def write_to_csv(self):
        csvfile = self.depDF.to_csv(index=False)
        with open('kivano.csv', 'w', encoding='utf-8') as file:
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

def parser():
    url = 'https://www.kivano.kg/'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')
    paginator = soup.find('div', class_='pager-wrap').find_all('a')[3].get('href')
    pag = paginator.split('=')[-1]
    pag = int(pag)
    ads = soup.find('div', class_='list-view').find_all('div', class_='item product_listbox oh')
    lst = []
    for ad in ads:
        try:
            category_name = ad.find('div', class_='pull-left').find_all('div',                                                          class_='rel js_hidden_category hidden_category').text
            title = ad.find('div', class_='listbox_title oh').text
            link = ad.find('div', class_='listbox_title oh').find_all('a').get('href').text
        except:
            category_name = 'No category'
            title = 'No title'
            link = 'No link'
        lst.append(Kivano_ad(category_name, title, link))
    return lst

url = 'https://www.kivano.kg/'

def change(url):
    page_part = '?page='
    for s in range(1, 4):
        url_gen = url + page_part + str(s)
        res = End_res(parser())
        write_ = Kivano(res)



parser()
change(url)
