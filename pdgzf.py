# -*- coding: utf-8 -*-
import os, sys, time
from selenium import webdriver

driver = webdriver.Chrome()

def get_house_status(filter=2, type=2):
    page_url = "https://select.pdgzf.com/houseLists"
    driver.get(page_url)
    filter_xpath = '//ul[@class="clearfix fl"]'
    filter_element = driver.find_elements_by_xpath(filter_xpath)[filter]
    type_element = filter_element.find_elements_by_tag_name("li")[type]
    type_element.click()
    time.sleep(5)
    house_count_xpath = '//h4[@class="fs26 c-6 village-house-tit"]/span'
    house_count_element = driver.find_element_by_xpath(house_count_xpath)
    return house_count_element.text

while True:
    if int(get_house_status(2, 2)) > 0:
        print("New Source Found!")
        break
    else:
        time.sleep(60)
#driver.quit()