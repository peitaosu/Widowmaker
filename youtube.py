import os, sys, json, urllib2
from urlparse import unquote
from utils.down import download

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
        "video_urls": [unquote(x[x.find("url=")+4:]) for x in player_config["args"]["url_encoded_fmt_stream_map"].split(",")]
    }

def parse_video_url(video_url):
    # TODO: fix 403 forbidden issue while download from url directly
    
    # Remove itag, but seems it's not the correct solution
    # return "&".join([x for x in video_url.split("&") if not x.startswith("itag=")])
    return video_url

def get_high_quality_url(video_urls):
    for down_url in video_urls:
        if "quality=hd720" in down_url:
            return down_url
    return video_urls[0]

def pring_video_info(video_info):
    print "Title: {}\nAuthor: {}\nVideo ID: {}".format(video_info["title"], video_info["author"], video_info["video_id"])

def video(argv):
    if len(argv) < 3:
        print "Please provide url of youtube video."
        return
    video_url = argv[2]
    video_player_cfg = get_player_config(video_url)
    video_info = get_video_info(video_player_cfg)
    pring_video_info(video_info)
    file_path = "-".join(video_info["title"].replace(":", "").split()) + ".mp4"
    video_url = get_high_quality_url(video_info["video_urls"])
    if len(argv) > 3:
        file_path = os.path.join(argv[3], file_path)
    video_url = parse_video_url(video_url)
    download(video_url, file_path, REQ_HEADERS)

def file(argv):
    if len(argv) < 3:
        print "Please provide file of youtube video url list."
        return
    with open(argv[2]) as in_file:
        video_list = in_file.readlines()
    for video_url in video_list:
        if video_url.startswith("http"):
            video([None, None, video_url])
        
def help(argv):
    print "Usage:"
    print "    > python youtube.py video/file <video_url>/<file_path> [<save_location>]"
    print "    - video_url: url of youtube video"
    print "    - save_location: location to save downloaded video, default is current location"
    print "    - file_path: read video urls from file"

execute = {
    "video": video,
    "file": file,
    "help": help
}

if len(sys.argv) == 1 or sys.argv[1] == "help" or sys.argv[1] not in execute.keys():
    argv = "help"
else:
    argv = sys.argv[1]

execute[argv](sys.argv)