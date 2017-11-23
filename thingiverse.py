import os, sys, time
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.javascript": 1
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
