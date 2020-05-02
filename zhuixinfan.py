import os, sys, time
from selenium import webdriver

driver = webdriver.Chrome()

def get_sub_pages(list_page):
    driver.get(list_page)
    list_xpath = '//td[@class="td2"]/a'
    list_elements = driver.find_elements_by_xpath(list_xpath)
    return [list.get_attribute("href") for list in list_elements]

def get_magnet(page_url):
    driver.get(page_url)
    magnet_xpath = '//dd[@id="torrent_url"]'
    magnet_element = driver.find_element_by_xpath(magnet_xpath)
    return magnet_element.text

def save_magnet_to_file(out_file, magnet):
    with open(out_file, "a+") as out:
        out.write(magnet + "\n")

if __name__=="__main__":
    for sub_page in get_sub_pages(sys.argv[1]):
        save_magnet_to_file(sys.argv[2], get_magnet(sub_page))
    driver.quit()