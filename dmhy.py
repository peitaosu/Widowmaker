import os, sys, time, json
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.javascript": 2
    }
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

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
    for i in range(max_page):
        search_url = "https://share.dmhy.org/topics/list/page/{}?keyword={}".format(i+1, keyword)
        page_dict = get_items_by_page(search_url)
        if page_dict == {}:
            return parsed_dict
        else:
            parsed_dict.update(page_dict)
    return parsed_dict

def get_items_by_filter(filter, max_page=1000):
    parsed_dict = {}
    for i in range(max_page):
        filter_url = "https://share.dmhy.org/topics/list/sort_id/{}/page/{}".format(filter, i+1)
        page_dict = get_items_by_page(filter_url)
        if page_dict == {}:
            return parsed_dict
        else:
            parsed_dict.update(page_dict)
    return parsed_dict

def get_all_items():
    parsed_dict = {}
    for i in range(5000):
        page_url = "https://share.dmhy.org/topics/list/page/{}".format(i+1)
        page_dict = get_items_by_page(page_url)
        if page_dict == {}:
            return parsed_dict
        else:
            parsed_dict.update(page_dict)
    return parsed_dict

def dump_to_file(parsed_dict, file_path="result.json"):
    if os.path.isfile(file_path):
        with open(file_path) as ori_file:
            ori_dict = json.load(ori_file)
            parsed_dict.update(ori_dict)
    with open(file_path, "w") as out_file:
        json.dump(parsed_dict, out_file)

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
            file_path = argv[4]
        max_page = int(argv[3])
    parsed_dict = get_items_by_filter(filter_num, max_page)
    dump_to_file(parsed_dict, file_path)

def search(argv):
    keyword = argv[2]
    file_path = "result.json"
    max_page = 1000
    if len(argv) > 3:
        if len(argv) > 4:
            file_path = argv[4]
        max_page = int(argv[3])
    parsed_dict = get_items_by_search(keyword, max_page)
    dump_to_file(parsed_dict, file_path)

def help(argv):
    print "Usage:"
    print "    > python dmhy.py all [save_file]"
    print "    >                filter <filter> [pages] [save_file]"
    print "    >                search <keyword> [pages] [save_file]"
    print "    - all/filter/search: get all items or by filter or by search"
    print "    - filter: Animation 2, Animation Season 31, Comic 3, HK/TW Comic 41, JP Comic 42, Music 4, Animation Music 43, DouJin Music 44, Pop Music 15,"
    print "              JP TV 6, RAW 7, Game 9, PC Game 17, Video Game 18, Console Game 19, Net Game 20, Game Accessories 21, Tokusatsu 12, Other 1"
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
else:
    argv = sys.argv[1]
execute[argv](sys.argv)
driver.quit()