 # -*- coding: UTF-8 -*-

import os, sys, time
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.javascript": 1,
    "download.default_directory": "<path/to/download>"
    }
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

def get_thing_item_from_page(filter, page_num):
    page_url = "https://www.youmagine.com/designs/" + filter + "/3d-printer-parts-and-enhancements?state=" + str(page_num)
    driver.get(page_url)
    thing_xpath = '//div[@class="tile"]'
    thing_elements = driver.find_elements_by_xpath(thing_xpath)
    thing_urls = []
    for thing in thing_elements:
        a_elements = thing.find_element_by_tag_name('div').find_elements_by_tag_name('a')
        for a_element in a_elements:
            if a_element.get_attribute('class') == "":
                thing_url = a_element.get_attribute('href')
                thing_urls.append(thing_url)
    return thing_urls

def download_thing_zip_from_page(thing_url):
    thing_down_url = thing_url + "/download"
    driver.get(thing_down_url)

def get_thing_url_with_id_string(id_string):
    return "https://www.youmagine.com/designs/" + id_string

def top(argv):
    filter = argv[2]
    if argv[3] == "all":
        thing_count = None
    else:
        thing_count = int(argv[3])
    thing_urls = get_thing_item_from_page(filter, 30000)
    if thing_count != None:
        for thing in thing_urls[0:thing_count]:
            download_thing_zip_from_page(thing)
    else:
        for thing in thing_urls:
            download_thing_zip_from_page(thing)

def thing(argv):
    if argv[2] != "id":
        print("'thing' only accept arguments like 'id thing_id_string', please use 'python youmagine.py help' to get usage detail.")
        return
    else:
        id_string = argv[3]
        thing_url = get_thing_url_with_id_string(id_string)
        download_thing_zip_from_page(thing_url)

def help(argv):
    print("Usage:")
    print("    > python youmagine.py <thing|top> <id|latest/popular/featured/...> <id_string|all/5/10/100/...>")
    print("    - thing|top: download thing with id string or top items of filter")
    print("    - id|latest/popular/featured/...: download things with id string or filter")
    print("    - id_string|all/5/10/100/...: download things with id string or top N items of filter")

execute = {
    "thing": thing,
    "top": top,
    "help": help
}

if len(sys.argv) == 1 or sys.argv[1] == "help":
    argv = "help"
else:
    argv = sys.argv[1]

execute[argv](sys.argv)
driver.quit()