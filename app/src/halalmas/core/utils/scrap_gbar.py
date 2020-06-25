import csv
import json
import re
import requests
import pprint

from time import sleep
from bs4 import BeautifulSoup


class WebScrapping(object):
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    def scrap_scripts(self):
        print("START Scrapping Script Part")

        html = None
        try:
            url_detail_page = self.url
            print("url_detail_page: {}".format(
                url_detail_page))
            r = requests.get(
                url_detail_page, headers=self.headers, timeout=100)
            # print("OK #1", r)
            if r.status_code == 200:
                html = r.text
                # print("OK #2", html)

                soup = BeautifulSoup(html, 'html.parser')
                # print("soup: {}".format(soup))

                h1_text = soup.find('h1').text
                print("h1_text: {}".format(h1_text))
                h2_text = soup.find('h2').text
                print("h2_text: {}".format(h2_text))

                div_lubh_bar = soup.find_all(
                    'div', attrs={'class': "lubh-bar"})
                # print("div_lubh_bar: {}".format(div_lubh_bar))
                for item in div_lubh_bar:
                    print("style: {}".format(item.get('style', '-')))

                div_spent_time = soup.find(
                    'div', attrs={'class': "UYKlhc"})
                print("div_spent_time: {}".format(div_spent_time))

                # script_ = soup.find_all(
                #     'script')
                # for src_ in script_:
                #     print('res_find: {}'.format(src_))

        except Exception as ex:
            print("ERR Exception : {}".format(str(ex)))
        finally:
            print("finnaly OK")
        print("END Scrapping Script Part")


def run_scrap():
    url_master = "https://www.google.com/search?q=gudang+rottie&oq=gudang+rottie&aqs=chrome.0.69i59j69i60j0l3j69i60.1892j1j7&sourceid=chrome&ie=UTF-8"
    print("url_master: {}".format(url_master))
    WebScrapping(url_master).scrap_scripts()


if __name__ == "__main__":
    run_scrap()
