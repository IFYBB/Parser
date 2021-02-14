import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re

CSV = 'cards.csv'
HOST = 'https://spb.cian.ru/'
URL = 'https://spb.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p=1'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='_93444fe79c--card--2umme _93444fe79c--promoted--62c4a')
    rooms = []
    for item in items:
        rooms.append(
            {
                'title':item.find('div', class_='_93444fe79c--container--JdWD4').get_text(strip=True),
                'adress':item.find('div', class_='_93444fe79c--container--2h0AF').get_text(strip=True),
                'price': item.find('span', class_='_93444fe79c--color_black_100--A_xYw _93444fe79c--lineHeight_28px--3QLml _93444fe79c--fontWeight_bold--t3Ars _93444fe79c--fontSize_22px--3UVPd _93444fe79c--display_block--1eYsq _93444fe79c--text--2_SER').get_text(strip=True),
                'link': item.find('div', class_='_93444fe79c--container--2Kouc _93444fe79c--link--2-ANY').find('a').get('href')
            }
        )
    return rooms

def save_csv(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow(['Название', 'Адрес', 'Цена', 'Ссылка'])
        for item in items:
            writer.writerow((item['title'], item['adress'], item['price'], item['link']))

def make_money(roomss): # ф-я вытаскивает число - цену из текста.
    for room in roomss:
        item = room['price']  # Получаем нужную строку
        value = ''.join(re.findall(r'\d+', item))  # Достаём из неё все цифры и объединяем через пустую строку
        value = int(value)  # Приводим к типу int
        #print(value)  # Вывод для наглядности
        del room['price']
        room['price'] = value
    print(roomss)
    return roomss

def parser():
    """PAGENATION = input('Введите число страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())"""
    PAGENATION = 2
    html = get_html(URL)
    if html.status_code == 200:
        roomss = []
        for page in range(1, PAGENATION+1):
            print(f'Парсим страницу {page}')
            html = get_html(URL, params={'page': page})
            roomss.extend(get_content(html.text))
            #save_csv(roomss, CSV)
        make_money(roomss)
        df = pd.DataFrame(roomss)
        df.to_csv(CSV, sep=';', encoding='utf-8-sig')
        print(df)
    else:
        print('Error')

parser()
