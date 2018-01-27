import os, sys, urllib2
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.managed_default_content_settings.images": 1, 
    "profile.managed_default_content_settings.javascript": 1
    }
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

request_headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

def download_image(image_link, local_file):
    try:
        request = urllib2.Request(image_link, headers=request_headers)
        img = urllib2.urlopen(request)
        with open(local_file, 'wb') as save_file:
            print local_file
            save_file.write(img.read())
    except urllib2.URLError,e:
        print e.reason

def get_pics_from_url(page_url):
    driver.get(page_url)
    image_xpath = '//img'
    image_elements = driver.find_elements_by_xpath(image_xpath)
    for image_element in image_elements:
        img_src = image_element.get_attribute('src')
        download_image(img_src, img_src.split("/")[-1])
