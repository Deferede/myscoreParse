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
import re
import id_lists_test

SITE_URL = 'https://www.myscore.ru/'
HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
}

# BROWSER = webdriver.Firefox(executable_path='geckodriver.exe')

def init_browser(headless=False, browser='firefox'):
    options = Options()
    options.headless = headless
    if browser == 'firefox':
        browser = webdriver.Firefox(executable_path='geckodriver.exe', options=options)
        print ("Firefox Initialized")
    elif browser == 'chrome':
        browser = webdriver.Firefox(options=options)
        print ("Chrome Initialized")
    browser.implicitly_wait(30)
    browser.set_window_position(0, 0)
    browser.set_window_size(360, 240)
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
    browser.find_element_by_id('tab-h2h-overall')
    html = browser.find_element_by_id('tab-h2h-overall').get_attribute('outerHTML')
    # html = BeautifulSoup(html, 'lxml')
    html = BeautifulSoup(browser.page_source, 'lxml')
    return html

def get_browser_BS_html_ODDS(browser):
    browser.find_element_by_id('block-under-over')
    html = browser.find_element_by_id('odds-comparison-content').get_attribute('outerHTML')
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
    # session = init_session()
    teams_links = []
    match_details = []
    for id in id_list:
        # print('https://www.myscore.ru/match/' + 'id['id']')
        browser.get('https://www.myscore.ru/match/' + id['id'] + '/#h2h;overall')
        html_H2H = get_browser_BS_html_H2H(browser)
        time = html_H2H.find(id='utime').text
        descriptionMatch = html_H2H.find('span', class_='description__country')
        country = descriptionMatch.contents[0].replace(":", "")
        leage = descriptionMatch.contents[1].text.split('- Тур')[0].strip()
        tour = descriptionMatch.contents[1].text.split('- Тур')[1].strip()
        teams = html_H2H.find_all('div', class_='tname__text')
        team1 = teams[0].find('a', class_='participant-imglink').text.strip()
        team2 = teams[1].find('a', class_='participant-imglink').text.strip()
        score = html_H2H.find(id='event_detail_current_result').text.strip()

        for team in teams:
            linkToTeam = re.search('\(\'(.*)\'\)',team.find('a', class_='participant-imglink')['onclick']).group(1).strip()
            teams_links.append({
                'link_to_team': linkToTeam
            })

        # browser.find_element_by_class_name('calendar__direction--tomorrow').click()
        # browser.get('https://www.myscore.ru/match/' + id['id'] + '/#odds-comparison;over-under;full-time')
        # html_H2H = get_browser_BS_html_H2H(browser)
        # browser.get('https://www.myscore.ru/match/' + id['id'] + '/#odds-comparison;asian-handicap;full-time')

        ##### H2H
        tableHome = html_H2H.find('table', class_='head_to_head h2h_home')
        tableGuest = html_H2H.find('table', class_='head_to_head h2h_away')
        tableBoth = html_H2H.find('table', class_='head_to_head h2h_mutual')
        gamesHome = []
        gamesGuest = []
        gamesBoth = []
        for match in tableHome.find('tbody').find_all('tr', limit=5):
            date = match.find('span', class_='date').text.strip()
            country =  match.find('td', class_='flag_td')['title'].strip()
            leage =  match.find('td', class_='flag_td').text.strip()
            team1 = match.find_all('td', class_='name')[0].text.strip()
            team2 = match.find_all('td', class_='name')[1].text.strip()
            score = match.find('span', class_='score').text.strip()
            match_result = match.find('td', class_='winLose').find('a')['title'].strip()
            gamesHome.append({
                'date': date,
                'country': country,
                'leage': leage,
                'team1': team1,
                'team2': team2,
                'score': score,
                'match_result': match_result,
            })
        for match in tableGuest.find('tbody').find_all('tr', limit=5):
            date = match.find('span', class_='date').text.strip()
            country =  match.find('td', class_='flag_td')['title'].strip()
            leage =  match.find('td', class_='flag_td').text.strip()
            team1 = match.find_all('td', class_='name')[0].text.strip()
            team2 = match.find_all('td', class_='name')[1].text.strip()
            score = match.find('span', class_='score').text.strip()
            match_result = match.find('td', class_='winLose').find('a')['title'].strip()
            gamesGuest.append({
                'date': date,
                'country': country,
                'leage': leage,
                'team1': team1,
                'team2': team2,
                'score': score,
                'match_result': match_result,
            })
        for match in tableBoth.find('tbody').find_all('tr', limit=5):
            date = match.find('span', class_='date').text.strip()
            country =  match.find('td', class_='flag_td')['title'].strip()
            leage =  match.find('td', class_='flag_td').text.strip()
            team1 = match.find_all('td', class_='name')[0].text.strip()
            team2 = match.find_all('td', class_='name')[1].text.strip()
            score = match.find('span', class_='score').text.strip()
            gamesBoth.append({
                'date': date,
                'country': country,
                'leage': leage,
                'team1': team1,
                'team2': team2,
                'score': score,
            })
        #####

        ##### ODD
        browser.find_element_by_id('a-match-odds-comparison').click()
        html_ODD = get_browser_BS_html_ODDS(browser)
        ### тотал
        odds_total = []

        total_block = html_ODD.find(id='block-under-over-ft')
        tables = total_block.find_all('table', class_='odds')
        for table in tables:
            # if table['id'].split('_')[-1][2] != '2' or table['id'].split('_')[-1][2] != '7':
            for tr in table.find('tbody').find_all('tr'):
                tds = tr.find_all('td')
                if  str(float(tds[1].text))[2] == '2' or str(float(tds[1].text))[2] == '7':
                    continue
                if tds[2].find('span')['class'][-1] == 'down':
                    bookmaker = tds[0].find('a')['title'].strip()
                    total = tds[1].text.strip()
                    coeff_over = '>'+ tds[2].text.strip()
                    odds_total.append({
                        'bookmaker': bookmaker,
                        'total': total,
                        'coeff_over': coeff_over,
                    })
                
        ###
        ### asian_total

        #####

        match_details.append({
            'time': time,
            'country': country,
            'leage': leage,
            'tour': tour,
            'team1': team1,
            'team2': team2,
            'score': score,
            'gamesHome': gamesHome,
            'gamesGuest': gamesGuest,
            'gamesBoth': gamesBoth,
            'odds_total': odds_total,
        })

        print(match_details)
        browser.quit()
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
