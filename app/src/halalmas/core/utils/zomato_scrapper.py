from time import sleep
from bs4 import BeautifulSoup
import csv
import requests

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
URL_BI_CURRENCY_PAGE = 'https://www.zomato.com/jakarta/restaurants?page=2'


class CurrencyScrappingFromBI(object):

    def __init__(self, url):
        self.url = url
        self.headers = {
            'user-agent': USER_AGENT
        }
        self.dict_key_name = ['code', 'value', 'sale', 'buy']

    def get_currency_list(self):
        html = None
        currency_output = []
        try:
            r = requests.get(self.url, headers=self.headers, timeout=100)
            print("OK #1", r)
            if r.status_code == 200:
                html = r.text
                # print("OK #2", html)

                soup = BeautifulSoup(html, 'html.parser')
                print(soup.prettify(formatter="minimal"))

                # find_table_1 = soup.find('table', attrs={'class': 'table1'})
                # strip() is used to remove starting and trailing
                # table_table1 = find_table_1.text.strip()
                # print("table_table1: ", table_table1)

                # find_table_1_tbody = soup.find(
                #     'table', attrs={'class': 'table1'}).find_all("tr")
                # # print("find_table_1_tbody: ", len(
                # #     find_table_1_tbody), find_table_1_tbody)

                # rows = find_table_1_tbody
                # for idx, row in enumerate(rows):
                #     print("row {}".format(idx))
                #     if idx >= 1:
                #         cells = row.find_all("td")
                #         dict_here = {}
                #         for idx_td, td in enumerate(cells):
                #             if idx_td <= 3:
                #                 # print("col {} {}".format(idx_td, td.get_text()))
                #                 dict_here[self.dict_key_name[idx_td]
                #                           ] = td.get_text().strip()
                #         currency_output.append(dict_here.copy())
        except Exception as ex:
            print(str(ex))
        finally:
            return currency_output

    # parse a single item to get information

    def parse_to_csv(self, dict_in, path_to_save=None):
        try:
            csv_filename = 'currency_rate_from_BI.csv'
            # open a csv file with append, so old data will not be erased
            if path_to_save:
                output_file = "{}/{}".format(path_to_save, csv_filename)
            else:
                output_file = csv_filename
            with open(output_file, 'w') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(self.dict_key_name)
                for item in dict_in:
                    writer.writerow([item[self.dict_key_name[0]],
                                     item[self.dict_key_name[1]],
                                     item[self.dict_key_name[2]],
                                     item[self.dict_key_name[3]]])
        except Exception as ex:
            print(str(ex))
        finally:
            return "OKAY"


def execute_scrapper():
    clsScrapping = CurrencyScrappingFromBI(URL_BI_CURRENCY_PAGE)
    currency_data = clsScrapping.get_currency_list()
    print(currency_data)

    # if len(dict.keys()):
    #     ret_output = clsScrapping.parse_to_csv(currency_data)
    #     print(ret_output)


if __name__ == "__main__":
    execute_scrapper()
