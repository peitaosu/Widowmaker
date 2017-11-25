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
    page_url = "https://www.thingiverse.com/explore/" + filter + "/page:" + str(page_num)
    driver.get(page_url)
    thing_xpath = '//div[@class="thing thing-interaction-parent item-card"]'
    thing_elements = driver.find_elements_by_xpath(thing_xpath)
    thing_ids = []
    for thing in thing_elements:
        id = thing.get_attribute('data-id')
        thing_ids.append(id)
    return thing_ids

def download_thing_zip(thing_id):
    thing_down_url = "https://www.thingiverse.com/thing:" + str(thing_id) + "/zip"
    driver.get(thing_down_url)

def get_thing_page_count():
    page_url = "https://www.thingiverse.com/explore/popular/page:30000"
    driver.get(page_url)
    page_count = int(driver.current_url.split(":")[-1])
    return page_count

def top(argv):
    filter = argv[2]
    thing_count = argv[3]
    if thing_count == "all":
        page_count = get_thing_page_count()
        for it in range(page_count):
            thing_ids = get_thing_item_from_page(filter, it+1)
            for thing_id in thing_ids:
                download_thing_zip(thing_id)
    else:
        page_count = int(thing_count)/12 + 1
        thing_downloaded_count = 0
        for it in range(page_count):
            thing_ids = get_thing_item_from_page(filter, it+1)
            for thing_id in thing_ids:
                download_thing_zip(thing_id)
                thing_downloaded_count = thing_downloaded_count + 1
                if thing_downloaded_count == thing_count:
                    return

def thing(argv):
    if argv[2] != "id":
        print "'thing' only accept arguments like 'id 1234', please use 'python thingiverse.py help' to get usage detail."
        return
    else:
        id_number = int(argv[3])
        download_thing_zip(id_number)

def help(argv):
    print "Usage:"
    print "    > python thingiverse.py <thing|top> <id|newest/popular/random-things/...> <1234|all/5/10/100/...>"
    print "    - thing|top: download thing with id or top items of filter"
    print "    - id|newest/popular/random-things/...: download things with id or filter"
    print "    - 1234|all/5/10/100/...: download things with id or top N items of filter"

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
