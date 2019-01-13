import os, sys, time
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
    down_url = "https://unsplash.com/photos/{}/download?force=true".format(image_id)
    download_image(down_url, os.path.join(out_dir, image_id + ".jpg"), driver, REQ_HEADERS)
