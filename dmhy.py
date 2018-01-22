import os, sys, time
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.javascript": 1
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

def get_items_by_search(keyword):
    parsed_dict = {}
    for i in range(1, 1000):
        search_url = "https://share.dmhy.org/topics/list/page/{}?keyword={}".format(i, keyword)
        page_dict = get_items_by_page(search_url)
        if page_dict == {}:
            return parsed_dict
        else:
            parsed_dict.update(page_dict)
