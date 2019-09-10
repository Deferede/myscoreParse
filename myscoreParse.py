import requests
from bs4 import BeautifulSoup
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
import xlsxwriter
import id_lists_test

SITE_URL = 'https://www.myscore.ru/'
HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'X-Fsign': 'SW9D1eZo'
}

proxy = {
# 'https':'https://95.47.183.23:3128',
'https':'socks4://178.215.86.254:44259',
'https':'socks4://109.106.139.225:44297',
# 'https':'http://95.141.193.14:80',
# 'https':'http://62.33.207.197:80'
}



# BROWSER = webdriver.Firefox(executable_path='geckodriver.exe')

def init_browser(headless=False, browser='firefox'):
    options = Options()

    options.headless = headless
    if browser == 'firefox':
        profile = webdriver.FirefoxProfile()
        # 1 - Allow all images
        # 2 - Block all images
        # 3 - Block 3rd party images
        profile.set_preference("permissions.default.image", 2)
        # browser = webdriver.Firefox(executable_path='geckodriver.exe', options=options)
        browser = webdriver.Firefox(firefox_profile=profile, options=options)
        print ("Firefox Initialized")
    elif browser == 'chrome':
        browser = webdriver.Firefox(options=options)
        print ("Chrome Initialized")
    browser.implicitly_wait(30)
    browser.set_window_position(0, 0)
    # browser.set_window_size(360, 240)
    return browser

def init_session():
    session = requests.Session()
    return session

def get_request_BS_html(session, url):

    while True:
        try:
            response = session.get(url, headers=HEADERS, proxies=proxy)
            if response.status_code != 200:
                print('Ошибка соединения')
                continue
            html = BeautifulSoup(response.text, 'lxml')
            return html
        except Exception as e:
            print(e)
            print('Ошибка соединения исключение')
            time.sleep(5)


def get_request_BS_html_H2H(session, url):
    response = session.get(url, headers=HEADERS).text
    html = BeautifulSoup(response, 'lxml')
    return html

def get_browser_BS_html_ODDS(session, url):
    response = session.get(url, headers=HEADERS).text
    html = BeautifulSoup(response, 'lxml')
    return html


def get_browser_BS_html(browser):
    loadingOverlay = browser.find_element_by_class_name('loadingOverlay')
    WebDriverWait(browser, 30, ignored_exceptions=True).until(EC.invisibility_of_element(loadingOverlay))
    html = BeautifulSoup(browser.page_source, 'lxml')
    return html

def get_browser_BS_html_H2H(browser):
    browser.implicitly_wait(30)
    browser.find_element_by_id('tab-h2h-overall')
    # browser.find_element_by_id('tab-h2h-overall').get_attribute('outerHTML')
    # html = BeautifulSoup(html, 'lxml')
    html = BeautifulSoup(browser.page_source, 'lxml')

    return html

def get_browser_BS_html_ODDS(browser):
    browser.implicitly_wait(30)
    browser.find_element_by_id('block-under-over')
    html = browser.find_element_by_id('odds-comparison-content').get_attribute('outerHTML')
    # html = BeautifulSoup(html, 'lxml')
    html = BeautifulSoup(html, 'lxml')
    return html

def get_matchs_id(browser):
    match_id = []
    browser.implicitly_wait(30)
    browser.get(SITE_URL)
    match_id = []
    loadingOverlay = browser.find_element_by_class_name('loadingOverlay')
    WebDriverWait(browser, 30, ignored_exceptions=True).until(EC.invisibility_of_element(loadingOverlay))
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
        print ('Листинг {}%'.format(float((i / 8 * 100))))
        try:
            WebDriverWait(browser, 30, ignored_exceptions=True).until(EC.invisibility_of_element(loadingOverlay))
            browser.find_element_by_class_name('calendar__direction--tomorrow').click()
            WebDriverWait(browser, 30, ignored_exceptions=True).until(EC.invisibility_of_element(loadingOverlay))
            html = BeautifulSoup(browser.page_source, 'lxml')
            divs = html.find_all('div', class_='event__match')
            for div in divs:
                id = div.get('id')
                if id.startswith('g_1'):
                    match_id.append({
                        'id': id[4:]
                    })
        except Exception as e:
            print('Завтра больше нет=(')
    browser.quit()
    print(match_id)
    sys.exit()
    return match_id

