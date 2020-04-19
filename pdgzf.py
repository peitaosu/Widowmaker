import os, sys, time
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.javascript": 1,
}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

def get_house_status(house_type):
    page_url = "https://select.pdgzf.com/houseLists"
    driver.get(page_url)
    house_xpath = '//li[@text="{}"]'.format(house_type)
    house_element = driver.find_element_by_xpath(house_xpath)
    house_element.click()
    house_count_xpath = '//h4[@class="fs26 c-6 village-house-tit"]/span'
    house_count_element = driver.find_element_by_xpath(house_count_xpath)
    return house_count_element.text
