import urllib.request
import csv
from bs4 import BeautifulSoup
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

SITE_URL = 'https://www.myscore.ru/'

BROWSER = webdriver.Firefox(executable_path='geckodriver.exe')
BROWSER.get(SITE_URL)
BROWSER.find_element_by_class_name('calendar__direction--yesterday').click()
match_id = []

html = BeautifulSoup(BROWSER.page_source, 'lxml')

divs = html.find_all('div', class_='event__match')

for div in divs:
    id = div.get('id')
    if id.startswith('g_1'):
        match_id.append({
        'opened_id': id[4:]
        })

for i in range(8):
    time.sleep(3)
    BROWSER.find_element_by_class_name('calendar__direction--tomorrow').click()
    html = BeautifulSoup(BROWSER.page_source, 'lxml')
    divs = html.find_all('div', class_='event__match')
    for div in divs:
        id = div.get('id')
        if id.startswith('g_1'):
            match_id.append({
            'opened_id': id[4:]
            })

BROWSER.quit()
print(match_id)
# def get_html(url):
    
#     return response.read()