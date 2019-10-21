 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import xlsxwriter
from datetime import datetime

def save_xlsx_match_details(matchs_details, path='matchs_'):
    if path.startswith('matchs_'):
        workbook = xlsxwriter.Workbook(path + datetime.strftime(datetime.now(), "%d-%m-%Y") + '.xlsx')
    else:
        workbook = xlsxwriter.Workbook(path + '.xlsx')
    worksheet = workbook.add_worksheet()

    columns = [
    'Дата',
    'Страна',
    'Чемпионат',
    # 'Тур',
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
    'Коэффициент',
    'Букмекер',
    'Коэффициент',
    'Букмекер',
    'Коэффициент',
    'Букмекер',
    'Коэффициент',
    'Букмекер',
    'Коэффициент',
    'Букмекер',
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
        # worksheet.write(row, col, matchs_details['tour'])
        # col += 1
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
            worksheet.write(row, col, odd['coeff_over'])
            col += 1
            worksheet.write(row, col, odd['bookmaker'])
            col += 1


    workbook.close()

def save_xlsx_urls(links_to_matches, path='urls_'):
    if path.startswith('urls_'):
        workbook = xlsxwriter.Workbook(path + datetime.strftime(datetime.now(), "%d-%m-%Y") + '.xlsx')
    else:
        workbook = xlsxwriter.Workbook(path + '.xlsx')
    worksheet = workbook.add_worksheet()

    columns = [
        'Ссылки',
    ]

    row = 0
    col = 0
    for column in columns:
        worksheet.write(row, col, column)
    
    for link in links_to_matches:
        row += 1
        worksheet.write(row, col, link['url'])
    
    workbook.close()
    
def save_xlsx_teams(links_to_matches, path='teams_'):
    if path.startswith('teams_'):
        workbook = xlsxwriter.Workbook(path + datetime.strftime(datetime.now(), "%d-%m-%Y") + '.xlsx')
    else:
        workbook = xlsxwriter.Workbook(path + '.xlsx')
    worksheet = workbook.add_worksheet()

    columns = [
        'Страна',
        'Команда',
        'Ссылка',
    ]

    row = 0
    col = 0
    for column in columns:
        worksheet.write(row, col, column)
        col += 1
    
    for link in links_to_matches:
        col = 0
        row += 1
        worksheet.write(row, col, link['country'])
        col += 1
        worksheet.write(row, col, link['teamName'])
        col += 1
        worksheet.write(row, col, link['teamLogo'])
    
    workbook.close()