import os, time
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=C:/Users/<user>/AppData/Local/Google/Chrome/User Data/Default")
chrome_options.add_argument("--proxy-server=<ip:port>")
prefs = {
    "profile.managed_default_content_settings.images": 2
    , "profile.managed_default_content_settings.javascript": 1
    ,"download.default_directory": "<path/to/download>"
    }
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

def login():
    login = "https://www.flaticon.com/profile/login"
    driver.get(login)
    element_user = driver.find_element_by_id("gr_login_username")
    element_user.send_keys("username")
    element_pswd = driver.find_element_by_id("gr_login_password")
    element_pswd.send_keys("password")
    element = driver.find_element_by_id("signin_button")
    element.click()

def get_total_packs():
    packs_page = "https://www.flaticon.com/packs"
    driver.get(packs_page)
    total_count_xpath = "//span[@class='total-items']"
    element = driver.find_element_by_xpath(total_count_xpath)
    total_count = int(element.text.replace(",", ""))
    return total_count

def get_packs_info(total_count):
    packs = []
    list_count = total_count/24 + 1
    if total_count%24 > 0:
        list_count += 1
    for pack_list in range(1, list_count):
        pack_list_url = "https://www.flaticon.com/packs/" + str(pack_list)
        try:
            driver.get(pack_list_url)
            pack_item_xpath = "//article[@class='box ']"
            elements = driver.find_elements_by_xpath(pack_item_xpath)
            for element in elements:
                id = element.get_attribute('data-id')
                element_a = element.find_element_by_xpath('.//a')
                link = element_a.get_attribute('href')
                title = element_a.get_attribute('title')
                pack = {}
                pack["id"] = id
                pack["title"] = title
                pack["link"] = link
                packs.append(pack)
        except Exception as e:
            print e
    return packs

def download_packs(pack):
    driver.get(pack["link"])
    down_xpath = '//button[@title="Download Pack"]'
    element_down = driver.find_element_by_xpath(down_xpath)
    element_down.click()
    time.sleep(5)
    free_xpath = '//button[@id="download-pack-free"]'
    element_free = driver.find_element_by_xpath(free_xpath)
    element_free.click()
    time.sleep(5)

login()
total_count = get_total_packs()
packs = get_packs_info(total_count)
for pack in packs:
    download_packs(pack)
driver.quit()