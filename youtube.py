import json, urllib2

REQ_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Connection": "keep-alive",
    "Origin": "https://www.youtube.com",
    "Referer": "https://www.youtube.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}

def get_player_config(video_url):
    request = urllib2.Request(video_url, headers=REQ_HEADERS)
    response = urllib2.urlopen(request)
    if response:
        content = response.read().decode("utf-8")
        player_cfg_start = content.find("ytplayer.config = ") + 18
        bracket = 0
        player_cfg_end = 0
        for i, char in enumerate(content[player_cfg_start:]):
            if char == "{":
                bracket += 1
            elif char == "}":
                bracket -= 1
                if bracket == 0:
                    player_cfg_end = i + 1 + player_cfg_start
                    break
        return json.loads(content[player_cfg_start:player_cfg_end])

def get_video_info(player_config):
    return {
        "title": player_config["args"]["title"],
        "author": player_config["args"]["author"],
        "video_id": player_config["args"]["video_id"],
        "video_urls": [x.strip("url=") for x in player_config["args"]["url_encoded_fmt_stream_map"].split(",")]
    }