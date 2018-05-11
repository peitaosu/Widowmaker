import os, sys, json, urllib2
from urlparse import unquote

REQ_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Connection": "keep-alive",
    "Origin": "https://www.youtube.com",
    "Referer": "https://www.youtube.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}

CHUNK_SIZE = 16 * 1024

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
        "video_urls": [unquote(x.strip("url=")) for x in player_config["args"]["url_encoded_fmt_stream_map"].split(",")]
    }

def download_video(video_url, file_path):
    request = urllib2.Request(video_url, headers=REQ_HEADERS)
    response = urllib2.urlopen(request)

    bytes_received = 0
    download_size = int(response.info().getheader("Content-Length"))

    with open(file_path, 'wb') as dst_file:
        while True:
            buffer = response.read(CHUNK_SIZE)
            if not buffer and bytes_received == download_size:
                break
            bytes_received += len(buffer)
            dst_file.write(buffer)

def video(argv):
    if len(argv) < 3:
        print "Please provide url of youtube video."
        return
    video_url = argv[2]
    video_info = get_video_info(video_url)
    file_path = video_info["title"]
    for down_url in video_info["video_urls"]:
        if "quality=hd720" in down_url:
            video_url = down_url
    if len(argv) > 3:
        file_path = os.path.join(argv[3], file_path)
    download_video(video_url, file_path)

def help(argv):
    print "Usage:"
    print "    > python youtube.py video <video_url> [<save_location>]"
    print "    - video_url: url of youtube video"
    print "    - save_location: location to save downloaded video, default is current location"

execute = {
    "video": video,
    "help": help
}

if len(sys.argv) == 1 or sys.argv[1] == "help" or sys.argv[1] not in execute.keys():
    argv = "help"
else:
    argv = sys.argv[1]

execute[argv](sys.argv)