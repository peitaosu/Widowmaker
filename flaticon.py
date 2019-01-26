import os, sys, time
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

def download_pack_by_link(pack_link):
    driver.get(pack_link)
    down_xpath = '//button[@title="Download Pack"]'
    element_down = driver.find_element_by_xpath(down_xpath)
    element_down.click()
    time.sleep(5)
    free_xpath = '//button[@id="download-pack-free"]'
    element_free = driver.find_element_by_xpath(free_xpath)
    element_free.click()
    time.sleep(5)

def get_icons_by_keyword(keyword):
    icons_list = []
    search_link = "https://www.flaticon.com/search?word=" + keyword
    driver.get(search_link)
    icons_count_xpath = '//section[@class="search-data"]/div[@class="row"]/h2'
    element_icons_count = driver.find_element_by_xpath(icons_count_xpath)
    icons_count = int(element_icons_count.text.replace("(", "").replace(",", "").replace(")", ""))
    icons_pages_count = icons_count/96 + 1
    if icons_pages_count%96 > 0:
        icons_pages_count += 1
    for icons_page in range(1, icons_pages_count):
        icons_page_link = "https://www.flaticon.com/search/" + str(icons_page) + "?word=" + keyword
        driver.get(icons_page_link)
        icons_xpath = '//section[@class="search-result"]/ul/li/div/a'
        element_icons = driver.find_elements_by_xpath(icons_xpath)
        for icon in element_icons:
            icons_list.append(icon.get_attribute("href"))
    return icons_list

def download_icon_by_link(icon_link, format="svg"):
    driver.get(icon_link)
    formats_xpath = '//div[@class="container"]/ul[@id="fi-premium-download-buttons"]/li'
    element_formats = driver.find_elements_by_xpath(formats_xpath)
    for element_format in element_formats:
        if len(element_format.find_elements_by_tag_name("a")) is 0:
            continue
        data_format = element_format.find_element_by_tag_name("a").get_attribute("data-format")
        if data_format == format:
            element_format.click()
            time.sleep(5)
            free_xpath = '//button[@id="download-free"]'
            element_free = driver.find_element_by_xpath(free_xpath)
            element_free.click()
            time.sleep(5)

def all(argv):
    total_count = get_total_packs()
    packs = get_packs_info(total_count)
    for pack in packs:
        download_pack_by_link(pack["link"])

def pack(argv):
    pack_link = argv[2]
    download_pack_by_link(pack_link)

def icon(argv):
    if argv[2].startswith("https://") or argv[2].startswith("www."):
        icon_link = argv[2]
        download_icon_by_link(icon_link)
    else:
        icon_keyword = argv[2]
        icons_list = get_icons_by_keyword(icon_keyword)
        for icon_link in icons_list:
            download_icon_by_link(icon_link)

def help(argv):
    print("Usage:")
    print("    > python flaticon.py <pack/icon/all> [link/keyword]")
    print("    - pack/icon/all: download icon pack or sign icon or all packs")
    print("    - link/keyword: download pack by link or icon by link or keyword")

execute = {
    "all": all,
    "pack": pack,
    "icon": icon,
    "help": help
}

if len(sys.argv) == 1 or sys.argv[1] == "help":
    argv = "help"
else:
    argv = sys.argv[1]
    login()
execute[argv](sys.argv)
driver.quit()