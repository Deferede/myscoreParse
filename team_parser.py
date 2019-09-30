 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import main_parser
import re, sys

def team_parse(links_to_teams):
    teams = []
    mainUrl = 'https://www.myscore.ru'
    session = main_parser.init_session()


    for idx, link in enumerate(links_to_teams):
        print ('command parse {}%'.format(float('{:.3f}'.format((idx / len(links_to_teams) * 100)))))
        html = main_parser.get_request_BS_html(session, mainUrl + link)
        teamId = link.replace('/team/','').replace('/','-')
        country = html.find('h2', class_='tournament').find_all('a')[-1].text
        
        teamHeader__info = html.find('div', class_='teamHeader').find('div', class_='teamHeader__info')

        teamLogo = teamHeader__info.find('div', class_='teamHeader__logo')['style']
        teamLogo = mainUrl + re.search('url\((.*)\)', teamLogo).group(1)

        teamName = teamHeader__info.find('div', class_='teamHeader__name').text.strip()

        teams.append({
            'country': country,
            'teamName': teamName,
            'id': teamId,
            'teamLogo': teamLogo
        })
    return teams
