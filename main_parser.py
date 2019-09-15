import requests, time, re, sys
from bs4 import BeautifulSoup
from datetime import datetime
from random import choice
### MINE
import proxy_list
###

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'X-Fsign': 'SW9D1eZo'
}

proxies_list = proxy_list.get_proxies()
current_proxy = {'https': choice(proxies_list)}

def init_session():
    session = requests.Session()
    return session

def get_request_BS_html(session, url):
    global current_proxy
    while True:
        try:
            print('Пробуем проксю ' + current_proxy['https'] + ' на ' + url)
            response = session.get(url, headers=headers, proxies=current_proxy, timeout=3.0)
            if response.status_code != 200:
                print('Ошибка соединения')
                continue
            html = BeautifulSoup(response.text, 'lxml')
            try:
                check = html.find('title').text.strip()
                if check.startswith('Доступ'):
                    print('Попали на страницу с блокировкой')
                    current_proxy = {'https': choice(proxies_list)}
                    continue
            except Exception as e:
                var = 1
            return html
        except Exception as e:
            current_proxy = {'https': choice(proxies_list)}
            print('Ошибка соединения исключение Поменяли прокси')
            time.sleep(1)

def main_parse(id_list):
    session = init_session()
    teams_links = []
    matchs_details = []
    urls = []
    for idx, id in enumerate(id_list):
        print(id)
        print ('Парсинг {}%'.format(float('{:.3f}'.format((idx / len(id_list) * 100)))))
        urls.append({
            'url': 'https://www.myscore.ru/match/' + id['id']
        })
        html = get_request_BS_html(session, 'https://www.myscore.ru/match/' + id['id'])
        match_detail = html.find('script', text=re.compile(r'var game_utime =')).text
        timestamp = re.search('var game_utime = (\d+);', match_detail).group(1)

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
            teams_links.append(linkToTeam)

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

        teams_links = list(set(teams_links))
    return matchs_details, urls, teams_links
