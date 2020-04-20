# -*- coding: utf-8 -*-
import os, sys, time
from selenium import webdriver

driver = webdriver.Chrome()

def get_house_status():
    page_url = "https://select.pdgzf.com/houseLists"
    driver.get(page_url)
    filter_xpath = '//ul[@class="clearfix fl"]'
    filter_element = driver.find_elements_by_xpath(filter_xpath)[2]
    type_element = filter_element.find_elements_by_tag_name("li")[2]
    type_element.click()
    time.sleep(5)
    house_count_xpath = '//h4[@class="fs26 c-6 village-house-tit"]/span'
    house_count_element = driver.find_element_by_xpath(house_count_xpath)
    return house_count_element.text

