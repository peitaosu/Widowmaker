#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time
from selenium import webdriver
from utils.down import *
from utils.common import *

chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.javascript": 1
    }
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

TAG_LIST = ['wallpapers', 'textures-patterns', 'nature', 'current-events', 'architecture', 'business-work', 'animals', 'travel', 'fashion', 'food-drink', 'spirituality', 'experimental', 'people', 'health', 'arts-culture']

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

    SCROLL_PAUSE_TIME = 2
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

def update(argv):
    for tag in TAG_LIST:
        ids = get_pic_list_from_page('https://unsplash.com/t/{}'.format(tag))
        for id in ids:
            thread.start_new_thread(down_image_by_id, (id, os.path.join("unsplash", tag), ))
            time.sleep(0.5)
 
def tag(argv):
    ids = get_pic_list_from_page('https://unsplash.com/t/{}'.format(argv[1]))
    for id in ids:
        thread.start_new_thread(down_image_by_id, (id, os.path.join("unsplash", argv[1]), ))
        time.sleep(2)

def id(argv):
    down_image_by_id(argv[1], os.path.join("unsplash", argv[2]))


def help():
    print("Usage:")
    print("    > python unsplash.py [update\<tag>\<id>] [<tag>]")
    print("    - tag: download with tag, such as wallpapers, nature, ...")
    print("    - id: download with id and specific tag, such as xxxx wallpapers, xxxx nature, ...")
    print("    - update: update pictures with all tags.")

execute = {
    "tag": tag,
    "id": id,
    "update": update,
    "help": help
}

if len(sys.argv) == 1:
    execute["help"]()
if len(sys.argv) == 2:
    if sys.argv[1] == "update":
        execute["update"](sys.argv)
    else:
        execute["tag"](sys.argv)
if len(sys.argv) > 2:
    execute["id"](sys.argv)

driver.quit()
