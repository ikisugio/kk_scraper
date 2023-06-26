from utils.parser import BS4, Selenium
from utils import generic, const
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import re


class KK_Selenium():

    def __init__(self, url):
        self.parser = Selenium(url)
        self.url = self.parser.url
        self.driver = self.parser.driver
        

    def get_pref_urls(self, filter_list=None):
        # natl => 全国
        natl_top_url = self.url
        natl_top_soup = BS4(natl_top_url)

        # pref => 都道府県
        pref_list = natl_top_soup.select('#zenkokuMap area')
        url_list_rcs = generic.attr_dict(pref_list, "alt", "href")
        cgi_query = "?action_kouhyou_pref_search_condition_index=true"
        pref_url_dict = { k : natl_top_url[:-1] + v + cgi_query
            for k, v in url_list_rcs.items()}
        
        if filter is not None:
            filtered_pref_url_dict = {k: v for k, v in pref_url_dict.items() if k in filter_list}
        
        # print(pref_url_dict)
        return filtered_pref_url_dict


    def _wait(self):
        # CookieのPHPSESSIDフィールドを削除 <= URLで直アクのため
        # self.driver.delete_cookie("PHPSESSID")
        generic.wait()
        return None


    def all_search_pref_page(self):
        def select_checkbox(range="all"):
            houjin_checkbox_specifier: str = "//input[@type='checkbox' and @name='HoujinType[]']"
            houjin_checkboxes = self.driver.find_elements(By.XPATH, houjin_checkbox_specifier)
            if range == "all":
                print(f"houjin is {houjin_checkboxes}")
                for checkbox in houjin_checkboxes:
                    self.driver.execute_script("arguments[0].checked = true;", checkbox)
                    print("test")
            return None
        select_checkbox()
        self._wait()
        print("aiueo")
        self.driver.execute_script("document.querySelector('.btn-search').click();")
        self._wait()
        return None

    def select_list_number(self, str_num: str) -> None:
        list_select = Select(self.driver.find_element(By.CSS_SELECTOR, "#displayNumber"))
        list_select.select_by_value(str_num)
        self._wait()
        return None


    def get_jigyosyo_list_page(self, num=50):
        self.select_list_number(str(num))
        jigyosyo_all = self.driver.find_elements(By.CSS_SELECTOR, "#resultList > li")
        jigyosyo_html_list = list(map(lambda x: x.get_attribute("outerHTML"), jigyosyo_all))
        jigyosyo_soup_list = list(map(lambda x: BeautifulSoup(x, 'html.parser'), jigyosyo_html_list))
        jigyosyo_name_list = list(map(self.make_jigyosyo_dict, jigyosyo_soup_list))


    def make_jigyosyo_dict(self, soup):
        jigyosyo_code = soup.select_one('.jigyosyoCd').text
        _jigyosyo_name = soup.select_one('.jigyosyoName').text
        jigyosyo_name = re.sub(r'[\u3000]', '_', _jigyosyo_name)
        jigyosyoUrl = const.NATL_TOP_URL + soup.select_one('.detailBtn')['href'][1:]
        fetch_date = generic.today()

        jigyosyo_dict = {
            "jigyosyo_cd": jigyosyo_code,
            "jigyosyo_detail": {
                "jigyosyo_name": jigyosyo_name,
                "jigyosyo_url": jigyosyoUrl,
            },
        }

        return jigyosyo_dict


    def go_next_list_page(self):
        next_list_page_link = self.driver.find_elements(By.CSS_SELECTOR, '.page-item')[-1]
        li_class_str = next_list_page_link.get_attribute("class")
        next_list_page_a = next_list_page_link.find_elements(By.CSS_SELECTOR, 'a')[0]
        print(next_list_page_a.get_attribute("outerHTML"))
        if "disabled" not in li_class_str:
            print("GO")
            next_list_page_a.click()
            return True
        else:
            print("STOP")
            return False
        return None


    def search(self, match_key, return_key, value, data_list):
        for data in data_list:
            if data[match_key] == value:
                return data[return_key]
        return None


    def iterate_pages(self, page_list):
        return None
