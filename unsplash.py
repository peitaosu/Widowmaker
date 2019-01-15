#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time, thread
from selenium import webdriver
from utils.down import *

chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.javascript": 1
    }
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

REQ_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "big5,ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Connection": "keep-alive",
    "Origin": "https://webgis.sinica.edu.tw/",
    "Referer": "https://webgis.sinica.edu.tw/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}

def down_image_by_id(image_id, out_dir):
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    down_url = 'https://unsplash.com/photos/{}/download?force=true'.format(image_id)
    save_path = os.path.join(out_dir, image_id + '.jpg')
    if os.path.isfile(save_path):
        if os.stat(save_path).st_size > 0:
            return
    download_image(down_url, save_path, driver, REQ_HEADERS)

def get_pic_list_from_page(page_url):
    driver.get(page_url)

    SCROLL_PAUSE_TIME = 1
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    pic_xpath = '//a[@itemprop="contentUrl"]'
    pic_elements = driver.find_elements_by_xpath(pic_xpath)
    pic_ids = []
    for pic in pic_elements:
        pic_url = pic.get_attribute('href')
        pic_id = pic_url.replace('https://unsplash.com/photos/', '')
        pic_ids.append(pic_id)
    return pic_ids

def unsplash(argv):
    if len(argv) < 2:
        for tag in ['textures-patterns', 'current-events', 'business-work', 'animals', 'travel', 'fashion', 'food-drink', 'spirituality', 'experimental', 'people', 'health', 'arts-culture']:
            ids = get_pic_list_from_page('https://unsplash.com/t/{}'.format(tag))
            for id in ids:
                thread.start_new_thread(down_image_by_id, (id, "unsplash_{}".format(tag), ))
                time.sleep(2)
 
    else:
        ids = get_pic_list_from_page('https://unsplash.com/t/{}'.format(argv[1]))
        for id in ids:
            thread.start_new_thread(down_image_by_id, (id, "unsplash_{}".format(argv[1]), ))
            time.sleep(0.5)


def help():
    print "Usage:"
    print "    > python unsplash.py [<tag>]"
    print "    - tag: download with tag, such as wallpapers, nature, ..."

execute = {
    "unsplash": unsplash,
    "help": help
}

if len(sys.argv) > 1 and sys.argv[1] == "help":
    execute["help"]()
else:
    execute["unsplash"](sys.argv)

driver.quit()
