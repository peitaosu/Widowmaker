import os, sys, urllib2, thread
from selenium import webdriver


CHUNK_SIZE = 16 * 1024

def download(url, file_path, header):
    print "Start download from: {}".format(url)
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
        print "Download Finished."
    except Exception as err:
        print "Download Failed: {}".format(err)

def download_image(image_link, local_file, driver, request_headers):
    try:
        request = urllib2.Request(image_link, headers=request_headers)
        img = urllib2.urlopen(request)
        with open(local_file, 'wb') as save_file:
            print local_file
            save_file.write(img.read())
    except urllib2.URLError,e:
        print e.reason

def get_pics_from_url(page_url, driver):
    driver.get(page_url)
    image_xpath = '//img'
    image_elements = driver.find_elements_by_xpath(image_xpath)
    for image_element in image_elements:
        img_src = image_element.get_attribute('src')
        thread.start_new_thread(download_image, (img_src, img_src.split("/")[-1], ) )


