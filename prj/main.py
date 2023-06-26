from libs import base
from utils import const, generic
from utils.parser import Selenium, BS4


jigyosyo_natl_list = []
natl_kk_selenium = base.KK_Selenium(const.NATL_TOP_URL)

search_prefs = ["滋賀県", "北海道"]
pref_url_dict = natl_kk_selenium.get_pref_urls(search_prefs)


for pref_url in pref_url_dict.values():
    # selenium = Selenium(pref_url)
    natl_kk_selenium.driver.get(pref_url)
    natl_kk_selenium.all_search_pref_page()

    is_next = True

    # _dict = natl_kk_selenium.get_jigyosyo_list_page()
    # natl_kk_selenium.go_next_list_page()
    while is_next:
        natl_kk_selenium._wait()
        _dict = natl_kk_selenium.get_jigyosyo_list_page()
        jigyosyo_natl_list.append(_dict)
        natl_kk_selenium._wait()
        is_next = natl_kk_selenium.go_next_list_page()


print("Fin...")
print(jigyosyo_natl_list)