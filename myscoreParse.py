import requests
import csv
from bs4 import BeautifulSoup
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import id_lists_test

SITE_URL = 'https://www.myscore.ru/'
HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
}

# BROWSER = webdriver.Firefox(executable_path='geckodriver.exe')

def init_browser(headless=False, browser='firefox'):
    options = Options()
    options.headless = headless;
    if browser == 'firefox':
        browser = webdriver.Firefox(options=options)
        print ("Firefox Initialized")
    elif browser == 'chrome':
        browser = webdriver.Firefox(options=options)
        print ("Chrome Initialized")
    browser.implicitly_wait(30)
    return browser

def init_session():
    session = requests.Session()
    return session

def get_request_BS_html(session, url):
    time.sleep(3)
    response = session.get(url, headers=HEADERS).text

    html = BeautifulSoup(response, 'lxml')
    print(html.prettify)
    sys.exit()
    return html

def get_browser_BS_html(browser):
    html = BeautifulSoup(browser.page_source, 'lxml')
    return html

def get_browser_BS_html_H2H(browser):
    html = browser.find_element_by_id('tab-h2h-overall').get_attribute('outerHTML')
    # html = BeautifulSoup(html, 'lxml')
    html = BeautifulSoup(browser.page_source, 'lxml')
    return html

def get_browser_BS_html_ODDS(browser):
    html = browser.find_element_by_id('tab-match-odds-comparison').get_attribute('outerHTML')
    # html = BeautifulSoup(html, 'lxml')
    html = BeautifulSoup(browser.page_source, 'lxml')
    return html

def get_matchs_id(browser):
    browser.implicitly_wait(30)
    browser.get(SITE_URL)
    match_id = []
    time.sleep(3)
    browser.find_element_by_class_name('calendar__direction--yesterday').click()
    html = get_browser_BS_html(browser)

    divs = html.find_all('div', class_='event__match')
    for div in divs:
        id = div.get('id')
        if id.startswith('g_1'):
            match_id.append({
            'id': id[4:]
            })

    for i in range(8):
        time.sleep(3)
        browser.find_element_by_class_name('calendar__direction--tomorrow').click()
        html = BeautifulSoup(browser.page_source, 'lxml')
        divs = html.find_all('div', class_='event__match')
        for div in divs:
            id = div.get('id')
            if id.startswith('g_1'):
                match_id.append({
                'id': id[4:]
                })

    return match_id

def main_parse(browser, id_list):
    session = init_session()
    for id in id_list:
        # print('https://www.myscore.ru/match/' + 'id['id']')
        browser.get('https://www.myscore.ru/match/' + id['id'] + '/#h2h;overall')
        html = get_browser_BS_html_H2H(browser)
        time = html.find(id='utime').text

        print(time)
        # browser.quit()
        sys.exit()
        result = []
        result.append({
        'id': id[4:]
        })
    browser.quit()

def main():
    browser = init_browser()

    # id_list = get_matchs_id(browser)
    id_list = id_lists_test.id_lists

    main_parse(browser, id_list)


if __name__ == '__main__':
    main()

# BROWSER.quit()
# print(match_id)
# def get_html(url):
#
#     return response.read()
