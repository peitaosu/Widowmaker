# -*- coding: utf-8 -*-
import os, sys, time
from helper import Helper

helper = Helper()

def get_house_status(filter=2, type=2):
    page_url = "https://select.pdgzf.com/houseLists"
    filter_xpath = '//ul[@class="clearfix fl"]'
    filter_element = helper.get_elements_by_xpath(page_url, filter_xpath)[filter]
    type_element = filter_element.find_elements_by_tag_name("li")[type]
    type_element.click()
    time.sleep(5)
    house_count_xpath = '//h4[@class="fs26 c-6 village-house-tit"]/span'
    house_count_element = driver.find_element_by_xpath(house_count_xpath)
    return house_count_element.text

if len(sys.argv) >= 3:
    filter = int(sys.argv[1])
    type = int(sys.argv[2])
else:
    filter = 2
    type = 2
while True:
    time.sleep(10)
    if int(get_house_status(filter, type)) > 0:
        print("New Source Found!")
        break
    else:
        time.sleep(60)
