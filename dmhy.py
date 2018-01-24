import os, sys, time, json
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.javascript": 2
    }
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

filter_mapping = {
    "动画": 2, "季度全集": 31, "漫画": 3, "港台原版": 41, 
    "日文原版": 42, "音乐": 4, "动漫音乐": 43, "同人音乐": 44, 
    "流行音乐": 15, "日剧": 6, "RAW": 7, "游戏": 9, "电脑游戏": 17, 
    "电视游戏": 18, "掌机游戏": 19, "网络游戏": 20, "游戏周边": 21, 
    "特摄": 12, "其他": 1
}

def get_items_by_page(page_url):
    driver.get(page_url)
    resource_xpath = '//table[@id="topic_list"]/tbody/tr'
    resource_elements = driver.find_elements_by_xpath(resource_xpath)
    if len(resource_elements) == 0:
        return {}
    parsed_dict = {}
    for resource_element in resource_elements:
        items = resource_element.find_elements_by_tag_name('td')
        filter = items[1].find_element_by_tag_name('a').text
        title = items[2].find_element_by_tag_name('a').text
        magnet = items[3].find_element_by_tag_name('a').get_attribute('href')
        magnet_hash = magnet[20: 52]
        parsed_dict[magnet_hash] = {
            "title": title,
            "magnet": magnet,
            "filter": filter
        }
    return parsed_dict

def get_items_by_search(keyword, max_page=1000):
    parsed_dict = {}
    for i in range(1, max_page):
        search_url = "https://share.dmhy.org/topics/list/page/{}?keyword={}".format(i, keyword)
        page_dict = get_items_by_page(search_url)
        if page_dict == {}:
            return parsed_dict
        else:
            parsed_dict.update(page_dict)

def get_items_by_filter(filter, max_page=1000):
    parsed_dict = {}
    for i in range(1, max_page):
        filter_url = "https://share.dmhy.org/topics/list/sort_id/{}/page/{}".format(filter, i)
        page_dict = get_items_by_page(filter_url)
        if page_dict == {}:
            return parsed_dict
        else:
            parsed_dict.update(page_dict)

def get_all_items():
    parsed_dict = {}
    for i in range(1, 5000):
        page_url = "https://share.dmhy.org/topics/list/page/{}".format(i)
        page_dict = get_items_by_page(page_url)
        if page_dict == {}:
            return parsed_dict
        else:
            parsed_dict.update(page_dict)

def dump_to_file(parsed_dict, file_path="result.json"):
    with open(file_path, "w") as output:
        json.dump(parsed_dict, output)

def all(argv):
    file_path = "result.json"
    if len(argv) > 2:
        file_path = argv[2]
    parsed_dict = get_all_items()
    dump_to_file(parsed_dict, file_path)

def filter(argv):
    filter_num = argv[2]
    file_path = "result.json"
    max_page = 1000
    if len(argv) > 3:
        if len(argv) > 4:
            max_page = int(argv[4])
        file_path = argv[3]
    parsed_dict = get_items_by_filter(filter_num, max_page)
    dump_to_file(parsed_dict, file_path)

def search(argv):
    keyword = argv[2]
    file_path = "result.json"
    max_page = 1000
    if len(argv) > 3:
        if len(argv) > 4:
            max_page = int(argv[4])
        file_path = argv[3]
    parsed_dict = get_items_by_search(keyword, max_page)
    dump_to_file(parsed_dict, file_path)

def help(argv):
    print "Usage:"
    print "    > python dmhy.py all [save_file]"
    print "    >                filter <filter> [pages] [save_file]"
    print "    >                search <keyword> [pages] [save_file]"
    print "    - all/filter/search: get all items or by filter or by search"
    print "    - pages: get items from number of pages"
    print "    - save_file: save items information into file"

execute = {
    "all": all,
    "filter": filter,
    "search": search,
    "help": help
}

if len(sys.argv) == 1 or sys.argv[1] == "help":
    argv = "help"
execute[argv](sys.argv)
driver.quit()