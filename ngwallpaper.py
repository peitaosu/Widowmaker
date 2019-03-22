 # -*- coding: UTF-8 -*-

import os, sys, time
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.javascript": 1
    }
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

def get_ng_photo_of_day():
    image_list = []
    page_url = "https://www.nationalgeographic.com/photography/photo-of-the-day/archive/"
    driver.get(page_url)
    more_xpath = '//div[@class="show-more-button"]'
    while True:
        more_element = driver.find_element_by_xpath(more_xpath)
        time.sleep(5)
        if not more_element:
            break
        more_element.click()
    image_xpath = '//div[@class="photogrid-image-container"]/a'
    image_elements = driver.find_elements_by_xpath(image_xpath)
    for image in image_elements:
        image_list.append(image.get_attribute("href"))
    return image_list

def get_link(argv):
    save_file = "result.txt"
    if len(argv) > 2:
        save_file = argv[2]
    result = get_ng_photo_of_day()
    with open(save_file, "w") as out_file:
        out_file.write("\n".join(result))

def help(argv):
    print("Usage:")
    print("    > python ngwallpaper.py link [result.txt]")

execute = {
    "link": get_link,
    "help": help
}

if len(sys.argv) == 1 or sys.argv[1] == "help" or sys.argv[1] not in execute.keys():
    argv = "help"
else:
    argv = sys.argv[1]

execute[argv](sys.argv)  
driver.quit()


        