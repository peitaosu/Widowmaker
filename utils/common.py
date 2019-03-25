import sys

if (sys.version_info > (3, 0)):
    # python 3.x
    PY3 = True
else:
    # python 2.x
    PY3 = False

REQ_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "big5,ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}
