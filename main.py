import sys
import pre_parse, main_parser, excel_saver
import id_lists_test



def main():
    ids_list = pre_parse.get_matchs_id()
    # ids_list = id_lists_test.id_lists

    matchs_details, links_to_match = main_parser.main_parse(ids_list)
    excel_saver.save_xlsx_match_details(matchs_details)
    excel_saver.save_xlsx_urls(links_to_match)


if __name__ == '__main__':
    main()