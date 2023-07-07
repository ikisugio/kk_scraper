from libs import kk_parsers
from conf import settings


def run():
    jigyosyo_natl_list = []
    initial_url = settings.NATL_TOP_URL
    wait_time = settings.DEFAULT_SELENIUM_WAIT_TIME
    search_prefs = settings.SEARCH_PREFS
    
    
    natl_kk_selenium = kk_parsers.KK_Selenium(initial_url, wait_time)
    pref_url_dict = natl_kk_selenium.get_pref_urls(search_prefs)
    ### e.g. pref_url_dict => {'北海道': 'https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_pref_search_condition_index=true', '滋賀県': 'https://www.kaigokensaku.mhlw.go.jp/25/index.php?action_kouhyou_pref_search_condition_index=true'}

    for pref_url in pref_url_dict.values():
        print("1")
        natl_kk_selenium.driver.get(pref_url)
        print("2")
        natl_kk_selenium.all_search_pref_page()
        print("3")
        is_next = True

        while is_next:
            natl_kk_selenium._wait()
            print("4")
            _dict = natl_kk_selenium.get_jigyosyo_list_page()
            print("5")
            jigyosyo_natl_list.append(_dict)
            natl_kk_selenium._wait()
            print(jigyosyo_natl_list)
            print("6")
            is_next = natl_kk_selenium.go_next_list_page()
            print("7")


    print("Fin...")
    print(jigyosyo_natl_list)