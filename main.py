 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import sys
import pre_parse, main_parser, team_parser, excel_saver
import id_lists_test
from multiprocessing.pool import ThreadPool
import time

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m): (i + 1) * k + min(i + 1, m)] for i in range(n))

def main():
    start_time = time.time()
    # ids_list = pre_parse.get_matchs_id()
    ids_list = id_lists_test.id_lists

    matchs_details, links_to_matchs, links_to_teams = main_parser.main_parse(ids_list)

    links_to_teams = team_parser.team_parse(links_to_teams)

    excel_saver.save_xlsx_match_details(matchs_details)
    excel_saver.save_xlsx_urls(links_to_matchs)
    excel_saver.save_xlsx_teams(links_to_teams)
    
    print("--- %s seconds ---" % (time.time() - start_time))

def main_threads():
    start_time = time.time()
    # ids_list = pre_parse.get_matchs_id()
    ids_list = id_lists_test.id_lists
    print(len(ids_list))
    print('***************************************')

    ids_list = list(split(ids_list, 4))

    pool = ThreadPool(processes=4)
    async_result1 = pool.apply_async(main_parser.main_parse, (ids_list[0],))
    async_result2 = pool.apply_async(main_parser.main_parse, (ids_list[1],))
    async_result3 = pool.apply_async(main_parser.main_parse, (ids_list[2],))
    async_result4 = pool.apply_async(main_parser.main_parse, (ids_list[3],))


    matchs_details1, links_to_matchs1, links_to_teams1 = async_result1.get()
    matchs_details2, links_to_matchs2, links_to_teams2 = async_result2.get()
    matchs_details3, links_to_matchs3, links_to_teams3 = async_result3.get()
    matchs_details4, links_to_matchs4, links_to_teams4 = async_result4.get()
    
    matchs_details1.extend(matchs_details2)
    matchs_details1.extend(matchs_details3)
    matchs_details1.extend(matchs_details4)

    links_to_matchs1.extend(links_to_matchs2)
    links_to_matchs1.extend(links_to_matchs3)
    links_to_matchs1.extend(links_to_matchs4)

    links_to_teams1.extend(links_to_teams2)
    links_to_teams1.extend(links_to_teams3)
    links_to_teams1.extend(links_to_teams4)

    links_to_teams = list(split(links_to_teams1, 4))

    async_result1 = pool.apply_async(team_parser.team_parse, (links_to_teams[0],))
    async_result2 = pool.apply_async(team_parser.team_parse, (links_to_teams[1],))
    async_result3 = pool.apply_async(team_parser.team_parse, (links_to_teams[2],))
    async_result4 = pool.apply_async(team_parser.team_parse, (links_to_teams[3],))

    links_to_teams1 = async_result1.get()
    links_to_teams2 = async_result2.get()
    links_to_teams3 = async_result3.get()
    links_to_teams4 = async_result4.get()

    links_to_teams1.extend(links_to_teams2)
    links_to_teams1.extend(links_to_teams3)
    links_to_teams1.extend(links_to_teams4)

    excel_saver.save_xlsx_match_details(matchs_details1)
    excel_saver.save_xlsx_urls(links_to_matchs1)
    excel_saver.save_xlsx_teams(links_to_teams1)

    excel_saver.save_xlsx_match_details(matchs_details1, 'matches')
    excel_saver.save_xlsx_urls(links_to_matchs1, 'urls')
    excel_saver.save_xlsx_teams(links_to_teams1, 'teams')
    
    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == '__main__':
    # main()
    main_threads()