def main_parse(id_list):
    session = init_session()
    teams_links = []
    matchs_details = []
    i = 0
    print(len(id_list))
    for id in id_list:
        print(id)
        print ('Парсинг {}%'.format(float((i / len(id_list) * 100))))
        i += 1
        html = get_request_BS_html(session, 'https://www.myscore.ru/match/' + id['id'])

        # html_H2H = get_browser_BS_html_H2H(browser)
        math_detail = html.find('script', text=re.compile(r'var game_utime =')).text
        timestamp = re.search('var game_utime = (\d+)', math_detail).group(1)
        # print(re.search('var game_utime =', html.text))

        time_main = datetime.fromtimestamp(int(timestamp)).strftime('%d.%m.%Y %H:%M:%S')
        descriptionMatch = html.find('meta', {'property':'og:description'}).get('content')
        descriptionMatch = descriptionMatch.split(":")
        country_main = descriptionMatch.pop(0).strip()
        descriptionMatch = descriptionMatch[0].split("-")
        tour_main = descriptionMatch.pop().strip()
        leage_main = ''.join(descriptionMatch).strip()
        teams = html.find_all('div', class_='tname__text')
        team_main1 = teams[0].find('a', class_='participant-imglink').text.strip()
        team_main2 = teams[1].find('a', class_='participant-imglink').text.strip()
        score_main = html.find(id='event_detail_current_result').text.strip()
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
        html_H2H = get_request_BS_html(session, 'https://d.myscore.ru/x/feed/d_hh_' + id['id'] + '_ru_1')

        tableHome = html_H2H.find('table', class_='head_to_head h2h_home')
        tableGuest = html_H2H.find('table', class_='head_to_head h2h_away')
        tableBoth = html_H2H.find('table', class_='head_to_head h2h_mutual')
        gamesHome = []
        gamesGuest = []
        gamesBoth = []
        try:
            for match in tableHome.find('tbody').find_all('tr', limit=5):
                date = match.find('span', class_='date').text.strip()
                date = datetime.fromtimestamp(int(date)).strftime('%d.%m.%Y %H:%M:%S')
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
        except Exception as e:
            gamesHome.append({
                'date': '',
                'country': '',
                'leage': '',
                'team1': '',
                'team2': '',
                'score': '',
                'match_result': '',
            })
        try:
            for match in tableGuest.find('tbody').find_all('tr', limit=5):
                date = match.find('span', class_='date').text.strip()
                date = datetime.fromtimestamp(int(date)).strftime('%d.%m.%Y %H:%M:%S')
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
        except Exception as e:
            gamesGuest.append({
                'date': '',
                'country': '',
                'leage': '',
                'team1': '',
                'team2': '',
                'score': '',
                'match_result': '',
            })

        for match in tableBoth.find('tbody').find_all('tr', limit=5):
            try:
                date = match.find('span', class_='date').text.strip()
                date = datetime.fromtimestamp(int(date)).strftime('%d.%m.%Y %H:%M:%S')
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
            except Exception as e:
                gamesBoth.append({
                    'date': '',
                    'country': '',
                    'leage': '',
                    'team1': '',
                    'team2': '',
                    'score': '',
                })
        if len(gamesBoth) < 5:
            for i in range(5 - len(gamesBoth)):
                gamesBoth.append({
                    'date': '',
                    'country': '',
                    'leage': '',
                    'team1': '',
                    'team2': '',
                    'score': '',
                })
        #####
        ##### ODD
        html_ODD = get_request_BS_html(session, 'https://d.myscore.ru/x/feed/d_od_' + id['id'] + '_ru_1_eu')

        ### тотал
        odds_total = []
        try:
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
                        coeff_over = float(tds[2].text.strip())
                        if coeff_over >= 1.7 and coeff_over <= 2.1:
                            odds_total.append({
                                'bookmaker': bookmaker,
                                'total': total,
                                'coeff_over': coeff_over,
                            })
        except Exception as e:
            odds_total.append({
                'bookmaker': '',
                'total': '',
                'coeff_over': '',
            })


        ###
        ### asian_total
        # TODO ASIAN TOTAL
        #####

        matchs_details.append({
            'time': time_main,
            'country': country_main,
            'leage': leage_main,
            'tour': tour_main,
            'team1': team_main1,
            'team2': team_main2,
            'score': score_main,
            'gamesHome': gamesHome,
            'gamesGuest': gamesGuest,
            'gamesBoth': gamesBoth,
            'odds_total': odds_total,
        })

        # result = []
        # result.append({
        # 'id': id[4:]
        # })
    save_xlsx_match_details(matchs_details, 'test')



