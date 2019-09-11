import sys
import pre_parse, main_parser, excel_saver



def main():
    ids_list = pre_parse.get_matchs_id()
    # id_list = id_lists_test.id_lists

    matchs_details = main_parser.main_parse(ids_list)

    excel_saver.save_xlsx_match_details(matchs_details)


if __name__ == '__main__':
    main()

# BROWSER.quit()
# print(match_id)
# def get_html(url):
#
#     return response.read()
