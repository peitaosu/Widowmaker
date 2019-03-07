import os, sys
from selenium import webdriver
from common import *

if PY3:
    import urllib.request
    import _thread as thread
else:
    import urllib2
    import thread

CHUNK_SIZE = 16 * 1024

def download(url, file_path, header):
    print("Start download from: {}".format(url))
    if PY3:
        request = urllib.request.Request(url, headers=header)
        response = urllib.request.urlopen(request)
    else:
        request = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(request)

    bytes_received = 0
    download_size = int(response.info().getheader("Content-Length"))

    try:
        with open(file_path, 'wb') as dst_file:
            while True:
                buffer = response.read(CHUNK_SIZE)
                if not buffer and bytes_received == download_size:
                    break
                bytes_received += len(buffer)
                dst_file.write(buffer)
        print("File saved to: {}".format(dst_file))
    except Exception as err:
        print("Download Failed: {}".format(err))

def download_image(image_link, local_file, driver, request_headers):
    print("Start download from: {}".format(image_link))
    if PY3:
        try:
            request = urllib.request.Request(image_link, headers=request_headers)
            img = urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            print("Download Failed: {}".format(e.reason))
            return
    else:
        try:
            request = urllib2.Request(image_link, headers=request_headers)
            img = urllib2.urlopen(request)
        except urllib2.URLError as e:
            print("Download Failed: {}".format(e.reason))
            return
    with open(local_file, 'wb') as save_file:
        print("Image saved to: {}".format(local_file))
        save_file.write(img.read())


def get_pics_from_url(page_url, driver):
    driver.get(page_url)
    image_xpath = '//img'
    image_elements = driver.find_elements_by_xpath(image_xpath)
    for image_element in image_elements:
        img_src = image_element.get_attribute('src')
        thread.start_new_thread(download_image, (img_src, img_src.split("/")[-1], ) )


