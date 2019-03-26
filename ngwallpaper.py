 # -*- coding: UTF-8 -*-

import os, sys, time
from selenium import webdriver
from utils.common import *
from utils.down import *

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

def get_images(argv):
    result = get_ng_photo_of_day()
    for image_page in result:
        down_image(image_page)

def get_image_link(page_url):
    driver.get(page_url)
    image_xpath = '//picture/source'
    image_element = driver.find_element_by_xpath(image_xpath)
    image_source = image_element.get_attribute("srcset")
    return image_source.split("1600w, ")[1].split("2048w")[0]

def down_image(page_url):
    image_link = get_image_link(page_url)
    image_id = page_url.rstrip("/").split("/")[-1]
    download_image(image_link, image_id + ".jpg", driver, REQ_HEADERS)

def help(argv):
    print("Usage:")
    print("    > python ngwallpaper.py link [result.txt]")
    print("    > python ngwallpaper.py image")

execute = {
    "link": get_link,
    "image": get_images,
    "help": help
}

if len(sys.argv) == 1 or sys.argv[1] == "help" or sys.argv[1] not in execute.keys():
    argv = "help"
else:
    argv = sys.argv[1]

execute[argv](sys.argv)  
driver.quit()


        