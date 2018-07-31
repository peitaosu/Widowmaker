# -*- coding: UTF-8 -*-

import os
import sys
import json
import re
import sqlite3
import _thread
import time
import urllib.request
from selenium import webdriver

driver = webdriver.Chrome()

REQ_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "big5,ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Connection": "keep-alive",
    "Origin": "https://webgis.sinica.edu.tw/",
    "Referer": "https://webgis.sinica.edu.tw/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}

SEARCH_URL = "http://webgis.sinica.edu.tw/place/query.asp?A1=%AC%D9%A5%F7&B1=containing&C1=%B6%B3%ABn&Page_setup=10&D1=AND&A2=99&B2=containing&C2=&D2=AND&A3=99&B3=containing&C3=&page="
PAGE_URL = "http://webgis.sinica.edu.tw/place/detail.asp?ID={}&Source=1"
DB_PATH = "data.db"

conn = sqlite3.connect(DB_PATH)
conn.text_factory = str
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS `INFO` (`ID` INTEGER NOT NULL, `省份` TEXT, `地區` TEXT, `卷數` TEXT, `編修者年代` TEXT, `人名` TEXT, `年代` TEXT, `西元` TEXT, `性質` TEXT,`館藏地` TEXT,`註記` TEXT, PRIMARY KEY(`ID`));''')
conn.commit()

def get_total_pages():
    request = urllib.request.Request(SEARCH_URL + "1", headers=REQ_HEADERS)
    response = urllib.request.urlopen(request)
    if response:
        content = response.read()
        content = content.decode("big5", errors="ignore")
        regex = r"<font face=\"Arial, Helvetica, sans-serif\">(\d*)</font>"
        total = int(re.findall(regex, content)[0])
        return total


def get_page_ids(search_url):
    request = urllib.request.Request(search_url, headers=REQ_HEADERS)
    response = urllib.request.urlopen(request)
    if response:
        content = response.read()
        content = content.decode("big5", errors="ignore")
        content = content.replace("\t", "").replace("\r", "").replace("\n", "")
        regex = r"<a href=\"detail\.asp\?ID=(\d*)\&Source=1\">"
        matches = re.findall(regex, content)
        IDs = []
        for id in matches:
            IDs.append(id)
        return IDs


def get_all_pages(start):
    total = get_total_pages()
    print("Totals: " + str(total))
    for i in range(start, total):
        IDs = get_page_ids(SEARCH_URL + str(i + 1))
        for id in IDs:
            get_info(id)
        time.sleep(1)


def get_info(page_id):
    print("Getting Data from ID:" + page_id)
    url = PAGE_URL.format(page_id)
    driver.get(url)
    content = driver.page_source
    content = content.replace("\t", "").replace("\r", "").replace("\n", "")
    regex = r"width=\"100\">([^<]*)： </th><td class=\"calc\" align=\"left\" valign=\"top\">\xa0([^<]*)</td>"
    matches = re.findall(regex, content)
    info = {}
    for key, value in matches:
        info[key] = value
    write_to_db(page_id, info)


def write_to_db(id, info):
    try:
        c.execute('''INSERT OR IGNORE INTO INFO(`ID`, `省份`, `地區`, `卷數`, `編修者年代`, `人名`, `年代`, `西元`, `性質`,`館藏地`,`註記`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                (id, info["省份"], info["地區"], info["卷數"], info["編修者年代"], info["人名"], info["年代"], info["西元"], info["性質"], info["館藏地"], info["註記"]))
        conn.commit()
    except Exception as e:
        print(e)

get_all_pages(0)
conn.close()
