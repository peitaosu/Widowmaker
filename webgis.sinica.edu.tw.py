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

SEARCH_URL = "http://webgis.sinica.edu.tw/place/query.asp?A1=%AC%D9%A5%F7&B1=containing&C1=%B6%B3%ABn&Page_setup=50&D1=AND&A2=99&B2=containing&C2=&D2=AND&A3=99&B3=containing&C3=&page="
INFO_URL_PREFIX = "http://webgis.sinica.edu.tw/place/"
DB_PATH = "data.db"
DATA_PATH = "data.json"

conn = sqlite3.connect(DB_PATH)
conn.text_factory = str
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS `INFO_1` (`ID` INTEGER NOT NULL, `省份` TEXT, `地區` TEXT, `卷數` TEXT, `編修者年代` TEXT, `人名` TEXT, `年代` TEXT, `西元` TEXT, `性質` TEXT,`館藏地` TEXT,`註記` TEXT, PRIMARY KEY(`ID`));''')
c.execute('''CREATE TABLE IF NOT EXISTS `INFO_2` (`ID` INTEGER NOT NULL, `省份` TEXT, `地區` TEXT, `地方志名` TEXT, `卷數` TEXT, `修纂時間` TEXT, `編纂單位` TEXT, `叢書名` TEXT, `出版地` TEXT, `出版時間` TEXT, `稽核項` TEXT, `館藏/藏書者` TEXT, `版本` TEXT, `備考/附註` TEXT, PRIMARY KEY(`ID`));''')
conn.commit()

def get_total_pages():
    request = urllib.request.Request(SEARCH_URL + "1", headers=REQ_HEADERS)
    response = urllib.request.urlopen(request)
    if response:
        content = response.read()
        content = content.decode("big5", errors="ignore")
        total_regex = r"<font face=\"Arial, Helvetica, sans-serif\">(\d*)</font>"
        return int(re.findall(total_regex, content)[0])

def get_info_urls(page_url):
    request = urllib.request.Request(page_url, headers=REQ_HEADERS)
    response = urllib.request.urlopen(request)
    if response:
        content = response.read()
        content = content.decode("big5", errors="ignore")
        content = content.replace("\t", "").replace("\r", "").replace("\n", "")
        url_regex = r"(detail\.asp\?ID=\d*\&Source=\d)"
        return re.findall(url_regex, content)

def get_all_pages(start):
    total = get_total_pages()
    print("Totals: " + str(total))
    for i in range(start, total):
        info_urls = get_info_urls(SEARCH_URL + str(i+1))
        print("Getting Pages from:" + str(i+1))
        for info_url in info_urls:
            get_info(info_url)

def get_info(info_url):
    url = INFO_URL_PREFIX + info_url
    print("Getting Data from URL:" + url)
    driver.get(url)
    content = driver.page_source
    content = content.replace("\t", "").replace("\r", "").replace("\n", "")
    id_regex = r"detail\.asp\?ID=(\d*)\&Source=\d"
    source_regex = r"detail\.asp\?ID=\d*\&Source=(\d)"
    info_regex = r"width=\"100\">([^<]*)：    </th><td class=\"calc\" align=\"left\" valign=\"top\">\xa0([^<]*)</td>"
    id = re.findall(id_regex, url)[0]
    source = re.findall(source_regex, url)[0]
    info = {}
    for key, value in re.findall(info_regex, content):
        info[key] = value
    write_to_db(id, info, source)

def write_to_db(id, info, source):
    try:
        if source == "1":
            c.execute('''INSERT OR IGNORE INTO INFO_1 (`ID`, `省份`, `地區`, `卷數`, `編修者年代`, `人名`, `年代`, `西元`, `性質`,`館藏地`,`註記`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                        (id, info["省份"], info["地區"], info["卷數"], info["編修者年代"], info["人名"], info["年代"], info["西元"], info["性質"], info["館藏地"], info["註記"]))
            conn.commit()
        if source == "2":
            c.execute('''INSERT OR IGNORE INTO INFO_2 (`ID`, `省份`, `地區`, `地方志名`, `卷數`, `修纂時間`, `編纂單位`, `叢書名`, `出版地`, `出版時間`, `稽核項`, `館藏/藏書者`, `版本`, `備考/附註`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                        (id, info["省份"], info["地區"], info["地方志名"], info["卷數"], info["修纂時間"], info["編纂單位"], info["叢書名"], info["出版地"], info["出版時間"], info["稽核項"], info["館藏/藏書者"], info["版本"], info["備考/附註"]))
            conn.commit()
    except Exception as e:
        print(e)

get_all_pages(0)
conn.close()
