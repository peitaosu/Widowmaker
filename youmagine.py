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