def save_xlsx_match_details(matchs_details, path):
    workbook = xlsxwriter.Workbook(path + '.xlsx')

    worksheet = workbook.add_worksheet()

    columns = [
    'Дата',
    'Страна',
    'Чемпионат',
    'Тур',
    'Команда 1',
    'Команда 2',
    'Счет',
    'Последние игры команды 1 (Дата 1)',
    'Последние игры команды 1 (Дата 2)',
    'Последние игры команды 1 (Дата 3)',
    'Последние игры команды 1 (Дата 4)',
    'Последние игры команды 1 (Дата 5)',
    'Последние игры команды 1 (Страна 1)',
    'Последние игры команды 1 (Страна 2)',
    'Последние игры команды 1 (Страна 3)',
    'Последние игры команды 1 (Страна 4)',
    'Последние игры команды 1 (Страна 5)',
    'Последние игры команды 1 (Лига 1)',
    'Последние игры команды 1 (Лига 2)',
    'Последние игры команды 1 (Лига 3)',
    'Последние игры команды 1 (Лига 4)',
    'Последние игры команды 1 (Лига 5)',
    'Последние игры команды 1 (Команда 1-1)',
    'Последние игры команды 1 (Команда 1-2)',
    'Последние игры команды 1 (Команда 1-3)',
    'Последние игры команды 1 (Команда 1-4)',
    'Последние игры команды 1 (Команда 1-5)',
    'Последние игры команды 1 (Команда 2-1)',
    'Последние игры команды 1 (Команда 2-2)',
    'Последние игры команды 1 (Команда 2-3)',
    'Последние игры команды 1 (Команда 2-4)',
    'Последние игры команды 1 (Команда 2-5)',
    'Последние игры команды 1 (Счет 1)',
    'Последние игры команды 1 (Счет 2)',
    'Последние игры команды 1 (Счет 3)',
    'Последние игры команды 1 (Счет 4)',
    'Последние игры команды 1 (Счет 5)',
    'Последние игры команды 1 (Исход 1)',
    'Последние игры команды 1 (Исход 2)',
    'Последние игры команды 1 (Исход 3)',
    'Последние игры команды 1 (Исход 4)',
    'Последние игры команды 1 (Исход 5)',
    'Последние игры команды 2 (Дата 1)',
    'Последние игры команды 2 (Дата 2)',
    'Последние игры команды 2 (Дата 3)',
    'Последние игры команды 2 (Дата 4)',
    'Последние игры команды 2 (Дата 5)',
    'Последние игры команды 2 (Страна 1)',
    'Последние игры команды 2 (Страна 2)',
    'Последние игры команды 2 (Страна 3)',
    'Последние игры команды 2 (Страна 4)',
    'Последние игры команды 2 (Страна 5)',
    'Последние игры команды 2 (Лига 1)',
    'Последние игры команды 2 (Лига 2)',
    'Последние игры команды 2 (Лига 3)',
    'Последние игры команды 2 (Лига 4)',
    'Последние игры команды 2 (Лига 5)',
    'Последние игры команды 2 (Команда 1-1)',
    'Последние игры команды 2 (Команда 1-2)',
    'Последние игры команды 2 (Команда 1-3)',
    'Последние игры команды 2 (Команда 1-4)',
    'Последние игры команды 2 (Команда 1-5)',
    'Последние игры команды 2 (Команда 2-1)',
    'Последние игры команды 2 (Команда 2-2)',
    'Последние игры команды 2 (Команда 2-3)',
    'Последние игры команды 2 (Команда 2-4)',
    'Последние игры команды 2 (Команда 2-5)',
    'Последние игры команды 2 (Счет 1)',
    'Последние игры команды 2 (Счет 2)',
    'Последние игры команды 2 (Счет 3)',
    'Последние игры команды 2 (Счет 4)',
    'Последние игры команды 2 (Счет 5)',
    'Последние игры команды 2 (Исход 1)',
    'Последние игры команды 2 (Исход 2)',
    'Последние игры команды 2 (Исход 3)',
    'Последние игры команды 2 (Исход 4)',
    'Последние игры команды 2 (Исход 5)',
    'Очные встречи команды 1 - команды 2 (Дата 1)',
    'Очные встречи команды 1 - команды 2 (Дата 2)',
    'Очные встречи команды 1 - команды 2 (Дата 3)',
    'Очные встречи команды 1 - команды 2 (Дата 4)',
    'Очные встречи команды 1 - команды 2 (Дата 5)',
    'Очные встречи команды 1 - команды 2 (Страна 1)',
    'Очные встречи команды 1 - команды 2 (Страна 2)',
    'Очные встречи команды 1 - команды 2 (Страна 3)',
    'Очные встречи команды 1 - команды 2 (Страна 4)',
    'Очные встречи команды 1 - команды 2 (Страна 5)',
    'Очные встречи команды 1 - команды 2 (Лига 1)',
    'Очные встречи команды 1 - команды 2 (Лига 2)',
    'Очные встречи команды 1 - команды 2 (Лига 3)',
    'Очные встречи команды 1 - команды 2 (Лига 4)',
    'Очные встречи команды 1 - команды 2 (Лига 5)',
    'Очные встречи команды 1 - команды 2 (Команда 1-1)',
    'Очные встречи команды 1 - команды 2 (Команда 1-2)',
    'Очные встречи команды 1 - команды 2 (Команда 1-3)',
    'Очные встречи команды 1 - команды 2 (Команда 1-4)',
    'Очные встречи команды 1 - команды 2 (Команда 1-5)',
    'Очные встречи команды 1 - команды 2 (Команда 2-1)',
    'Очные встречи команды 1 - команды 2 (Команда 2-2)',
    'Очные встречи команды 1 - команды 2 (Команда 2-3)',
    'Очные встречи команды 1 - команды 2 (Команда 2-4)',
    'Очные встречи команды 1 - команды 2 (Команда 2-5)',
    'Очные встречи команды 1 - команды 2 (Счет 1)',
    'Очные встречи команды 1 - команды 2 (Счет 2)',
    'Очные встречи команды 1 - команды 2 (Счет 3)',
    'Очные встречи команды 1 - команды 2 (Счет 4)',
    'Очные встречи команды 1 - команды 2 (Счет 5)',
    'Прогноз тотал',
    '1хставка',
    'Винлайн',
    'Леон',
    'Олимп',
    'Пари-матч',
    ]

    row = 0
    col = 0
    for column in columns:
        worksheet.write(row, col, column)
        col += 1

    for matchs_details in matchs_details:
        row += 1
        col = 0
        worksheet.write(row, col, matchs_details['time'])
        col += 1
        worksheet.write(row, col, matchs_details['country'])
        col += 1
        worksheet.write(row, col, matchs_details['leage'])
        col += 1
        worksheet.write(row, col, matchs_details['tour'])
        col += 1
        worksheet.write(row, col, matchs_details['team1'])
        col += 1
        worksheet.write(row, col, matchs_details['team2'])
        col += 1
        worksheet.write(row, col, matchs_details['score'])
        col += 1
        # Последние игры команды 1 дата n
        for game in matchs_details['gamesHome']:
            worksheet.write(row, col, game['date'])
            col += 1
        # Последние игры команды 1 страна n
        for game in matchs_details['gamesHome']:
            worksheet.write(row, col, game['country'])
            col += 1
        # Последние игры команды 1 лига n
        for game in matchs_details['gamesHome']:
            worksheet.write(row, col, game['leage'])
            col += 1
        # Последние игры команды 1 команда 1 - n
        for game in matchs_details['gamesHome']:
            worksheet.write(row, col, game['team1'])
            col += 1
        # Последние игры команды 1 команда 2 - n
        for game in matchs_details['gamesHome']:
            worksheet.write(row, col, game['team2'])
            col += 1
        # Последние игры команды 1 счет n
        for game in matchs_details['gamesHome']:
            worksheet.write(row, col, game['score'])
            col += 1
        # Последние игры команды 1 исход n
        for game in matchs_details['gamesHome']:
            worksheet.write(row, col, game['match_result'])
            col += 1

        # Последние игры команды 2 дата n
        for game in matchs_details['gamesGuest']:
            worksheet.write(row, col, game['date'])
            col += 1
        # Последние игры команды 2 страна n
        for game in matchs_details['gamesGuest']:
            worksheet.write(row, col, game['country'])
            col += 1
        # Последние игры команды 2 лига n
        for game in matchs_details['gamesGuest']:
            worksheet.write(row, col, game['leage'])
            col += 1
        # Последние игры команды 2 команда 1 - n
        for game in matchs_details['gamesGuest']:
            worksheet.write(row, col, game['team1'])
            col += 1
        # Последние игры команды 2 команда 2 - n
        for game in matchs_details['gamesGuest']:
            worksheet.write(row, col, game['team2'])
            col += 1
        # Последние игры команды 2 счет n
        for game in matchs_details['gamesGuest']:
            worksheet.write(row, col, game['score'])
            col += 1
        # Последние игры команды 2 исход n
        for game in matchs_details['gamesGuest']:
            worksheet.write(row, col, game['match_result'])
            col += 1

        # Очные встречи дата n
        for game in matchs_details['gamesBoth']:
            worksheet.write(row, col, game['date'])
            col += 1
        # Очные встречи страна n
        for game in matchs_details['gamesBoth']:
            worksheet.write(row, col, game['country'])
            col += 1
        # Очные встречи лига n
        for game in matchs_details['gamesBoth']:
            worksheet.write(row, col, game['leage'])
            col += 1
        # Очные встречи команда 1 - n
        for game in matchs_details['gamesBoth']:
            worksheet.write(row, col, game['team1'])
            col += 1
        # Очные встречи команда 2 - n
        for game in matchs_details['gamesBoth']:
            worksheet.write(row, col, game['team2'])
            col += 1
        # Очные встречи счет n
        for game in matchs_details['gamesBoth']:
            worksheet.write(row, col, game['score'])
            col += 1
        # Прогноз счет n
        for odd in matchs_details['odds_total']:
            worksheet.write(row, col, odd['total'])
        col += 1
        # Прогноз счет n
        for odd in matchs_details['odds_total']:
            worksheet.write(row, col, odd['bookmaker'])
            col += 1
            worksheet.write(row, col, odd['coeff_over'])
            col += 1


    workbook.close()
# 'date': date,
# 'country': country,
# 'leage': leage,
# 'team1': team1,
# 'team2': team2,
# 'score': score,

# 'date': date,
# 'country': country,
# 'leage': leage,
# 'team1': team1,
# 'team2': team2,
# 'score': score,
# 'match_result': match_result,


# 'time': time_main,
# 'country': country_main,
# 'leage': leage_main,
# 'tour': tour_main,
# 'team1': team_main1,
# 'team2': team_main2,
# 'score': score_main,
# 'gamesHome': gamesHome,
# 'gamesGuest': gamesGuest,
# 'gamesBoth': gamesBoth,
# 'odds_total': odds_total,

def main():
    # browser = init_browser()

    # id_list = get_matchs_id(browser)
    id_list = id_lists_test.id_lists

    main_parse(id_list)


if __name__ == '__main__':
    main()

# BROWSER.quit()
# print(match_id)
# def get_html(url):
#
#     return response.read()
